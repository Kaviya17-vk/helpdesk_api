from fastapi import FastAPI
import models
from database import engine
from routers import users, tickets, comments

# Compile schema structures directly maps databases engine tables instantly 
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Helpdesk Ticket Management System API",
    description="Advanced API managing user logs, business transitions, metrics, and pagination workflows.",
    version="1.0.0"
)

# Route endpoints register loops mounting
app.include_router(users.router)
app.include_router(tickets.router)
app.include_router(comments.router)

@app.get("/", tags=["Root"])
def root():
    return {"message": "Helpdesk Ticket Management API is up and running. Navigate to /docs for interactive Swagger UI."}
