from accounts.models import ActivityLog

def add_activity(logged_user, activity_type, activity_location, activity_message):
    activity = ActivityLog.objects.create(type=activity_type,location=activity_location,user=logged_user,message=activity_message) 
    return activity.save()