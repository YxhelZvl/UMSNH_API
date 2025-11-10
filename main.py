from fastapi import FastAPI
import os
from dotenv import load_dotenv

from src.app.features.user.presentation.routers.user_router import router as user_router
from src.app.features.rol.presentation.routers.rol_router import router as rol_router
from src.app.features.carrera.presentation.routers.carrera_router import router as carrera_router
from src.app.features.estudiante.presentation.routers.estudiante_router import router as estudiante_router
from src.app.features.ciclo.presentation.routers.ciclo_router import router as ciclo_router
from src.app.features.inscripcion.presentation.routers.inscripcion_router import router as inscripcion_router
from src.app.features.administrativo.presentation.routers.administrativo_router import router as administrativo_router
from src.app.features.maestros.presentation.routers.maestro_router import router as maestros_router
from src.app.features.bibliotecas.presentation.routers.biblioteca_router import router as bibliotecas_router
from src.app.features.laboratorios.presentation.routers.laboratorio_router import router as laboratorios_router
from src.app.features.catalogo.presentation.routers.catalogo_router import router as catalogo_router
from src.app.features.ejemplares.presentation.routers.ejemplar_router import router as ejemplares_router
from src.app.features.prestamos.presentation.routers.prestamo_router import router as prestamos_router

load_dotenv()
db_username = os.getenv('USER_DB')

print(db_username)




app = FastAPI(title="Sistema UMSNH", version="1.0.0")

# Registrar routers
app.include_router(rol_router)
app.include_router(user_router)
app.include_router(carrera_router) 
app.include_router(estudiante_router)
app.include_router(ciclo_router)
app.include_router(inscripcion_router)
app.include_router(administrativo_router)
app.include_router(maestros_router)
app.include_router(bibliotecas_router)
app.include_router(laboratorios_router)
app.include_router(catalogo_router)
app.include_router(ejemplares_router)
app.include_router(prestamos_router)


@app.get("/")
def read_root():
    return {"message": "Sistema UMSNH API"}

