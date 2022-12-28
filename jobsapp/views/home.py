from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView, CreateView

from jobsapp.forms import ApplyJobForm
from jobsapp.models import Job, Applicant, User
from accounts.models import ActivityLog
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.utils.timezone import make_aware
import datetime
from jobsapp.forms import *


class HomeView(ListView):
    model = Job
    template_name = 'home.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.all()[:6]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['trendings'] = self.model.objects.filter(created_at__month=timezone.now().month)[:3]
        context['employees_count'] = User.objects.filter(role='employee').count()
        context['activity_count'] = ActivityLog.objects.all().count()
        context['employers_count'] = User.objects.filter(role='employer').count()
        context['jobs_count'] = Job.objects.all().count()
        # context['dateform'] = DateRangeForm()
        logs = ActivityLog.objects.all()
        if 'name' in self.request.GET:
            searchlogs = self.request.GET['name']
            multiple_search =  Q(Q(location__icontains=searchlogs)|Q(message__icontains=searchlogs)|Q(user__username__icontains=searchlogs)|Q(type__icontains=searchlogs))
            logs = ActivityLog.objects.filter(multiple_search)
        # if 'fromdate' in self.request.GET and 'todate' in self.request.GET:
        #     fromdate=self.request.GET['fromdate']
        #     todate=self.request.GET['todate']
        #     logs = ActivityLog.objects.filter(datetime__range=(make_aware(datetime.datetime.strptime(fromdate, '%Y%m/%d/ %H:%M:%S.%f')),make_aware(datetime.datetime.strptime(todate, '%Y%m/%d/ %H:%M:%S.%f')) + datetime.timedelta(days=1)))
      
        page = Paginator(logs,5)
        page_list = self.request.GET.get('page')
        page = page.get_page(page_list)
        context['page']=page
        
        return context
        


class SearchView(ListView):
    model = Job
    template_name = 'jobs/search.html'
    context_object_name = 'jobs'

    def get_queryset(self):
        return self.model.objects.filter(location__contains=self.request.GET['location'],
                                         title__contains=self.request.GET['position'])


class JobListView(ListView):
    model = Job
    template_name = 'jobs/jobs.html'
    context_object_name = 'jobs'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = User.objects.filter(role='employer')
        
        return context



class JobDetailsView(DetailView):
    model = Job
    template_name = 'jobs/details.html'
    context_object_name = 'job'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        obj = super(JobDetailsView, self).get_object(queryset=queryset)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = User.objects.filter(role='employer')
        
        return context


class ApplyJobView(CreateView):
    model = Applicant
    form_class = ApplyJobForm
    slug_field = 'job_id'
    slug_url_kwarg = 'job_id'

    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            messages.info(self.request, 'Successfully applied for the job!')
            return self.form_valid(form)
        else:
            return HttpResponseRedirect(reverse_lazy('jobs:home'))

    def get_success_url(self):
        return reverse_lazy('jobs:jobs-detail', kwargs={'id': self.kwargs['job_id']})

    # def get_form_kwargs(self):
    #     kwargs = super(ApplyJobView, self).get_form_kwargs()
    #     print(kwargs)
    #     kwargs['job'] = 1
    #     return kwargs

    def form_valid(self, form):
        # check if user already applied
        applicant = Applicant.objects.filter(user_id=self.request.user.id, job_id=self.kwargs['job_id'])
        if applicant:
            messages.info(self.request, 'You already applied for this job')
            return HttpResponseRedirect(self.get_success_url())
        # save applicant
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)