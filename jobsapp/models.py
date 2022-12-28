from django.db import models
from django.utils import timezone

from accounts.models import User

JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
)


class Job(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    skillReq = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    salary = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class InactiveJob(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField()
    location = models.CharField(max_length=150)
    type = models.CharField(choices=JOB_TYPE, max_length=10)
    skillReq = models.CharField(max_length=100)
    last_date = models.DateTimeField()
    salary = models.CharField(max_length=100)
    created_at = models.DateTimeField(default=timezone.now)
    filled = models.BooleanField(default=False)
    def __str__(self):
        return self.title



class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applicants')
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.user.get_full_name()