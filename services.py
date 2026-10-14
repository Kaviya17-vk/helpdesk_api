from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models
import schemas

VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH", "CRITICAL"}
VALID_STATUSES = {"OPEN", "IN_PROGRESS", "RESOLVED", "CLOSED"}

# Valid Workflow States configuration rules definition
VALID_TRANSITIONS = {
    "OPEN": {"IN_PROGRESS", "RESOLVED", "CLOSED"},
    "IN_PROGRESS": {"RESOLVED", "CLOSED"},
    "RESOLVED": {"CLOSED"},
    "CLOSED": set()  # Modification block parameters activated
}

def validate_user_exists(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def validate_ticket_exists(db: Session, ticket_id: int):
    ticket = db.query(models.Ticket).filter(models.Ticket.id == ticket_id).first()
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return ticket

def check_closed_ticket(ticket: models.Ticket):
    if ticket.status == "CLOSED":
        raise HTTPException(status_code=400, detail="Closed tickets cannot be modified or receive comments")
