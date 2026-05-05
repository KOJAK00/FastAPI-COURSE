from fastapi import HTTPException
from src.task.dtos import TaskSchema
from src.utils.db import get_db
from sqlalchemy.orm import Session
from src.task.models import TaskModel
from src.user.models import UserModel

def create_task(body : TaskSchema,db:Session,user : UserModel ):
    data = body.model_dump()
    new_task = TaskModel(title = data["title"],
                         description = data["description"],
                         is_completed= data["is_completed"],
                         user_id = user.id
                         )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_tasks(db:Session,user :UserModel):
    tasks=db.query(TaskModel).filter(TaskModel.user_id==user.id).all()
    return tasks

def get_taskid(id: int,db:Session):
    task=db.query(TaskModel).filter(TaskModel.id==id).first()
    if not task:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    return task

def update_task(id:int,body : TaskSchema ,db:Session,user):
    one_task:TaskModel = db.query(TaskModel).get(id)
    if not one_task:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    if one_task.user_id!=user.id:
        raise HTTPException(status_code=401, detail="You are not allowed to update this task")
    body=body.model_dump()
    for field,value in body.items():
        setattr(one_task,field,value)
    db.add(one_task)
    db.commit()
    db.refresh(one_task)

    return one_task

def delete_task(id:int,db:Session,user:TaskModel):
    one_task:TaskModel = db.query(TaskModel).get(id)
    if not one_task:
        raise HTTPException(status_code=404, detail=f"Task with id {id} not found")
    if one_task.user_id!=user.id:
        raise HTTPException(status_code=401, detail="You are not allowed to delete this task")
    db.delete(one_task)
    db .commit()

    return None