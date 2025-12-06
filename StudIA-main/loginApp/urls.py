from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('logout', views.logoutProcess, name='logout'),
    path('home', views.home, name='home'),
    # URLs para usuarios
    path('solicitud/<int:pk>', views.verSolicitud, name="verSolicitud"),
    path('mis_solicitudes', views.solicitudesUsuario, name="infoSolicitudes"),
    path('borrarsolicitud/<int:pk>', views.borrarSolicitud, name="borrarSolicitud"),
    path('solicitudes_empresa', views.estadoSolicitudes, name="solicitudes_empresa"),
    path('bienvenida', bienvenida, name='bienvenida'),
    
    # URLs para tutores
    path('tutor/dashboard', views.tutor_dashboard, name='tutor_dashboard'),
    path('tutor/solicitudes', views.tutor_solicitudes, name='tutor_solicitudes'),
    path('tutor/solicitud/<int:pk>', views.tutor_ver_solicitud, name='tutor_ver_solicitud'),
    path('tutor/actualizar/<int:pk>', views.tutor_actualizar_solicitud, name='tutor_actualizar_solicitud'),
    path('tutor/ayudantias', views.tutor_mis_ayudantias, name='tutor_mis_ayudantias'),
    path('tutor/ayudantia/<int:ayudantia_id>', views.tutor_detalle_ayudantia, name='tutor_detalle_ayudantia'),
    path('tutor/ayudantia/<int:ayudantia_id>/registrar-asistencia', views.tutor_registrar_asistencia, name='tutor_registrar_asistencia'),
    path('tutor/ayudantia/<int:ayudantia_id>/marcar-cursada', views.tutor_marcar_cursada, name='tutor_marcar_cursada'),
    path('tutor/logs', views.tutor_logs, name='tutor_logs'),
    path('tutor/logs/exportar-excel', views.tutor_exportar_logs_excel, name='tutor_exportar_logs_excel'),
    
    # URLs para estudiantes
    path('estudiante/asignaturas', views.estudiante_asignaturas, name='estudiante_asignaturas'),
    path('estudiante/asignatura/<int:asignatura_id>', views.estudiante_ayudantias_asignatura, name='estudiante_ayudantias_asignatura'),
    path('estudiante/inscribirse/<int:ayudantia_id>', views.estudiante_inscribirse, name='estudiante_inscribirse'),
    path('estudiante/mis-ayudantias', views.estudiante_mis_ayudantias, name='estudiante_mis_ayudantias'),
    path('estudiante/cancelar/<int:inscripcion_id>', views.estudiante_cancelar_inscripcion, name='estudiante_cancelar_inscripcion'),
    
    # URLs para admins
    path('usuarios', views.usuarios, name='usuarios'),
    path('casos', views.casosDeUso, name='casosDeUso'),
    path('crear/usuario', views.crearUsuario, name='crearUsuario'),
    path('editar/usuario/<int:pk>', views.editarUsuario, name="editarUsuario"),
    path('editar/solicitud/<int:pk>', views.editarSolicitud, name="editarSolicitud"),
    path('editar/clave/<int:pk>', views.editarClaveAdmin, name='editarClaveAdmin'),
    path('borrarusuario/<int:pk>', views.borrarUsuario, name='borrarUsuario'),
    path('reportes', views.reportes, name='reporteria'),
    path('borrar/<int:pk>', views.borrarUsuario, name='borrarUsuario'),
    path('logout', views.logoutProcess, name='logout'),
    path('home', views.home, name='home'),
    path('usuarios', views.usuarios, name='usuarios'),
    path('crear/usuario', views.crearUsuario, name='nuevoUsuario'),
    
    # URLs para administradores - Asignaturas
    path('admin/asignaturas', views.admin_asignaturas, name='admin_asignaturas'),
    path('admin/editar-asignatura/<int:asignatura_id>', views.admin_editar_asignatura, name='admin_editar_asignatura'),
    path('admin/eliminar-asignatura/<int:asignatura_id>', views.admin_eliminar_asignatura, name='admin_eliminar_asignatura'),
    
    # URLs para administradores - Ayudantías
    path('admin/crear-ayudantia', views.admin_crear_ayudantia, name='admin_crear_ayudantia'),
    path('admin/ayudantias', views.admin_ayudantias, name='admin_ayudantias'),
    path('admin/editar-ayudantia/<int:ayudantia_id>', views.admin_editar_ayudantia, name='admin_editar_ayudantia'),
    path('admin/eliminar-ayudantia/<int:ayudantia_id>', views.admin_eliminar_ayudantia, name='admin_eliminar_ayudantia'),
    
    # URLs para administradores - Logs
    path('admin/logs', views.admin_logs, name='admin_logs'),
    path('admin/logs/exportar-excel', views.admin_exportar_logs_excel, name='admin_exportar_logs_excel'),
    
    # URLs para test de APIs
    path('test/api-feriados', views.test_api_feriados, name='test_api_feriados'),
    path('test/mapa-sedes', views.test_mapa_sedes, name='test_mapa_sedes'),

]