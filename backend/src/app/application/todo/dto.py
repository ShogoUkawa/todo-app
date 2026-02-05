from dataclasses import dataclass
from datetime import datetime

from app.domain.todo.entity import Todo


@dataclass
class CreateTodoRequest:
    title: str
    description: str = ""


@dataclass
class UpdateTodoRequest:
    title: str | None = None
    description: str | None = None


@dataclass
class TodoResponse:
    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


def to_todo_response(todo: Todo) -> TodoResponse:
    return TodoResponse(
        id=str(todo.id.value),
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
        created_at=todo.created_at,
        updated_at=todo.updated_at,
    )
