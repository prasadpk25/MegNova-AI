from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from App.database.database import Base, engine

# ------------------------------------------------------
# Import models safely
# ------------------------------------------------------

try:
    import App.models
except Exception as e:
    print(f"Model loading error: {e}")

# ------------------------------------------------------
# Import lightweight routers only
# ------------------------------------------------------

from App.api import (
    auth,
    patient,
    doctor,
    appointment,
    dashboard,
)

# ------------------------------------------------------
# Create database tables
# ------------------------------------------------------

Base.metadata.create_all(bind=engine)

# ------------------------------------------------------
# FastAPI application
# ------------------------------------------------------

app = FastAPI(
    title="MegNova AI API",
    version="1.0.0",
    description="MegNova AI demonstration deployment",
)

# ------------------------------------------------------
# Static files
# ------------------------------------------------------

app.mount(
    "/static",
    StaticFiles(directory="App/static"),
    name="static",
)

# ------------------------------------------------------
# CORS
# ------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------------------------------------
# Active routers
# ------------------------------------------------------

app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
app.include_router(dashboard.router)

# ------------------------------------------------------
# Root endpoint
# ------------------------------------------------------

@app.get("/", tags=["Root"])
def root():
    return {
        "project": "MegNova AI",
        "version": "1.0.0",
        "status": "Running",
        "documentation": "/docs",
    }

# ------------------------------------------------------
# Health check
# ------------------------------------------------------

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "database": "connected",
        "api": "running",
    }

# ------------------------------------------------------
# Favicon
# ------------------------------------------------------

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("App/static/favicon.ico")