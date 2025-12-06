def procesar_form(form, sol):
    if form.is_valid():
        sol.campos_sol = form.cleaned_data
        match sol.tipo_sol:
            case "Solicitud de hora":
                # Arreglar el formato de fecha para mostrarlo correctamente al ver el formulario
                if "fecha_expiracion" in sol.campos_sol and sol.campos_sol["fecha_expiracion"] is not None:
                    sol.campos_sol["fecha_expiracion"] = sol.campos_sol["fecha_expiracion"].strftime("%Y-%m-%d")
                else:
                    del(sol.campos_sol["fecha_expiracion"])
            case "IOC Automatico":
                # Mover el campo de archivo adjunto donde corresponde
                if form.files:
                    sol.adjunto_sol = form.files[f'{sol.tipo_sol}-adjunto']
                    del(sol.campos_sol["adjunto"])
            case "Cambio de Ruta":
                # Agregar el prefijo a la ruta que anotaron
                sol.campos_sol["interfaz_salida"] = sol.campos_sol["prefijo_interfaz"] + sol.campos_sol["interfaz_salida"]
                del(sol.campos_sol["prefijo_interfaz"])
                # Procesar la cantidad de IDs de ruta que vengan, mucho atao hacer un formset
                sol.campos_sol["ids_ruta"] = [id.strip() for id in sol.campos_sol["ids_ruta"].split(",")]
        return sol
    
def revision_form(sol, lista_sol):
    tipo_sol, campos_sol = sol.tipo_sol, sol.campos_sol
    #Cambiar a un switch a futuro si otros tipos de solicitudes requieren mas verificaciones
    match tipo_sol:
            case "Servicio VPN":
                for s in lista_sol:
                    campos_sol_alojado = s.campos_sol
                    if campos_sol["usuario"] == campos_sol_alojado["usuario"] and campos_sol["accion"] == campos_sol_alojado["accion"]:
                        return False
            case "Cambio de Ruta":
                if campos_sol["gateway"] == campos_sol["interfaz_salida"]:
                    return False
                
    return True