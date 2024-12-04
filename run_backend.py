import uvicorn
from backend import app
from backend.db import engine, Base, Session, test_db
from backend.db.models import Role


# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


def create_role(name: str):
    with Session() as session:
        # Перевірка, чи існує роль з таким іменем
        existing_role = session.query(Role).filter_by(name=name).first()
        if existing_role:
            print(f"Role '{name}' already exists.")
            return existing_role

        # Якщо такої ролі ще немає, створюємо її
        role = Role(name=name)
        session.add(role)
        session.commit()
        return role


employer_role = create_role(name="Employer")
employee_role = create_role(name="Employee")

test_db.main()

# run fastapi
if __name__ == "__main__":
    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)
