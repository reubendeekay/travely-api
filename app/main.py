from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import user, auth, travely, room, book, transaction

from .database import engine
from .models import Base


Base.metadata.create_all(bind=engine)
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(travely.router)
app.include_router(room.router)
app.include_router(book.router)
app.include_router(transaction.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Travely API"}
