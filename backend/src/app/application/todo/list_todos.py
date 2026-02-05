from app.application.todo.dto import TodoResponse, to_todo_response
from app.domain.todo.repository import TodoRepository


class ListTodos:
    def __init__(self, repo: TodoRepository) -> None:
        self._repo = repo

    async def execute(self) -> list[TodoResponse]:
        todos = await self._repo.find_all()
        return [to_todo_response(todo) for todo in todos]
