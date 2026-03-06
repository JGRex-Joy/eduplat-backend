from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users, profile
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Eduplat API",
    description="Backend for Eduplat - Educational Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(profile.router, prefix="/api/v1/profile", tags=["Profile"])


@app.get("/")
def root():
    return {"message": "Eduplat API is running"}