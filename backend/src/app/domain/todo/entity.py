import uuid
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class TodoId:
    value: uuid.UUID

    @classmethod
    def generate(cls) -> "TodoId":
        return cls(value=uuid.uuid4())

    @classmethod
    def from_str(cls, value: str) -> "TodoId":
        return cls(value=uuid.UUID(value))

    def __str__(self) -> str:
        return str(self.value)


@dataclass
class Todo:
    id: TodoId
    title: str
    description: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(cls, title: str, description: str = "") -> "Todo":
        now = datetime.now(tz=UTC)
        return cls(
            id=TodoId.generate(),
            title=title,
            description=description,
            completed=False,
            created_at=now,
            updated_at=now,
        )

    def complete(self) -> None:
        self.completed = True
        self.updated_at = datetime.now(tz=UTC)

    def update(self, title: str | None = None, description: str | None = None) -> None:
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        self.updated_at = datetime.now(tz=UTC)
