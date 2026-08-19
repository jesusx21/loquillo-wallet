# AGENTS.md

## Propósito del repositorio

Este proyecto es una wallet personal en Python con una separación clara entre:

- `domain/`: entidades y reglas del negocio
- `database/`: acceso a datos, stores y tablas SQLAlchemy
- `run_script/`: flujo de ejecución de la app
- `tests/`: pruebas unitarias y de integración
- `migrations/`: migraciones de Alembic

La idea general es mantener la lógica del negocio en `domain/` y la persistencia en `database/`, sin mezclar responsabilidades. Se usara la base de datos en memoria para las pruebas unitarias y la de SQL para pruebas de endpoints, integracion y para pruebas de los stores de sql.

## Cómo navegar el proyecto

### 1. Cambios de negocio

Cuando trabajes en reglas de negocio, revisa primero:

- `domain/entities/`
- `domain/use_cases/`
- `domain/errors.py`

Ejemplo: si agregas una nueva operación de cartera o usuario, normalmente se implementa en un use case y luego se conecta con un store.

### 2. Cambios de persistencia

Si la modificación afecta almacenamiento o consultas, revisa:

- `database/stores/`
- `database/tables/`
- `database/__init__.py`

La capa de datos debe devolver entidades del dominio y no mezclar lógica de negocio dentro de los stores.

### 3. Cambios de ejecución o CLI

Si necesitas cambiar cómo se ejecuta la aplicación o cómo se llena el demo inicial:

- `run_script/`
- `app/config.py`

Antes de ejecutar cualquier comando en terminal, activa el entorno del proyecto:

```bash
pyenv activate loquillo
```

## Convenciones de código

- Usa imports absolutos y consistentes con el estilo del proyecto.
- Mantén la capa de dominio independiente de SQLAlchemy cuando sea posible.
- No agregues lógica de negocio dentro de `database/`.
- Las entidades y use cases deben seguir el patrón ya usado en el proyecto.
- Si agregas nuevos casos de uso, agrégalos bajo `domain/use_cases/` y sigue la estructura de `BaseUseCase`.
- Si agregas nuevas tablas o stores, sigue el patrón existente de `database/stores/sql/` y `database/stores/memory/`.

## Comandos principales

### Instalar dependencias

```bash
make install-dev
```

O para producción:

```bash
make install-prod
```

### Ejecutar la app

```bash
make run
```

### Ejecutar pruebas

```bash
make test
```

### Ejecutar lint

```bash
make lint
```

### Crear migración

```bash
make migration-create
```

### Aplicar migraciones

```bash
make migration-run
```

### Revertir última migración

```bash
make rollback-run REVISION=-1
```

## Reglas de validación antes de cerrar cambios

Antes de considerar un cambio terminado:

1. Ejecuta la prueba más cercana al cambio.
2. Si toca arquitectura o flujo principal, ejecuta `make test`.
3. Si cambias estilo o imports, ejecuta `make lint`.
4. Si modificas la base de datos, revisa si hace falta una migración.

## Recomendación de flujo de trabajo

- Lee primero la estructura relevante antes de editar.
- Haz cambios pequeños y bien acotados.
- Mantén el nombre y la intención del feature alineados con el dominio.
- Prueba el comportamiento real, no solo el código escrito.
- Si hay dudas sobre el diseño, sigue el patrón de `CreateUser`, `CreateWallet` y los stores existentes como referencia.

## Referencias útiles

- `README.md`
- `makefile`
- `domain/`
- `database/`
- `tests/`

## Resumen corto

La regla principal es esta: el dominio define la lógica del negocio, la base de datos solo persiste, y las pruebas validan el comportamiento.


## Tipos de datos
- Cuando generes strins, usar '' y solo usa "" cuando sea realmente necesario
