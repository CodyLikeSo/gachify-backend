import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from tracks.dependencies import init_minio

from health.views import router as health_router
from tracks.views import router as tracks_router
from users.views.auth import router as auth_router

# from users.views.email_views import router as email_router
# from users.views.login_views import router as login_router
from users.views.crud import UsersCrud

from redisdb.utils import init_redis, close_redis


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_redis()
    await init_minio()
    yield
    await close_redis()


app = FastAPI(lifespan=lifespan)

# Utils routers
app.include_router(health_router)
app.include_router(tracks_router)
app.include_router(auth_router)
# app.include_router(login_router)

# Cruds routers
app.include_router(UsersCrud.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    try:
        host = "127.0.0.1"
        port = 8004
        print(f"SWAGGER - http://{host}:{port}/docs")
        uvicorn.run("main:app", host=host, port=port, reload=True)
    except Exception as e:
        print(e)
