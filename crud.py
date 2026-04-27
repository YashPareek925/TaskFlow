from sqlalchemy.orm import Session
from models import Task, PriorityEnum, StatusEnum
from schemas import TaskCreate, TaskUpdate
from typing import List, Optional

def create_task(db: Session, task: TaskCreate) -> Task:
    new_task = Task(**task.dict())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

def get_all_tasks(
    db        : Session,
    priority  : Optional[PriorityEnum] = None,
    status    : Optional[StatusEnum]   = None,
    completed : Optional[bool]         = None,
) -> List[Task]:
    query = db.query(Task)

    # Apply filters if provided
    if priority  is not None: query = query.filter(Task.priority  == priority)
    if status    is not None: query = query.filter(Task.status    == status)
    if completed is not None: query = query.filter(Task.completed == completed)

    return query.order_by(Task.created_at.desc()).all()

def get_task_by_id(db: Session, task_id: int) -> Optional[Task]:
    return db.query(Task).filter(Task.id == task_id).first()

def update_task(db: Session, task_id: int, updates: TaskUpdate) -> Optional[Task]:
    task = get_task_by_id(db, task_id)
    if not task:
        return None
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(task, key, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int) -> bool:
    task = get_task_by_id(db, task_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True

def get_summary(db: Session) -> dict:
    """Return count of tasks by status and priority"""
    total     = db.query(Task).count()
    pending   = db.query(Task).filter(Task.status == StatusEnum.pending).count()
    progress  = db.query(Task).filter(Task.status == StatusEnum.in_progress).count()
    completed = db.query(Task).filter(Task.status == StatusEnum.completed).count()
    high      = db.query(Task).filter(Task.priority == PriorityEnum.high).count()
    medium    = db.query(Task).filter(Task.priority == PriorityEnum.medium).count()
    low       = db.query(Task).filter(Task.priority == PriorityEnum.low).count()

    return {
        "total_tasks"  : total,
        "by_status"    : {"pending": pending, "in_progress": progress, "completed": completed},
        "by_priority"  : {"high": high, "medium": medium, "low": low},
    }
