from django.db import models
from loginApp.models import Usuario

class Solicitud(models.Model):
    id_sol = models.AutoField(primary_key=True, verbose_name="ID de la Solicitud")
    estado_sol = models.CharField(max_length=25, verbose_name = "Estado", default="Pendiente")
    tipo_sol = models.CharField(max_length=75, verbose_name="Tipo de Solicitud")
    campos_sol = models.JSONField(verbose_name="Campos del Formulario")
    created_at = models.DateTimeField(auto_now_add=True, null=True, verbose_name="Fecha de creación")
    
    #Este campo aplicará solo en formularios con adjuntos, asi evito que explote el json de arriba o crear otra tabla
    adjunto_sol = models.FileField(blank=True, null=True, verbose_name="Archivos Adjuntos")
    
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, verbose_name = "Usuario")

    class Meta:
        verbose_name = "Solicitud"
        verbose_name_plural = "Solicitudes"
        
    def __str__(self):
        return str(self.id_sol)
    
# Create your models here.
