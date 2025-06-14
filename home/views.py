from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout, authenticate
from django.contrib import messages, auth
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .models import LeadUser
from .models import Admin, Team_Leader, Staff, ProjectFile, Team_LeadData
from django.contrib.auth.models import User
from home.models import *
import pandas as pd
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .form import ProjectFileForm
User = get_user_model()
from .models import UserActivityLog
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .decorators import *
from django.http import JsonResponse
from calendar import monthrange
from datetime import date, time
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)
        print(email,password)
        if user is None:
            messages.error(request, "Email/Username or Password Incorrect")
            return redirect('login')
        if user is not None:
            auth.login(request, user)
            if request.user.is_superuser:
                user_type = "Super User"
            if request.user.is_admin:
                user_type = "Admin User"
            if request.user.is_team_leader:
                user_type = "Team leader User"
            if request.user.is_staff_new:
                user_type = "Staff User"

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            tagline = f"Log-In {request.user.name} - {user_type} at IP : {ip}"
            user = request.user
            if request.user.is_admin:
                admin_email = user.email
                admin_instance = Admin.objects.filter(email=admin_email).last()
                my_user = admin_instance.user
                ActivityLog.objects.create(
                    user = my_user,
                    description = tagline,
                    ip_address = ip
                )
            if request.user.is_team_leader:
                admin_email = user.email
                admin_instance = Team_Leader.objects.filter(email=admin_email).last()
                my_user1 = admin_instance.admin
                ActivityLog.objects.create(
                    admin = my_user1,
                    description = tagline,
                    ip_address = ip
                )

            if request.user.is_staff_new:
                admin_email = user.email
                admin_instance = Staff.objects.filter(email=admin_email).last()
                my_user2 = admin_instance.team_leader
                ActivityLog.objects.create(
                    team_leader = my_user2,
                    description = tagline,
                    ip_address = ip
                )

            # if not request.user.is_superuser:
                # ActivityLog.objects.create(
                #     user = my_user,
                #     admin = my_user1,
                #     team_leader = my_user2,
                #     description = tagline,
                #     ip_address = ip
                # )
            if user.is_superuser:
                messages.success(request, "Super User Login Successful")
                return redirect('super_admin')
            elif user.is_admin:
                # user1 = user.email
                # user = Admin.objects.get(email=user1)
                messages.success(request, "Admin Login Successful")
                return redirect('team_leader_user')
            elif user.is_team_leader:
                messages.success(request, "Team Leader Login Successful")
                return redirect('staff_user')
            elif user.is_staff_new:
                request.session['staff_email'] = user.email
                messages.success(request, "Staff Login Successful")
                return redirect('leads')
            else:
                messages.error(request, "User role not recognized")
                return redirect('login')
            
    return render(request, 'Login.html')


@login_required(login_url='login')
def logout_view(request):
    # if request.session['staff_email']:
    #     del request.session['staff_email']
    if request.user:
        request.user.is_login = False
        request.user.save()
    if request.user.is_superuser:
        user_type = "Super User"
    if request.user.is_admin:
        user_type = "Admin User"
    if request.user.is_team_leader:
        user_type = "Team leader User"
    if request.user.is_staff_new:
        user_type = "Staff User"

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    tagline = f"Log-Out {request.user.name} - {user_type} at IP : {ip}"

    user = request.user
    if request.user.is_admin:
        admin_email = user.email
        admin_instance = Admin.objects.filter(email=admin_email).last()
        my_user = admin_instance.user
        ActivityLog.objects.create(
            user = my_user,
            description = tagline,
            ip_address = ip
        )
    if request.user.is_team_leader:
        admin_email = user.email
        admin_instance = Team_Leader.objects.filter(email=admin_email).last()
        my_user1 = admin_instance.admin
        ActivityLog.objects.create(
            admin = my_user1,
            description = tagline,
            ip_address = ip
        )

    if request.user.is_staff_new:
        admin_email = user.email
        admin_instance = Staff.objects.filter(email=admin_email).last()
        my_user2 = admin_instance.team_leader
        ActivityLog.objects.create(
            team_leader = my_user2,
            description = tagline,
            ip_address = ip
        )
    # if request.user.is_team_leader:
    #     admin_email = user.email
    #     admin_instance = Team_Leader.objects.filter(email=admin_email).last()
    #     my_user = admin_instance.user
    # ActivityLog.objects.create(
    #     user = my_user,
    #     description = tagline,
    #     ip_address = ip
    # )

    logout(request)
    messages.success(request, "Logout Successfully")
    return render(request, 'login.html')


@superuser_required
def super_admin(request):
    if request.method == 'GET':
        user = request.user
        # if user.email != 'admin@gmail.com':
        #     messages.error(request, "You do not have permission to access this page.")
            
        if request.user.is_superuser:
            user_type = "Super User"
        if request.user.is_admin:
            user_type = "Admin User"
        if request.user.is_team_leader:
            user_type = "Team leader User"
        if request.user.is_staff_new:
            user_type = "Staff User"

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        tagline = f"Log-out user[Email : {request.user.email}, {user_type}, IP : {ip}]"

        ActivityLog.objects.create(
            user = request.user,
            description = tagline,
            ip_address = ip
        )
        # logout(request)
        # return redirect('login') 
    user = user.username
    us = User.objects.get(username=user)
    users = Admin.objects.filter(user=us)
    return render(request, "super_user/super_user.html", {'users': users})


@superuser_required
def superadmin_view_profile(request):
    user = request.user

    if request.method == 'GET':
        return render(request, 'super_user/super_user-profile.html', {'user': user})

    if request.method == 'POST':
        new_email = request.POST.get('email')

        if new_email != user.email and User.objects.filter(email=new_email).exclude(id=user.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('super_admin')

        user.email = new_email
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()

        messages.success(request, 'Your profile has been successfully updated.')
        return redirect('superuser_view_profile')

    return render(request, 'super_user/super_user-profile.html')


@superuser_required
def admin_add(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        if username:
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username Already Exists")
                return redirect('admin_add')

        if email:
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email Already Exists")
                return redirect('admin_add')

        user = User.objects.create(username=username, password=password,
                email=email, name=username, mobile=mobile, is_admin=True)
        user.set_password(password)
        user.save()

        Admin.objects.create(
            user=request.user,
            email=email,
            name=username,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
        )
        messages.success(request, "Admin Created Successfully.")
        return redirect('super_admin')
    context = {
        'messages': messages.get_messages(request),
    }
    return render(request, 'super_user/admin_add.html', context)


@superuser_required
def adminedit(request, id):
    admin = get_object_or_404(Admin, id=id)
    
    if request.method == 'GET':
        admin = Admin.objects.get(id=id)
        return render(request, 'super_user/admin_edit.html', {'admin': admin})

    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']

        admin.name = username
        admin.email = email
        admin.mobile = mobile
        admin.address = address
        admin.city = city
        admin.pincode = pincode
        admin.state = state

        admin.save()
        messages.success(request, 'Your Admin Edit successfully updated.')

    return redirect('super_admin')

@admin_required
def admin_user(request):
    if request.method == 'GET':
        user = request.user
        user1 = user.email
        us = Admin.objects.get(email=user1)
        users = Team_Leader.objects.filter(admin=us)

    return render(request, "admin_user/admin_user.html", {'users': users})

@admin_required
def add_team_leader_user(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Email Already Exists")
            return redirect('add_team_leader_user')

        if User.objects.filter(email=username).exists():
            messages.error(request, "Email Already Exists")
            return redirect('add_team_leader_user')

        user = User.objects.create_user(
            username=username, password=password, email=username, name=name, mobile=mobile, is_team_leader=True)
        user.set_password(password)
        user.save()
        admin_email = request.user.email
        admin1 = Admin.objects.get(email=admin_email)

        admin2 = Team_Leader.objects.create(
            admin=admin1,
            user=user,
            name=name,
            email=username,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
        )
        current_user = request.user
        super_admin = admin1.user

        if request.user.is_superuser:
                user_type = "Super User"
        if request.user.is_admin:
            user_type = "Admin User"
        if request.user.is_team_leader:
            user_type = "Team leader User"
        if request.user.is_staff_new:
            user_type = "Staff User"

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        tagline = f"Team Lead({name}) created by user[Email : {request.user.email}, {user_type}]"

        ActivityLog.objects.create(
            user = super_admin,
            description = tagline,
            ip_address = ip
        )

        messages.success(request, "Team Leader Created Successfully.")
        return redirect('team_leader_user')

    context = {
        'messages': messages.get_messages(request),
    }
    return render(request, "admin_user/add_team_leader_user.html", context)

@admin_required
def admin_view_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = Admin.objects.get(email=request.user.email)
            return render(request, 'admin_user/view-profile.html', {'admin': admin})

    if request.method == 'POST':
        admin = get_object_or_404(Admin, email=request.user.email)
        new_email = request.POST.get('email')

        if new_email != admin.email and Admin.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('admin_view_profile')

        admin.email = new_email
        admin.name = request.POST.get('name')
        admin.mobile = request.POST.get('mobile')
        admin.address = request.POST.get('address')
        admin.city = request.POST.get('city')
        admin.state = request.POST.get('state')
        admin.pincode = request.POST.get('pincode')

        admin.save()
        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('team_leader_user')

    return render(request, "admin_user/view-profile.html")

@admin_required
def teamedit(request, id):
    teamleader = get_object_or_404(Team_Leader, id=id)
    if request.method == 'GET':
        teamleader = Team_Leader.objects.get(id=id)
        return render(request, 'admin_dashboard/teamleadedit.html', {'teamleader': teamleader})


    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']

        teamleader.name = name
        teamleader.email = email
        teamleader.mobile = mobile
        teamleader.address = address
        teamleader.city = city
        teamleader.pincode = pincode
        teamleader.state = state

        teamleader.save()
        messages.success(request, 'Your Team Leader Edit successfully updated.')
    return redirect('team_leader_user')

@teamleader_required
def teamlead_user(request):
    if request.method == 'GET':
        user = request.user
        user1 = user.email
        us = Team_Leader.objects.get(email=user1)
        users = Staff.objects.filter(team_leader=us)
        now = timezone.now()

        user_logs = []
        logged_in_count = 0
        logged_out_count = 0

        for staff in users:
            last_log = UserActivityLog.objects.filter(user=staff.user).order_by('-login_time').first()
            if last_log:
                if last_log.logout_time:
                    status = 'Inactive'
                    duration = str(last_log.logout_time - last_log.login_time).split('.')[0]
                    logged_out_count+=1
                else:
                    status = 'Active'
                    duration = str(now - last_log.login_time).split('.')[0]
                    logged_in_count+=1
            else:
                status = 'No data'
                duration = 'No data'
                logged_out_count+=1
            user_logs.append({
                'user': staff.user,
                'id' : staff.id,
                'username':staff.name,
                'mobile': staff.mobile,
                'email': staff.user.email,
                'created_date': staff.user.date_joined,
                # 'updated_date':staff.user.updated_date,
                'status': status,
                'duration': duration
            })
        print(user_logs)
        total_staff=logged_in_count+logged_out_count
        context = {
            'user_logs': user_logs,
            'total_staff':total_staff,
            'logged_in_count': logged_in_count,
            'logged_out_count': logged_out_count
        }

        return render(request, "team_user/staff_user.html", context)


@teamleader_required
def team_view_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = Team_Leader.objects.get(email=request.user.email)
            return render(request, 'team_user/view-profile.html', {'admin': admin})

    if request.method == 'POST':
        admin = get_object_or_404(Team_Leader, email=request.user.email)
        new_email = request.POST.get('email')

        if new_email != admin.email and Team_Leader.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('team_view_profile')

        admin.email = new_email
        admin.name = request.POST.get('name')
        admin.mobile = request.POST.get('mobile')
        admin.address = request.POST.get('address')
        admin.city = request.POST.get('city')
        admin.state = request.POST.get('state')
        admin.pincode = request.POST.get('pincode')

        admin.save()
        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('staff_user')

    return render(request, "team_user/view-profile.html")

@teamleader_required
def add_staff(request):

    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']
        name = request.POST['name']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        state = request.POST['state']
        pincode = request.POST['pincode']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Email Already Exists")
            return redirect('add_staff')

        if User.objects.filter(email=username).exists():
            messages.error(request, "Email Already Exists")
            return redirect('add_staff')

        user = User.objects.create_user(
            username=username, password=password, email=username, name=name, mobile=mobile, is_staff_new=True)
        user.set_password(password)
        user.save()

        # team_leader_user = request.user
        admin_email = request.user.email
        team_leader = Team_Leader.objects.get(email=admin_email)

        staff = Staff.objects.create(
            team_leader=team_leader,
            user=user,
            name=name,
            email=username,
            mobile=mobile,
            address=address,
            city=city,
            state=state,
            pincode=pincode,
        )

        if request.user.is_superuser:
            user_type = "Super User"
        if request.user.is_admin:
            user_type = "Admin User"
        if request.user.is_team_leader:
            user_type = "Team leader User"
        if request.user.is_staff_new:
            user_type = "Staff User"

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

        tagline = f"staff : {staff.name} created by user[Email : {request.user.email}, {user_type}]"

        login_user = request.user
        admin_email = login_user.email
        admin_instance = Team_Leader.objects.filter(email=admin_email).last()
        my_user1 = admin_instance.admin
        ActivityLog.objects.create(
            admin = my_user1,
            description = tagline,
            ip_address = ip
        )

        messages.success(request, "Staff Created Successfully.")
        return redirect('staff_user')
    context = {
        'messages': messages.get_messages(request),
    }

    return render(request, "team_user/add_staff.html", context)

@teamleader_required
def staffedit(request, id):
    staff = get_object_or_404(Staff, id=id)
    if request.method == 'GET':
        staff = Staff.objects.get(id=id)
        return render(request, 'team_user/editstaff.html', {'staff': staff})

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        mobile = request.POST['mobile']
        address = request.POST['address']
        city = request.POST['city']
        pincode = request.POST['pincode']
        state = request.POST['state']

        staff.name = name
        staff.email = email
        staff.mobile = mobile
        staff.address = address
        staff.city = city
        staff.pincode = pincode
        staff.state = state

        staff.save()
        messages.success(request, 'Your Staff Edit successfully updated.')
    return redirect('staff_user')


@staff_required
def staff_view_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = Staff.objects.get(email=request.user.email)
            return render(request, "staff_user/view-profile.html", {'admin': admin})

    if request.method == 'POST':
        admin = get_object_or_404(Staff, email=request.user.email)
        new_email = request.POST.get('email')

        if new_email != admin.email and Staff.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('staff_view_profile')

        admin.email = new_email
        admin.name = request.POST.get('name')
        admin.mobile = request.POST.get('mobile')
        admin.address = request.POST.get('address')
        admin.city = request.POST.get('city')
        admin.state = request.POST.get('state')
        admin.pincode = request.POST.get('pincode')

        admin.save()
        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('leads')

    return render(request, "staff_user/view-profile.html")


@staff_required
def staff_user(request):
    staff_email = request.session.get('staff_email', '')
    try:
        staff = Staff.objects.get(email=staff_email)
    except Staff.DoesNotExist:
        staff = None
    if staff:
        users = LeadUser.objects.filter(status="Leads", assigned_to=staff)
        interested = LeadUser.objects.filter(status="Intrested", assigned_to=staff)
        not_interested = LeadUser.objects.filter(status="Not Interested", assigned_to=staff)
        other_location = LeadUser.objects.filter(status="Other Location", assigned_to=staff)
        not_picked = LeadUser.objects.filter(status="Not Picked", assigned_to=staff)
        lost = LeadUser.objects.filter(status="Lost", assigned_to=staff)
    else:
        users = LeadUser.objects.none()
    total_leads = users.count()
    
    total_interested_leads = interested.count()
    total_not_interested_leads = not_interested.count()
    total_other_location_leads = other_location.count()
    total_not_picked_leads = not_picked.count()
    total_lost_leads = lost.count()

    whatsapp_marketing = Marketing.objects.filter(source="whatsapp").last()

    return render(request, "staff_user/leads.html", {'users': users, 
                                                                      'total_interested_leads': total_interested_leads, 
                                                                      'total_leads': total_leads, 
                                                                      'total_lost_leads': total_lost_leads, 
                                                                      'total_not_interested_leads': total_not_interested_leads,
                                                                      'total_other_location_leads': total_other_location_leads, 
                                                                      'total_not_picked_leads': total_not_picked_leads, 
                                                                      'whatsapp_marketing': whatsapp_marketing})


@staff_required
def create_lead(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        call = request.POST.get('call')
        send = 'True' if request.POST.get('send') == 'True' else 'False'
        status = request.POST.get('status', 'Leads')

        # Automatically get related staff and team leader
        staff = Staff.objects.filter(user=request.user).first()
        team_leader = Team_Leader.objects.filter(user=request.user).first()

        lead = LeadUser.objects.create(
            team_leader=team_leader,
            assigned_to=staff,
            name=name,
            email=email,
            call=call,
            send=send,
            status=status
        )
        messages.success(request, 'Lead created successfully!')
        return redirect('leads')




@csrf_exempt
@login_required
def clock_in_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            clock_in_time_str = data.get('clock_in_time')

            # Parse clock_in_time or use current time
            clock_in_time = parse_datetime(clock_in_time_str)
            if not clock_in_time:
                clock_in_time = timezone.now()

            today = clock_in_time.date()
            local_time = clock_in_time.time()

            # Get or create today's attendance
            attendance, created = Attendance.objects.get_or_create(user=request.user, date=today)

            if not attendance.clock_in:
                attendance.clock_in = local_time
                attendance.save()  # Triggers status logic

                return JsonResponse({
                    'success': True,
                    'message': 'Clock-in successful',
                    'status': attendance.status,
                    'clock_in': attendance.clock_in.strftime("%H:%M:%S"),
                    'day': today.day,
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'Already clocked in',
                    'status': attendance.status,
                    'clock_in': attendance.clock_in.strftime("%H:%M:%S"),
                    'day': today.day,
                })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)



@login_required
@csrf_exempt
def clock_out_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            clock_out_time_str = data.get('clock_out_time')

            # Use local time if provided, else use server time
            clock_out_time = parse_datetime(clock_out_time_str)
            if not clock_out_time:
                clock_out_time = timezone.now()

            today = clock_out_time.date()
            local_time = clock_out_time.time()

            try:
                attendance = Attendance.objects.get(user=request.user, date=today)
            except Attendance.DoesNotExist:
                return JsonResponse({'error': 'No clock-in record found today'}, status=404)

            if attendance.clock_out:
                return JsonResponse({'success': False, 'message': 'Already clocked out'})

            attendance.clock_out = local_time
            attendance.save()

            return JsonResponse({
                'success': True,
                'message': 'Clock-out successful',
                'attendance': {
                    'date': str(attendance.date),
                    'clock_in': attendance.clock_in.strftime("%H:%M:%S") if attendance.clock_in else None,
                    'clock_out': attendance.clock_out.strftime("%H:%M:%S"),
                    'hours_worked': attendance.hours_worked
                }
            })

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def check_clock_status(request):
    date_str = request.GET.get('date')
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid date'}, status=400)

    try:
        attendance = Attendance.objects.get(user=request.user, date=date_obj)
        return JsonResponse({
            'clock_in_done': bool(attendance.clock_in),
            'clock_out_done': bool(attendance.clock_out)
        })
    except Attendance.DoesNotExist:
        return JsonResponse({
            'clock_in_done': False,
            'clock_out_done': False
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def overview(request):
    today = timezone.localdate()
    now = timezone.localtime().time()

    # Selected month/year or default to current
    month = int(request.GET.get('month', today.month))
    year = int(request.GET.get('year', today.year))
    user_id = request.GET.get('user_id')
    print(user_id)
    current_user = request.user
    target_user = current_user  # default for staff

    if getattr(current_user, 'is_superuser', False) or getattr(current_user, 'is_admin', False):
        if user_id:
            target_user = get_object_or_404(User, id=user_id)
        else:
            target_user = current_user  # show own calendar if no user_id
    elif getattr(current_user, 'is_team_leader', False):
        if user_id:
            target_user = get_object_or_404(User, id=user_id)

    # --- Attendance Filtering ---
    join_date = target_user.date_joined.date()
    days_in_month = monthrange(year, month)[1]

    attendance_qs = Attendance.objects.filter(
        user=target_user,
        date__year=year,
        date__month=month
    )

    # Preprocess into dict
    attendance_map = {
        att.date.day: {
            'hours': att.hours_worked,
            'clock_in': att.clock_in.strftime("%H:%M:%S") if att.clock_in else None,
            'clock_out': att.clock_out.strftime("%H:%M:%S") if att.clock_out else None,
            'status': att.status,
        }
        for att in attendance_qs
    }

    attendance_data = {}

    for day in range(1, days_in_month + 1):
        current_date = date(year, month, day)

        if current_date < join_date or current_date > today:
            continue

        if current_date == today and now < time(19, 0):
            continue

        if day in attendance_map:
            attendance_data[day] = attendance_map[day]
        else:
            # Mark absent only for days after join and before today cutoff
            attendance_data[day] = {
                'hours': 0,
                'clock_in': None,
                'clock_out': None,
                'status': 'Absent',
            }

    # AJAX response
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'attendance_data': attendance_data,
            'user': target_user.username,
            'user_id': target_user.id,
        })

    # Select template
    if getattr(current_user, 'is_superuser', False):
        template = 'super_user/overview.html'
    elif getattr(current_user, 'is_admin', False):
        template = 'admin_user/overview.html'
    elif getattr(current_user, 'is_team_leader', False):
        template = 'team_user/overview.html'
    else:
        template = 'staff_user/overview.html'

    return render(request, template, {
        'month': month,
        'year': year,
        'attendance_data': attendance_data,
        'target_user': target_user,
        'today': today.day,
    })



@login_required(login_url='login')
def activitylogs(request):
    if request.method == "GET":
        if request.user.is_superuser:
            logs = ActivityLog.objects.all().order_by('-created_date')
            context = {
                'logs': logs,
            }
            return render(request, "super_user/activity_log.html", context)
        if request.user.is_admin:
            user_email = request.user.email
            admin_user = Admin.objects.filter(email=user_email).last()
            logs = ActivityLog.objects.filter(admin=admin_user).order_by('-created_date')
            context = {
                'logs': logs,
            }
            return render(request, "admin_user/activity_log.html", context)
        
        if request.user.is_team_leader:
            user_email = request.user.email
            admin_user = Team_Leader.objects.filter(email=user_email).last()
            logs = ActivityLog.objects.filter(team_leader=admin_user).order_by('-created_date')
            context = {
                'logs': logs,
            }
            return render(request, "team_user/activity_log.html", context)
        
        if request.user.is_staff_new:
            logs = ActivityLog.objects.filter(user=request.user).order_by('-created_date')
            context = {
                'logs': logs,
            }
            return render(request, "staff_user/activity_log.html", context)

    return render(request, "activity_log.html", context)


def lost_leads(request):
    staff_email = request.session.get('staff_email', '')
    try:
        staff = Staff.objects.get(email=staff_email)
    except Staff.DoesNotExist:
        staff = None
    if staff:
        users_lead_lost = LeadUser.objects.filter(status="Intrested", assigned_to=staff)
    else:
        users_lead_lost = LeadUser.objects.none()
    return render(request, "staff_user/lost_leads.html", {'users_lead_lost': users_lead_lost, })


@login_required(login_url='login')
def customer(request):
    staff_email = request.session.get('staff_email', '')
    try:
        staff = Staff.objects.get(email=staff_email)
    except Staff.DoesNotExist:
        staff = None
    if staff:
        customer_lead_lost = LeadUser.objects.filter(status="Not Interested", assigned_to=staff)
    else:
        customer_lead_lost = LeadUser.objects.none()
    return render(request, "staff_user/Customer.html", {'customer_lead_lost': customer_lead_lost})


@login_required(login_url='login')
def maybe(request):
    staff_email = request.session.get('staff_email', '')
    try:
        staff = Staff.objects.get(email=staff_email)
    except Staff.DoesNotExist:
        staff = None
    if staff:
        lead_maybe = LeadUser.objects.filter(status="Other Location", assigned_to=staff)
    else:
        lead_maybe = LeadUser.objects.none()
    return render(request, "staff_user/follow.html", {'lead_maybe': lead_maybe})


@login_required(login_url='login')
def not_picked(request):
    staff_email = request.session.get('staff_email', '')
    try:
        staff = Staff.objects.get(email=staff_email)
    except Staff.DoesNotExist:
        staff = None
    if staff:
        lead_maybe = LeadUser.objects.filter(status="Not Picked", assigned_to=staff)
    else:
        lead_maybe = LeadUser.objects.none()
    return render(request, "staff_user/not_picked.html", {'lead_maybe': lead_maybe})

@login_required(login_url='login')
def lost(request):
    staff_email = request.session.get('staff_email', '')
    try:
        staff = Staff.objects.get(email=staff_email)
    except Staff.DoesNotExist:
        staff = None
    if staff:
        lead_maybe = LeadUser.objects.filter(status="Lost", assigned_to=staff)
    else:
        lead_maybe = LeadUser.objects.none()
    return render(request, "staff_user/lost.html", {'lead_maybe': lead_maybe})


@login_required(login_url='login')
def project(request):
    files = ProjectFile.objects.all()
    if request.method == 'POST':
        form = ProjectFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

    else:
        form = ProjectFileForm()
    return render(request, 'staff_user/project.html', {'files': files, 'form': form})




@login_required(login_url='login')
def status_update(request):
    if request.method == 'POST':
        merchant_id = request.POST.get('leads_id')
        print(merchant_id, 'AAAAAAAAAAAAAAAA')

        if request.user.is_superuser:
            user_type = "Super User"
        if request.user.is_admin:
            user_type = "Admin User"
        if request.user.is_team_leader:
            user_type = "Team leader User"
        if request.user.is_staff_new:
            user_type = "Staff User"

        if merchant_id:
            new_status = request.POST.get('new_status')
            status_update_user = LeadUser.objects.get(id=merchant_id)
            status_update_user.status = new_status
            status_update_user.save()

            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            tagline = f"Lead status change from {status_update_user.status} to {new_status} by user[Email : {request.user.email}, {user_type}]"
            
            user = request.user
            if request.user.is_staff_new:
                admin_email = user.email
                admin_instance = Staff.objects.filter(email=admin_email).last()
                my_user2 = admin_instance.team_leader
                ActivityLog.objects.create(
                    team_leader = my_user2,
                    description = tagline,
                    ip_address = ip
                )

        return redirect('leads')
    return render(request, 'staff_user/leads.html', {'status_update_user': status_update_user})

@csrf_exempt
def update_send_status(request):
    if request.method == 'POST':
        import json
        data = json.loads(request.body)
        user_id = data.get('id')
        new_send_status = data.get('send')

        try:
            user = LeadUser.objects.get(id=user_id)
            user.send = new_send_status
            user.save()
            return JsonResponse({'success': True, 'new_send_status': new_send_status})
        except LeadUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


def send_file_to_client(request, file_id):
    project_file = get_object_or_404(ProjectFile, id=file_id)
    LeadUser.objects.filter(send=True).update(send=False) 
    return redirect('leads')


@login_required(login_url='login')
def lead(request):
    user = request.user
    total_leads, total_lost_leads, total_customer, total_maybe = 0, 0, 0, 0

    try:
        team_lead = Team_Leader.objects.get(user=user)
    except Team_Leader.DoesNotExist:
        team_lead = None

    if team_lead:
        # Team leader's unassigned leads
        leads2 = Team_LeadData.objects.filter(assigned_to=None, team_leader=team_lead)
        total_uplode_leads = leads2.count()

        # Staff assigned to the team leader
        staff_members = Staff.objects.filter(team_leader=team_lead)
        
        # Collect data for each staff member
        for staff in staff_members:
            staff_leads = LeadUser.objects.filter(assigned_to=staff)
            total_leads += staff_leads.filter(status="Leads").count()
            total_lost_leads += staff_leads.filter(status="Lost_Leads").count()
            total_customer += staff_leads.filter(status="Customer").count()
            total_maybe += staff_leads.filter(status="Maybe").count()

        # Add team leader's own data
        total_leads += leads2.filter(status="Leads").count()
        total_lost_leads += leads2.filter(status="Lost_Leads").count()
        total_customer += leads2.filter(status="Customer").count()
        total_maybe += leads2.filter(status="Maybe").count()
    else:
        leads2 = Team_LeadData.objects.none()

    context = {
        'total_uplode_leads':total_uplode_leads,
        'leads2': leads2,
        'total_leads': total_leads,
        'total_lost_leads': total_lost_leads,
        'total_customer': total_customer,
        'total_maybe': total_maybe,
    }

    return render(request, "team_user/lead.html", context)

def bulk_from(request):
    if request.method == 'POST':
        assigned_id = request.POST.get('assigned_id')
        selected_lead_ids = request.POST.getlist('user_ids')
        request.session['selected_lead_ids'] = selected_lead_ids

        if not selected_lead_ids:
            messages.error(request, 'Assigned ID is missing.')
            return redirect('bulk_from')

        if not selected_lead_ids:
            messages.error(request, 'No leads selected.')
            return redirect('bulk_from')
        
        if selected_lead_ids:
            messages.error(request, 'Selected Leads Successfully')
            return redirect('bulk_from')

        try:
            assigned_user = get_object_or_404(Staff, id=assigned_id)
            for lead_id in selected_lead_ids:
                teams_leaders = Team_LeadData.objects.get(id=lead_id)
                lead_user = LeadUser.objects.create(
                    id=assigned_user
                )
                lead_user.save()
            messages.success(request, 'Leads have been successfully assigned.')
        except Staff.DoesNotExist:
            messages.error(request, 'Assigned user does not exist.')
        except LeadUser.DoesNotExist:
            messages.error(request, 'One or more selected leads do not exist.')

    selected_lead_ids = request.session.get('selected_lead_ids', [])

    user = request.user
    user1 = user.username
    us = Team_Leader.objects.get(email=user1)
    staff_users2 = Staff.objects.filter(team_leader=us)
    lead_users = LeadUser.objects.all()

    context = {
        'staff_users2': staff_users2,
        'lead_users': lead_users,
        'selected_lead_ids': selected_lead_ids, 
    }
    return render(request, "team_user/bulk_from.html", context)

def bulk_from_data(request):
    if request.method == 'POST':
        selected_lead_ids = request.session.get('selected_lead_ids', [])
        assigned_id = request.POST.get('assigned_id', [])
        selected_lead_ids = selected_lead_ids[0].split(',')
        # Ensure selected_lead_ids is a list of strings
        if isinstance(selected_lead_ids, str):
            selected_lead_ids = selected_lead_ids.split(',')
        teams_leader = Staff.objects.get(id=assigned_id)


        action = request.POST.get('action')

        # Process the action based on the value of `action`
        if action == 'assign_leads':
            
            # Ensure selected_lead_ids is a list of strings
            selected_lead_ids = [lead_id.strip() for lead_id in selected_lead_ids if lead_id.strip()]
            
            
            teams_leader = get_object_or_404(Staff, id=assigned_id)
            
            for lead_id1 in selected_lead_ids:
                try:
                    if lead_id1.strip():
                        lead_id_int = int(lead_id1)
                    
                        teams_leaders = Team_LeadData.objects.get(id=lead_id_int)
                        teams_leaders.assigned_to = teams_leader  # Replace new_assigned_to with the new value
                        teams_leaders.save()
                        lead_user = LeadUser(
                            name=teams_leaders.name,
                            email=teams_leaders.email,
                            call=teams_leaders.call,
                            send=False,
                            status="Leads",
                            assigned_to=teams_leader,
                            )
                        lead_user.save()
                except ValueError:
                    print(f"Invalid ID value: {lead_id_str}")
                except Team_LeadData.DoesNotExist:
                    print(f"Team_LeadData with id {lead_id_str} does not exist.")
            
            messages.success(request, 'Leads have been successfully assigned.')
        elif action == 'delete_leads':
            if isinstance(selected_lead_ids, str):
                selected_lead_ids = selected_lead_ids.split(',')
            
            selected_lead_ids = [lead_id.strip() for lead_id in selected_lead_ids if lead_id.strip()]
            
            for lead_id_str in selected_lead_ids:
                try:
                    lead_id_int = int(lead_id_str)
                    lead_to_delete = get_object_or_404(Team_LeadData, id=lead_id_int)
                    lead_to_delete.delete()
                except ValueError:
                    print(f"Invalid ID value: {lead_id_str}")
                except Team_LeadData.DoesNotExist:
                    print(f"Team_LeadData with id {lead_id_str} does not exist.")
            
            messages.success(request, 'Selected leads have been successfully deleted.')

        return redirect('lead')

    # If GET request, or after form submission, render the page
    selected_lead_ids = request.session.get('selected_lead_ids', [])
    staff_users = Staff.objects.all()
    lead_users = LeadUser.objects.all()

    context = {
        'staff_users': staff_users,
        'lead_users': lead_users,
        'selected_lead_ids': selected_lead_ids,
    }
    return render(request, "team_user/bulk_from.html", context)




def excel_upload(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file)
        user_count =df.shape[0]
        duplicates = []
        team_leader = Team_Leader.objects.get(user=request.user)

        for i, row in df.iterrows():
            try:
                lead_user, created = Team_LeadData.objects.get_or_create(
                    call=row['call'],
                    defaults={
                        'name': row['name'],
                        'send': row['send'],
                        'status': row['status'],
                        'team_leader': team_leader
                    }
                )
                if not created:
                    lead_user.name = row['name']
                    lead_user.send = row['send']
                    lead_user.status = row['status']
                    lead_user.team_leader = team_leader
                    lead_user.save()
            except IntegrityError:
                duplicates.append(row['call'])
                continue

        message = "Excel file uploaded successfully!"
        users = Team_LeadData.objects.all()

        return redirect("lead")

    users = Team_LeadData.objects.filter(assigned_to = None, team_leader=team_leader)
    return render(request, "team_user/importlead.html", {'users': users})


###################################################################################################################


def team_dashboard(request):
    return render(request, "admin_dashboard/index.html")


@login_required(login_url='login')
def view_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = LeadUser.objects.get(email=request.user.username)
            return render(request, 'staff_user/view-profile.html', {'admin': admin})
    if request.method == 'POST':
        admin = LeadUser.objects.get(email=request.user.username)
        new_email = request.POST['email']
        username = request.user.username
        user = Staff.objects.get(username=username)
        if new_email != admin.email and LeadUser.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('view_profile')

        user.email = request.POST['email']
        user.username = request.POST['email']

        admin.name = request.POST.get('name', admin.name)
        admin.email = new_email
        admin.call = request.POST.get('call', admin.call)
        admin.save()
        user.save()
        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('leads')

    return render(request, "staff_user/view-profile.html")



# def staff(request):
# @login_required(login_url='login')
# def home(request):
#     return render(request, "admin_dashboard/team_leader/index.html")


#     users = Staff.objects.all()
#     return render(request, "home/staff.html", {'users': users})





# @login_required(login_url='login')
# def staff_user(request):
#     if request.method == 'GET':
#         user = request.user
#         user1 = user.username
#         us = Team_Leader.objects.get(email=user1)
#         users = Staff.objects.filter(team_leader=us)
#     return render(request, "team_user/staff_user.html", {'users': users})

# @login_required
# def logout_view(request):
#     user = request.user
#     user.logout_time = timezone.now()
#     user.save()
#     auth_logout(request)
#     return redirect('login.html')



@login_required(login_url='login')
def staff_dashboard(request):
    return render(request, "admin_dashboard/staff/index.html")


@login_required(login_url='login')
def view_profile(request):
    if request.method == 'GET':
        if request.user:
            admin = User.objects.get(email=request.user.email)
            return render(request, 'view-profile.html', {'admin': admin})
    if request.method == 'POST':
        admin = User.objects.get(email=request.user.email)
        new_email = request.POST['email']
        username = request.user.username
        user = User.objects.get(username=username)
        if new_email != admin.email and User.objects.filter(email=new_email).exclude(id=admin.id).exists():
            messages.error(request, "Email Already Exists")
            return redirect('view_profile')

        user.email = request.POST['email']
        user.username = request.POST['email']

        admin.name = request.POST.get('name', admin.name)
        admin.email = new_email
        admin.save()
        user.save()
        messages.success(
            request, 'Your profile has been successfully updated.')
        return redirect('super_admin')

    return render(request, "user-profile.html")







# @login_required(login_url='login')
# def update_user(request):
#     users = LeadUser.objects.all()

#     if request.method == 'POST':
#         merchant_id = request.POST.get('leads_id')
#         new_status = request.POST.get('new_status')

#         if merchant_id and new_status:
#             try:
#                 user_to_update = LeadUser.objects.get(id=merchant_id)
#                 user_to_update.status = new_status
#                 user_to_update.save()

#                 # Recalculate statistics after update
#                 total_leads = LeadUser.objects.filter(status='Leads').count()
#                 total_lost_leads = LeadUser.objects.filter(status='Lost_Leads').count()
#                 total_customer = LeadUser.objects.filter(status='Customer').count()
#                 total_maybe = LeadUser.objects.filter(status='Maybe').count()

#                 return render(request, "admin_dashboard/team_leader/leads.html", {
#                     'users': users,
#                     'total_leads': total_leads,
#                     'total_lost_leads': total_lost_leads,
#                     'total_customer': total_customer,
#                     'total_maybe': total_maybe,
#                 })

#             except LeadUser.DoesNotExist:
#                 pass

#     return redirect('lead')







# def Staff_excel_upload(request):
#     if request.method == "POST":
#         form = UploadFileForm(request.POST, request.FILES)
#         if form.is_valid():
#             file = request.FILES['file']
#             df = pd.read_excel(file)
#             for index, row in df.iterrows():
#                 Staff.objects.create(
#                     name=row['name'],
#                     email=row['email'],
#                     mobile=row['mobile']
#                 )
#             return redirect('success')
#     else:
#         form = UploadFileForm()
#     return render(request, "admin_dashboard/staff/staff_user.html", {'form': form})













    # users_lead_lost = Team_LeadData.objects.filter(status="Lost_Leads")
    # total_lost_leads = users_lead_lost.count()

    # customer_lead_lost = Team_LeadData.objects.filter(status="Customer")
    # total_customer = customer_lead_lost.count()

    # lead_maybe = Team_LeadData.objects.filter(status="Maybe")
    # total_maybe = lead_maybe.count()


































from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import LeadUser, Team_Leader, Staff, Team_LeadData





def edit_record(request, source):
    
    # record = get_object_or_404(Marketing, source=source)
    record = Marketing.objects.filter(source=source).last()
    if record:
        data = {
            'id': record.id,
            'source': record.source,
            'url': record.url,
            'message': record.message,
            'media_file': record.media_file.url if record.media_file else '',
        }
    else:
        data = {
            'source': source,
        }
    return JsonResponse(data)

def update_record(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        # record_id = data.get('id')
        source = data.get('source')
        message = data.get('message')
        url = data.get('url')
        media_file = data.get('media_file')

        user = request.user
        marketing = Marketing.objects.create(
            user = user,
            source = source,
            message = message,
            url = url,
            media_file = media_file
        )
        
        return JsonResponse({'message': 'Record updated successfully', 'status':'200'})
    return HttpResponse(status=400)