from sqlalchemy import Table, Column, ForeignKey

from .. import Base
    
    
user_task_association_table = Table(
    "user_task_association_table",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("task_id", ForeignKey("tasks.id"), primary_key=True),
)