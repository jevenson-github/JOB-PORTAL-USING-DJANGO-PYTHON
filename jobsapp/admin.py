from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Job)
admin.site.register(Applicant)
admin.site.register(InactiveJob)