from app.domain.todo.entity import Todo


def test_create_sets_defaults() -> None:
    todo = Todo.create(title="Buy milk", description="Whole milk")
    assert todo.title == "Buy milk"
    assert todo.description == "Whole milk"
    assert todo.completed is False
    assert todo.id is not None
    assert todo.created_at == todo.updated_at


def test_create_description_defaults_empty() -> None:
    todo = Todo.create(title="Buy milk")
    assert todo.description == ""


def test_complete() -> None:
    todo = Todo.create(title="Buy milk")
    todo.complete()
    assert todo.completed is True
    assert todo.updated_at >= todo.created_at


def test_update_title_only() -> None:
    todo = Todo.create(title="Original")
    todo.update(title="Updated")
    assert todo.title == "Updated"
    assert todo.description == ""


def test_update_description_only() -> None:
    todo = Todo.create(title="Original", description="Old")
    todo.update(description="New")
    assert todo.title == "Original"
    assert todo.description == "New"


def test_update_with_no_args_changes_nothing() -> None:
    todo = Todo.create(title="Original", description="Desc")
    created_at = todo.created_at
    todo.update()
    assert todo.title == "Original"
    assert todo.description == "Desc"
    # updated_at still changes because update() was called
    assert todo.created_at == created_at
