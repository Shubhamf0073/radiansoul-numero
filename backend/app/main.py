# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import name_analysis, loshu_grid, profession_analysis_report

app = FastAPI(
    title="Numerology API",
    description="Backend for Chandlean Numerology Analysis",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(name_analysis.router)
app.include_router(loshu_grid.router)
app.include_router(profession_analysis_report.router)

@app.get("/")
def root():
    return {"message": "Numerology API is running"}