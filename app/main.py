from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import user, auth, travely, room, book, transaction, destination, promo, review

from .database import engine
from .models import Base


Base.metadata.create_all(bind=engine)
app = FastAPI()

# Set up all CORS

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# DEPENDENCY INJECTION

app.include_router(user.router)
app.include_router(auth.router)
app.include_router(travely.router)
app.include_router(room.router)
app.include_router(book.router)
app.include_router(transaction.router)
app.include_router(destination.router)
app.include_router(promo.router)
app.include_router(review.router)


@app.get("/")
def root():
    return {"message": "Welcome to the Travely API"}
