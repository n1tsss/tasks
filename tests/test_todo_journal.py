# pylint: disable=missing-function-docstring

import json

import pytest

from src.todo_journal import TodoJournal


def test_create_and_init(tmp_path):
    todo_path = tmp_path / "todo.json"
    TodoJournal.create(todo_path, "test")

    todo = TodoJournal(todo_path)

    assert todo.name == "test"
    assert todo.entries == []
    assert len(todo) == 0


def test_add_entry(tmp_path):
    todo_path = tmp_path / "todo.json"
    TodoJournal.create(todo_path, "test")
    todo = TodoJournal(todo_path)

    todo.add_entry("Сходить за молоком")

    with todo_path.open("r", encoding="utf-8") as file:
        data = json.load(file)
    assert data["todos"] == ["Сходить за молоком"]


def test_remove_entry(tmp_path):
    todo_path = tmp_path / "todo.json"
    with todo_path.open("w", encoding="utf-8") as file:
        json.dump({"name": "test", "todos": ["a", "b", "c"]}, file)
    todo = TodoJournal(todo_path)

    todo.remove_entry(1)

    assert todo.entries == ["a", "c"]


def test_iter_and_getitem(tmp_path):
    todo_path = tmp_path / "todo.json"
    with todo_path.open("w", encoding="utf-8") as file:
        json.dump({"name": "test", "todos": ["a", "b", "c"]}, file)
    todo = TodoJournal(todo_path)

    assert list(iter(todo)) == ["a", "b", "c"]
    assert todo[0] == "a"
    assert todo.first == "a"
    assert todo.last == "c"


def test_not_found_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        TodoJournal(tmp_path / "missing.json")
