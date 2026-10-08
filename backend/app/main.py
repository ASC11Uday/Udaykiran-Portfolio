import json

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from . import models
from .database import Base, SessionLocal, engine, get_db

import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_TO = os.getenv("EMAIL_TO")

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
    allow_origins=["http://localhost:4200","http://127.0.0.1:8080",
    "http://localhost:8080","https://udaykiran-portfolio-nine.vercel.app",],
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


def send_contact_email(
    name: str,
    email: str,
    message: str
):
    email_message = EmailMessage()

    email_message["Subject"] = f"New Portfolio Contact from {name}"
    email_message["From"] = EMAIL_USERNAME
    email_message["To"] = EMAIL_TO
    email_message["Reply-To"] = email

    email_message.set_content(
        f"""
New contact message from your portfolio.

Name: {name}
Email: {email}

Message:
{message}
"""
    )

    server = smtplib.SMTP(
        EMAIL_HOST,
        EMAIL_PORT,
        timeout=30
    )

    try:
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(
            EMAIL_USERNAME,
            EMAIL_PASSWORD
        )

        server.send_message(email_message)

    finally:
        server.quit()


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
                    "A Python-based machine learning project that analyzes "
    "news content and classifies articles based on patterns "
    "associated with misleading information."
                ),
                                overview=(
                    "A machine learning application that processes "
    "news content, applies text preprocessing and NLP "
    "techniques, and predicts whether an article is "
    "likely to contain misleading information."
                ),

                contribution=(
                     "Built the complete machine learning workflow in Python, "
    "including data preparation, text preprocessing, NLP-based "
    "feature processing, model training, and news classification."
                ),

                highlights=json.dumps([
                    "Text preprocessing and NLP",
    "News classification workflow",
    "Model training and prediction",
    "Python-based ML implementation"
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
        "workflows with user authentication, REST APIs, and "
        "relational data management."
    ),

    overview=(
        "A full-stack web application designed to manage "
        "tour-related workflows through an Angular frontend "
        "and Spring Boot backend, with JWT authentication "
        "and MySQL for persistent data management."
    ),

    contribution=(
        "Built the full-stack application using Angular and Spring Boot, "
    "implementing the frontend, REST APIs, JWT-based authentication, "
    "and MySQL database integration."
    ),

    highlights=json.dumps([
        "Angular frontend development",
        "Spring Boot REST API integration",
        "JWT-based authentication",
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
        "A computer vision project exploring automated "
        "glaucoma detection from medical images using "
        "deep learning techniques."
    ),

    overview=(
        "A computer vision project that explores automated "
        "glaucoma detection from medical images using "
        "CNN-based deep learning and YOLOv8."
    ),

    contribution=(
        "Built a computer vision workflow for glaucoma detection "
    "using medical image processing, CNN-based deep learning, "
    "and YOLOv8 object detection."

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
        "A Python-based desktop music player developed "
        "to explore application development and audio "
        "file handling."
    ),

    overview=(
        "A Python-based desktop application focused on "
        "playing and managing local audio files while "
        "exploring desktop application development."
    ),

    contribution=(
        "Built a Python-based desktop music player for loading, "
    "playing, and managing local audio files."
    ),

    highlights=json.dumps([
        "Python application development",
        "Audio playback",
        "Desktop application workflow",
        "Local media file handling"
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
        "description": (
            "A Python-based machine learning project that analyzes "
            "news content and classifies articles based on patterns "
            "associated with misleading information."
        ),
        "overview": (
            "A machine learning application that processes "
            "news content, applies text preprocessing and NLP "
            "techniques, and predicts whether an article is "
            "likely to contain misleading information."
        ),
        "contribution": (
    "Built the complete machine learning workflow in Python, "
    "including data preparation, text preprocessing, NLP-based "
    "feature processing, model training, and news classification."
),
        "highlights": [
            "Text preprocessing and NLP",
            "News classification workflow",
            "Model training and prediction",
            "Python-based ML implementation"
        ]
    },

    "Tour Management System": {
        "description": (
            "A full-stack web application for managing tour-related "
            "workflows with user authentication, REST APIs, and "
            "relational data management."
        ),
        "overview": (
            "A full-stack web application designed to manage "
            "tour-related workflows through an Angular frontend "
            "and Spring Boot backend, with JWT authentication "
            "and MySQL for persistent data management."
        ),
        "contribution": (
    "Built the full-stack application using Angular and Spring Boot, "
    "implementing the frontend, REST APIs, JWT-based authentication, "
    "and MySQL database integration."
),
        "highlights": [
            "Angular frontend development",
            "Spring Boot REST API integration",
            "JWT-based authentication",
            "MySQL database integration"
        ]
    },

    "Glaucoma Detection": {
        "description": (
            "A computer vision project exploring automated "
            "glaucoma detection from medical images using "
            "deep learning techniques."
        ),
        "overview": (
            "A computer vision project that explores automated "
            "glaucoma detection from medical images using "
            "CNN-based deep learning and YOLOv8."
        ),
        "contribution": (
    "Built a computer vision workflow for glaucoma detection "
    "using medical image processing, CNN-based deep learning, "
    "and YOLOv8 object detection."
),
        "highlights": [
            "Medical image analysis",
            "CNN-based deep learning",
            "YOLOv8 object detection",
            "Computer vision workflow"
        ]
    },

    "Music Player": {
        "description": (
            "A Python-based desktop music player developed "
            "to explore application development and audio "
            "file handling."
        ),
        "overview": (
            "A Python-based desktop application focused on "
            "playing and managing local audio files while "
            "exploring desktop application development."
        ),
        "contribution": (
    "Built a Python-based desktop music player for loading, "
    "playing, and managing local audio files."
),
        "highlights": [
            "Python application development",
            "Audio playback",
            "Desktop application workflow",
            "Local media file handling"
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
                project.description = details["description"]
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
    "Working across full-stack development, test automation, "
    "and AI-driven engineering workflows. Contributing to "
    "Angular and backend development while building and "
    "validating automated testing workflows using PyTest "
    "and Selenium."
),
                technologies=json.dumps([
                    "Angular",
                    "Spring Boot",
                    "Python",
                    "PyTest",
                    "Selenium",
                    "AI / Agentic Workflows"
                ])
            ),

            models.Experience(
                role="Machine Learning Intern",
                company="YBI Foundation",
                period="Jun 2022 — Aug 2022",
                description=(
    "Worked on machine learning projects and concepts, "
    "gaining practical experience with Python, data analysis, "
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

def update_experience_details():    
    db = SessionLocal()

    try:
        experience_details = {
            "Senior Associate Engineer": {
                "description": (
                    "Working across full-stack development, test automation, "
                    "and AI-driven engineering workflows. Contributing to "
                    "Angular and backend development while building and "
                    "validating automated testing workflows using PyTest "
                    "and Selenium."
                ),
                "period": "2024 — Present",
                "technologies": [
                    "Angular",
                    "Spring Boot",
                    "Python",
                    "PyTest",
                    "Selenium",
                    "AI / Agentic Workflows"
                ]
            },
            "Machine Learning Intern": {
                "description": (
                    "Worked on machine learning projects and concepts, "
                    "gaining practical experience with Python, data analysis, "
                    "and machine learning workflows."
                ),
                "period": "Jun 2022 — Aug 2022",
                "technologies": [
                    "Python",
                    "Machine Learning",
                    "Data Analysis"
                ]
            }
        }

        for role, details in experience_details.items():

            experience = (
                db.query(models.Experience)
                .filter(models.Experience.role == role)
                .first()
            )

            if experience:
                experience.description = details["description"]
                experience.period = details["period"]
                experience.technologies = json.dumps(
                    details["technologies"]
                )

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
    "Building web applications and backend services "
    "using Angular, Spring Boot, Python, and SQL-based "
    "data technologies."
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
    "Designing and validating automated test workflows "
    "for web and Windows applications using PyTest, "
    "Selenium, and testing tools."
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
    "Exploring machine learning, computer vision, "
    "generative AI, and agentic workflows for "
    "intelligent software automation."
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
    "Tools used across development, testing, version control, "
    "API validation, and engineering collaboration workflows."
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

def update_skill_group_details():
    db = SessionLocal()

    try:
        skill_details = {
            "Development": (
                "Building web applications and backend services "
                "using Angular, Spring Boot, Python, and SQL-based "
                "data technologies."
            ),
            "Automation & Testing": (
                "Designing and validating automated test workflows "
                "for web and Windows applications using PyTest, "
                "Selenium, and testing tools."
            ),
            "AI & Intelligent Automation": (
                "Exploring machine learning, computer vision, "
                "generative AI, and agentic workflows for "
                "intelligent software automation."
            ),
            "Tools & Workflow": (
                "Tools used across development, testing, version control, "
                "API validation, and engineering collaboration workflows."
            )
        }

        for title, description in skill_details.items():

            skill_group = (
                db.query(models.SkillGroup)
                .filter(models.SkillGroup.title == title)
                .first()
            )

            if skill_group:
                skill_group.description = description

        db.commit()

    finally:
        db.close()


# Create the initial project records
seed_projects()
seed_experiences()
update_experience_details()
seed_skill_groups()
update_skill_group_details()




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

    try:
        send_contact_email(
            name=request.name,
            email=request.email,
            message=request.message
        )

    except Exception as error:
        print(f"Email sending failed: {error}")

        return {
            "message": (
                "Your message was saved successfully, "
                "but email notification could not be sent."
            )
        }

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