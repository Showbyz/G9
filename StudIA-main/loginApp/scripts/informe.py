import csv
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from loginApp.models import Usuario
from solicitudesManager.models import Solicitud

now = timezone.now()
last_24h = now - relativedelta(hours=24)
last_7d = now - relativedelta(days=7)
last_1m = now - relativedelta(months=1)

def gen_informe(periodo, response, formato):
    match periodo:
        case "24h":
            lista_solicitudes = Solicitud.objects.filter(created_at__gte=last_24h)
        case "7d":
            lista_solicitudes = Solicitud.objects.filter(created_at__gte=last_7d)
        case "1m":
            lista_solicitudes = Solicitud.objects.filter(created_at__gte=last_1m)
    # hocus pocus crear el csv
    if formato == "pdf":
        to_pdf()
    else:
        to_csv(lista_solicitudes, response)
    
    # pendiente el crear un pdf cuando sea necesario, ver que libreria usar y procesar el formato requerido si fuera posible

def to_csv(datos, response):
    campos = [campo.verbose_name for campo in Solicitud._meta.fields]
    archivo = csv.writer(response)
    archivo.writerow(campos)
    solicitudes = datos.values_list()
    for solicitud in solicitudes:
        solicitud = list(solicitud)
        usuario = Usuario.objects.get(id_usuario = solicitud[-1])
        solicitud[-1] = usuario.nombre_usuario
        archivo.writerow(solicitud)

def to_pdf():
    print("pum, archivo pdf")
    pass