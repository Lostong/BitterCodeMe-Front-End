from fastapi import HTTPException

from .. import api_router
from ..schemas import AuthRequest
from ..db import Session
from ..db.models.user import User
from backend.db.models.shared_tables import Role
from backend.db.models import User, Role


@api_router.post("/register")
def register(data: AuthRequest):
    with Session.begin() as session:
        user = session.query(User).where(User.email == data.email).one_or_none()
        curr_role = session.query(Role).where(Role.id == data.role_id).one_or_none()

        if user:
            raise HTTPException(
                status_code=400, detail="User with this email already exists"
            )
        if not curr_role:
            raise HTTPException(status_code=400, detail="Undefined role")

        new_user = User(email=data.email, role_id=curr_role.id)
        new_user.set_password(data.password)
        print("user added...")
        session.add(new_user)
        session.commit()
        print("user add!")

    return {"message": "User registered"}


@api_router.post("/login")
def login(data: AuthRequest):
    with Session.begin() as session:
        user = session.query(User).where(User.email == data.email).one_or_none()
        if user:
            if user.check_password(data.password):
                return user
            raise HTTPException(status_code=401, detail="Wrong password")
        raise HTTPException(status_code=404, detail="User not found")


@api_router.get("/user/email/{email}")
def get_user_byid(email: str):
    with Session.begin() as session:
        user = session.query(User).where(User.email == email).one_or_none()
        print(email)
        if user:
            print(user.id, user.email)
            return {"id": user.id, "email": user.email, "role_id": user.role_id}
        return {"error": "User not foend"}, 404
