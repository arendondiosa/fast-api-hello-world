from fastapi import FastAPI, Body, Query, Path
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum

app = FastAPI()

# Models
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"


class Location(BaseModel):
    city: str
    state: str
    country: str


class Person(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=50)
    last_name: str = Field(..., min_length=1, max_length=50)
    age: int = Field(..., gt=0, le=115)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Alejandro",
                "last_name": "Rendon",
                "age": 27,
                "hair_color": "red",
                "is_married": False,
            }
        }


@app.get("/")
def home():
    return {"hello": "world"}


@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person


@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters",
        example="Rocio",
    ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required",
        example=25,
    ),
):
    return {name: age}


@app.get("/person/detal/{person_id}")
def show_person(person_id: int = Path(..., gt=0)):
    return {person_id: "It exist"}


@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ..., title="Person Id", description="This is the person id", gt=0
    ),
    person: Person = Body(...),
    location: Location = Body(...),
):
    results = person.dict()
    results.update(location.dict())
    return results
