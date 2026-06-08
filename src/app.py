"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Club de Ajedrez": {
        "description": "Aprende estrategias y compite en torneos de ajedrez",
        "schedule": "Viernes, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Clase de Programación": {
        "description": "Aprende fundamentos de programación y construye proyectos de software",
        "schedule": "Martes y Jueves, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Clase de Educación Física": {
        "description": "Educación física y actividades deportivas",
        "schedule": "Lunes, Miércoles, Viernes, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Fútbol": {
        "description": "Práctica y competencia de fútbol con entrenamiento profesional",
        "schedule": "Lunes y Miércoles, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["lucas@mergington.edu", "alejandro@mergington.edu"]
    },
    "Baloncesto": {
        "description": "Desarrollo de habilidades de baloncesto y torneos interescolares",
        "schedule": "Martes y Jueves, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["james@mergington.edu", "carlos@mergington.edu"]
    },
    "Taller de Pintura": {
        "description": "Aprende técnicas de pintura y expresión artística",
        "schedule": "Miércoles, 3:30 PM - 5:00 PM",
        "max_participants": 16,
        "participants": ["isabella@mergington.edu", "sofia@mergington.edu"]
    },
    "Taller de Música": {
        "description": "Aprende a tocar instrumentos musicales y participa en conciertos",
        "schedule": "Lunes y Viernes, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["laura@mergington.edu", "marco@mergington.edu"]
    },
    "Club de Ciencias": {
        "description": "Realiza experimentos y explora disciplinas científicas",
        "schedule": "Jueves, 3:30 PM - 5:00 PM",
        "max_participants": 20,
        "participants": ["juan@mergington.edu", "patricia@mergington.edu"]
    },
    "Debate y Oratoria": {
        "description": "Desarrolla habilidades de argumentación y comunicación pública",
        "schedule": "Martes, 4:00 PM - 5:30 PM",
        "max_participants": 14,
        "participants": ["sebastian@mergington.edu", "victoria@mergington.edu"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Validate that the student is not already registered
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already registered for this activity")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}


@app.delete("/activities/{activity_name}/signup")
def remove_participant(activity_name: str, email: str):
    """Remove a student from an activity"""
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity = activities[activity_name]

    if email not in activity["participants"]:
        raise HTTPException(status_code=404, detail="Student not registered for this activity")

    activity["participants"].remove(email)
    return {"message": f"Removed {email} from {activity_name}"}
