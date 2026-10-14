from sqlalchemy.orm import Session
import models
import schemas
from services import (
    VALID_PRIORITIES, VALID_STATUSES, VALID_TRANSITIONS,
    validate_user_exists, validate_ticket_exists, check_closed_ticket
)
from fastapi import HTTPException, status

# --- USER OPERATIONS ---
def create_user(db: Session, user: schemas.UserCreate):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Duplicate user email is not allowed")
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- TICKET OPERATIONS ---
def create_ticket(db: Session, ticket: schemas.TicketCreate):
    validate_user_exists(db, ticket.user_id)
    if ticket.priority not in VALID_PRIORITIES:
        raise HTTPException(status_code=422, detail=f"Priority must be one of {VALID_PRIORITIES}")
    
    db_ticket = models.Ticket(**ticket.dict(), status="OPEN")
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    return db_ticket

def get_tickets(db: Session, status_filter: str = None, priority_filter: str = None, assigned_to_filter: int = None, page: int = 1, limit: int = 10):
    query = db.query(models.Ticket)
    
    # Conditional Filtering logic
    if status_filter:
        query = query.filter(models.Ticket.status == status_filter)
    if priority_filter:
        query = query.filter(models.Ticket.priority == priority_filter)
    if assigned_to_filter:
        query = query.filter(models.Ticket.assigned_to == assigned_to_filter)
        
    total = query.count()
    offset = (page - 1) * limit
    tickets = query.offset(offset).limit(limit).all()
    
    return {"page": page, "limit": limit, "total": total, "tickets": tickets}

def assign_ticket(db: Session, ticket_id: int, employee_id: int):
    ticket = validate_ticket_exists(db, ticket_id)
    check_closed_ticket(ticket)
    validate_user_exists(db, employee_id)
    
    ticket.assigned_to = employee_id
    db.commit()
    db.refresh(ticket)
    return ticket

def update_ticket_status(db: Session, ticket_id: int, status_update: str):
    ticket = validate_ticket_exists(db, ticket_id)
    
    if status_update not in VALID_STATUSES:
        raise HTTPException(status_code=422, detail="Invalid status value")
        
    current_status = ticket.status
    if status_update != current_status:
        if status_update not in VALID_TRANSITIONS.get(current_status, set()):
            raise HTTPException(status_code=400, detail=f"Invalid status transition from {current_status} to {status_update}")
            
    ticket.status = status_update
    db.commit()
    db.refresh(ticket)
    return ticket

def update_ticket_priority(db: Session, ticket_id: int, priority_update: str):
    ticket = validate_ticket_exists(db, ticket_id)
    check_closed_ticket(ticket)
    
    if priority_update not in VALID_PRIORITIES:
        raise HTTPException(status_code=422, detail="Invalid priority value")
        
    ticket.priority = priority_update
    db.commit()
    db.refresh(ticket)
    return ticket

# --- COMMENT OPERATIONS ---
def add_comment(db: Session, ticket_id: int, comment_data: schemas.CommentCreate):
    ticket = validate_ticket_exists(db, ticket_id)
    check_closed_ticket(ticket)
    validate_user_exists(db, comment_data.user_id)
    
    db_comment = models.TicketComment(ticket_id=ticket_id, **comment_data.dict())
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments(db: Session, ticket_id: int):
    validate_ticket_exists(db, ticket_id)
    return db.query(models.TicketComment).filter(models.TicketComment.ticket_id == ticket_id).all()

# --- SUMMARY CALCULATION ---
def get_ticket_summary(db: Session):
    total = db.query(models.Ticket).count()
    open_count = db.query(models.Ticket).filter(models.Ticket.status == "OPEN").count()
    in_progress = db.query(models.Ticket).filter(models.Ticket.status == "IN_PROGRESS").count()
    resolved = db.query(models.Ticket).filter(models.Ticket.status == "RESOLVED").count()
    closed = db.query(models.Ticket).filter(models.Ticket.status == "CLOSED").count()
    critical = db.query(models.Ticket).filter(models.Ticket.priority == "CRITICAL").count()
    
    return {
        "total_tickets": total,
        "open": open_count,
        "in_progress": in_progress,
        "resolved": resolved,
        "closed": closed,
        "critical": critical
    }
