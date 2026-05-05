from fastapi import APIRouter,Depends,status
from typing import List
from src.task import controller
from src.task.dtos import TaskSchema,TaskResponseSchema
from src.utils.db import get_db
from src.utils.helpers import is_authenticated
from src.user.models import UserModel

task_routes = APIRouter(prefix="/tasks",tags=["tasks"])

@task_routes.post("/create",response_model=TaskResponseSchema,status_code=status.HTTP_201_CREATED)
def create_task(body : TaskSchema ,db =Depends(get_db),user : UserModel = Depends(is_authenticated)):
    return controller.create_task(body,db,user)

@task_routes.get("/get",response_model=List[TaskResponseSchema],status_code=status.HTTP_200_OK)
def get_tasks(db = Depends(get_db),user : UserModel = Depends(is_authenticated)):
    return controller.get_tasks(db,user)

@task_routes.get("/get/{id}",response_model=TaskResponseSchema,status_code=status.HTTP_200_OK)
def get_task_by_id(id : int,db = Depends(get_db),user : UserModel = Depends(is_authenticated)):
    return controller.get_taskid(id,db)

@task_routes.put("/update/{id}",response_model=TaskResponseSchema,status_code=status.HTTP_201_CREATED)
def update_task(id : int,body : TaskSchema,db=Depends(get_db),user : UserModel = Depends(is_authenticated)):
    return controller.update_task(id,body,db,user)

@task_routes.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id : int,db=Depends(get_db),user : UserModel = Depends(is_authenticated)):
    return controller.delete_task(id,db,user)