from abc import ABC, abstractmethod

from app.domain.todo.entity import Todo, TodoId


class TodoRepository(ABC):
    @abstractmethod
    async def save(self, todo: Todo) -> None: ...

    @abstractmethod
    async def find_by_id(self, id: TodoId) -> Todo | None: ...

    @abstractmethod
    async def find_all(self) -> list[Todo]: ...

    @abstractmethod
    async def delete(self, id: TodoId) -> None: ...
