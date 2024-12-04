from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
from sqlalchemy.ext.mutable import MutableDict
from typing import List
from bcrypt import hashpw, checkpw, gensalt

from .. import Base
from .task import Task
from .associations import user_task_association_table


class User(Base):
    """Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        email (str): The user's email address (must be unique).
        _password_hashed (str): The hashed password of the user.
        role (Role): The role assigned to the user.
        role_id (int): Role's ID
        reputation_score (int): The user's reputation score.
        is_active (bool): Indicates whether the user is active.
        created_tasks (List[Task]): The tasks created by the user.
        completed_tasks (List[Task]): The tasks completed by the user.
        tasks_attempts (JSON): User attempts to perform some task
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    _password_hashed: Mapped[str] = mapped_column(nullable=False)

    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"))
    role: Mapped["Role"] = relationship(back_populates="users")

    reputation_score: Mapped[int] = mapped_column(default=0)

    is_active: Mapped[bool] = mapped_column(default=True, unique=False)

    created_tasks: Mapped[List["Task"]] = relationship(
        back_populates="employer",
        cascade="all, delete-orphan",
        foreign_keys="[Task.employer_id]",
    )

    completed_tasks: Mapped[List["Task"]] = relationship(
        back_populates="executors",
        secondary=user_task_association_table,
        # foreign_keys="[user_task_association_table.user_id]",
    )
    
    tasks_attempts: Mapped[dict] = mapped_column(MutableDict.as_mutable(JSON), default=dict)


    # TODO: можна добавити валідацію паролю (мінімальна довжина, найпростіші паролі і т.д.)
    def set_password(self, password: str) -> None:
        self._password_hashed = hashpw(password.encode("utf-8"), gensalt())

    def check_password(self, password: str) -> bool:
        return checkpw(password.encode("utf-8"), self._password_hashed)

    def complete_task(self, task: "Task") -> None:
        if task not in self.completed_tasks:
            self.completed_tasks.append(task)
        
    
    def __repr__(self) -> str:
        return (
            f"User(id={self.id!r}, email={self.email!r}, role_id={self.role_id!r}, "
            f"reputation_score={self.reputation_score!r}, is_active={self.is_active!r}), "
            f"tasks_attempts={self.tasks_attempts!r})"
        )
