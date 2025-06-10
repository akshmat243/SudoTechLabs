from django.contrib import admin

# Register your models here.
# from .models import LeadUser
from .models import *



# @admin.register(LeadUser)
# class LeadUserAdmin(admin.ModelAdmin):
#     list_display = ('name','email', 'call', 'send', 'status')
@admin.register(LeadUser)
class LeadUserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'call', 'send', 'status', 'assigned_to')
    
# @admin.register(Staff)
# class StaffAdmin(admin.ModelAdmin):
#     list_display= ('name', 'phone','email','last_login','action')

class AllUser(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_admin', 'is_team_leader', 'is_staff_new', 'login_time', 'logout_time', 'created_date','updated_date']
    search_fields = ('name',)
    
class AdminUser(admin.ModelAdmin):
    list_display = ['user', 'name', 'email', 'admin_id', 'created_date', 'updated_date']
    search_fields = ('user',)

class Team_LeaderUser(admin.ModelAdmin):
    list_display = ['name', 'admin','email', 'team_leader_id', 'created_date','updated_date']
    search_fields = ('name',)

@admin.register(Team_LeadData)
class Team_LeadData(admin.ModelAdmin):
    list_display = ('name', 'email', 'call', 'send', 'status','assigned_to')

class StaffUser(admin.ModelAdmin):
    list_display = ['name','team_leader', 'email', 'staff_id', 'created_date','updated_date']
    search_fields = ('name',)
# class AssignedUser(admin.ModelAdmin):
#     list_display = ['assigned_to']
    # search_fields = ('name',)



@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'clock_in', 'clock_out', 'hours_worked', 'status_display')
    list_filter = ('date', 'user')
    search_fields = ('user__username', 'user__email')
    ordering = ('-date',)
    readonly_fields = ('hours_worked',)

    def status_display(self, obj):
        if obj.clock_in and obj.clock_out:
            return 'Present'
        elif obj.clock_in and not obj.clock_out:
            return 'Incomplete'
        else:
            return 'Absent'
    status_display.short_description = 'Status'

    def has_add_permission(self, request):
        # Optionally prevent adding from admin manually
        return True

    def has_change_permission(self, request, obj=None):
        # You can allow edits if needed
        return True

    def has_delete_permission(self, request, obj=None):
        # Allow or disallow deletion of attendance logs
        return True

    
admin.site.register(User, AllUser)
admin.site.register(Admin, AdminUser)
admin.site.register(Team_Leader, Team_LeaderUser)
admin.site.register(Staff, StaffUser)
admin.site.register(ActivityLog)
admin.site.register(Marketing)
# admin.site.register(UserActivityLog)
# admin.site.register(Assigned, AssignedUser)

