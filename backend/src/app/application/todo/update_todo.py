from app.application.todo.dto import TodoResponse, UpdateTodoRequest, to_todo_response
from app.domain.exceptions import TodoNotFoundError
from app.domain.todo.entity import TodoId
from app.domain.todo.repository import TodoRepository


class UpdateTodo:
    def __init__(self, repo: TodoRepository) -> None:
        self._repo = repo

    async def execute(self, todo_id: str, request: UpdateTodoRequest) -> TodoResponse:
        entity_id = TodoId.from_str(todo_id)
        todo = await self._repo.find_by_id(entity_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        todo.update(title=request.title, description=request.description)
        await self._repo.save(todo)
        return to_todo_response(todo)
