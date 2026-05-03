"""Todo journal module."""

from __future__ import annotations

import json
from pathlib import Path


class TodoJournal:
    """Manage a todo journal stored in JSON."""

    shortcut_names = {"first": 0, "last": -1}

    def __init__(self, path_todo: str | Path) -> None:
        self.path_todo = Path(path_todo)
        data = self._parse()
        self.name = data["name"]
        self.entries = data["todos"]

    @staticmethod
    def create(filename: str | Path, name: str) -> None:
        """Create an empty todo journal file."""
        file_path = Path(filename)
        if file_path.exists():
            raise FileExistsError(f"Todo file already exists: {file_path}")
        with file_path.open("w", encoding="utf-8") as todo_file:
            json.dump(
                {"name": name, "todos": []},
                todo_file,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    def __len__(self) -> int:
        """Return number of todo entries."""
        return len(self.entries)

    def __iter__(self):
        """Iterate through todo entries."""
        return iter(self.entries)

    def __getitem__(self, index: int) -> str:
        """Return entry by index or slice."""
        return self.entries[index]

    def __getattr__(self, item: str):
        """Support virtual readonly attributes first/last."""
        index = self.shortcut_names.get(item)
        if index is not None:
            return self.entries[index]
        cls = type(self)
        raise AttributeError(f"{cls.__name__} object has no attribute {item}")

    def __setattr__(self, name: str, value) -> None:
        """Disallow writing virtual readonly attributes."""
        if name in self.shortcut_names:
            raise AttributeError(f"readonly attribute {name}")
        super().__setattr__(name, value)

    def add_entry(self, new_entry: str) -> None:
        """Add a new todo entry and save journal."""
        self.entries.append(new_entry)
        self._update({"name": self.name, "todos": self.entries})

    def remove_entry(self, index: int) -> None:
        """Remove todo entry by index and save journal."""
        try:
            self.entries.pop(index)
        except IndexError as error:
            raise IndexError(f"No todo entry with index {index}") from error
        self._update({"name": self.name, "todos": self.entries})

    def _update(self, new_data: dict) -> None:
        """Write todo data to file."""
        with self.path_todo.open("w", encoding="utf-8") as todo_file:
            json.dump(
                new_data,
                todo_file,
                sort_keys=True,
                indent=4,
                ensure_ascii=False,
            )

    def _parse(self) -> dict:
        """Read and validate todo data from file."""
        if not self.path_todo.exists():
            raise FileNotFoundError(f"Todo file does not exist: {self.path_todo}")
        with self.path_todo.open("r", encoding="utf-8") as todo_file:
            data = json.load(todo_file)
        if not isinstance(data, dict) or "name" not in data or "todos" not in data:
            raise ValueError("Invalid todo JSON format")
        if not isinstance(data["todos"], list):
            raise ValueError("Invalid todo JSON format: todos must be a list")
        return data
