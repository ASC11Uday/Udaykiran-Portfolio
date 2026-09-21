from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Udaykiran Portfolio API",
    description="Backend API for my personal portfolio",
    version="1.0.0",
)
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
def contact(request: ContactRequest):
    print("New contact message received:")
    print(f"Name: {request.name}")
    print(f"Email: {request.email}")
    print(f"Message: {request.message}")

    return {
        "message": f"Thanks {request.name}, your message has been received."
    }
