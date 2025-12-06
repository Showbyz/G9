"""
URLs públicas para cuando no se identifica un tenant.
Estas URLs se usan cuando el middleware de tenants no puede identificar un tenant.
"""
from django.urls import path, include
from . import views_public

urlpatterns = [
    path('', views_public.public_index, name='public_index'),
    path('welcome/', views_public.public_welcome, name='public_welcome'),
    # Incluir las URLs de globalAdmin para que funcionen desde el schema público
    path('global/', include('globalAdmin.urls')),
    # Incluir las URLs de la API móvil
    path('api/mobile/', include('api_mobile.urls')),
]

