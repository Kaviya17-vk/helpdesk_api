from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: str = Field(..., min_length=1)

class UserCreate(UserBase):
    pass

class UserResponse(UserBase):
    id: int
    created_at: datetime

    # Pydantic V2 specific attributes compilation setup mapping 
    model_config = {"from_attributes": True}

# --- COMMENT SCHEMAS ---
class CommentBase(BaseModel):
    comment: str = Field(..., min_length=1)

class CommentCreate(CommentBase):
    user_id: int

class CommentResponse(CommentBase):
    id: int
    ticket_id: int
    user_id: int
    created_at: datetime

    # Pydantic V2 specific attributes compilation setup mapping
    model_config = {"from_attributes": True}

# --- TICKET SCHEMAS ---
class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=5)
    priority: str  # LOW, MEDIUM, HIGH, CRITICAL
    user_id: int

class TicketPriorityUpdate(BaseModel):
    priority: str

class TicketStatusUpdate(BaseModel):
    status: str

class TicketResponse(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    status: str
    user_id: int
    assigned_to: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    # Pydantic V2 specific attributes compilation setup mapping
    model_config = {"from_attributes": True}

class PaginatedTicketResponse(BaseModel):
    page: int
    limit: int
    total: int
    tickets: List[TicketResponse]

class TicketSummaryResponse(BaseModel):
    total_tickets: int
    open: int
    in_progress: int
    resolved: int
    closed: int
    critical: int
