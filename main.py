from fastapi import FastAPI, HTTPException, Request, Header, Depends, UploadFile, File
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
import os
from dotenv import load_dotenv
import json

load_dotenv()

app = FastAPI(
    title="AnchorScore API",
    description="Score and assess risk levels for companies using AI systems.",
    version="0.1.0"
)

# Optional: API Key security for endpoints
API_KEY = os.getenv("ANCHORSCORE_API_KEY", "changeme")

def verify_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

# Input data model for scoring
class ScoreInput(BaseModel):
    name: str = Field(..., example="Sample Org")
    sector: str = Field(..., example="Finance")
    annual_revenue: float = Field(..., gt=0, example=1_000_000)
    ai_usage_level: int = Field(..., ge=0, le=10, example=7)

# Output model for response
class ScoreOutput(BaseModel):
    name: str
    score: float
    risk_level: str

@app.post(
    "/score",
    response_model=ScoreOutput,
    dependencies=[Depends(verify_api_key)],
    tags=["Scoring"],
    summary="Score company AI risk"
)
async def score_endpoint(input_data: ScoreInput):
    """
    Calculates a basic AI risk score based on usage level and revenue.
    """
    base_score = 100 - (input_data.ai_usage_level * 5)
    risk_level = "Low" if base_score > 70 else "Medium" if base_score > 40 else "High"

    return ScoreOutput(
        name=input_data.name,
        score=round(base_score, 2),
        risk_level=risk_level
    )

# =====================
# Upload Endpoint
# =====================
@app.post("/upload", tags=["Ingestion"])
async def upload_file(file: UploadFile = File(...), x_api_key: str = Depends(verify_api_key)):
    if file.content_type not in ["application/json", "application/jsonl", "text/csv"]:
        raise HTTPException(status_code=415, detail="Unsupported file type")

    content = await file.read()
    filename = file.filename

    try:
        if file.content_type == "application/json":
            data = json.loads(content)
            count = len(data) if isinstance(data, list) else 1
        elif file.content_type == "application/jsonl":
            lines = content.decode().splitlines()
            count = len(lines)
        elif file.content_type == "text/csv":
            count = len(content.decode().splitlines()) - 1
        else:
            count = 0

        return {
            "filename": filename,
            "records_received": count,
            "status": "Accepted"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse: {str(e)}")

# =====================
# Data Ingest Endpoint
# =====================
class Record(BaseModel):
    name: str
    sector: str
    annual_revenue: float
    ai_usage_level: int

@app.post("/data", tags=["Ingestion"])
async def ingest_data(records: list[Record], x_api_key: str = Depends(verify_api_key)):
    count = len(records)
    return {"message": f"{count} records received"}

@app.get("/", tags=["Health"], summary="Health check")
def health_check():
    return {"status": "AnchorScore API is up"}
