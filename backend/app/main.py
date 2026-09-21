from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .database import Base, engine
from . import models
from fastapi import Depends
from sqlalchemy.orm import Session

from .database import get_db


app = FastAPI(
    title="Udaykiran Portfolio API",
    description="Backend API for my personal portfolio",
    version="1.0.0",
)
Base.metadata.create_all(bind=engine)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ContactRequest(BaseModel):
    name: str
    email: str
    message: str
    
@app.get("/")
def home():
    return {
        "message": "Welcome to Udaykiran's Portfolio API",
        "status": "running"
    }


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
@app.get("/api/contacts")
def get_contacts(db: Session = Depends(get_db)):
    contacts = db.query(models.Contact).all()

    return contacts

@app.get("/api/projects")
def get_projects():
    return [
        {
            "id": 1,
            "title": "Fake News Prediction",
            "description": "A machine learning project designed to classify news content and identify potentially misleading information using Python-based ML techniques.",
            "type": "AI / MACHINE LEARNING",
            "category": "AI / ML",
            "technologies": [
                "Python",
                "Machine Learning",
                "NLP"
            ],
            "github": "#",
            "featured": True
        },
        {
            "id": 2,
            "title": "Tour Management System",
            "description": "A full-stack web application for managing tour-related workflows with authentication, backend APIs, and relational data management.",
            "type": "FULL STACK",
            "category": "FULL STACK",
            "technologies": [
                "Angular",
                "Spring Boot",
                "MySQL",
                "JWT"
            ],
            "github": "#",
            "featured": False
        },
        {
            "id": 3,
            "title": "Glaucoma Detection",
            "description": "A computer vision project exploring automated glaucoma detection using deep learning and object detection techniques.",
            "type": "COMPUTER VISION",
            "category": "DEEP LEARNING",
            "technologies": [
                "Python",
                "CNN",
                "YOLOv8",
                "Computer Vision"
            ],
            "github": "#",
            "featured": False
        },
        {
            "id": 4,
            "title": "Music Player",
            "description": "A Python-based music player application developed to explore desktop application development and media handling.",
            "type": "PYTHON",
            "category": "PYTHON",
            "technologies": [
                "Python",
                "Desktop Application"
            ],
            "github": "#",
            "featured": False
        }
    ]
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