from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from api.router import api_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from core.tortoise_config import TORTOISE_ORM
from commands.__init__ import create_superuser
from fastapi.staticfiles import StaticFiles
import os



app = FastAPI(title="FastAPI Django-Like App")


# Set Cors Headers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API router
app.include_router(api_router)


register_tortoise(
    app,
    config=TORTOISE_ORM,
    generate_schemas=False,  # Let Aerich handle migrations
    add_exception_handlers=True,
)


# Serve static files (like Django's MEDIA_URL)
app.mount("/media", StaticFiles(directory="media"), name="media")

@app.on_event("startup")
async def startup_event():
    await create_superuser()
