from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel
from health_check import run_all_checks

# Crear app
app = FastAPI(title="API FinTech Nova", version="1.0")


# Middleware de seguridad
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"

    return response


# TOKEN
API_KEY = "12345"

def verificar_token(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="No autorizado")


# Base de datos simulada
datos_usuarios = {
    "user1": "Activo",
    "user2": "Inactivo"
}


# MODELO PARA EVALUAR RIESGO
class SolicitudCredito(BaseModel):
    nombre: str
    edad: int
    ingresos: float
    deudas: float


# LÓGICA DE NEGOCIO
def calcular_riesgo(ingresos, deudas):
    if deudas == 0:
        return "Bajo"

    ratio = deudas / ingresos

    if ratio < 0.3:
        return "Bajo"
    elif ratio < 0.6:
        return "Medio"
    else:
        return "Alto"


# Endpoint raíz
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API FinTech Nova"}


#  Estado
@app.get("/status")
def status():
    return {"status": "ok", "servicios": "operativos"}


# HEALTH CHECK
@app.get("/health")
def health():
    result = run_all_checks()

    if result["status"] != "healthy":
        raise HTTPException(status_code=503, detail=result)

    return result


# Endpoint protegido - Datos Sensibles
@app.get("/datos-sensibles/{usuario}")
def obtener_datos_privados(usuario: str, x_api_key: str = Header(...)):
    verificar_token(x_api_key)

    if usuario in datos_usuarios:
        return {
            "usuario": usuario,
            "estado": datos_usuarios[usuario],
            "datos_financieros": "Confidencial"
        }

    raise HTTPException(status_code=404, detail="Usuario no encontrado")


#  ENDPOINT EVALUAR RIESGO
@app.post("/evaluar-riesgo")
def evaluar_riesgo(solicitud: SolicitudCredito):

    if solicitud.edad < 18:
        raise HTTPException(status_code=400, detail="Edad inválida")

    riesgo = calcular_riesgo(solicitud.ingresos, solicitud.deudas)

    return {
        "nombre": solicitud.nombre,
        "riesgo": riesgo,
        "mensaje": "Evaluación completada"
    }