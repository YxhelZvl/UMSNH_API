# Sistema UMSNH - Backend API

Sistema de gestión universitaria desarrollado con FastAPI siguiendo **Clean Architecture** (Arquitectura Limpia) con principios de **Domain-Driven Design (DDD)** para la Universidad Michoacana de San Nicolás de Hidalgo.

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Arquitectura](#-arquitectura)
- [Requisitos Previos](#-requisitos-previos)
- [Instalación](#-instalación)
- [Configuración](#️-configuración)
- [Ejecución](#-ejecución)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Módulos Disponibles](#-módulos-disponibles)
- [API Endpoints](#-api-endpoints)
- [Diagramas](#-diagramas)
- [Contribuir](#-contribuir)

## ✨ Características

- 🏗️ **Clean Architecture**: Independencia de frameworks, UI, bases de datos y agentes externos
- 🎯 **Domain-Driven Design**: El dominio es el centro de la aplicación
- 🔐 **Autenticación y Autorización**: Sistema de roles y usuarios
- 📚 **Gestión Académica Completa**: Estudiantes, maestros, carreras, ciclos, inscripciones
- 📖 **Sistema de Biblioteca**: Catálogo, ejemplares, préstamos
- 🔬 **Gestión de Laboratorios**: Administración de recursos de laboratorio
- 🗄️ **Base de Datos MySQL**: Integración con SQLModel/SQLAlchemy
- 📝 **Documentación Automática**: Swagger UI y ReDoc
- ✅ **Validación de Datos**: Pydantic schemas y Value Objects
- 🔄 **Inversión de Dependencias**: Las dependencias apuntan hacia el dominio

## 🏛️ Arquitectura

El proyecto sigue los principios de **Clean Architecture** propuesta por Robert C. Martin (Uncle Bob):

```
┌─────────────────────────────────────────────────────────────┐
│                    CAPA DE PRESENTACIÓN                      │
│                  (Presentation / UI Layer)                   │
│          Routers, Controllers, Schemas de API                │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │            CAPA DE APLICACIÓN                          │ │
│  │           (Application Layer)                          │ │
│  │    Services, Use Cases, DTOs, Orchestration           │ │
│  │                                                        │ │
│  │  ┌──────────────────────────────────────────────────┐ │ │
│  │  │         CAPA DE DOMINIO (NÚCLEO)                 │ │ │
│  │  │          (Domain Layer / Core)                   │ │ │
│  │  │   Entities, Value Objects, Domain Logic          │ │ │
│  │  │         Business Rules, Interfaces               │ │ │
│  │  │                                                  │ │ │
│  │  │         ⭐ INDEPENDIENTE DE TODO ⭐              │ │ │
│  │  └──────────────────────────────────────────────────┘ │ │
│  │                                                        │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                              │
└──────────────────────────┬───────────────────────────────────┘
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                 CAPA DE INFRAESTRUCTURA                       │
│               (Infrastructure Layer)                          │
│   Database Models, External APIs, File System, etc.          │
│   Implementations of Repository Interfaces                    │
└───────────────────────────────────────────────────────────────┘
```

### Principios de Clean Architecture Aplicados

1. **Regla de Dependencia**: Las dependencias del código fuente solo pueden apuntar hacia adentro
2. **Independencia de Frameworks**: El negocio no depende de FastAPI
3. **Independencia de UI**: La lógica de negocio no conoce la presentación
4. **Independencia de Base de Datos**: El dominio no conoce MySQL
5. **Independencia de Agentes Externos**: El negocio no depende de librerías externas
6. **Testeable**: Las reglas de negocio se pueden probar sin UI, BD, servidor web, etc.

### Capas del Sistema (De adentro hacia afuera)

#### 1. **Domain Layer (Capa de Dominio)** - 🎯 NÚCLEO
**Ubicación**: `features/*/domain/`

Es el **corazón** de la aplicación. No depende de nada externo.

- **Entities**: Objetos del negocio con identidad única
  ```python
  # Ejemplo: User entity
  class User:
      def __init__(self, id, nombre_usuario, email):
          self.id = id
          self.nombre_usuario = nombre_usuario
          self.email = email
  ```

- **Value Objects**: Objetos inmutables que representan valores del dominio
  ```python
  # Ejemplo: NombreUsuario value object
  class NombreUsuario:
      def __init__(self, valor: str):
          if len(valor) < 3:
              raise ValueError("Nombre debe tener al menos 3 caracteres")
          self.valor = valor
  ```

- **Repository Interfaces**: Contratos (abstracciones) de persistencia
  ```python
  # Interface que el dominio define
  class UserRepository(ABC):
      @abstractmethod
      def save(self, user: User) -> User:
          pass
  ```

- **Domain Services**: Lógica de negocio que no pertenece a una entidad específica

#### 2. **Application Layer (Capa de Aplicación)**
**Ubicación**: `features/*/application/`

Orquesta el flujo de datos entre la presentación y el dominio.

- **Use Cases / Services**: Casos de uso específicos del negocio
  ```python
  class UserService:
      def __init__(self, repository: UserRepository):
          self.repository = repository
      
      def create_user(self, dto: CreateUserDTO) -> User:
          # Lógica del caso de uso
          user = User(dto.nombre, dto.email)
          return self.repository.save(user)
  ```

- **DTOs (Data Transfer Objects)**: Objetos para transferir datos entre capas
  ```python
  class CreateUserDTO:
      nombre: str
      email: str
  ```

- **Application Services**: Coordinación de múltiples use cases

#### 3. **Infrastructure Layer (Capa de Infraestructura)**
**Ubicación**: `features/*/infrastructure/`

Implementaciones concretas de las interfaces del dominio.

- **Database Models**: Modelos ORM (SQLModel)
  ```python
  class UserModel(SQLModel, table=True):
      id: int
      nombre_usuario: str
      email: str
  ```

- **Repository Implementations**: Implementación concreta de los repositorios
  ```python
  class UserRepositoryImpl(UserRepository):
      def save(self, user: User) -> User:
          # Implementación con SQLModel/MySQL
          model = UserModel(**user.__dict__)
          session.add(model)
          session.commit()
  ```

- **Mappers**: Transforman entre objetos de dominio y modelos de BD
  ```python
  class UserMapper:
      @staticmethod
      def to_domain(model: UserModel) -> User:
          return User(model.id, model.nombre_usuario, model.email)
      
      @staticmethod
      def to_model(entity: User) -> UserModel:
          return UserModel(**entity.__dict__)
  ```

- **External Services**: APIs externas, sistemas de archivos, etc.

#### 4. **Presentation Layer (Capa de Presentación)**
**Ubicación**: `features/*/presentation/`

Interfaz con el mundo exterior (HTTP, CLI, etc.)

- **Routers**: Endpoints de FastAPI
  ```python
  @router.post("/users")
  def create_user(data: UserCreateSchema, service: UserService):
      result = service.create_user(data)
      return result
  ```

- **Schemas**: Validación de entrada/salida con Pydantic
  ```python
  class UserCreateSchema(BaseModel):
      nombre_usuario: str
      email: EmailStr
  ```

- **Controllers**: Coordinación entre routers y servicios (opcional)

### Flujo de Datos en Clean Architecture

```
    HTTP Request
         │
         ▼
┌────────────────┐
│   Router       │ ◄── Presentation Layer
│  (FastAPI)     │
└────────┬───────┘
         │ Schema/DTO
         ▼
┌────────────────┐
│   Service      │ ◄── Application Layer
│  (Use Case)    │
└────────┬───────┘
         │ Domain Entity
         ▼
┌────────────────┐
│   Repository   │ ◄── Domain Interface
│  (Interface)   │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│  Repository    │ ◄── Infrastructure Implementation
│    Impl        │
└────────┬───────┘
         │
         ▼
┌────────────────┐
│    Mapper      │ ◄── Infrastructure
└────────┬───────┘
         │
         ▼
┌────────────────┐
│   DB Model     │ ◄── Infrastructure
│  (SQLModel)    │
└────────┬───────┘
         │
         ▼
    MySQL Database
```

## 🔧 Requisitos Previos

- **Python**: 3.10 o superior
- **MySQL**: 8.0 o superior
- **pip**: Gestor de paquetes de Python
- **virtualenv** (recomendado)

## 📥 Instalación

### 1. Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd backend_app
```

### 2. Crear Entorno Virtual

```bash
# Linux/macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos MySQL

```bash
# Acceder a MySQL
mysql -u root -p

# Crear base de datos
CREATE DATABASE sistema_universitario CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Crear usuario (ejemplo)
CREATE USER 'usuario_app'@'localhost' IDENTIFIED BY 'password_seguro_123';
GRANT ALL PRIVILEGES ON sistema_universitario.* TO 'usuario_app'@'localhost';
FLUSH PRIVILEGES;
```

## ⚙️ Configuración

### 1. Archivo de Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Configuración de Base de Datos
USER_DB=usuario_app
PASSWORD_DB=password_seguro_123
HOST_DB=localhost
NAME_DB=sistema_universitario
PORT_DB=3306

# Configuración de Seguridad
SECRET_KEY=tu-clave-secreta-super-segura-de-al-menos-32-caracteres-aqui

# URL de Conexión (no modificar la sintaxis)
URL_CONECCION=mysql+pymysql://${USER_DB}:${PASSWORD_DB}@${HOST_DB}:${PORT_DB}/${NAME_DB}
```

> ⚠️ **IMPORTANTE**: Nunca compartas tu archivo `.env` ni lo subas a repositorios públicos. Está incluido en `.gitignore` por seguridad.

### 2. Generar Secret Key Segura

```python
# Ejecutar en Python para generar una clave segura
import secrets
print(secrets.token_urlsafe(32))
# Ejemplo de salida: "5k8x_9mP2qL7nR4tV6wY8zA3bC1dE0fG2hI4jK6lM8nO"
```

### 3. Variables de Entorno Explicadas

| Variable | Descripción | Ejemplo |
|----------|-------------|---------|
| `USER_DB` | Usuario de MySQL con permisos | `usuario_app` |
| `PASSWORD_DB` | Contraseña segura del usuario MySQL | `password_seguro_123` |
| `HOST_DB` | Host de la base de datos | `localhost` o `127.0.0.1` |
| `NAME_DB` | Nombre de la base de datos | `sistema_universitario` |
| `PORT_DB` | Puerto de MySQL (por defecto 3306) | `3306` |
| `SECRET_KEY` | Clave para JWT/sesiones (mínimo 32 caracteres) | `5k8x_9mP2qL...` |

## 🚀 Ejecución

### Modo Desarrollo

```bash
# Opción 1: FastAPI CLI (recomendado para desarrollo)
fastapi dev main.py

# Opción 2: Uvicorn directamente
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Modo Producción

```bash
# Con múltiples workers para mejor rendimiento
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# O usando Gunicorn con Uvicorn workers
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Verificar Funcionamiento

- **API**: http://localhost:8000
- **Documentación (Swagger)**: http://localhost:8000/docs
- **Documentación (ReDoc)**: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

```
backend_app/
├── main.py                     # Punto de entrada - FastAPI App
├── requirements.txt            # Dependencias del proyecto
├── .env                        # Variables de entorno (NO VERSIONAR)
├── .env.example               # Plantilla de variables de entorno
├── .gitignore                 # Archivos ignorados por Git
│
└── src/
    └── app/
        ├── core/              # Configuración central
        │   └── database/
        │       └── database.py    # Setup de DB y dependencias
        │
        ├── shared/            # Código compartido entre módulos
        │   └── schemas/
        │       └── generic_response.py
        │
        └── features/          # Módulos organizados por feature
            │
            └── [feature_name]/     # Ejemplo: user, carrera, etc.
                │
                ├── domain/              # ⭐ CAPA DE DOMINIO (NÚCLEO)
                │   ├── entities/        # Entidades del negocio
                │   │   └── user.py      # Ejemplo: clase User
                │   ├── repositories/    # Interfaces de repositorios
                │   │   └── user_repository.py
                │   └── value_objects/   # Value Objects
                │       └── nombre_usuario.py
                │
                ├── application/         # 🎯 CAPA DE APLICACIÓN
                │   ├── services/        # Casos de uso / Services
                │   │   └── user_service.py
                │   └── dtos.py          # Data Transfer Objects
                │
                ├── infrastructure/      # 🔧 CAPA DE INFRAESTRUCTURA
                │   ├── models/          # Modelos de BD (SQLModel)
                │   │   └── user_model.py
                │   ├── repositories/    # Implementaciones
                │   │   └── user_repository_impl.py
                │   ├── mappers/         # Mappers entre capas
                │   │   └── user_mapper.py
                │   └── dependencies.py  # Inyección de dependencias
                │
                └── presentation/        # 🌐 CAPA DE PRESENTACIÓN
                    ├── routers/         # Endpoints HTTP
                    │   └── user_router.py
                    └── schemas/         # Pydantic schemas
                        └── user_schemas.py
```

### Principios de Organización por Capas

```
┌─────────────────────────────────────────────────────────┐
│  Presentation (routers, schemas)                         │
│  ↓ Depende de ↓                                          │
├─────────────────────────────────────────────────────────┤
│  Application (services, dtos)                            │
│  ↓ Depende de ↓                                          │
├─────────────────────────────────────────────────────────┤
│  Domain (entities, value objects, interfaces)            │
│  ⭐ NO DEPENDE DE NADA ⭐                                │
├─────────────────────────────────────────────────────────┤
│  Infrastructure (models, mappers, implementations)       │
│  ↑ Implementa ↑ las interfaces del Domain               │
└─────────────────────────────────────────────────────────┘
```

## 📦 Módulos Disponibles

| Módulo | Descripción | Endpoint Base |
|--------|-------------|---------------|
| **User** | Gestión de usuarios del sistema | `/users` |
| **Rol** | Roles y permisos | `/roles` |
| **Carrera** | Programas académicos | `/carreras` |
| **Estudiante** | Información de estudiantes | `/estudiantes` |
| **Maestros** | Gestión de docentes | `/maestros` |
| **Administrativo** | Personal administrativo | `/administrativos` |
| **Ciclo** | Ciclos/periodos escolares | `/ciclos` |
| **Inscripcion** | Inscripciones a cursos | `/inscripciones` |
| **Bibliotecas** | Gestión de bibliotecas | `/bibliotecas` |
| **Catalogo** | Catálogo bibliográfico | `/catalogo` |
| **Ejemplares** | Ejemplares físicos | `/ejemplares` |
| **Prestamos** | Préstamos de biblioteca | `/prestamos` |
| **Laboratorios** | Gestión de laboratorios | `/laboratorios` |

## 🔌 API Endpoints

### Ejemplo: Módulo de Usuarios

```http
GET    /users              # Listar todos los usuarios
GET    /users/{id}         # Obtener usuario específico por ID
POST   /users              # Crear nuevo usuario
PUT    /users/{id}         # Actualizar usuario existente
DELETE /users/{id}         # Eliminar usuario
```

### Formato de Petición POST (Crear Usuario)

```json
{
  "nombre_usuario": "juan.perez",
  "email": "juan.perez@example.com",
  "password": "password_seguro_123",
  "rol_id": 1
}
```

### Respuesta Genérica del Sistema

```json
{
  "status": "success",
  "message": "Operación completada exitosamente",
  "data": {
    "id": 1,
    "nombre_usuario": "juan.perez",
    "email": "juan.perez@example.com",
    "rol_id": 1,
    "created_at": "2025-11-10T12:00:00"
  },
  "errors": null
}
```

### Respuesta de Error

```json
{
  "status": "error",
  "message": "Error al procesar la solicitud",
  "data": null,
  "errors": [
    {
      "field": "email",
      "message": "El email ya está registrado"
    }
  ]
}
```

## 📊 Diagramas

### Clean Architecture - Círculos Concéntricos

```
        ┌─────────────────────────────────────┐
        │     FRAMEWORKS & DRIVERS            │
        │  (Web, UI, DB, External Interfaces) │
        │                                     │
        │  ┌───────────────────────────────┐ │
        │  │   INTERFACE ADAPTERS          │ │
        │  │ (Controllers, Gateways,       │ │
        │  │  Presenters, Mappers)         │ │
        │  │                               │ │
        │  │  ┌─────────────────────────┐ │ │
        │  │  │  APPLICATION BUSINESS   │ │ │
        │  │  │      RULES              │ │ │
        │  │  │  (Use Cases, Services)  │ │ │
        │  │  │                         │ │ │
        │  │  │  ┌───────────────────┐ │ │ │
        │  │  │  │   ENTERPRISE      │ │ │ │
        │  │  │  │  BUSINESS RULES   │ │ │ │
        │  │  │  │    (Entities)     │ │ │ │
        │  │  │  │                   │ │ │ │
        │  │  │  │   ⭐ DOMAIN ⭐   │ │ │ │
        │  │  │  └───────────────────┘ │ │ │
        │  │  └─────────────────────────┘ │ │
        │  └───────────────────────────────┘ │
        └─────────────────────────────────────┘

        Dependencias: ────────────────────────►
                     (Solo hacia adentro)
```

### Flujo de una Petición HTTP

```
1. HTTP Request
   │
   ▼
2. Router (Presentation)
   │ - Recibe petición HTTP
   │ - Valida con Pydantic Schema
   │
   ▼
3. Service (Application)
   │ - Ejecuta caso de uso
   │ - Usa DTOs para comunicación
   │
   ▼
4. Repository Interface (Domain)
   │ - Contrato definido por el dominio
   │ - No conoce la implementación
   │
   ▼
5. Repository Implementation (Infrastructure)
   │ - Implementación concreta
   │ - Usa Mapper para transformar
   │
   ▼
6. Mapper (Infrastructure)
   │ - Domain Entity ↔ DB Model
   │
   ▼
7. Database Model (Infrastructure)
   │ - SQLModel/MySQL
   │
   ▼
8. MySQL Database

   [Respuesta sigue el camino inverso]
```

### Diagrama de Componentes del Sistema

```
┌─────────────────────────────────────────────────────┐
│                   Sistema UMSNH                      │
│              (Clean Architecture)                    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐   │
│  │ Académico  │  │ Biblioteca │  │  Usuarios  │   │
│  ├────────────┤  ├────────────┤  ├────────────┤   │
│  │ Estudiantes│  │  Catálogo  │  │   Roles    │   │
│  │  Maestros  │  │ Ejemplares │  │    Auth    │   │
│  │  Carreras  │  │  Préstamos │  │            │   │
│  │   Ciclos   │  │            │  │            │   │
│  │Inscripciones│  │            │  │            │   │
│  └────────────┘  └────────────┘  └────────────┘   │
│                                                      │
│  ┌────────────┐  ┌────────────┐                    │
│  │ Laboratorio│  │Administrativo│                   │
│  ├────────────┤  ├────────────┤                    │
│  │  Recursos  │  │  Personal  │  │                    │
│  │  Horarios  │  │  Gestión   │                    │
│  └────────────┘  └────────────┘                    │
│                                                      │
│         Cada módulo sigue Clean Architecture        │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
                   ┌──────────────┐
                   │  MySQL DB    │
                   │sistema_univ. │
                   └──────────────┘
```

## 🛠️ Dependencias Principales

```
FastAPI          → Framework web (capa externa)
SQLModel         → ORM (capa de infraestructura)
Pydantic         → Validación (presentación y aplicación)
Uvicorn          → Servidor ASGI (capa externa)
PyMySQL          → Driver MySQL (infraestructura)
python-dotenv    → Variables de entorno
passlib          → Hashing de contraseñas
argon2-cffi      → Algoritmo seguro de hashing
```

## 🧪 Testing en Clean Architecture

Una de las grandes ventajas de Clean Architecture es la facilidad para testing:

```bash
# Tests unitarios del dominio (sin dependencias externas)
pytest tests/unit/domain/

# Tests de casos de uso (con mocks de repositorios)
pytest tests/unit/application/

# Tests de integración (con BD de prueba)
pytest tests/integration/

# Tests end-to-end
pytest tests/e2e/
```

### Ejemplo de Test del Dominio

```python
# No necesita BD, frameworks, ni nada externo
def test_nombre_usuario_valido():
    nombre = NombreUsuario("juan123")
    assert nombre.valor == "juan123"

def test_nombre_usuario_invalido():
    with pytest.raises(ValueError):
        NombreUsuario("ab")  # Muy corto
```

## 📝 Ventajas de Clean Architecture en Este Proyecto

1. ✅ **Testeable**: Puedes probar la lógica de negocio sin BD ni frameworks
2. ✅ **Independiente de UI**: Puedes cambiar FastAPI por Flask sin tocar el dominio
3. ✅ **Independiente de BD**: Puedes cambiar MySQL por PostgreSQL fácilmente
4. ✅ **Mantenible**: Cambios en una capa no afectan a las demás
5. ✅ **Escalable**: Fácil agregar nuevos features siguiendo la misma estructura
6. ✅ **Comprensible**: Cada capa tiene responsabilidades claras
7. ✅ **Evolutivo**: El sistema puede crecer sin degradarse

## 🎯 Reglas de Oro de Clean Architecture

### ✅ LO QUE SÍ debes hacer:

1. **El dominio nunca importa de capas externas**
   ```python
   # ❌ MAL - Domain importando de infrastructure
   from infrastructure.models import UserModel
   
   # ✅ BIEN - Domain define sus propias entidades
   class User:
       pass
   ```

2. **Las dependencias apuntan hacia adentro**
   ```python
   # ✅ BIEN
   Service(repository: UserRepository)  # App depende de Domain
   
   # ❌ MAL
   Entity(service: UserService)  # Domain NO debe depender de App
   ```

3. **Usa interfaces (abstracciones) en el dominio**
   ```python
   # ✅ BIEN - Interface en Domain
   class UserRepository(ABC):
       @abstractmethod
       def save(self, user: User): pass
   
   # ✅ BIEN - Implementación en Infrastructure
   class UserRepositoryImpl(UserRepository):
       def save(self, user: User):
           # Código de BD aquí
   ```

### ❌ LO QUE NO debes hacer:

1. ❌ Importar FastAPI en el dominio
2. ❌ Importar SQLModel en el dominio
3. ❌ Poner lógica de negocio en los routers
4. ❌ Mezclar modelos de BD con entidades de dominio
5. ❌ Hacer que el dominio conozca detalles de implementación

## 🐛 Problemas Conocidos y Soluciones

[... resto del contenido de problemas conocidos ...]

## 📚 Recursos Adicionales

### Clean Architecture
- [The Clean Architecture - Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Architecture Book](https://www.amazon.com/Clean-Architecture-Craftsmans-Software-Structure/dp/0134494164)

### Domain-Driven Design
- [Domain-Driven Design - Martin Fowler](https://martinfowler.com/bliki/DomainDrivenDesign.html)
- [DDD Quickly](https://www.infoq.com/minibooks/domain-driven-design-quickly/)

### Frameworks
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 👥 Contribuir

Al contribuir, respeta los principios de Clean Architecture:

1. ✅ **No rompas la regla de dependencias**: Solo hacia adentro
2. ✅ **Mantén el dominio puro**: Sin dependencias externas
3. ✅ **Usa inyección de dependencias**: Desacopla componentes
4. ✅ **Escribe tests**: Especialmente del dominio y aplicación

### Convenciones de Commits

```
Add: nueva funcionalidad
Fix: corrección de bug
Update: actualización de código existente
Refactor: refactorización sin cambio de funcionalidad
Docs: cambios en documentación
Test: agregar o modificar tests
Arch: cambios en la arquitectura
```

## 📄 Licencia

Este proyecto es privado y pertenece a la Universidad Michoacana de San Nicolás de Hidalgo.

## 📧 Contacto

Para dudas, sugerencias o reportar problemas, contacta al equipo de desarrollo.

---

**Desarrollado con ❤️ siguiendo Clean Architecture**

> "The center of your application is not the database. Nor is it one or more of the frameworks you may be using. **The center of your application is the use cases of your application**" - Uncle Bob

**Última revisión**: Noviembre 2025