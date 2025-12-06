const $usuario = document.getElementById('usuario');
const $accion = document.getElementById('accion');
const $tipoSolicitud = document.getElementById('tipoSolicitud');

document.addEventListener('DOMContentLoaded', function() {
    const $tipoSolicitud = document.getElementById('tipoSolicitud');
    // Otros elementos y lógica de validación aquí...
});
(function () {
    // Evento change para el select de tipo de solicitud
    $tipoSolicitud.addEventListener('change', function () {
        let tipoSeleccionado = this.value;

        // Limpiar el contenido del select de acciones
        $accion.innerHTML = '';
        
        // Si el tipo de solicitud es diferente de la opción por defecto
        if (tipoSeleccionado !== "") {
            // Dependiendo del tipo de solicitud seleccionado, mostrar las opciones correspondientes
            if (tipoSeleccionado === "ISE VPN") {
                // Mostrar el select de acciones
                $accion.style.display = 'block';

                // Agregar las opciones correspondientes al select de acciones
                let opciones = ["Extensión de cuenta", "Cambio de contraseña", "Deshabilitación de cuenta"];
                opciones.forEach(function (opcion) {
                    let option = document.createElement('option');
                    option.text = opcion;
                    $accion.add(option);
                });
            } else {
                // Ocultar el select de acciones si no es ISE VPN
                $accion.style.display = 'none';
            }
        } else {
            // Ocultar el select de acciones si no se ha seleccionado un tipo de solicitud
            $accion.style.display = 'none';
        }
    });

    // Evento change para el select de acciones
    $accion.addEventListener('change', function () {
        let accionSeleccionada = this.value;

        // Validar según la acción seleccionada
        if (accionSeleccionada === "Extensión de cuenta" || accionSeleccionada === "Cambio de contraseña" || accionSeleccionada === "Deshabilitación de cuenta") {
            let nombre = String($usuario.value).trim();
            if (nombre.length === 0) {
                alert("El nombre del usuario no puede ir vacío...");
            }
        }
        // Agregar más validaciones para otras acciones si es necesario
    });
})();

