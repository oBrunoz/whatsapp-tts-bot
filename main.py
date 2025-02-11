from fastapi import FastAPI
from app.api.routes import router as api_router
import uvicorn

app = FastAPI(title="WhatsApp TTS Bot")

# Registro de rotas
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)