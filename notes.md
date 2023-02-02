## Installation

```bash
pip install fastapi uvicorn streamlit sqlmodel
```

# FAST API
```bash
mkdir backend frontend
cd backend

```
## Hello world

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}
```

    uvicorn main:app --reload

- Montrer la doc
- une API REST

## exemple appronfondi
```python
from pydantic import BaseModel

class Message(BaseModel):
    author: str
    message: str

@app.put("/messages/{message_id}")
def read_message(message_id: int, message: Message):
    return {"message_id": message_id, "message": message}
```
## Intérets? 
- Editor support: error checks, autocompletion, etc. 
- Data "parsing"
- Data validation 
- API annotation and automatic documentation

## SQLModel
ORM Créé par le même dev que FastAPI

```python
from sqlmodel import Field, Session, SQLModel, create_engine, select

class Message(SQLModel, table=True):
    author: str = Field()
    message: str = Field()

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True, connect_args={"check_same_thread": False})

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
```

## Frontend
Streamlit : python to code

```bash
cd frontend
streamlit run App.py
```
