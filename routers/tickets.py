from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session
from database import get_db
import schemas
import crud
from typing import Optional

router = APIRouter(prefix="/tickets", tags=["Tickets"])

@router.post("/", response_model=schemas.TicketResponse, status_code=status.HTTP_201_CREATED, description="Create new active helpdesk query tickets.")
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    return crud.create_ticket(db=db, ticket=ticket)

@router.get("/", response_model=schemas.PaginatedTicketResponse, status_code=status.HTTP_200_OK, description="Fetch records using dynamic filtering matrix.")
def list_tickets(
    status: Optional[str] = Query(None, description="Filter by status (OPEN, IN_PROGRESS, RESOLVED, CLOSED)"),
    priority: Optional[str] = Query(None, description="Filter by priority (LOW, MEDIUM, HIGH, CRITICAL)"),
    assigned_to: Optional[int] = Query(None, description="Filter by support staff agent ID allocation parameter."),
    page: int = Query(1, ge=1, description="Numerical index value of pages requested."),
    limit: int = Query(10, ge=1, le=100, description="Upper bound limits for dataset results serialization window."),
    db: Session = Depends(get_db)
):
    return crud.get_tickets(db=db, status_filter=status, priority_filter=priority, assigned_to_filter=assigned_to, page=page, limit=limit)

@router.get("/summary", response_model=schemas.TicketSummaryResponse, status_code=status.HTTP_200_OK, description="Provides live computed metrics data aggregations maps safely from tables data counters directly.")
def get_ticket_summary(db: Session = Depends(get_db)):
    return crud.get_ticket_summary(db=db)

@router.put("/{ticket_id}/assign", response_model=schemas.TicketResponse, status_code=status.HTTP_200_OK, description="Assign a specific tracking agent parameter safely.")
def assign_ticket(ticket_id: int, employee_id: int, db: Session = Depends(get_db)):
    return crud.assign_ticket(db=db, ticket_id=ticket_id, employee_id=employee_id)

@router.put("/{ticket_id}/status", response_model=schemas.TicketResponse, status_code=status.HTTP_200_OK, description="Verify state machine changes workflow securely.")
def update_ticket_status(ticket_id: int, status_update: schemas.TicketStatusUpdate, db: Session = Depends(get_db)):
    return crud.update_ticket_status(db=db, ticket_id=ticket_id, status_update=status_update.status)

@router.put("/{ticket_id}/priority", response_model=schemas.TicketResponse, status_code=status.HTTP_200_OK, description="Alter operational response priorities metadata parameters values strings safely.")
def update_ticket_priority(ticket_id: int, priority_update: schemas.TicketPriorityUpdate, db: Session = Depends(get_db)):
    return crud.update_ticket_priority(db=db, ticket_id=ticket_id, priority_update=priority_update.priority)
