from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils.pipeline import run_reserch_pipeline

app = FastAPI(
    title="Multi-Agent Research API",
    description="AI-powered research pipeline using Search, Scrape, Write and Critic agents.",
    version="1.0.0"
)

# Request body
class ResearchRequest(BaseModel):
    topic: str

# Response body
class ResearchResponse(BaseModel):
    search_results: str
    scraped_content: str
    report: str
    feedback: str


@app.get("/")
def root():
    return {"message": "Multi-Agent Research API is running 🚀"}


@app.post("/research", response_model=ResearchResponse)
def research(request: ResearchRequest):
    if not request.topic.strip():
        raise HTTPException(status_code=400, detail="Topic cannot be empty.")
    
    try:
        result = run_reserch_pipeline(topic=request.topic)
        return ResearchResponse(
            search_results=result["search_results"],
            scraped_content=result["scraped_content"],
            report=result["report"],
            feedback=result["feedback"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))