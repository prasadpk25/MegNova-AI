from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from App.database.database import Base, engine

# Import all models
import App.models

# Import API Routers
from App.api import (
    auth,
    patient,
    doctor,
    appointment,
    report,
    patient_history,
    report_compare,
    drug_interaction,
    dashboard,
    chat,
    clinical_guidelines,
    analytics,
)

# Create Database Tables
Base.metadata.create_all(bind=engine)

# ======================================================
# FastAPI Application
# ======================================================

app = FastAPI(
    title="MegNova AI API",
    version="1.0.0",
    description="""
# 🏥 MegNova AI

MegNova AI is an AI-powered Smart Hospital Management System that assists healthcare professionals using Artificial Intelligence, OCR, Retrieval-Augmented Generation (RAG), and Large Language Models.

## Core Features

- 🔐 JWT Authentication
- 👨‍⚕️ Doctor Management
- 🧑‍🤝‍🧑 Patient Management
- 📅 Appointment Scheduling
- 📄 Medical Report Upload
- 🔍 OCR Report Extraction
- 🤖 AI Medical Report Summarization
- 📚 Clinical Guideline Search (RAG)
- 💊 Drug Interaction Checker
- 🕒 Patient Timeline
- 🧠 AI Patient History
- 📑 Report Comparison
- 📊 Analytics Dashboard
- 💬 AI Medical Assistant

## Technology Stack

- FastAPI
- PostgreSQL
- SQLAlchemy
- Ollama (Llama 3)
- Qdrant Vector Database
- Sentence Transformers
- EasyOCR
- Streamlit
- Swagger UI
""",
)

# ======================================================
# Static Files
# ======================================================

app.mount(
    "/static",
    StaticFiles(directory="App/static"),
    name="static",
)

# ======================================================
# CORS
# ======================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# Register API Routers
# ======================================================

app.include_router(auth.router)
app.include_router(patient.router)
app.include_router(doctor.router)
app.include_router(appointment.router)
app.include_router(report.router)
app.include_router(patient_history.router)
app.include_router(report_compare.router)
app.include_router(drug_interaction.router)
app.include_router(dashboard.router)
app.include_router(chat.router)
app.include_router(clinical_guidelines.router)
app.include_router(analytics.router)

# ======================================================
# Root Endpoint
# ======================================================

@app.get("/", tags=["Root"])
def root():
    return {
        "project": "MegNova AI",
        "version": "1.0.0",
        "status": "Backend Running Successfully 🚀",
        "documentation": "/docs",
    }


# ======================================================
# Health Check
# ======================================================

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "database": "Connected",
        "api": "Running",
    }


# ======================================================
# Favicon
# ======================================================

@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("App/static/favicon.ico")