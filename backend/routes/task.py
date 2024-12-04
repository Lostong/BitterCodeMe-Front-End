from fastapi import HTTPException, Request
from os import getenv
from dotenv import load_dotenv
from fastapi import HTTPException

from .. import api_router
from ..utils import execute_with_timeout
from ..db import Session
from ..db.models import Task, User
from ..schemas import TaskData, TaskIDResponse
from sqlalchemy import select


load_dotenv()


# TODO можна утілку створити, бо тут трохи DRY
@api_router.get("/tasks")
def get_tasks():
    with Session() as session:
        tasks = session.query(Task).all()
        return tasks


@api_router.post("/tasks/create")
def create_task(task_data: TaskData):
    with Session() as session:
        task = Task(
            name=task_data.name,
            description=task_data.description,
            employer_id=task_data.employer_id,
            unit_tests=task_data.unit_tests,
            complexity_id=task_data.complexity_id,
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task


@api_router.put("/tasks/update/{id}")
def update_task(id: int, task_data: TaskData):
    with Session() as session:
        task = session.query(Task).filter(Task.id == id).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        data_to_update = task_data.model_dump(exclude_unset=True)
        for key, value in data_to_update.items():
            setattr(task, key, value)

        session.add(task)
        session.commit()
        session.refresh(task)

        return task


@api_router.delete("/tasks/delete/{id}")
def delete_task(id: int):
    with Session() as session:
        task = session.query(Task).filter(Task.id == id).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        session.delete(task)
        session.commit()

        return {"message": f"{task} was deleted"}


@api_router.post("/tasks/{id}/add_executor")
def add_executor(id: int, email: str):
    with Session() as session:
        task = session.query(Task).filter(Task.id == id).first()
        user = session.query(User).filter(User.email == email).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        task.add_executor(user=user)
        session.commit()
        return {"message": f"User {user.email} added as executor."}


@api_router.get("/tasks/not_executor_tasks/{email}", response_model=TaskIDResponse)
@api_router.get("/tasks/not_executor_tasks", response_model=TaskIDResponse)
def get_non_executor_tasks(email: str):
    with Session() as session:
        user = session.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        tasks = session.execute(
            select(Task.id, Task.name).where(~Task.executors.any(User.id == user.id))
        ).all()

        if tasks:
            task_ids, task_names = zip(*tasks)
        else:
            task_ids, task_names = [], []

        return {"task_ids": list(task_ids), "task_names": list(task_names)}


@api_router.put("/change_reputation")
def change_reputation(id: int, rep: int):
    with Session() as session:
        user = session.query(User).filter(User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        user.reputation_score += rep
        session.commit()
        return {"message": "Reputation changed"}


@api_router.get("/tasks/{id}")
def get_task(id: int):
    with Session() as session:
        task = session.query(Task).filter(Task.id == id).first()

        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        return task


@api_router.post("/execute_task")
async def execute_task(code: str, task_id: int, user_id: int):
    with Session() as session:
        user = session.query(User).filter(user_id == User.id).first()
        task = session.query(Task).filter(task_id == Task.id).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        elif not task:
            raise HTTPException(status_code=404, detail="Task not found")
        # elif user.tasks_attempts.get(str(task_id), 0) >= int(
        #     getenv("MAX_ATTEMPTS_CODE")
        # ):
        elif user.tasks_attempts.get(str(task_id), 0) >= int(2):
            raise HTTPException(
                status_code=403, detail="Maximum attempts reached for this task."
            )

        data = await execute_with_timeout(f"{code}\n\n{task.unit_tests}")

        user.tasks_attempts[str(task_id)] = user.tasks_attempts.get(str(task_id), 0) + 1

        session.commit()
        session.refresh(user)

        print(user)

        if data["status"] == "success":
            task.add_executor(user)

        return data


@api_router.get("/tasks/get_employer_tasks/")
async def get_employer_tasks(email: str):
    with Session() as session:
        user = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        tasks = session.query(Task).filter(Task.employer == user).all()
        return tasks
