from app.domain.exceptions import TodoNotFoundError
from app.domain.todo.entity import TodoId
from app.domain.todo.repository import TodoRepository


class DeleteTodo:
    def __init__(self, repo: TodoRepository) -> None:
        self._repo = repo

    async def execute(self, todo_id: str) -> None:
        entity_id = TodoId.from_str(todo_id)
        todo = await self._repo.find_by_id(entity_id)
        if todo is None:
            raise TodoNotFoundError(todo_id)
        await self._repo.delete(entity_id)
