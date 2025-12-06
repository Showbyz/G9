"""
URLs para la administración global.
"""
from django.urls import path
from . import views

app_name = 'global_admin'

urlpatterns = [
    path('login/', views.global_login, name='login'),
    path('logout/', views.global_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tenants/', views.tenant_list, name='tenant_list'),
    path('tenants/create/', views.tenant_create, name='tenant_create'),
    path('tenants/<int:tenant_id>/edit/', views.tenant_edit, name='tenant_edit'),
    path('tenants/<int:tenant_id>/suspend/', views.tenant_suspend, name='tenant_suspend'),
    path('tenants/<int:tenant_id>/activate/', views.tenant_activate, name='tenant_activate'),
    path('tenants/<int:tenant_id>/impersonate/', views.tenant_impersonate, name='tenant_impersonate'),
    path('tenants/<int:tenant_id>/create-admin-user/', views.tenant_create_admin_user, name='tenant_create_admin_user'),
    path('tenants/<int:tenant_id>/run-migrations/', views.tenant_run_migrations, name='tenant_run_migrations'),
    path('stop-impersonate/', views.tenant_stop_impersonate, name='stop_impersonate'),
]

