from celery import shared_task
from django.utils import timezone
from .models import Attendance, BlogPost, ActivityLog, UserActivityLog
from datetime import time
from django.contrib.auth import get_user_model
from django.conf import settings
import tweepy, requests


User = get_user_model()

@shared_task
def daily_auto_clockout_and_absent():
    today = timezone.localdate()
    default_clock_out = time(20, 0, 0)  # 8:00 PM

    for user in User.objects.filter(is_superuser=False):
        attendance, created = Attendance.objects.get_or_create(user=user, date=today)

        if not attendance.clock_in:
            attendance.status = 'Absent'
            attendance.save()
        elif attendance.clock_in and not attendance.clock_out:
            attendance.clock_out = default_clock_out
            attendance.save()

    return "Auto processed clock-outs and absentees at 7 PM"


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


@shared_task
def post_to_twitter(blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    title = blog.title
    caption = blog.caption

    auth = tweepy.OAuth1UserHandler(
        settings.TWITTER_API_KEY,
        settings.TWITTER_API_SECRET,
        settings.TWITTER_ACCESS_TOKEN,
        settings.TWITTER_ACCESS_TOKEN_SECRET
    )
    api = tweepy.API(auth)

    status = f"{title}\n\n{caption[:240]}"
    api.update_status(status=status)

@shared_task
def post_to_facebook(blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    message = f"{blog.title}\n\n{blog.caption}"
    access_token = settings.FB_ACCESS_TOKEN
    page_id = settings.FB_PAGE_ID

    url = f"https://graph.facebook.com/{settings.GRAPH_API_VERSION}/{page_id}/feed"
    data = {
        'message': message,
        'access_token': access_token
    }
    requests.post(url, data=data)

@shared_task
def post_to_linkedin(blog_id):
    blog = BlogPost.objects.get(id=blog_id)
    message = f"{blog.title}\n\n{blog.caption}"
    access_token = settings.LINKEDIN_ACCESS_TOKEN
    org_urn = settings.LINKEDIN_ORG_URN

    url = "https://api.linkedin.com/v2/ugcPosts"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0',
    }
    payload = {
        "author": org_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {"text": message},
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {"com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"}
    }

    requests.post(url, headers=headers, json=payload)
