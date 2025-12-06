"""
Views API para la aplicación móvil de estudiantes.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import date
import sys

from loginApp.models import Usuario, Asignatura, Ayudantia, Inscripcion, Sede
from .serializers import (
    UsuarioSerializer,
    AsignaturaSerializer,
    AyudantiaSerializer,
    InscripcionSerializer,
    SedeSerializer,
    LoginSerializer,
)


class EstudianteOnlyPermission(IsAuthenticated):
    """
    Permiso personalizado que verifica que el usuario sea un estudiante.
    """
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        
        # Verificar que sea del tipo Usuario
        from loginApp.models import Usuario
        if not isinstance(request.user, Usuario):
            return False
        
        # Verificar que sea estudiante (no staff ni tutor)
        if request.user.is_staff or request.user.is_tutor:
            return False
        
        return True


class LoginView(APIView):
    """
    Endpoint para login de estudiantes.
    Retorna tokens JWT para autenticación.
    """
    permission_classes = []
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            # Generar tokens JWT con el campo personalizado
            refresh = RefreshToken()
            refresh['user_id'] = user.id_usuario
            refresh['email'] = user.email
            refresh['is_student'] = not (user.is_staff or user.is_tutor)
            
            access = refresh.access_token
            access['user_id'] = user.id_usuario
            access['email'] = user.email
            access['is_student'] = not (user.is_staff or user.is_tutor)
            
            # Actualizar last_login dentro del schema_context
            from django_tenants.utils import schema_context
            if hasattr(request, 'tenant'):
                with schema_context(request.tenant.schema_name):
                    user.last_login = timezone.now()
                    user.save(update_fields=['last_login'])
            
            return Response({
                'success': True,
                'message': 'Login exitoso',
                'user': UsuarioSerializer(user).data,
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            }, status=status.HTTP_200_OK)
        
        # Formatear errores de manera más amigable
        error_messages = []
        for field, errors in serializer.errors.items():
            if isinstance(errors, list):
                error_messages.extend(errors)
            else:
                error_messages.append(str(errors))
        
        return Response({
            'success': False,
            'errors': serializer.errors,
            'message': error_messages[0] if error_messages else 'Error de validación',
            'non_field_errors': error_messages
        }, status=status.HTTP_400_BAD_REQUEST)


class PerfilView(APIView):
    """
    Endpoint para obtener el perfil del estudiante autenticado.
    """
    permission_classes = [EstudianteOnlyPermission]
    
    def get(self, request):
        from django_tenants.utils import schema_context
        
        # Usar schema_context si hay tenant en el request
        if hasattr(request, 'tenant'):
            with schema_context(request.tenant.schema_name):
                serializer = UsuarioSerializer(request.user)
                return Response({
                    'success': True,
                    'data': serializer.data
                })
        else:
            return Response({
                'success': False,
                'error': 'No se pudo identificar el tenant'
            }, status=status.HTTP_400_BAD_REQUEST)


class AsignaturaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar y ver detalles de asignaturas.
    Solo muestra asignaturas con ayudantías disponibles.
    """
    permission_classes = [EstudianteOnlyPermission]
    serializer_class = AsignaturaSerializer
    queryset = Asignatura.objects.none()  # Se sobrescribe en get_queryset
    
    def get_queryset(self):
        """Retorna solo asignaturas con ayudantías activas disponibles"""
        # El schema_context se maneja en list(), aquí solo construimos el queryset
        if hasattr(self.request, 'tenant'):
            return Asignatura.objects.filter(
                is_active=True,
                ayudantias__is_active=True,
                ayudantias__is_cursada=False,
                ayudantias__fecha__gte=date.today(),
                ayudantias__cupos_disponibles__gt=0
            ).distinct().prefetch_related('ayudantias').order_by('nombre')
        else:
            return Asignatura.objects.none()
    
    def list(self, request, *args, **kwargs):
        """Sobrescribir list para asegurar que el schema_context esté activo durante toda la operación"""
        from django_tenants.utils import schema_context
        
        if not hasattr(request, 'tenant'):
            sys.stdout.write("[API Mobile AsignaturaViewSet] ERROR: No hay tenant en request\n")
            sys.stdout.flush()
            return Response({
                'success': False,
                'error': 'No se pudo identificar el tenant'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        sys.stdout.write(f"[API Mobile AsignaturaViewSet] Tenant: {request.tenant.schema_name}\n")
        sys.stdout.flush()
        
        # Asegurar que el schema_context esté activo durante toda la operación
        # Esto es crítico: todas las operaciones de BD deben ejecutarse dentro del schema_context
        with schema_context(request.tenant.schema_name):
            try:
                sys.stdout.write(f"[API Mobile AsignaturaViewSet] Construyendo queryset en schema: {request.tenant.schema_name}\n")
                sys.stdout.flush()
                
                # Construir el queryset dentro del schema_context
                queryset = Asignatura.objects.filter(
                    is_active=True,
                    ayudantias__is_active=True,
                    ayudantias__is_cursada=False,
                    ayudantias__fecha__gte=date.today(),
                    ayudantias__cupos_disponibles__gt=0
                ).distinct().prefetch_related('ayudantias').order_by('nombre')
                
                sys.stdout.write(f"[API Mobile AsignaturaViewSet] Queryset construido, aplicando filtros\n")
                sys.stdout.flush()
                
                # Aplicar filtros si existen
                queryset = self.filter_queryset(queryset)
                
                sys.stdout.write(f"[API Mobile AsignaturaViewSet] Aplicando paginación\n")
                sys.stdout.flush()
                
                # Evaluar el queryset dentro del schema_context antes de paginar
                sys.stdout.write(f"[API Mobile AsignaturaViewSet] Evaluando queryset dentro del schema_context\n")
                sys.stdout.flush()
                
                # Convertir a lista para forzar evaluación dentro del schema_context
                queryset_list = list(queryset)
                sys.stdout.write(f"[API Mobile AsignaturaViewSet] Queryset evaluado: {len(queryset_list)} elementos\n")
                sys.stdout.flush()
                
                # Usar paginación de DRF pero con el queryset ya evaluado
                # Crear un queryset falso para la paginación
                from django.core.paginator import Paginator
                from rest_framework.pagination import PageNumberPagination
                
                page_size = 10  # Tamaño de página por defecto
                if hasattr(self, 'pagination_class') and self.pagination_class:
                    page_size = getattr(self.pagination_class, 'page_size', 10)
                
                page_number = request.query_params.get('page', 1)
                try:
                    page_number = int(page_number)
                except (ValueError, TypeError):
                    page_number = 1
                
                # Paginar la lista
                paginator = Paginator(queryset_list, page_size)
                try:
                    page_obj = paginator.page(page_number)
                except:
                    page_obj = paginator.page(1)
                    page_number = 1
                
                sys.stdout.write(f"[API Mobile AsignaturaViewSet] Serializando página {page_number} ({len(page_obj.object_list)} elementos)\n")
                sys.stdout.flush()
                
                # Serialización dentro del schema_context
                serializer = self.get_serializer(page_obj.object_list, many=True)
                
                # Construir respuesta paginada
                response_data = {
                    'count': paginator.count,
                    'next': page_obj.next_page_number() if page_obj.has_next() else None,
                    'previous': page_obj.previous_page_number() if page_obj.has_previous() else None,
                    'results': serializer.data
                }
                
                # Construir URLs de next y previous
                base_url = request.build_absolute_uri().split('?')[0]
                if response_data['next']:
                    response_data['next'] = f"{base_url}?page={response_data['next']}"
                if response_data['previous']:
                    response_data['previous'] = f"{base_url}?page={response_data['previous']}"
                
                sys.stdout.write(f"[API Mobile AsignaturaViewSet] Respuesta paginada construida\n")
                sys.stdout.flush()
                
                return Response(response_data)
            except Exception as e:
                import traceback
                sys.stdout.write(f"[API Mobile AsignaturaViewSet] ERROR en list: {e}\n")
                sys.stdout.write(f"[API Mobile AsignaturaViewSet] Traceback: {traceback.format_exc()}\n")
                sys.stdout.flush()
                return Response({
                    'success': False,
                    'error': f'Error al obtener asignaturas: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AyudantiaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar y ver detalles de ayudantías.
    """
    permission_classes = [EstudianteOnlyPermission]
    serializer_class = AyudantiaSerializer
    queryset = Ayudantia.objects.none()
    
    def get_queryset(self):
        """Retorna solo ayudantías activas y futuras"""
        # El schema_context se maneja en list(), aquí solo construimos el queryset
        if hasattr(self.request, 'tenant'):
            queryset = Ayudantia.objects.filter(
                is_active=True,
                is_cursada=False,
                fecha__gte=date.today()
            ).select_related('asignatura', 'tutor').order_by('fecha', 'horario')
            
            # Filtro opcional por asignatura
            asignatura_id = self.request.query_params.get('asignatura_id', None)
            if asignatura_id:
                queryset = queryset.filter(asignatura_id=asignatura_id)
            
            return queryset
        else:
            return Ayudantia.objects.none()
    
    def list(self, request, *args, **kwargs):
        """Sobrescribir list para asegurar que el schema_context esté activo durante toda la operación"""
        from django_tenants.utils import schema_context
        
        if not hasattr(request, 'tenant'):
            return Response({
                'success': False,
                'error': 'No se pudo identificar el tenant'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Asegurar que el schema_context esté activo durante toda la operación
        with schema_context(request.tenant.schema_name):
            # Llamar a get_queryset dentro del schema_context
            queryset = self.filter_queryset(self.get_queryset())
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
    
    def get_serializer_context(self):
        """Agrega el request al contexto del serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def get_object(self):
        """Sobrescribir get_object para usar schema_context"""
        from django_tenants.utils import schema_context
        
        if not hasattr(self.request, 'tenant'):
            from rest_framework.exceptions import NotFound
            raise NotFound('No se pudo identificar el tenant')
        
        # Obtener el objeto dentro del schema_context
        with schema_context(self.request.tenant.schema_name):
            return super().get_object()
    
    @action(detail=True, methods=['post'])
    def inscribirse(self, request, pk=None):
        """
        Endpoint para que un estudiante se inscriba en una ayudantía.
        """
        from django_tenants.utils import schema_context
        
        sys.stdout.write(f"[API Mobile AyudantiaViewSet] inscribirse llamado para pk={pk}\n")
        sys.stdout.flush()
        
        if not hasattr(request, 'tenant'):
            sys.stdout.write("[API Mobile AyudantiaViewSet] ERROR: No hay tenant en request\n")
            sys.stdout.flush()
            return Response({
                'success': False,
                'message': 'No se pudo identificar el tenant.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        sys.stdout.write(f"[API Mobile AyudantiaViewSet] Tenant: {request.tenant.schema_name}\n")
        sys.stdout.flush()
        sys.stdout.write(f"[API Mobile AyudantiaViewSet] Usuario: {request.user.email if request.user.is_authenticated else 'NO AUTENTICADO'}\n")
        sys.stdout.flush()
        
        with schema_context(request.tenant.schema_name):
            try:
                # get_object() ya usa schema_context internamente, pero lo llamamos dentro del contexto
                # para asegurar que todas las operaciones estén en el schema correcto
                ayudantia = self.get_object()
                sys.stdout.write(f"[API Mobile AyudantiaViewSet] Ayudantía obtenida: {ayudantia.id_ayudantia} - {ayudantia.titulo}\n")
                sys.stdout.flush()
                
                estudiante = request.user
                
                # Validaciones
                if ayudantia.is_cursada:
                    sys.stdout.write("[API Mobile AyudantiaViewSet] Ayudantía ya fue cursada\n")
                    sys.stdout.flush()
                    return Response({
                        'success': False,
                        'message': 'Esta ayudantía ya fue cursada.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if ayudantia.fecha < date.today():
                    sys.stdout.write("[API Mobile AyudantiaViewSet] Ayudantía ya pasó\n")
                    sys.stdout.flush()
                    return Response({
                        'success': False,
                        'message': 'Esta ayudantía ya pasó.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                if ayudantia.cupos_disponibles <= 0:
                    sys.stdout.write("[API Mobile AyudantiaViewSet] No hay cupos disponibles\n")
                    sys.stdout.flush()
                    return Response({
                        'success': False,
                        'message': 'No hay cupos disponibles para esta ayudantía.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Verificar si ya está inscrito
                if Inscripcion.objects.filter(
                    estudiante=estudiante,
                    ayudantia=ayudantia,
                    estado='activa'
                ).exists():
                    sys.stdout.write("[API Mobile AyudantiaViewSet] Ya está inscrito\n")
                    sys.stdout.flush()
                    return Response({
                        'success': False,
                        'message': 'Ya estás inscrito en esta ayudantía.'
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Crear la inscripción
                sys.stdout.write("[API Mobile AyudantiaViewSet] Creando inscripción\n")
                sys.stdout.flush()
                inscripcion = Inscripcion.objects.create(
                    estudiante=estudiante,
                    ayudantia=ayudantia,
                    estado='activa'
                )
                sys.stdout.write(f"[API Mobile AyudantiaViewSet] Inscripción creada: {inscripcion.id_inscripcion}\n")
                sys.stdout.flush()
                
                # Actualizar cupos disponibles
                ayudantia.cupos_disponibles -= 1
                ayudantia.save(update_fields=['cupos_disponibles'])
                sys.stdout.write(f"[API Mobile AyudantiaViewSet] Cupos actualizados: {ayudantia.cupos_disponibles}\n")
                sys.stdout.flush()
                
                serializer = InscripcionSerializer(inscripcion, context={'request': request})
                sys.stdout.write("[API Mobile AyudantiaViewSet] Inscripción exitosa\n")
                sys.stdout.flush()
                
                return Response({
                    'success': True,
                    'message': f'Te has inscrito exitosamente en la ayudantía: {ayudantia.titulo}',
                    'data': serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                import traceback
                sys.stdout.write(f"[API Mobile AyudantiaViewSet] ERROR en inscribirse: {e}\n")
                sys.stdout.write(f"[API Mobile AyudantiaViewSet] Traceback: {traceback.format_exc()}\n")
                sys.stdout.flush()
                return Response({
                    'success': False,
                    'message': f'Error al inscribirse: {str(e)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InscripcionViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar las inscripciones del estudiante.
    """
    permission_classes = [EstudianteOnlyPermission]
    serializer_class = InscripcionSerializer
    
    def get_queryset(self):
        """Retorna solo las inscripciones del estudiante autenticado"""
        # El schema_context se maneja en list(), aquí solo construimos el queryset
        if hasattr(self.request, 'tenant'):
            return Inscripcion.objects.filter(
                estudiante=self.request.user,
                estado='activa',
                ayudantia__is_cursada=False
            ).select_related('ayudantia', 'ayudantia__asignatura', 'ayudantia__tutor').order_by('-fecha_inscripcion')
        else:
            return Inscripcion.objects.none()
    
    def list(self, request, *args, **kwargs):
        """Sobrescribir list para asegurar que el schema_context esté activo durante toda la operación"""
        from django_tenants.utils import schema_context
        
        if not hasattr(request, 'tenant'):
            return Response({
                'success': False,
                'error': 'No se pudo identificar el tenant'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Asegurar que el schema_context esté activo durante toda la operación
        with schema_context(request.tenant.schema_name):
            # Llamar a get_queryset dentro del schema_context
            queryset = self.filter_queryset(self.get_queryset())
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
    
    def get_serializer_context(self):
        """Agrega el request al contexto del serializer"""
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
    
    def create(self, request, *args, **kwargs):
        """Sobrescribir create para usar ayudantia_id"""
        from django_tenants.utils import schema_context
        
        if not hasattr(request, 'tenant'):
            return Response({
                'success': False,
                'message': 'No se pudo identificar el tenant.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        ayudantia_id = request.data.get('ayudantia_id')
        if not ayudantia_id:
            return Response({
                'success': False,
                'message': 'Debe proporcionar ayudantia_id'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with schema_context(request.tenant.schema_name):
            ayudantia = get_object_or_404(Ayudantia, id_ayudantia=ayudantia_id, is_active=True, is_cursada=False)
            
            # Validaciones (similares a inscribirse)
            if ayudantia.fecha < date.today():
                return Response({
                    'success': False,
                    'message': 'Esta ayudantía ya pasó.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if ayudantia.cupos_disponibles <= 0:
                return Response({
                    'success': False,
                    'message': 'No hay cupos disponibles.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            if Inscripcion.objects.filter(estudiante=request.user, ayudantia=ayudantia, estado='activa').exists():
                return Response({
                    'success': False,
                    'message': 'Ya estás inscrito en esta ayudantía.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            inscripcion = Inscripcion.objects.create(
                estudiante=request.user,
                ayudantia=ayudantia,
                estado='activa'
            )
            
            ayudantia.cupos_disponibles -= 1
            ayudantia.save(update_fields=['cupos_disponibles'])
            
            serializer = self.get_serializer(inscripcion)
            return Response({
                'success': True,
                'message': 'Inscripción exitosa',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """
        Endpoint para cancelar una inscripción.
        """
        from django_tenants.utils import schema_context
        
        if not hasattr(request, 'tenant'):
            return Response({
                'success': False,
                'message': 'No se pudo identificar el tenant.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        with schema_context(request.tenant.schema_name):
            inscripcion = self.get_object()
            
            if inscripcion.estado != 'activa':
                return Response({
                    'success': False,
                    'message': 'Solo se pueden cancelar inscripciones activas.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Devolver cupo a la ayudantía
            ayudantia = inscripcion.ayudantia
            ayudantia.cupos_disponibles += 1
            ayudantia.save(update_fields=['cupos_disponibles'])
            
            # Eliminar la inscripción
            inscripcion.delete()
            
            return Response({
                'success': True,
                'message': 'Inscripción cancelada exitosamente.'
            }, status=status.HTTP_200_OK)


class SedeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para listar sedes.
    """
    permission_classes = [EstudianteOnlyPermission]
    serializer_class = SedeSerializer
    queryset = Sede.objects.none()
    
    def get_queryset(self):
        """Retorna solo sedes activas"""
        # El schema_context se maneja en list(), aquí solo construimos el queryset
        if hasattr(self.request, 'tenant'):
            return Sede.objects.filter(is_active=True).order_by('nombre')
        else:
            return Sede.objects.none()
    
    def list(self, request, *args, **kwargs):
        """Sobrescribir list para asegurar que el schema_context esté activo durante toda la operación"""
        from django_tenants.utils import schema_context
        
        if not hasattr(request, 'tenant'):
            return Response({
                'success': False,
                'error': 'No se pudo identificar el tenant'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Asegurar que el schema_context esté activo durante toda la operación
        with schema_context(request.tenant.schema_name):
            # Llamar a get_queryset dentro del schema_context
            queryset = self.filter_queryset(self.get_queryset())
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
