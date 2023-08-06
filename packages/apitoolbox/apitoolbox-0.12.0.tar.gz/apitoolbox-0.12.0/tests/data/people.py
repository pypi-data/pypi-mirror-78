""" Generic test data """
from datetime import datetime
from uuid import UUID

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.types import CHAR
from pydantic import BaseModel, PositiveInt, constr

from apitoolbox import models

PEOPLE_DATA = [
    {"name": "alice", "order": 1, "gender": "F", "age": 32},
    {"name": "bob", "order": 2, "gender": "M", "age": 22},
    {"name": "charlie", "order": 3, "gender": "M", "age": 60},
    {"name": "david", "order": 4, "gender": "M", "age": 32},
]


class Person(models.BASE, models.GuidMixin, models.TimestampMixin):
    __tablename__ = "people"

    name = sqlalchemy.Column(
        sqlalchemy.String(255),
        nullable=False,
        unique=True
    )

    order = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False,
        unique=True
    )

    gender = sqlalchemy.Column(
        CHAR(1),
        nullable=False
    )

    age = sqlalchemy.Column(
        sqlalchemy.Integer,
        nullable=False
    )


class PersonRequestModel(BaseModel):
    name: constr(max_length=255)
    order: int
    gender: constr(min_length=1, max_length=1)
    age: PositiveInt


class PersonResponseModel(PersonRequestModel):
    id: UUID
    created_at: datetime
    updated_at: datetime


def load_people(session: Session):
    people = []
    for data in PEOPLE_DATA:
        person = Person(**data)
        people.append(person)

    session.add_all(people)
    session.commit()

    assert len(people) == len(PEOPLE_DATA)
    return people
