class TodoNotFoundError(Exception):
    def __init__(self, todo_id: str) -> None:
        super().__init__(f"Todo with id {todo_id} not found")
