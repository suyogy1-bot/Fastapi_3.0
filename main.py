from fastapi import FastAPI, Path, Field, HTTPException
from pydantic import BaseModel, validate_email
import os
import json

app = FastAPI()


@app.get("/test")
def test():
    return {"message": "server is working"}

FILE_PATH = 'students.json'

def load_student() -> list:
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH,"r") as file:
        return json.load(file)

def save_students(data:list):
    with open(FILE_PATH,"w") as file:
        return json.dump(data,file,indent=4)


class StudentResponse(BaseModel):
    id: int
    name: str = Field(min_length=2, max_length=50)
    email: Emailstr = Field(min_length=2, max_length=50)
    age: int = Field(ge=15, le=40)
    course: str = Field(min_length=2, max_length=50)
    city: str = Field(min_length=2, max_length=50)


@app.get("/students", response_model=list[StudentResponse])
def get_all_students(
    course: str | None = Query(default=None, min_length=2, max_length=50)
    city: str | None = Query(default=None)
    minage: int | None = Query(default=None, ge=15, le=40)
    maxage: str | None = Query(default=None)
    name: str | None = Query(default=None)
    skip: int = Query(default=0, ge=0)
    limit: int = Query(default=10, ge=10)
):

    students = load_student()

    if course:
        students = [s for s in students if s["course"].lower() == course.lower()]

    if city:
        students = [s for s in students if s["city"].lower() == city.lower()]

    if minage:
        students = [s for s in students if s["age"] >= minage]

    if maxage: 
        students = [s for s in students if s["age"] <= maxage]

    if name:
        students = [s for s in students if name.lower() in s['name'].lower()]


    return students[skip: skip+limit]



@app.post("/")
def new_student():
    print("new")

@app.put("/")

@app.patch("/")

@app.delete("/")

class CreateStudent(BaseModel):
    name: str
    email: EmailStr
    course: str
    phone_number: int
    city: str
    batch: str

class StudentResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    course: str
    phone_number: int
    city: str
    batch: str

