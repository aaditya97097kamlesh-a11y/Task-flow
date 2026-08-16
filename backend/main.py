from sqlalchemy import func
from fastapi import FastAPI, Depends, HTTPException,Request
import time
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine, get_db
import models
from algorithms import insertion_sort, binary_search, linear_search
from schemas import (
    TaskCreate,
    TaskResponse,
    TaskUpdate,
    UserCreate,
    ProjectCreate,
    UserResponse,
    ProjectResponse
)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500", "http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"- {process_time:.2f} ms"
    )

    return response

def get_db_session(db: Session = Depends(get_db)):
    return db

Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "TaskFlow API is working"
    }
# -------------------------
# USER ENDPOINTS
# -------------------------

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = models.User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get("/users", response_model=list[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# -------------------------
# PROJECT ENDPOINTS
# -------------------------

@app.post("/projects", response_model=ProjectResponse, status_code=201)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db_session)
):
    new_project = models.Project(
        name=project.name,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return new_project


@app.get("/projects", response_model=list[ProjectResponse])
def get_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

# -------------------------
# TASK ENDPOINTS
# -------------------------

@app.post("/tasks", response_model=TaskResponse, status_code=201)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = models.Task(
        title=task.title,
        priority=task.priority,
        due_date=task.due_date,
        project_id=task.project_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.get("/tasks", response_model=list[TaskResponse])
def get_tasks(sort: str = "", db: Session = Depends(get_db)):
    tasks = db.query(models.Task).all()

    # Normal request: database order me tasks return
    if sort == "":
        return tasks

    # Priority ke according sorting
    if sort == "priority":
        records = [
            {
                "id": task.id,
                "title": task.title,
                "priority": task.priority,
                "due_date": task.due_date,
                "project_id": task.project_id
            }
            for task in tasks
        ]

        # low < medium < high
        priority_order = {
            "low": 1,
            "medium": 2,
            "high": 3
        }

        for record in records:
            record["priority_value"] = priority_order.get(
                record["priority"], 99
            )

        insertion_sort(records, "priority_value")

        for record in records:
            record.pop("priority_value")

        return records

    raise HTTPException(
        status_code=400,
        detail="Invalid sort option"
    )

@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):  
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task

@app.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_data: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = task_data.title
    task.priority = task_data.priority
    task.due_date = task_data.due_date

    db.commit()
    db.refresh(task)

    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    return None

@app.get("/projects/statistics")
def project_statistics(db: Session = Depends(get_db)):
    results = (
        db.query(
            models.Project.id,
            models.Project.name,
            func.count(models.Task.id).label("task_count")
        )
        .outerjoin(models.Task, models.Project.id == models.Task.project_id)
        .group_by(models.Project.id, models.Project.name)
        .all()
    )

    return [
        {
            "project_id": project_id,
            "project_name": project_name,
            "task_count": task_count
        }
        for project_id, project_name, task_count in results
    ]
