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