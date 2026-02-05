from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.domain.exceptions import TodoNotFoundError
from app.infrastructure.config import settings
from app.interface.routes import todo

app = FastAPI(title="TODO API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(TodoNotFoundError)
async def todo_not_found_handler(request: Request, exc: TodoNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(todo.router)
