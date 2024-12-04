from fastapi import FastAPI, APIRouter

app = FastAPI()

api_router = APIRouter(prefix="/api")

from . import routes

app.include_router(api_router)