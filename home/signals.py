from django.dispatch import receiver
from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from .models import UserActivityLog, ActivityLog
from django.utils import timezone

User = get_user_model()

@receiver(user_logged_in)
def create_user_login_log(sender, request, user, **kwargs):
    UserActivityLog.objects.create(user=user, login_time=timezone.now())

@receiver(user_logged_out)
def update_user_logout_log(sender, request, user, **kwargs):
    last_log = UserActivityLog.objects.filter(user=user, logout_time__isnull=True).last()
    
    if last_log:
        last_log.logout_time = timezone.now()
        last_log.save()

@shared_task
def auto_logout_users_at_midnight():
    current_time = timezone.now()
    users = User.objects.filter(is_login=True)

    for user in users:
        ActivityLog.objects.create(
            user=user,
            description=f"Auto Logout for {user.name} at midnight",
            ip_address="System"
        )
        user.is_login = False
        user.save()

        last_log = UserActivityLog.objects.filter(user=user, logout_time__isnull=True).last()
        if last_log:
            last_log.logout_time = current_time
            last_log.save()