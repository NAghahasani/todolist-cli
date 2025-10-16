"""CLI ToDoList – Phase 1 (In-Memory, Single File)."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Literal, Optional
from dotenv import load_dotenv
import os
import sys

Status = Literal["todo", "doing", "done"]


@dataclass
class Task:
  """Represents a task within a project."""
  title: str
  description: str = ""
  status: Status = "todo"


@dataclass
class Project:
  """Represents a project that groups tasks."""
  name: str
  description: str = ""
  tasks: List[Task] = field(default_factory=list)


class AppError(Exception):
  """Base error for the application."""


class ValidationError(AppError):
  """Raised when input validation fails."""


class ToDoApp:
  """In-memory application state and operations."""

  def __init__(self, max_projects: int, max_tasks: int) -> None:
    self._projects: List[Project] = []
    self._max_projects = max_projects
    self._max_tasks = max_tasks

  def run(self) -> None:
    """Entry point for the CLI loop (placeholder)."""
    print("ToDoList (In-Memory) — scaffold ready.")

  @staticmethod
  def from_env() -> "ToDoApp":
    """Factory that builds app from environment variables."""
    load_dotenv()
    try:
      max_projects = int(os.getenv("MAX_NUMBER_OF_PROJECT", "10"))
      max_tasks = int(os.getenv("MAX_NUMBER_OF_TASK", "100"))
    except ValueError as exc:
      raise ValidationError("Environment values must be integers.") from exc
    return ToDoApp(max_projects=max_projects, max_tasks=max_tasks)


def main(argv: Optional[List[str]] = None) -> int:
  """CLI entry point function."""
  _ = argv or sys.argv[1:]
  app = ToDoApp.from_env()
  app.run()
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
