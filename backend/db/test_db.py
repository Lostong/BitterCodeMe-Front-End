# TEST DB
# This script required to run as a module because of relative imports:
# $ ~/bittercodeme/backend > python -m db.test_db

from typing import Optional, List
from email_validator import validate_email, EmailNotValidError

from . import Base, Session, engine
from .models.task import Task
from .models.user import User
from .models.shared_tables import Role, Complexity


def email_validation(email):
    try:
        validate_email(email)
    except EmailNotValidError as ex:
        raise EmailNotValidError(f"Email {email} is not valid: {ex}")

    return email


def create_role(name: str) -> None:
    with Session() as session:
        role = Role(name=name)
        session.add(role)
        session.commit()

        return role


def create_user(email: str, role: Role, password: str, **kwargs) -> None:
    with Session() as session:
        user = User(email=email_validation(email), role=role, **kwargs)
        user.set_password(password)

        session.add(user)
        session.commit()

        return user


def create_complexity(name):
    with Session() as session:
        complexity = Complexity(name=name)
        session.add(complexity)
        session.commit()

        return complexity


def create_task(
    name: str,
    description: str,
    unit_tests: str,
    complexity: Complexity,
    employer: User,
    executors: List[User] = [],
):
    with Session() as session:
        task = Task(
            name=name,
            description=description,
            unit_tests=unit_tests,
            complexity=complexity,
            employer=employer,
            executors=executors,
        )
        session.add(task)
        session.commit()

        return task


# def create_solution(
#     task_id: Task,
#     user_id: int,
#     code: str,
#     is_passed: bool = False,
# ):
#     with Session() as session:
#         solution = Solution(
#             task_id=task_id,
#             user_id=user_id,
#             code=code,
#             is_passed=is_passed
#         )
#         session.add(solution)
#         session.commit()

#         return solution


def main():
    Base.metadata.drop_all(engine)  # for development stage
    Base.metadata.create_all(engine)

    employer_role = create_role(name="Employer")
    employee_role = create_role(name="Employee")
    admin_role = create_role(name="Admin")

    easy_complexity = create_complexity(name="easy")
    medium_complexity = create_complexity(name="medium")
    difficult_complexity = create_complexity(name="difficult")

    admin_user = create_user(
        email="someemail@gmail.com", role=admin_role, password="12345678"
    )
    employer_user = create_user(
        email="anotheremail@gmail.com", role=employer_role, password="qwert"
    )
    employee_user = create_user(
        email="vitalik@gmail.com", role=employee_role, password="dawawd"
    )
    # invalid_user = create_user(email="invalidemail", role=employee_role, password="dwadwa")  # invalid email

    create_task(
        name="Create email validator",
        description="I want you to create email validator using module 're'",
        employer=employer_user,
        unit_tests="*some tests*",
        complexity=easy_complexity,
        executors=[employee_user, admin_user],
    )

    create_task(
        name="Implement user authentication",
        description="Develop a user authentication system with JWT.",
        employer=employer_user,
        unit_tests="assert func(1,2) == 3",
        complexity=medium_complexity,
    )

    # create_solution(
    #     task_id=1,
    #     user_id=1,
    #     code="""
    #     print(123)
    #     """
    # )

    # create_solution(
    #     task_id=1,
    #     user_id=1,
    #     code="""
    #     a = lambda x: x+1
    #     print(a(1))
    #     """
    # )

    # with Session() as session:
    #     tasks = session.query(Task).all()
    #     print("\n"*3)
    #     for task in tasks:
    #         print(f"Task: {task.name}, Executors: {[executor.email for executor in task.executors]}")
    #     print("\n"*3)

    #     users = session.query(User).all()
    #     print("\n"*3)
    #     for user in users:
    #         print(f"User: {user.email}, Completed Tasks: {[task.name for task in user.completed_tasks]}")
    #     print("\n"*3)


if __name__ == "__main__":
    main()
