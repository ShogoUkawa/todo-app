from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.todo.complete_todo import CompleteTodo
from app.application.todo.create_todo import CreateTodo
from app.application.todo.delete_todo import DeleteTodo
from app.application.todo.list_todos import ListTodos
from app.application.todo.update_todo import UpdateTodo
from app.domain.todo.repository import TodoRepository
from app.infrastructure.database.connection import get_session
from app.infrastructure.database.todo_repository import SQLAlchemyTodoRepository


def get_todo_repository(session: AsyncSession = Depends(get_session)) -> TodoRepository:
    return SQLAlchemyTodoRepository(session)


def get_create_todo(repo: TodoRepository = Depends(get_todo_repository)) -> CreateTodo:
    return CreateTodo(repo)


def get_list_todos(repo: TodoRepository = Depends(get_todo_repository)) -> ListTodos:
    return ListTodos(repo)


def get_update_todo(repo: TodoRepository = Depends(get_todo_repository)) -> UpdateTodo:
    return UpdateTodo(repo)


def get_delete_todo(repo: TodoRepository = Depends(get_todo_repository)) -> DeleteTodo:
    return DeleteTodo(repo)


def get_complete_todo(repo: TodoRepository = Depends(get_todo_repository)) -> CompleteTodo:
    return CompleteTodo(repo)
