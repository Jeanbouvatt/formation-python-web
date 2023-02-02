from typing import Optional

from fastapi import FastAPI

app = FastAPI()
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    author: str
    message: str


sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/messages/")
def read_messages():
    with Session(engine) as session:
        messages = session.exec(select(Message)).all()
        return messages


@app.post("/messages/")
def create_message(message: Message):
    with Session(engine) as session:
        session.add(message)
        session.commit()
        session.refresh(message)
        return message
