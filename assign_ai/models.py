import uuid as uuid_pkg
from datetime import datetime

from passlib.context import CryptContext
from sqlalchemy_utils import UUIDType
from sqlmodel import Column, Field, Relationship, SQLModel

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hackathon(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, sa_column=Column(UUIDType(), primary_key=True)
    )
    title: str
    description: str
    background_image: str
    hackathon_image: str
    type_of_submission: str
    start_datetime: str
    end_datetime: str
    reward_prize: float
    users: list["HackathonUser"] = Relationship(back_populates="hackathon")
    submissions: list["Submission"] = Relationship(back_populates="hackathon")


class User(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(default_factory=uuid_pkg.uuid4, primary_key=True)
    username: str
    email: str
    password: str
    full_name: str
    hackathons: list["HackathonUser"] = Relationship(back_populates="user")
    submissions: list["Submission"] = Relationship(back_populates="user")

    def set_password(self, password: str):
        self.password = pwd_context.hash(password)


class HackathonUser(SQLModel, table=True):
    hackathon_id: uuid_pkg.UUID = Field(foreign_key="hackathon.id", primary_key=True)
    user_id: uuid_pkg.UUID = Field(foreign_key="user.id", primary_key=True)
    hackathon: Hackathon = Relationship(back_populates="users")
    user: User = Relationship(back_populates="hackathons")


class Submission(SQLModel, table=True):
    id: uuid_pkg.UUID = Field(
        default_factory=uuid_pkg.uuid4, sa_column=Column(UUIDType(), primary_key=True)
    )
    name: str
    summary: str
    submission: str
    user_id: uuid_pkg.UUID = Field(foreign_key="user.id")
    hackathon_id: uuid_pkg.UUID = Field(foreign_key="hackathon.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship(back_populates="submissions")
    hackathon: Hackathon = Relationship(back_populates="submissions")
