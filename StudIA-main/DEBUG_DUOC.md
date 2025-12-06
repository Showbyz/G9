# 🐛 Debug: Login con DUOC UC

## Cambios Realizados

1. ✅ **Tenant configurado a 'DUOC UC'** en `app-mobile/src/utils/tenant.js`
2. ✅ **Logs agregados** en el middleware para ver qué está pasando
3. ✅ **Logs agregados** en el serializer para verificar el schema

## 🔍 Verificar Logs

Cuando intentes hacer login, deberías ver en los logs de Django:

```
[API Mobile] Petición recibida: POST /api/mobile/auth/login/
[API Mobile] Usando tenant por defecto: DUOC UC
[API Mobile] Tenant establecido: DUOC UC (DUOC UC)
[API Mobile] Schema actual de BD: DUOC UC
[API Mobile Serializer] Schema establecido: DUOC UC
[API Mobile Serializer] Usuario encontrado: [email]
```

## ⚠️ Posibles Problemas

### 1. Schema con Espacios
El schema "DUOC UC" tiene espacios, lo cual puede causar problemas en PostgreSQL. Si ves errores relacionados con el schema, puede ser necesario:
- Usar comillas en las queries SQL
- O cambiar el schema name a uno sin espacios

### 2. Tablas No Migradas
Si el schema "DUOC UC" no tiene las tablas migradas, verás el error:
```
no existe la relación «loginApp_usuario»
```

**Solución:** Ejecutar migraciones para ese schema:
```bash
python manage.py migrate_schemas --schema="DUOC UC"
```

### 3. No Hay Usuarios en ese Schema
Si no hay usuarios de tipo estudiante en el schema "DUOC UC", el login fallará.

## 🧪 Próximos Pasos

1. **Intenta hacer login de nuevo**
2. **Revisa los logs de Django** - Deberías ver los mensajes `[API Mobile]`
3. **Si ves el error de "no existe la relación"**, ejecuta las migraciones
4. **Si no ves los logs del middleware**, el middleware no se está ejecutando

---

**Intenta el login y comparte los logs que aparecen en Django.**

