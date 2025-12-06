from django import forms
from .models import Usuario, Asignatura, Ayudantia, Inscripcion
from datetime import date, datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import re

design = "w-100 mb-2 p-2 border border-1"


class CambioClaveUsuarioForm(forms.Form):
    pass

class ReporteriaForm(forms.Form):
    opciones = (
        ("24h", "24 Horas" ),
        ("7d", "7 Días"),
        ("1m", "1 Mes"),
    )
    formatos = (
        ("csv", "CSV"),
        ("pdf", "PDF"),
    )
    periodo_reportes = forms.ChoiceField(choices=opciones, label="Periodo de Reportes")
    formato_reportes = forms.ChoiceField(choices=formatos, label="Formato de los Reportes")
    
class Ise_Vpn_Form(forms.Form):
    acciones = (
        ("Nada", "------"),
        ("Ayudantía de Matemáticas", "Ayudantía de Matemáticas"),
        ("Ayudantía de Base de datos", "Ayudantía de base de datos"),
        ("Ayudantía de programación web", "Ayudantía de programación web"),
        ("Ayudantía de Aplicaciones Móviles", "Ayudantía de Aplicaciones Móviles"),
  
    )
    accion = forms.ChoiceField(choices=acciones, label="Accion",
                               widget=forms.Select(attrs={'class': f"form-select {design}"}))

    usuario = forms.CharField(label="Usuario",
                              widget=forms.TextInput(attrs={"class": f"form-control {design}"}))

    correo_usuario = forms.EmailField(label="Correo del Usuario",
                                      widget=forms.EmailInput(attrs={"class": f"form-control {design}"}))

    fecha_expiracion = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', "class": f"form-control {design}"}),
                                       label="Fecha", required=False)

    prefix = "Solicitud de hora"
    
    def clean_usuario(self):
        usuario = self.cleaned_data['usuario']
        if not re.match(r'^[a-zA-Z]{3,}$', usuario):
            raise ValidationError(_('El usuario debe contener al menos 3 letras y no números.'))
        return usuario

    def clean_correo_usuario(self):
        correo_usuario = self.cleaned_data['correo_usuario']
        if not re.match(r'^\S+@\S+\.\S+$', correo_usuario):
            raise ValidationError(_('Por favor, ingrese una dirección de correo válida. Ej: Nombre@example.com'))
        return correo_usuario

    def clean_fecha_expiracion(self):
        fecha_expiracion = self.cleaned_data.get('fecha_expiracion')
        if fecha_expiracion and fecha_expiracion <= date.today():
            raise ValidationError(_('La fecha debe ser a partir del siguiente día en adelante.'))
        return fecha_expiracion
        
form_dict = {
    Ise_Vpn_Form().prefix: Ise_Vpn_Form,
}

class FiltrodeFormulariosForm(forms.Form):
    opciones = [(k,k) for k in form_dict.keys()]
    lista_formularios = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, choices=opciones)

class CambioClaveAdminForm(forms.Form):
    nueva_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={"class": f"form-control {design}"}), min_length=6)
    confirmar_nueva_contraseña = forms.CharField(widget=forms.PasswordInput(attrs={"class": f"form-control {design}"}))

    def clean(self):
        cleaned_data = super().clean()
        nueva_contraseña = cleaned_data.get("nueva_contraseña")
        confirmar_nueva_contraseña = cleaned_data.get("confirmar_nueva_contraseña")

        if nueva_contraseña and confirmar_nueva_contraseña and nueva_contraseña != confirmar_nueva_contraseña:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        if nueva_contraseña and not self.validar_contraseña(nueva_contraseña):
            raise forms.ValidationError("La contraseña debe tener al menos 6 caracteres, incluyendo al menos 2 números, una mayúscula y un punto.")

    def validar_contraseña(self, contraseña):
        if len(contraseña) < 6:
            return False
        if sum(c.isdigit() for c in contraseña) < 2:
            return False
        if not any(c.isupper() for c in contraseña):
            return False
        if '.' not in contraseña:
            return False
        return True

class CrearUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre_usuario", "email", "password", "telefono", "cargo", "is_staff", "is_tutor"]
        widgets = {
            "nombre_usuario": forms.TextInput(attrs={"class": "form-control", "id": "id_nombre_usuario"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "id": "id_email"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "id": "id_password"}),
            "telefono": forms.TextInput(attrs={"class": "form-control", "id": "id_telefono"}),
            "cargo": forms.TextInput(attrs={"class": "form-control", "id": "id_cargo"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_is_staff"}),
            "is_tutor": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_is_tutor"}),
        }

    def clean_nombre_usuario(self):
        nombre_usuario = self.cleaned_data['nombre_usuario']
        if len(nombre_usuario) < 3 or re.search(r'\d', nombre_usuario):
            raise ValidationError('El nombre de usuario debe tener al menos 3 caracteres y no puede contener números.')
        return nombre_usuario

    def clean_email(self):
        email = self.cleaned_data['email']
        if "@" not in email:
            raise ValidationError('Por favor, ingrese un correo electrónico válido.')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 6 or not re.search(r'[A-Z]', password) or len(re.findall(r'\d', password)) < 2 or '.' not in password:
            raise ValidationError('La contraseña debe tener al menos 6 caracteres, incluyendo al menos una letra mayúscula, dos números y un punto.')
        return password

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if telefono is not None: 
            telefono_str = str(telefono) 
            if not telefono_str.isdigit():
                raise ValidationError('El número de teléfono solo puede contener números.')
        else:
            raise ValidationError('Este campo es obligatorio.')
        return telefono

class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ["nombre_usuario", "telefono", "cargo", "is_active", "is_staff", "is_tutor"]
        widgets = {
            "nombre_usuario": forms.TextInput(attrs={"id": "id_nombre", "class": "form-control"}),
            "telefono": forms.TextInput(attrs={"id": "id_telefono", "class": "form-control"}),
            "cargo": forms.TextInput(attrs={"id": "id_cargo", "class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_is_active"}),
            "is_staff": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_is_staff"}),
            "is_tutor": forms.CheckboxInput(attrs={"class": "form-check-input", "id": "id_is_tutor"}),
        }

    def clean_nombre_usuario(self):
        nombre = self.cleaned_data.get('nombre_usuario')
        if not nombre:
            raise ValidationError('Por favor, complete el campo nombre.')
        if not re.match(r'^[a-zA-Z\s]+$', nombre):
            raise ValidationError('El nombre solo puede contener letras y espacios.')
        return nombre
    
    def clean_telefono(self):
        telefono = str(self.cleaned_data.get('telefono')) 
        if not telefono:
            raise ValidationError('Por favor, complete el campo de teléfono.')
        if not re.match(r'^\d+$', telefono):
          raise ValidationError('El teléfono solo puede contener números.')
        return telefono

    def clean_cargo(self):
        cargo = self.cleaned_data.get('cargo')
        if not cargo:
            raise ValidationError('Por favor, complete el campo de cargo.')
        return cargo

# ========== FORMULARIOS PARA AYUDANTÍAS ==========

class AsignaturaForm(forms.ModelForm):
    class Meta:
        model = Asignatura
        fields = ["nombre", "codigo", "carrera", "descripcion"]
        widgets = {
            "nombre": forms.TextInput(attrs={"class": "form-control", "id": "id_nombre"}),
            "codigo": forms.TextInput(attrs={"class": "form-control", "id": "id_codigo"}),
            "carrera": forms.TextInput(attrs={"class": "form-control", "id": "id_carrera"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "id": "id_descripcion", "rows": 3}),
        }
    
    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre:
            # Verificar si ya existe una asignatura con el mismo nombre
            queryset = Asignatura.objects.filter(nombre__iexact=nombre)
            if self.instance.pk:  # Si estamos editando
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError('Ya existe una asignatura con este nombre.')
        return nombre
    
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        if codigo:
            # Verificar si ya existe una asignatura con el mismo código
            queryset = Asignatura.objects.filter(codigo__iexact=codigo)
            if self.instance.pk:  # Si estamos editando
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise forms.ValidationError('Ya existe una asignatura con este código.')
        return codigo

class AyudantiaForm(forms.ModelForm):
    class Meta:
        model = Ayudantia
        fields = ["asignatura", "tutor", "titulo", "descripcion", "sala", "fecha", "horario", "duracion", "cupos_totales"]
        widgets = {
            "asignatura": forms.Select(attrs={"class": "form-control", "id": "id_asignatura"}),
            "tutor": forms.Select(attrs={"class": "form-control", "id": "id_tutor"}),
            "titulo": forms.TextInput(attrs={"class": "form-control", "id": "id_titulo"}),
            "descripcion": forms.Textarea(attrs={"class": "form-control", "id": "id_descripcion", "rows": 4}),
            "sala": forms.TextInput(attrs={"class": "form-control", "id": "id_sala"}),
            "fecha": forms.DateInput(attrs={"class": "form-control", "id": "id_fecha", "type": "date"}),
            "horario": forms.TimeInput(attrs={"class": "form-control", "id": "id_horario", "type": "time"}),
            "duracion": forms.NumberInput(attrs={"class": "form-control", "id": "id_duracion", "min": "30", "max": "180"}),
            "cupos_totales": forms.NumberInput(attrs={"class": "form-control", "id": "id_cupos_totales", "min": "5", "max": "20"}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha and fecha < date.today():
            raise ValidationError('La fecha debe ser a partir de hoy en adelante.')
        return fecha

    def clean_cupos_totales(self):
        cupos = self.cleaned_data.get('cupos_totales')
        if cupos is None:
            raise ValidationError('El campo de cupos totales es obligatorio.')
        if cupos < 5:
            raise ValidationError('Debe haber al menos 5 cupos disponibles.')
        if cupos > 20:
            raise ValidationError('No se pueden crear más de 20 cupos por ayudantía.')
        return cupos
        