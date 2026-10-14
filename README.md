# Helpdesk Ticket Management System API

A professional, enterprise-grade REST API built with **FastAPI**, **SQLAlchemy ORM**, **SQLite**, and **Pydantic V2**. This system handles user registration, automated incident ticket flows, strict business state-machine status transitions, and dynamic data filtering with pagination.

---

## 🚀 Features & Business Logic Implemented

### 1. Database Architecture & Relationships
* **Users Table:** Handles user records and strict duplicate email detection.
* **Tickets Table:** Manages ticket details linked securely via foreign keys to the original reporter (`user_id`) and assigned agent (`assigned_to`).
* **Comments Table:** Implements cascade deletion constraints linked directly to the parent ticket.

### 2. Guardrails & Validation Strict Rules
* **Automatic Initialization:** Every created ticket defaults immediately to the `OPEN` state.
* **State Machine Validation:** Strict transition routes allowed:
  * `OPEN` ➔ `IN_PROGRESS` | `RESOLVED` | `CLOSED`
  * `IN_PROGRESS` ➔ `RESOLVED` | `CLOSED`
  * `RESOLVED` ➔ `CLOSED`
  * *Illegal modifications backwards (e.g., `CLOSED` ➔ `OPEN` or `IN_PROGRESS` ➔ `OPEN`) are instantly blocked with a `400 Bad Request` error.*
* **Immutable Lockdowns:** Once a ticket transitions to `CLOSED`, its priority cannot be modified, and it is blocked from receiving any new comments.
* **Sanity Checks:** Blocks text operations on empty strings and flags assignment attempts to non-existing database user accounts.

### 3. Querying & Performance Filters
* Supports comprehensive multidimensional criteria logic queries (e.g., `/tickets?status=OPEN&priority=HIGH`).
* Integrated structured numerical cursor pagination (`page` and `limit`) with meta metrics.

---

## 🛠️ Tech Stack Used
* **Backend Framework:** FastAPI (Python 3.10+)
* **Database Layer:** SQLAlchemy Object Relational Mapper
* **Data Sanitization Engine:** Pydantic V2
* **Server Runner:** Uvicorn ASGI

---

## ⚙️ How to Set Up and Run locally

### 1. Install Project Dependencies
Run this command in your project root terminal folder to configure requirements:
```bash
pip install -r requirements.txt
```

### 2. Launch the Local Uvicorn Server
Execute the application entry runner file:
```bash
uvicorn main:app --reload
```
Once ignited, your live local server thread maps directly to: `http://127.0.0.1:8000`

### 3. Open Interactive Swagger API Docs
Navigate directly inside any web browser to view, test, and authenticate endpoints:
👉 **`http://127.0.0`**

---

## 📁 System Folder Directory Layout
```text
helpdesk_api/
│
├── main.py              # Application Entry point & API Initialization
├── database.py          # Session Manager Configuration
├── models.py            # SQLAlchemy Enterprise Database Schemas
├── schemas.py           # Pydantic V2 Integrity Serialization Rules
├── crud.py              # Raw Database Operations
├── services.py          # Guardrail Validations Engine
├── requirements.txt     # Global Application Core Packages Dependency Map
├── README.md            # Project Implementation Architecture Document
└── routers/
    ├── users.py         # Registration Processing Sub-Router Routing Hooks
    ├── tickets.py       # Workflow Operation & Processing Engine Hooks
    └── comments.py      # Conversation Ledger Data Processing Modules
```

---

## 📊 Live System Validation Evaluation Verification

All mandatory testing matrix parameters specified within the assignment manual have been verified successfully via Swagger UI:
* ✅ User Creation & Duplicate Prevention Validation Check
* ✅ Ticket Status Valid Transition Processing Checks
* ✅ Illegal Retrograde State Modification Interception Blocks
* ✅ Post-Closure Lockdown Immutable Data Block Intercepts
* ✅ Real-time Consolidated Analytics Status Summary Calculation Matrix Counters
