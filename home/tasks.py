from datetime import timedelta
from celery import shared_task
from django.utils import timezone
from .models import Attendance

@shared_task
def auto_clock_out(user_id, date_str):
    from django.contrib.auth import get_user_model
    User = get_user_model()

    try:
        user = User.objects.get(id=user_id)
        date = timezone.datetime.strptime(date_str, "%Y-%m-%d").date()
        attendance = Attendance.objects.get(user=user, date=date)

        if not attendance.clock_out:
            attendance.clock_out = (timezone.datetime.combine(date, attendance.clock_in) + timedelta(hours=9)).time()
            attendance.save()
    except Exception as e:
        print(f"[Auto Clock Out Error] {e}")
