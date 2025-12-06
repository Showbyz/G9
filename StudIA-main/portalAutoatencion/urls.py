"""
URL configuration for portalAutoatencion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

# IMPORTANTE: Las URLs de globalAdmin deben ir ANTES para que se procesen
# antes de que el middleware de tenants intente identificar el tenant
urlpatterns = [
    path('global/', include('globalAdmin.urls')),
    path('api/mobile/', include('api_mobile.urls')),  # API móvil para estudiantes
    path('', include('loginApp.urls')),
]
