# ✅ TaskFlow — Priority Based Task Management System

A full CRUD REST API built with **FastAPI**, **SQLAlchemy**, and **MySQL**.  
Manage tasks with priority levels, status tracking, filtering, and auto-generated Swagger docs.

---

## 🚀 Tech Stack

| Tool | Purpose |
|------|---------|
| FastAPI | Web framework & routing |
| SQLAlchemy | ORM for MySQL |
| PyMySQL | MySQL database driver |
| Pydantic | Request/response validation |
| Uvicorn | ASGI server |

---

## 📁 Project Structure

```
TaskFlow/
├── main.py          # All routes
├── crud.py          # Database operations
├── database.py      # MySQL connection
├── models.py        # Task table with enums
├── schemas.py       # Request/response validation
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone repo
git clone https://github.com/yourusername/TaskFlow.git
cd TaskFlow

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create MySQL database
# In MySQL: CREATE DATABASE taskflowdb;

# 5. Setup environment variables
cp .env.example .env
# Edit .env with your MySQL credentials

# 6. Run server
uvicorn main:app --reload
```

Open docs at: **http://127.0.0.1:8000/docs**

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/tasks/` | Create new task |
| GET | `/tasks/` | Get all tasks (filter by priority/status/completed) |
| GET | `/tasks/summary` | Count tasks by status and priority |
| GET | `/tasks/{id}` | Get task by ID |
| PUT | `/tasks/{id}` | Update any field |
| PATCH | `/tasks/{id}/complete` | Mark task as completed |
| DELETE | `/tasks/{id}` | Delete task |

---

## 🔍 Filter Examples

```
GET /tasks/?priority=high
GET /tasks/?status=pending
GET /tasks/?completed=false
GET /tasks/?priority=high&status=in_progress
```

---

## 📦 Sample Response

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "description": "Build a full CRUD backend",
  "priority": "high",
  "status": "in_progress",
  "completed": false,
  "created_at": "2025-04-27T10:00:00",
  "updated_at": null
}
```

---

## 👨‍💻 Author

**Yash Pareek** | BCA Student — Maharshi Dayanand University Ajmer  
[GitHub](https://github.com/YashPareek925/) • [LinkedIn](www.linkedin.com/in/yash-pareek-475765341)
