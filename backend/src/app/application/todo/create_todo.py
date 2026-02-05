from app.application.todo.dto import CreateTodoRequest, TodoResponse, to_todo_response
from app.domain.todo.entity import Todo
from app.domain.todo.repository import TodoRepository


class CreateTodo:
    def __init__(self, repo: TodoRepository) -> None:
        self._repo = repo

    async def execute(self, request: CreateTodoRequest) -> TodoResponse:
        todo = Todo.create(title=request.title, description=request.description)
        await self._repo.save(todo)
        return to_todo_response(todo)
