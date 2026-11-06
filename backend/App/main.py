from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Load database models
import App.models

# Import API routers
from App.api import (
    auth,
    patient,
    doctor,
    appointment,
    dashboard,
    chat,
    clinical_guidelines,
    analytics,
    report,
)

# Create FastAPI application
app = FastAPI(
    title="MegNova AI API",
    version="1.0.0",
    description="AI Hospital Digital Twin - Clinical Decision Support Platform",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
STATIC_DIR = Path("App/static")

if STATIC_DIR.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(STATIC_DIR)),
        name="static",
    )

# Register API routers
app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
app.include_router(dashboard.router)
app.include_router(chat.router)
app.include_router(clinical_guidelines.router)
app.include_router(analytics.router)
app.include_router(report.router)


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "project": "MegNova AI",
        "version": "1.0.0",
        "status": "Running",
        "documentation": "/docs",
    }


# Health check
@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "api": "running",
    }


# Favicon
@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    favicon_path = STATIC_DIR / "favicon.ico"

    if favicon_path.exists():
        return FileResponse(str(favicon_path))

    return {"message": "Favicon not found"}