from django.contrib import messages, auth
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import CreateView, FormView, RedirectView
from accounts.forms import *
from accounts.models import User
from jobsapp.models import Applicant
from django.shortcuts import render,redirect
from jobsapp.models import Job, InactiveJob
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from jobs.utils import add_activity
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.http import Http404
from jobsapp.decorators import user_is_employee
from django.urls import reverse_lazy




class RegisterEmployeeView(CreateView):
    model = User
    form_class = EmployeeRegistrationForm
    template_name = 'accounts/employee/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/employee/register.html', {'form': form})


class RegisterEmployerView(CreateView):
    model = User
    form_class = EmployerRegistrationForm
    template_name = 'accounts/employer/register.html'
    success_url = '/'

    extra_context = {
        'title': 'Register'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get("password1")
            user.set_password(password)
            user.save()
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/employer/register.html', {'form': form})


class LoginView(FormView):
    """
        Provides the ability to login as a user with an email and password
    """
    success_url = '/'
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    extra_context = {
        'title': 'Login'
    }

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().dispatch(self.request, *args, **kwargs)

    def get_success_url(self):
        if 'next' in self.request.GET and self.request.GET['next'] != '':
            return self.request.GET['next']
        else:
            return self.success_url

    def get_form_class(self):
        return self.form_class

    def form_valid(self, form):
        auth.login(self.request, form.get_user())
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        """If the form is invalid, render the invalid form."""
        return self.render_to_response(self.get_context_data(form=form))


class LogoutView(RedirectView):
    """
    Provides users the ability to logout
    """
    url = '/login'

    def get(self, request, *args, **kwargs):
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return super(LogoutView, self).get(request, *args, **kwargs)



# admin views --------------------------------------------------------------
@login_required
@require_http_methods(["GET"])
def admin_employees(request):
    employees = User.objects.filter(role='employee')
    if 'name' in request.GET:
        searchemploees = request.GET['name']
        multiple_search =  Q(Q(email__icontains=searchemploees)|Q(first_name__icontains=searchemploees)|Q(last_name__icontains=searchemploees))
        employees = User.objects.filter(multiple_search,role='employee')
    page = Paginator(employees,5)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page':page,
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
    }
    return render(request, 'adminemployees.html',context)

@login_required
@require_http_methods(["GET"])
def inactive_employees(request):
    employees = User.objects.filter(role='inactive-employee')
    if 'name' in request.GET:
        searchemploees = request.GET['name']
        multiple_search =  Q(Q(email__icontains=searchemploees)|Q(first_name__icontains=searchemploees)|Q(last_name__icontains=searchemploees))
        employees = User.objects.filter(multiple_search,role='inactive-employee')
    page = Paginator(employees,5)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page':page,
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
    }
    return render(request, 'inactiveemployees.html',context)


@login_required
@require_http_methods(["GET"])
def admin_employers(request):
    employers = User.objects.filter(role='employer')
    if 'name' in request.GET:
        searchemployers = request.GET['name']
        multiple_search =  Q(Q(email__icontains=searchemployers)|Q(first_name__icontains=searchemployers)|Q(email__icontains=searchemployers))
        employers = User.objects.filter(multiple_search,role='employer')
    page = Paginator(employers,5)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page':page,
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
    }
    return render(request, 'adminemployers.html',context)

@login_required
@require_http_methods(["GET"])
def inactive_employers(request):
    employers = User.objects.filter(role='inactive-employer')
    if 'name' in request.GET:
        searchemployers = request.GET['name']
        multiple_search =  Q(Q(email__icontains=searchemployers)|Q(first_name__icontains=searchemployers)|Q(email__icontains=searchemployers))
        employers = User.objects.filter(multiple_search,role='inactive-employer')
    page = Paginator(employers,5)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    context = {
        'page':page,
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
    }
    return render(request, 'inactiveemployers.html',context)


@login_required
@require_http_methods(["GET"])
def admin_jobs(request):
    jobslist = Job.objects.all().order_by('id')
    if 'name' in request.GET:
        searchjob = request.GET['name']
        multiple_search =  Q(Q(title__icontains=searchjob)|Q(location__icontains=searchjob))
        jobslist = Job.objects.filter(multiple_search)
    if 'type-filter' in request.GET:
        searchtype = request.GET['type-filter']
        if searchtype == 'Full Time':
            jobslist = jobslist.filter(type__exact='1')
        elif searchtype == 'Part Time':
            jobslist = jobslist.filter(type__exact='2')
        elif searchtype == 'Internship':
            jobslist = jobslist.filter(type__exact='3')
    page = Paginator(jobslist,5)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
        'page':page,
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
        'type':Job.objects.values('type').distinct(),
    }
    return render(request, 'adminjobs.html' ,context)


@login_required
@require_http_methods(["GET"])
def inactive_jobs(request):
    jobslist = InactiveJob.objects.all().order_by('id')
    if 'name' in request.GET:
        searchjob = request.GET['name']
        multiple_search =  Q(Q(title__icontains=searchjob)|Q(location__icontains=searchjob)|Q(category__icontains=searchjob))
        jobslist = InactiveJob.objects.filter(multiple_search)
    if 'type-filter' in request.GET:
        searchtype = request.GET['type-filter']
        if searchtype == 'Full Time':
            jobslist = jobslist.filter(type__exact='1')
        elif searchtype == 'Part Time':
            jobslist = jobslist.filter(type__exact='2')
        elif searchtype == 'Internship':
            jobslist = jobslist.filter(type__exact='3')
    page = Paginator(jobslist,5)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)

    context = {
        'page':page,
        'count':page.paginator.count if page.paginator.per_page * page.number > page.paginator.count else page.paginator.per_page * page.number,
        'itemcount':page.paginator.count,
        'type':InactiveJob.objects.values('type').distinct(),
    }
    return render(request, 'inactivejobs.html' ,context)

    
@login_required
def deactivate(request,pk):
    job = Job.objects.get(id=pk)
    deactivate = InactiveJob.objects.create(user=job.user,title=job.title,description=job.description,location=job.location,type=job.type,skillReq=job.skillReq,last_date=job.last_date,salary=job.salary,created_at=job.created_at,filled=job.filled)
    deactivate.save()
    messages.success(request,f"{job.title} has been successfully deactivated.")
    add_activity(logged_user=request.user,activity_type='DEACTIVATE JOB',activity_location='ADMIN',activity_message=f"{request.user} has been successfully deactivate {job.title} job.")
    job.delete()
    return redirect('accounts:inactive_jobs')

@login_required
def activate(request,pk):
    job = InactiveJob.objects.get(id=pk)
    deactivate = Job.objects.create(user=job.user,title=job.title,description=job.description,location=job.location,type=job.type,skillReq=job.skillReq,last_date=job.last_date,salary=job.salary,created_at=job.created_at,filled=job.filled)
    deactivate.save()
    messages.success(request,f"{job.title} has been successfully activated.")
    add_activity(logged_user=request.user,activity_type='ACTIVATE JOB',activity_location='ADMIN',activity_message=f"{request.user} has been successfully activate {job.title}.")
    job.delete()
    return redirect('accounts:admin-jobs')


@login_required
def deactivate_employee(request,pk):
    employee = User.objects.get(id=pk)
    employee.role = 'inactive-employee'
    employee.save()
    messages.success(request,f"{employee.first_name} {employee.last_name} has been successfully deactivated.")
    add_activity(logged_user=request.user,activity_type='DEACTIVATE EMPLOYEE',activity_location='ADMIN',activity_message=f"{request.user} has been successfully deactivate {employee.username}.")
    return redirect('accounts:inactive_employees')

@login_required
def deactivate_employer(request,pk):
    employer = User.objects.get(id=pk)
    employer.role = 'inactive-employer'
    employer.save()
    messages.success(request,f"{employer.first_name} has been successfully deactivated.")
    add_activity(logged_user=request.user,activity_type='DEACTIVATE EMPLOYER',activity_location='ADMIN',activity_message=f"{request.user} has been successfully deactivate {employer.username}.")
    return redirect('accounts:inactive_employers')

@login_required
def activate_employee(request,pk):
    employee = User.objects.get(id=pk)
    employee.role = 'employee'
    employee.save()
    messages.success(request,f"{employee.first_name} {employee.last_name} has been successfully activated.")
    add_activity(logged_user=request.user,activity_type='ACTIVATE EMPLOYEE',activity_location='ADMIN',activity_message=f"{request.user} has been successfully activate {employee.username}.")
    return redirect('accounts:admin-employees')

@login_required
def activate_employer(request,pk):
    employer = User.objects.get(id=pk)
    employer.role = 'employer'
    employer.save()
    messages.success(request,f"{employer.first_name} has been successfully activated.")
    add_activity(logged_user=request.user,activity_type='ACTIVATE EMPLOYER',activity_location='ADMIN',activity_message=f"{request.user} has been successfully activate {employer.username}.")
    return redirect('accounts:admin-employers')


class AdminEditProfileViewEmployee(UpdateView):
    model = User
    form_class = EmployeeProfileUpdateForm
    context_object_name = 'employee'
    template_name = 'jobs/employee/edit-profile.html'
    # success_url = reverse_lazy('accounts:admin-employees')
    
    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            employee_pk = self.kwargs.get('pk', None)
            self.object = User.objects.get(id=employee_pk)
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        employee_pk = self.kwargs.get('pk', None)
        title = User.objects.get(id=employee_pk)
        add_activity(logged_user=self.request.user,activity_type='UPDATE EMPLOYEE',activity_location='ADMIN',activity_message=f"{title.first_name} {title.last_name} has been successfully updated.")
        messages.success(self.request,f"{title.first_name} {title.last_name} has been successfully updated.")
        return reverse_lazy('accounts:admin-employees')


class AdminEditProfileViewEmployer(UpdateView):
    model = User
    form_class = EmployerProfileUpdateForm
    context_object_name = 'employer'
    template_name = 'jobs/employer/edit-profile.html'
    # success_url = reverse_lazy('accounts:admin-employees')
    
    @method_decorator(login_required(login_url=reverse_lazy('accounts:login')))
 
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(self.request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        try:
            employer_pk = self.kwargs.get('pk', None)
            self.object = User.objects.get(id=employer_pk)
        except Http404:
            raise Http404("User doesn't exists")
        # context = self.get_context_data(object=self.object)
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        employer_pk = self.kwargs.get('pk', None)
        title = User.objects.get(id=employer_pk)
        add_activity(logged_user=self.request.user,activity_type='UPDATE EMPLOYER',activity_location='ADMIN',activity_message=f"{title.first_name} has been successfully updated.")
        messages.success(self.request,f"{title.first_name} has been successfully updated.")
        return reverse_lazy('accounts:admin-employers')
    
    
@login_required
def employee_applications(request, pk):
    employee = User.objects.get(id=pk)
    applications = Applicant.objects.filter(user=pk)
    context = {
        'employee':employee,
        'applications':applications
    }
    return render(request, 'employeeview.html', context)

@login_required
def employer_view(request, pk):
    employer = User.objects.get(id=pk)
    posted_jobs = Job.objects.filter(user=pk)
    context = {
        'employer':employer,
        'posted_jobs':posted_jobs
    }
    return render(request, 'employerview.html', context)

@login_required
def job_view(request, pk):
    job = Job.objects.get(id=pk)
    applicants = Applicant.objects.filter(job=job)

    context = {
        'job':job,
        'applicants':applicants
    }
    return render(request, 'jobview.html', context)


class DeleteAccountView(RedirectView):
    url = '/login'

    def get(self, request, *args, **kwargs):
        username = request.user.username
        object = User.objects.get(username=username)
        object.delete()
        auth.logout(request)
        messages.success(request, 'Account has been deleted.')
        return super(DeleteAccountView, self).get(request, *args, **kwargs)


# end here -----------------------------------------------------------------