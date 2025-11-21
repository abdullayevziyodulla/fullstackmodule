import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from datetime import datetime
from typing import List

app = FastAPI(title="SPASS")

class Appointment(BaseModel):
    doctor_name: str
    patient_name: str
    date: datetime
    duration_minutes: int

appointments = []

@app.get('/')
def home():
    return {"message": "Welcome to the SPASS API"}

@app.get('/appointments/', response_model=List[Appointment])
def list_appointments():
    return appointments

@app.post('/appointments/create')
def create_appointment(a: Appointment):
    appointments.append(a)
    return {"message": "Appointment created successfully", "appointment": a}

@app.delete('/appointments/{id}/delete/')
def delete_appointment(id: int):
    appointments.pop(id)
    return {"message": "Appointment deleted successfully"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
