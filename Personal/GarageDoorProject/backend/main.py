import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse

import auth
import door
import state


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.start_state_subscriber()
    yield


app = FastAPI(title="Garage Door API", lifespan=lifespan)

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")

app.include_router(auth.router)
app.include_router(door.router)
app.include_router(state.router)


@app.get("/")
def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))


@app.get("/login")
def serve_login():
    return FileResponse(os.path.join(FRONTEND_DIR, "login.html"))
