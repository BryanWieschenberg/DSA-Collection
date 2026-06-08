from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.runner import router, executor


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    try:
        executor.shutdown(wait=True)
    except Exception:
        pass


app = FastAPI(title="DSA Execution API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)
