import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.todo.entity import Todo, TodoId
from app.domain.todo.repository import TodoRepository
from app.infrastructure.database.models import TodoModel


class SQLAlchemyTodoRepository(TodoRepository):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def save(self, todo: Todo) -> None:
        result = await self._session.execute(select(TodoModel).where(TodoModel.id == str(todo.id.value)))
        model = result.scalar_one_or_none()

        if model is None:
            model = TodoModel(
                id=str(todo.id.value),
                title=todo.title,
                description=todo.description,
                completed=todo.completed,
                created_at=todo.created_at,
                updated_at=todo.updated_at,
            )
            self._session.add(model)
        else:
            model.title = todo.title
            model.description = todo.description
            model.completed = todo.completed
            model.updated_at = todo.updated_at

    async def find_by_id(self, id: TodoId) -> Todo | None:
        result = await self._session.execute(select(TodoModel).where(TodoModel.id == str(id.value)))
        model = result.scalar_one_or_none()
        if model is None:
            return None
        return self._to_entity(model)

    async def find_all(self) -> list[Todo]:
        result = await self._session.execute(select(TodoModel).order_by(TodoModel.created_at))
        return [self._to_entity(m) for m in result.scalars().all()]

    async def delete(self, id: TodoId) -> None:
        result = await self._session.execute(select(TodoModel).where(TodoModel.id == str(id.value)))
        model = result.scalar_one_or_none()
        if model is not None:
            await self._session.delete(model)

    @staticmethod
    def _to_entity(model: TodoModel) -> Todo:
        return Todo(
            id=TodoId(value=uuid.UUID(model.id)),
            title=model.title,
            description=model.description,
            completed=model.completed,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
