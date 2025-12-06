
# Portal de Autoatención



## Despliegue

Para comenzar a ejecutar el proyecto, seguir los siguientes pasos:

- Instalar los paquetes de python requeridos para el proyecto (de preferencia en un entorno virtual).
```bash
  pip install -r requirements.txt
```

- Inicializar el contenedor de docker con la base de datos de postgresql.

```bash
  docker-compose up
```

- Con la base de datos en pie, migrar los modelos a la base de datos.

```bash
  py manage.py migrate_schemas --shared
  py manage.py migrate_schemas

```

## Creación de Tenants

Para la creación de tenants se utiliza

```bash
  py manage.py create_tenant

```

En este se ejecutara el proceso de creación de tenant siguiendo el modelo alojado en `clientManager/models.py` con los campos que se puedan rellenar, así como la asignación de dominio con el formato `[subdominio].[dominio]`.

Durante el proceso de creación se genera la base de datos correspondiente al tenant, con el nombre del campo `schema name`.

## Creación de Superusuario

Como no se estará utilizando el sistema integrado de Django para la creación de superusuarios al inicio de un proyecto, se utilizará el de django-tenants para finalizar la configuración de un tenant, este se utiliza con:

```bash
  py manage.py create_tenant_superuser

```

Te solicitará el nombre de esquema en donde crear el superusuario y las credenciales correspondientes al modelo de usuario del proyecto.