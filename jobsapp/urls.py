from django.urls import path, include

from .views import *
from.import views

app_name = "jobs"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('search', SearchView.as_view(), name='searh'),
    path('employer/dashboard', include([
        path('', DashboardView.as_view(), name='employer-dashboard'),
        path('all-applicants', ApplicantsListView.as_view(), name='employer-all-applicants'),
        path('applicants/<int:job_id>', ApplicantPerJobView.as_view(), name='employer-dashboard-applicants'),
        path('mark-filled/<int:job_id>', filled, name='job-mark-filled'),
    ])),
    path('employer/profile/update', EmployerEditProfileView.as_view(), name='employer-profile-update'),
    path('apply-job/<int:job_id>', ApplyJobView.as_view(), name='apply-job'),
    path('jobs', JobListView.as_view(), name='jobs'),
    path('jobs/<int:id>', JobDetailsView.as_view(), name='jobs-detail'),
    path('employer/jobs/create', JobCreateView.as_view(), name='employer-jobs-create'),
    path('employer/jobs/update/<int:id>', JobUpdateView.as_view(), name='employer-jobs-update'),
    
    path('delete-job/<int:job_id>', views.deleteJob, name='employer-delete-job'),
]
