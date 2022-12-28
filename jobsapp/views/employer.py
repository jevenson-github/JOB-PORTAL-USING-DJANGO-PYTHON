from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView
from django.views.generic import UpdateView

from accounts.forms import EmployerProfileUpdateForm
from accounts.models import User
from jobsapp.decorators import user_is_employer
from jobsapp.forms import CreateJobForm, UpdateJobForm
from jobsapp.models import Job, Applicant
from jobs.utils import add_activity

from django.core.mail import send_mail
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_protect

class DashboardView(ListView):
    model = Job
    template_name = 'jobs/employer/dashboard.html'
    context_object_name = 'jobs'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return self.model.objects.filter(user_id=self.request.user.id)
        

class EmployerEditProfileView(UpdateView):
    model = User
    form_class = EmployerProfileUpdateForm
    context_object_name = 'employer'
    template_name = 'jobs/employer/edit-profile.html'
    success_url = reverse_lazy('jobs:employer-profile-update')
    
    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            add_activity(logged_user=self.request.user,activity_type='UPDATE EMPLOYER',activity_location='ADMIN',activity_message=f"{self.object.first_name} has been successfully updated.")
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_object(self,queryset=None):
        obj = self.request.user
        print(obj)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj



class ApplicantPerJobView(ListView):
    model = Applicant
    template_name = 'jobs/employer/applicants.html'
    context_object_name = 'applicants'
    paginate_by = 1

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    @method_decorator(user_is_employer)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get_queryset(self):
        return Applicant.objects.filter(job_id=self.kwargs['job_id']).order_by('id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = Job.objects.get(id=self.kwargs['job_id'])
        return context


class JobCreateView(CreateView):
    template_name = 'jobs/create.html'
    form_class = CreateJobForm
    extra_context = {
        'title': 'Post New Job'
    }
    success_url = reverse_lazy('jobs:employer-dashboard')

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return reverse_lazy('accounts:login')
        if self.request.user.is_authenticated and self.request.user.role != 'employer':
            return reverse_lazy('accounts:login')
        return super().dispatch(self.request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        title = form.cleaned_data['title']
        add_activity(logged_user=self.request.user,activity_type='CREATE JOB',activity_location='JOB PROVIDER',activity_message=f"{self.request.user} has been successfully created {title} job.")
        return super(JobCreateView, self).form_valid(form)

    def post(self, request, *args, **kwargs):
        skillReq = request.POST['skillReq']
        email_list = User.objects.filter(role='employee', skill__contains=skillReq).values_list("email", flat=True)
        form = self.get_form()
        if form.is_valid():
            for email in email_list:
                send_mail(
                    'New Job Hiring!',
                    'A new job has been posted that may be for you! Go ahead and log in to The Job Board to see it!',
                    'settings.EMAIL_HOST_USER',
                    [email],
                    fail_silently=False,
                )
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

class JobUpdateView(UpdateView):
    model = Job
    form_class = UpdateJobForm
    template_name = 'jobs/update-job.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('jobs:employer-dashboard')

    def get_object(self, queryset=None):
        obj = super(JobUpdateView, self).get_object(queryset=queryset)
        if obj is None:
            raise Http404("Job doesn't exists")
        return obj

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
        except Http404:
            # redirect here
            raise Http404("Job doesn't exists")
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)  

    def form_valid(self, form):
    # """If the form is valid, save the associated model."""
        self.object = form.save()
        return super().form_valid(form)

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

class ApplicantsListView(ListView):
    model = Applicant
    template_name = 'jobs/employer/all-applicants.html'
    context_object_name = 'applicants'

    def get_queryset(self):
        # jobs = Job.objects.filter(user_id=self.request.user.id)
        return self.model.objects.filter(job__user_id=self.request.user.id)


@login_required(login_url=reverse_lazy('accounts:login'))
def filled(request, job_id=None):
    job = Job.objects.get(user_id=request.user.id, id=job_id)
    job.filled = True
    add_activity(logged_user=request.user,activity_type='FILLED JOB',activity_location='JOB PROVIDER',activity_message=f"{request.user} has been successfully filled {job.title} job")
    job.save()
    return HttpResponseRedirect(reverse_lazy('jobs:employer-dashboard'))

def deleteJob(request,job_id =None):
    object = Job.objects.get(id=job_id)
    object.delete()
    return redirect(request.META['HTTP_REFERER'])