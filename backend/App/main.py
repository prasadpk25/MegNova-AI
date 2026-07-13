from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from App.api import chat

from App.database.database import Base, engine

# Import all models
import App.models

# Import API routers
from App.api import (
    auth,
    patient,
    doctor,
    appointment,
    report,
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="MegNova AI API",
    description="AI-Powered Digital Twin Platform for Smart Healthcare",
    version="1.0.0",
)

# Static files
app.mount(
    "/static",
    StaticFiles(directory="App/static"),
    name="static",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
app.include_router(report.router)

# -----------------------------
# Root Endpoint
# -----------------------------
@app.get("/")
def root():
    return {
        "project": "MegNova AI",
        "version": "1.0.0",
        "status": "Backend Running Successfully 🚀",
    }


# -----------------------------
# Health Check
# -----------------------------
@app.get("/health")
def health():
    return {
        "status": "healthy",
        "database": "Connected",
    }

# -----------------------------
# Favicon
# -----------------------------
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("App/static/favicon.ico")
app.include_router(chat.router)