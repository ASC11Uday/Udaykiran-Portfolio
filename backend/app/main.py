import json

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from . import models
from .database import Base, SessionLocal, engine, get_db


# --------------------------------------------------
# Database initialization
# --------------------------------------------------

Base.metadata.create_all(bind=engine)

def migrate_project_table():
    inspector = inspect(engine)

    columns = {
        column["name"]
        for column in inspector.get_columns("projects")
    }

    new_columns = {
        "overview": "TEXT NOT NULL DEFAULT ''",
        "contribution": "TEXT NOT NULL DEFAULT ''",
        "highlights": "TEXT NOT NULL DEFAULT '[]'"
    }

    with engine.begin() as connection:

        for column_name, column_definition in new_columns.items():

            if column_name not in columns:

                connection.execute(
                    text(
                        f"""
                        ALTER TABLE projects
                        ADD COLUMN {column_name}
                        {column_definition}
                        """
                    )
                )

migrate_project_table()
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
                                overview=(
                    "A machine learning application that analyzes "
                    "news content and predicts whether an article "
                    "is likely to be misleading."
                ),

                contribution=(
                    "Developed the machine learning workflow in Python, "
                    "including data preparation, text processing, model "
                    "training, and prediction."
                ),

                highlights=json.dumps([
                    "Text preprocessing and NLP",
                    "Machine learning classification",
                    "Training and prediction workflow",
                    "Python-based implementation"
                ]),
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
                overview=(
    "A full-stack web application for managing tour-related "
    "workflows with user authentication, backend APIs, and "
    "relational data management."
),

contribution=(
    "Worked across the Angular frontend and Spring Boot backend, "
    "integrating REST APIs, authentication, and MySQL persistence."
),

highlights=json.dumps([
    "Angular frontend development",
    "Spring Boot REST APIs",
    "JWT authentication",
    "MySQL database integration"
]),
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
                overview=(
    "A computer vision project that explores automated glaucoma "
    "detection from medical images using deep learning techniques."
),

contribution=(
    "Worked on the image-processing and deep-learning workflow "
    "for detecting glaucoma-related patterns using CNN and YOLOv8."
),

highlights=json.dumps([
    "Medical image analysis",
    "CNN-based deep learning",
    "YOLOv8 object detection",
    "Computer vision workflow"
]),
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
                overview=(
    "A Python-based music player application created to explore "
    "desktop application development and media handling."
),

contribution=(
    "Developed the core Python application flow for playing and "
    "managing audio files."
),

highlights=json.dumps([
    "Python application development",
    "Audio playback",
    "Desktop application workflow",
    "Media file handling"
]),
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

def update_project_details():
    db = SessionLocal()

    try:
        project_details = {

            "Fake News Prediction": {
                "overview": (
                    "A machine learning application that analyzes "
                    "news content and predicts whether an article "
                    "is likely to be misleading."
                ),
                "contribution": (
                    "Developed the machine learning workflow in Python, "
                    "including data preparation, text processing, model "
                    "training, and prediction."
                ),
                "highlights": [
                    "Text preprocessing and NLP",
                    "Machine learning classification",
                    "Training and prediction workflow",
                    "Python-based implementation"
                ]
            },

            "Tour Management System": {
                "overview": (
                    "A full-stack web application for managing "
                    "tour-related workflows with user authentication, "
                    "backend APIs, and relational data management."
                ),
                "contribution": (
                    "Worked across the Angular frontend and Spring Boot "
                    "backend, integrating REST APIs, authentication, "
                    "and MySQL persistence."
                ),
                "highlights": [
                    "Angular frontend development",
                    "Spring Boot REST APIs",
                    "JWT authentication",
                    "MySQL database integration"
                ]
            },

            "Glaucoma Detection": {
                "overview": (
                    "A computer vision project that explores automated "
                    "glaucoma detection from medical images using "
                    "deep learning techniques."
                ),
                "contribution": (
                    "Worked on the image-processing and deep-learning "
                    "workflow for detecting glaucoma-related patterns "
                    "using CNN and YOLOv8."
                ),
                "highlights": [
                    "Medical image analysis",
                    "CNN-based deep learning",
                    "YOLOv8 object detection",
                    "Computer vision workflow"
                ]
            },

            "Music Player": {
                "overview": (
                    "A Python-based music player application created "
                    "to explore desktop application development "
                    "and media handling."
                ),
                "contribution": (
                    "Developed the core Python application flow for "
                    "playing and managing audio files."
                ),
                "highlights": [
                    "Python application development",
                    "Audio playback",
                    "Desktop application workflow",
                    "Media file handling"
                ]
            }
        }

        for title, details in project_details.items():

            project = (
                db.query(models.Project)
                .filter(models.Project.title == title)
                .first()
            )

            if project:
                project.overview = details["overview"]
                project.contribution = details["contribution"]
                project.highlights = json.dumps(
                    details["highlights"]
                )

        db.commit()

    finally:
        db.close()
update_project_details()

def seed_experiences():
    db = SessionLocal()

    try:
        existing_experiences = db.query(models.Experience).count()

        if existing_experiences > 0:
            return

        experiences = [

            models.Experience(
                role="Senior Associate Engineer",
                company="Ascendion Engineering Pvt. Ltd.",
                period="2024 — Present",
                description=(
                    "Working on full-stack development, automation testing, "
                    "and intelligent automation workflows. Contributing to "
                    "Angular and backend development while working with "
                    "PyTest, Selenium, and AI-driven testing workflows."
                ),
                technologies=json.dumps([
                    "Angular",
                    "Spring Boot",
                    "Python",
                    "PyTest",
                    "Selenium",
                    "AI"
                ])
            ),

            models.Experience(
                role="Machine Learning Intern",
                company="YBI Foundation",
                period="2022",
                description=(
                    "Worked on machine learning concepts and projects, "
                    "gaining practical exposure to Python, data analysis, "
                    "and machine learning workflows."
                ),
                technologies=json.dumps([
                    "Python",
                    "Machine Learning",
                    "Data Analysis"
                ])
            )

        ]

        db.add_all(experiences)

        db.commit()

    finally:
        db.close()


def seed_skill_groups():
    db = SessionLocal()

    try:
        existing_skill_groups = db.query(models.SkillGroup).count()

        if existing_skill_groups > 0:
            return

        skill_groups = [

            models.SkillGroup(
                title="Development",
                description=(
                    "Building responsive web applications and backend "
                    "services using modern development frameworks."
                ),
                skills=json.dumps([
                    "Angular",
                    "TypeScript",
                    "JavaScript",
                    "HTML",
                    "CSS / SCSS",
                    "Spring Boot",
                    "Java",
                    "Python",
                    "MySQL",
                    "MongoDB"
                ])
            ),

            models.SkillGroup(
                title="Automation & Testing",
                description=(
                    "Designing automated test workflows for web and "
                    "Windows applications with a focus on reliability "
                    "and maintainability."
                ),
                skills=json.dumps([
                    "PyTest",
                    "Selenium",
                    "Manual Testing",
                    "Windows Automation",
                    "JIRA",
                    "TestRail",
                    "Xray",
                    "Zephyr",
                    "Postman"
                ])
            ),

            models.SkillGroup(
                title="AI & Intelligent Automation",
                description=(
                    "Exploring machine learning, computer vision and "
                    "agent-based workflows for intelligent software "
                    "automation."
                ),
                skills=json.dumps([
                    "Machine Learning",
                    "Computer Vision",
                    "Generative AI",
                    "Agentic AI",
                    "AI Agents",
                    "OCR",
                    "YOLOv8",
                    "CNN"
                ])
            ),

            models.SkillGroup(
                title="Tools & Workflow",
                description=(
                    "Development and collaboration tools used across "
                    "software engineering and testing workflows."
                ),
                skills=json.dumps([
                    "Git",
                    "GitHub",
                    "GitHub Desktop",
                    "VS Code",
                    "IntelliJ IDEA",
                    "JIRA",
                    "Postman"
                ])
            )

        ]

        db.add_all(skill_groups)

        db.commit()

    finally:
        db.close()

# Create the initial project records
seed_projects()
seed_experiences()
seed_skill_groups()




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
    "featured": project.featured,
    "overview": project.overview,
    "contribution": project.contribution,
    "highlights": json.loads(project.highlights)
})

    return result

@app.get("/api/experiences")
def get_experiences(
    db: Session = Depends(get_db)
):
    experiences = db.query(models.Experience).all()

    result = []

    for experience in experiences:

        result.append({
            "id": experience.id,
            "role": experience.role,
            "company": experience.company,
            "period": experience.period,
            "description": experience.description,
            "technologies": json.loads(
                experience.technologies
            )
        })

    return result

@app.get("/api/skills")
def get_skills(
    db: Session = Depends(get_db)
):
    skill_groups = db.query(models.SkillGroup).all()

    result = []

    for skill_group in skill_groups:

        result.append({
            "id": skill_group.id,
            "title": skill_group.title,
            "description": skill_group.description,
            "skills": json.loads(skill_group.skills)
        })

    return result