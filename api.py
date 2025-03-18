from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from main import process_artifact

app = FastAPI()

class ArtifactInput(BaseModel):
    code: str

@app.post("/process_artifact/")
async def process_artifact_endpoint(data: ArtifactInput):
    try:
        response = process_artifact(data.code)
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "Artifact Processing API is running! New version"}