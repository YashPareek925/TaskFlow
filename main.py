from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional

import models, crud, schemas
from database import engine, get_db
from models import PriorityEnum, StatusEnum

# ── Create MySQL tables automatically ────────────────────────────────────────
models.Base.metadata.create_all(bind=engine)

# ── App Setup ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="TaskFlow",
    description="Priority Based Task Management System built with FastAPI and MySQL",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/", tags=["Health"])
def root():
    return {"message": "TaskFlow is running!", "docs": "/docs"}


@app.post("/tasks/", response_model=schemas.TaskResponse, status_code=201, tags=["Tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
    """Create a new task with title, description, priority and status"""
    return crud.create_task(db, task)


@app.get("/tasks/", response_model=List[schemas.TaskResponse], tags=["Tasks"])
def get_all_tasks(
    priority  : Optional[PriorityEnum] = Query(None, description="Filter: low / medium / high"),
    status    : Optional[StatusEnum]   = Query(None, description="Filter: pending / in_progress / completed"),
    completed : Optional[bool]         = Query(None, description="Filter: true / false"),
    db        : Session                = Depends(get_db),
):
    """Get all tasks — filter by priority, status, or completion"""
    return crud.get_all_tasks(db, priority, status, completed)


@app.get("/tasks/summary", tags=["Tasks"])
def get_summary(db: Session = Depends(get_db)):
    """Get count of tasks grouped by status and priority"""
    return crud.get_summary(db)


@app.get("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
    """Get a single task by ID"""
    task = crud.get_task_by_id(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse, tags=["Tasks"])
def update_task(task_id: int, updates: schemas.TaskUpdate, db: Session = Depends(get_db)):
    """Update any field of a task"""
    task = crud.update_task(db, task_id, updates)
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.patch("/tasks/{task_id}/complete", response_model=schemas.TaskResponse, tags=["Tasks"])
def mark_complete(task_id: int, db: Session = Depends(get_db)):
    """Shortcut — mark task as completed"""
    task = crud.update_task(db, task_id, schemas.TaskUpdate(
        completed=True,
        status=StatusEnum.completed
    ))
    if not task:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task


@app.delete("/tasks/{task_id}", tags=["Tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
    """Delete a task permanently"""
    deleted = crud.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return {"message": f"Task {task_id} deleted successfully"}
