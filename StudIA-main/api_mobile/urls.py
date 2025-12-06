"""
URLs para la API móvil de estudiantes.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginView,
    PerfilView,
    AsignaturaViewSet,
    AyudantiaViewSet,
    InscripcionViewSet,
    SedeViewSet,
)

# Crear router para los viewsets
router = DefaultRouter()
router.register(r'asignaturas', AsignaturaViewSet, basename='asignatura')
router.register(r'ayudantias', AyudantiaViewSet, basename='ayudantia')
router.register(r'inscripciones', InscripcionViewSet, basename='inscripcion')
router.register(r'sedes', SedeViewSet, basename='sede')

urlpatterns = [
    # Autenticación
    path('auth/login/', LoginView.as_view(), name='api_login'),
    path('auth/perfil/', PerfilView.as_view(), name='api_perfil'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Incluir rutas del router
    path('', include(router.urls)),
]

