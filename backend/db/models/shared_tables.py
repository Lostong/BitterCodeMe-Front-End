from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

from .. import Base

class Role(Base):
    """Represents a role that can be assigned to a user (Admin, Employer, Employee).

    Attributes:
        id (int): The unique identifier for the role.
        name (str): The name of the role.
        users (List[User]): The users assigned to this role.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    users: Mapped[List["User"]] = relationship(back_populates="role")

    def __repr__(self) -> str:
        return f"Role(id={self.id!r}, name={self.name!r})"


class Complexity(Base):
    """Represents the complexity of a task (Difficult, Medium, Easy).

    Attributes:
        id (int): The unique identifier for the complexity.
        name (str): The name of the complexity level.
        tasks (List[Task]): The tasks associated with this complexity.
    """
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    
    tasks: Mapped[List["Task"]] = relationship(back_populates="complexity")
    
    def __repr__(self) -> str:
        return f"Complexity(id={self.id!r}, name={self.name!r})"
    