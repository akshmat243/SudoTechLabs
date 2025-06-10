from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    path('super_admin_dashboard/', views.super_admin, name='super_admin'),
    path('super_admin_profile/', views.superadmin_view_profile, name='super_admin_profile'),
    path('admin_add/', views.admin_add, name='admin_add'),
    path('adminedit/<int:id>/', views.adminedit, name='editadmin'),
    
    path('admin_dashboard/', views.admin_user, name='team_leader_user'),
    path('add_team_leader_user/', views.add_team_leader_user, name='add_team_leader_user'),
    path('admin_view_profile/', views.admin_view_profile,name='admin_view_profile'),
    path('teamedit/<int:id>/', views.teamedit, name='teamedit'),
    
    path('teamlead_dashboard/', views.teamlead_user, name='staff_user'),
    path('team_view_profile/', views.team_view_profile, name='team_view_profile'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('staffedit/<int:id>/', views.staffedit, name='staffedit'),
    
    path('staff_dashboard/', views.staff_user, name='leads'),       #1
    path('staff_view_profile/', views.staff_view_profile, name='staff_view_profile'),
    path('overview/', views.overview, name='overview'),
    
    path('clock-in/', views.clock_in_user, name='clock_in'),
    path('clock-out/', views.clock_out_user, name='clock_out'),
    path('clock-status/', views.check_clock_status, name='clock_status'),
    
    path('activitylogs/', views.activitylogs, name='activitylogs'),
    path('create-lead/', views.create_lead, name='create_lead'),
    
    path('lost_leads/', views.lost_leads, name='lost_leads'),               #2
    path('customer/', views.customer, name='customer'),                     #3
    path('maybe/', views.maybe, name='maybe'),                              #4
    path('not_picked/', views.not_picked, name='not_picked'),               #5
    path('lost/', views.lost, name='lost'),                                 #6
    path('project/', views.project, name='project'),                        #7
    
    path('status_update/', views.status_update, name='status_update'),          #1
    path('update_send_status/', views.update_send_status, name='update_send_status'),
    path('send_file/<int:file_id>/', views.send_file_to_client, name='send_file_to_client'),
    path('lead/', views.lead, name='lead'),
    path('bulk_from/', views.bulk_from, name='bulk_from'),
    path('to-test-data/', views.bulk_from_data, name='bulk_from_data'),
    path('excel_upload/', views.excel_upload, name='excel_upload'),
    
    # path('import_leads/', views.import_leads, name='import_leads'),
    # path('home/', views.home, name='home'),
    # path('', views.super_dashboard, name='super_dashboard'),
    # path('add_user/', views.add_user, name='add_user'),
    # path('staff/', views.staff, name='staff'),
    # path('new_staff_add/', views.new_staff_add, name='new_staff_add'),
    # path('import/', views.import_data, name='import_data'),
    # path('update_user/', views.update_user, name='update_user'),
    # path('Staff_excel_upload/', views.Staff_excel_upload, name='Staff_excel_upload'),
    # path('send-data/', views.send_data, name='send_data'),

    path('team_dashboard/', views.team_dashboard, name='team_dashboard'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('leads/', views.staff_dashboard, name='staff_dashboard'),
    path('edit-marketing/<str:source>/', views.edit_record, name='edit-marketing'),
    path('update-record/', views.update_record, name='update_record'),





] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
