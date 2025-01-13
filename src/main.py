from fastapi import FastAPI

from infrastructure.routers import profile_router

app = FastAPI()


app.include_router(profile_router.router, prefix="/profile", tags=["profile"])
