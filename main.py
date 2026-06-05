from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from database import Base, engine
import models
from students import router

# Automatically create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Management System",
    description="A simple API for managing student records and generating AI feedback.",
    version="1.0.0"
)

# Root endpoint redirects to interactive Swagger documentation
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")

# Include student management routes
app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
