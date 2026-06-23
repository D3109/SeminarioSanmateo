from fastapi import FastAPI, Header, HTTPException

app = FastAPI(title="API de Predicción de Datos", version="1.0")

# 🔐 Middleware de seguridad (NO rompe Swagger)
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)

    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"


    return response


# 🔑 TOKEN
API_KEY = "12345"


def verificar_token(x_api_key: str):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="No autorizado")


# 📦 Base de datos simulada
datos_usuarios = {
    "user1": "Activo",
    "user2": "Inactivo"
}


# 🌐 Endpoint raíz
@app.get("/")
def read_root():
    return {"mensaje": "Bienvenido a la API de Análisis. El sistema está en línea."}


# ✅ Estado
@app.get("/status")
def health_check():
    return {"status": "ok", "servicios": "operativos"}


# 🔐 HARDENING (endpoint protegido)
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