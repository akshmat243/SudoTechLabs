from celery import shared_task
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Attendance
from datetime import time

@shared_task
def daily_auto_clockout_and_absent():
    today = timezone.localdate()
    default_clock_out = time(20, 0, 0)  # 7:00 PM

    for user in User.objects.filter(is_superuser=False):
        attendance, created = Attendance.objects.get_or_create(user=user, date=today)

        if not attendance.clock_in:
            attendance.status = 'Absent'
            attendance.save()
        elif attendance.clock_in and not attendance.clock_out:
            attendance.clock_out = default_clock_out
            attendance.save()

    return "Auto processed clock-outs and absentees at 7 PM"
