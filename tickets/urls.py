from django.urls import path
from . import views, analytics_views, debug_views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('create-ticket/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_detail, name='ticket_detail'),
    path('tickets/', views.ticket_list, name='ticket_list'),
    path('export-tickets/', views.export_tickets, name='export_tickets'),
    path('api/ticket-stats/', views.api_ticket_stats, name='api_ticket_stats'),
    
    # Debug URLs
    path('debug/admin/', debug_views.debug_admin_credentials, name='debug_admin'),
    
    # Analytics URLs
    path('analytics/', analytics_views.analytics_dashboard, name='analytics_dashboard'),
    path('forecasting/', analytics_views.forecasting_dashboard, name='forecasting_dashboard'),
    path('budget/', analytics_views.budget_management, name='budget_management'),
    path('budget/report/', analytics_views.budget_report_table, name='budget_report_table'),
    path('budget/download/', analytics_views.download_budget_report, name='download_budget_report'),
    path('budget/create/', analytics_views.create_budget, name='create_budget'),
    path('budget/<int:budget_id>/edit/', analytics_views.edit_budget, name='edit_budget'),
    path('api/analytics/', analytics_views.api_analytics_data, name='api_analytics_data'),
 
    path('archived-tickets/', views.view_archived_tickets, name='archived_tickets'),
    path('archive-resolved/', views.archive_resolved_tickets, name='archive_resolved_tickets'),
    
    # User Management URLs

]
