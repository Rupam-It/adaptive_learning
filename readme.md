## 🏗️ Architecture Overview

The system follows a two-stage orchestration pattern designed for future LLM integration:

### **1. The Planner (The Brain)**
- **Input**: Student profile + assessment request
- **Output**: Structured `AssessmentPlan` (JSON contract)
- **Role**: Makes strategic decisions about WHAT problems to select based on pedagogy
- **Current Implementation**: Rule-based logic (can be swapped with LLM later)

### **2. The Executor (The Hands)**
- **Input**: `AssessmentPlan` from Planner
- **Output**: Selected problems from database
- **Role**: Executes the plan without making decisions
- **Implementation**: Queries PostgreSQL and assembles assessment

### **Why This Design?**
- **Decoupled**: Planner and Executor are independent
- **Swappable**: Tomorrow, replace Planner with GPT-4 without changing Executor
- **Contract**: `AssessmentPlan` is the interface between components
- **Scalable**: Database handles 10K+ problems efficiently with indexes

---

## 🚀 Quick Start

### **1. Start Docker (Database + pgAdmin)**
```bash
docker-compose up -d
```

### **2. Setup Python Virtual Environment**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

### **3. Initialize Database**
```bash
python init_db.py
```

### **4. Run API Locally**
```bash
uvicorn app.main:app --reload
```

### **5. Access Services**
- **API Docs**: http://localhost:8000/docs
- **pgAdmin**: http://localhost:5050 (admin@admin.com / admin123)

---

## 🔄 How to Re-run Everything

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Ensure Docker is running
docker-compose up -d

# 3. Run FastAPI
uvicorn app.main:app --reload
```

---

## 🧪 Testing with Thunder Client (VS Code)

### **1. Install Thunder Client Extension**
Search "Thunder Client" in VS Code extensions

### **2. Test CRUD Operations**

**GET All Problems:**
```
GET http://localhost:8000/api/problems
```

**GET Single Problem:**
```
GET http://localhost:8000/api/problems/5052e02a-2a05-4eb9-8669-063c89e03c10
```

**POST Create Problem:**
```
POST http://localhost:8000/api/problems
Content-Type: application/json

{
  "id": "test-001",
  "text": "What is 5 + 5?",
  "topic": "Arithmetic",
  "difficulty": 1,
  "estimated_time_to_solve_minutes": 2
}
```

### **3. Test Assessment Generation**

**POST Generate Assessment:**
```
POST http://localhost:8000/api/assessments/generate
Content-Type: application/json

{
  "student_profile": {
    "id": "student123",
    "mastered_topics": ["Algebra", "Arithmetic"],
    "learning_goals": ["Geometry"]
  },
  "assessment_request": {
    "max_total_time_minutes": 30,
    "pedagogical_strategy": "REVIEW"
  }
}
```

**Pedagogical Strategies:**
- `REVIEW` - Easy/medium problems from mastered topics
- `NEW_TOPIC_INTRODUCTION` - Easy problems from learning goals
- `CHALLENGE` - Hard problems from mastered topics

---

## 📊 Database Management (Adminer)
### **2. Access Adminer:**
Open browser: **http://localhost:8080**

### **3. Login:**
```
System:   PostgreSQL
Server:   db
Username: admin
Password: admin123
Database: adaptive_learning

---
