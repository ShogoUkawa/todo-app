from datetime import datetime

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, ConfigDict

from app.application.todo.complete_todo import CompleteTodo
from app.application.todo.create_todo import CreateTodo
from app.application.todo.delete_todo import DeleteTodo
from app.application.todo.dto import CreateTodoRequest, UpdateTodoRequest
from app.application.todo.list_todos import ListTodos
from app.application.todo.update_todo import UpdateTodo
from app.infrastructure.di import (
    get_complete_todo,
    get_create_todo,
    get_delete_todo,
    get_list_todos,
    get_update_todo,
)

router = APIRouter(prefix="/todos", tags=["todos"])


class CreateTodoSchema(BaseModel):
    title: str
    description: str = ""


class UpdateTodoSchema(BaseModel):
    title: str | None = None
    description: str | None = None


class TodoResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime


@router.post("", response_model=TodoResponseSchema, status_code=status.HTTP_201_CREATED)
async def create_todo(
    body: CreateTodoSchema,
    use_case: CreateTodo = Depends(get_create_todo),
) -> TodoResponseSchema:
    result = await use_case.execute(CreateTodoRequest(title=body.title, description=body.description))
    return TodoResponseSchema.model_validate(result)


@router.get("", response_model=list[TodoResponseSchema])
async def list_todos(
    use_case: ListTodos = Depends(get_list_todos),
) -> list[TodoResponseSchema]:
    results = await use_case.execute()
    return [TodoResponseSchema.model_validate(r) for r in results]


@router.put("/{todo_id}", response_model=TodoResponseSchema)
async def update_todo(
    todo_id: str,
    body: UpdateTodoSchema,
    use_case: UpdateTodo = Depends(get_update_todo),
) -> TodoResponseSchema:
    result = await use_case.execute(todo_id, UpdateTodoRequest(title=body.title, description=body.description))
    return TodoResponseSchema.model_validate(result)


@router.patch("/{todo_id}/complete", response_model=TodoResponseSchema)
async def complete_todo(
    todo_id: str,
    use_case: CompleteTodo = Depends(get_complete_todo),
) -> TodoResponseSchema:
    result = await use_case.execute(todo_id)
    return TodoResponseSchema.model_validate(result)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(
    todo_id: str,
    use_case: DeleteTodo = Depends(get_delete_todo),
) -> None:
    await use_case.execute(todo_id)
