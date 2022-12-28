from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from jobsapp.views import EditProfileView
from .views import *
from.import views

app_name = "accounts"

urlpatterns = [
    path('employee/register', RegisterEmployeeView.as_view(), name='employee-register'),
    path('employer/register', RegisterEmployerView.as_view(), name='employer-register'),
    path('employee/profile/update', EditProfileView.as_view(), name='employee-profile-update'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('login', LoginView.as_view(), name='login'),
    path(
        'change-password/',
        auth_views.PasswordChangeView.as_view(
            template_name='accounts/change-password.html',
            success_url = ''
        ),
        name='change_password'
    ),
    path('delete', DeleteAccountView.as_view(), name='delete-account'),
       
# admin url --------------------------------------------------------------
    path('admin/employees',views.admin_employees, name='admin-employees'),
    path('admin/employers',views.admin_employers, name='admin-employers'),
    path('admin/jobs',views.admin_jobs, name='admin-jobs'),
    path('admin/inactive-jobs',views.inactive_jobs, name='inactive_jobs'),
    path('admin/inactive-employees',views.inactive_employees, name='inactive_employees'),
    path('admin/inactive-employers',views.inactive_employers, name='inactive_employers'),
    path('admin/deactivate-job/<int:pk>/',views.deactivate, name='job-deactivate'),
    path('admin/activate-job/<int:pk>/',views.activate, name='job-activate'),
    path('admin/deactivate-employee/<int:pk>/',views.deactivate_employee, name='employee-deactivate'),
    path('admin/deactivate-employer/<int:pk>/',views.deactivate_employer, name='employer-deactivate'),
    path('admin/activate-employee/<int:pk>/',views.activate_employee, name='employee-activate'),
    path('admin/activate-employer/<int:pk>/',views.activate_employer, name='employer-activate'),
    path('admin-employee/profile/update/<int:pk>/', AdminEditProfileViewEmployee.as_view(), name='admin-employee-profile-update'),
    path('admin-employer/profile/update/<int:pk>/', AdminEditProfileViewEmployer.as_view(), name='admin-employer-profile-update'),
    path('employee/view/<int:pk>/',views.employee_applications, name='employee-applications'),
    path('job/view/<int:pk>/',views.job_view, name='job-view'),
    path('employer/view/<int:pk>/',views.employer_view, name='employer-view'),
# end here -----------------------------------------------------------------
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
