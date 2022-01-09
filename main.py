from fastapi import FastAPI, Body, Query
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# Models
class Person(BaseModel):
    first_name: str
    last_name: str
    age: int
    hair_color: Optional[str] = None
    is_married: Optional[bool] = None

@app.get("/")
def home():
    return {"hello": "world"}

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(None, min_length=1, max_length=50),
    age: str = Query(...)
):
    return {name: age}
