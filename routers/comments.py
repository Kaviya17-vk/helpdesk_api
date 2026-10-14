from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from database import get_db
import schemas
import crud
from typing import List

router = APIRouter(prefix="/tickets", tags=["Comments"])

@router.post("/{ticket_id}/comments", response_model=schemas.CommentResponse, status_code=status.HTTP_201_CREATED, description="Post text communications safely under an active non-closed target incident record log reference identifier instance.")
def add_comment(ticket_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.add_comment(db=db, ticket_id=ticket_id, comment_data=comment)

@router.get("/{ticket_id}/comments", response_model=List[schemas.CommentResponse], status_code=status.HTTP_200_OK, description="Query chronological commentary data sequence lists efficiently.")
def get_comments(ticket_id: int, db: Session = Depends(get_db)):
    return crud.get_comments(db=db, ticket_id=ticket_id)
