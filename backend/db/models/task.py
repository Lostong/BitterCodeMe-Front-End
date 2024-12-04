from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from typing import Optional, List

from .. import Base
from .associations import user_task_association_table


class Task(Base):
    """Represents a task creater by an employer

    Attributes:
        id (int): The unique identifier for the task.
        name (str): The name of the task.
        description (str): The description of the task.
        unit_tests (str): The unit tests provided by the employer.
        complexity (Complexity): The complexity level of the task.
        complexity_id int(): Complexity's ID
        employer (User): The user who created the task.
        employer_id (int): Employer's ID 
        executors (List[User]): The user who is completing (or completed) the task.
    """

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    unit_tests: Mapped[str] = mapped_column(nullable=False)

    complexity_id: Mapped[int] = mapped_column(ForeignKey("complexitys.id"))
    complexity: Mapped["Complexity"] = relationship(
        back_populates="tasks", foreign_keys=[complexity_id]
    )

    employer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    employer: Mapped["User"] = relationship(
        back_populates="created_tasks", foreign_keys=[employer_id]
    )

    executors: Mapped[List["User"]] = relationship(
        back_populates="completed_tasks",
        secondary=user_task_association_table,
    )

    # TODO: change value limits
    @validates("name")
    def validate_name(self, key, name):
        if not (200 > len(name) > 1):
            raise ValueError("Description length must be between 10 and 50.")
        return name

    # TODO: change value limits
    @validates("description")
    def validate_description(self, key, description):
        if not (200 > len(description) > 1):
            raise ValueError("Description length must be between 20 and 200.")
        return description

    # TODO: додати валідацію на рівні апішки (при потребі)
    # @validates("employer")
    # def validate_employer(self, key, user):
    #     if user.role.name not in ["Employer", "Admin"]:
    #         raise ValueError("Only employers and admins can create tasks.")
    #     return user
    
    def add_executor(self, user: "User") -> None:
        if user not in self.executors:
            self.executors.append(user)

    def __repr__(self) -> str:
        return (
            f"Task(id={self.id!r}, name={self.name!r}, description={self.description!r}, "
            f"unit_tests={self.unit_tests!r}, complexity_id={self.complexity_id!r}, "
            f"employer_id={self.employer_id!r})"
        )
