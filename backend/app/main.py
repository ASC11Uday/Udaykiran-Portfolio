import json

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from . import models
from .database import Base, SessionLocal, engine, get_db


# --------------------------------------------------
# Database initialization
# --------------------------------------------------

Base.metadata.create_all(bind=engine)


# --------------------------------------------------
# FastAPI application
# --------------------------------------------------

app = FastAPI(
    title="Udaykiran Portfolio API",
    description="Backend API for my personal portfolio",
    version="1.0.0",
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Request Models
# --------------------------------------------------

class ContactRequest(BaseModel):
    name: str
    email: str
    message: str


# --------------------------------------------------
# Seed Projects
# --------------------------------------------------

def seed_projects():
    db = SessionLocal()

    try:
        existing_projects = db.query(models.Project).count()

        # Don't insert projects again if they already exist
        if existing_projects > 0:
            return

        projects = [

            models.Project(
                title="Fake News Prediction",
                description=(
                    "A machine learning project designed to classify news "
                    "content and identify potentially misleading information "
                    "using Python-based ML techniques."
                ),
                type="AI / MACHINE LEARNING",
                category="AI / ML",
                technologies=json.dumps([
                    "Python",
                    "Machine Learning",
                    "NLP"
                ]),
                github="#",
                featured=True
            ),

            models.Project(
                title="Tour Management System",
                description=(
                    "A full-stack web application for managing tour-related "
                    "workflows with authentication, backend APIs, and "
                    "relational data management."
                ),
                type="FULL STACK",
                category="FULL STACK",
                technologies=json.dumps([
                    "Angular",
                    "Spring Boot",
                    "MySQL",
                    "JWT"
                ]),
                github="#",
                featured=False
            ),

            models.Project(
                title="Glaucoma Detection",
                description=(
                    "A computer vision project exploring automated glaucoma "
                    "detection using deep learning and object detection "
                    "techniques."
                ),
                type="COMPUTER VISION",
                category="DEEP LEARNING",
                technologies=json.dumps([
                    "Python",
                    "CNN",
                    "YOLOv8",
                    "Computer Vision"
                ]),
                github="#",
                featured=False
            ),

            models.Project(
                title="Music Player",
                description=(
                    "A Python-based music player application developed to "
                    "explore desktop application development and media "
                    "handling."
                ),
                type="PYTHON",
                category="PYTHON",
                technologies=json.dumps([
                    "Python",
                    "Desktop Application"
                ]),
                github="#",
                featured=False
            )

        ]

        db.add_all(projects)
        db.commit()

    finally:
        db.close()


# Create the initial project records
seed_projects()


# --------------------------------------------------
# Basic API
# --------------------------------------------------

@app.get("/")
def home():
    return {
        "message": "Welcome to Udaykiran's Portfolio API",
        "status": "running"
    }


# --------------------------------------------------
# About API
# --------------------------------------------------

@app.get("/api/about")
def about():
    return {
        "name": "Udaykiran",
        "role": "Senior Associate Engineer",
        "skills": [
            "Angular",
            "Python",
            "FastAPI",
            "Spring Boot",
            "Automation",
            "AI/ML"
        ]
    }


# --------------------------------------------------
# Contact API
# --------------------------------------------------

@app.post("/api/contact")
def contact(
    request: ContactRequest,
    db: Session = Depends(get_db)
):
    new_contact = models.Contact(
        name=request.name,
        email=request.email,
        message=request.message
    )

    db.add(new_contact)
    db.commit()
    db.refresh(new_contact)

    return {
        "message": f"Thanks {request.name}, your message has been received."
    }


# --------------------------------------------------
# Get Contacts
# Development / Testing Only
# --------------------------------------------------

@app.get("/api/contacts")
def get_contacts(
    db: Session = Depends(get_db)
):
    contacts = db.query(models.Contact).all()

    return contacts


# --------------------------------------------------
# Projects API
# --------------------------------------------------

@app.get("/api/projects")
def get_projects(
    db: Session = Depends(get_db)
):
    projects = db.query(models.Project).all()

    result = []

    for project in projects:

        result.append({
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "type": project.type,
            "category": project.category,
            "technologies": json.loads(project.technologies),
            "github": project.github,
            "featured": project.featured
        })

    return result