from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from data_process import initial_processing, boolean_algebra_tool
from data_retrieval import retrieve_all_runs, retrieve_one_run
from data_delete import delete_run


app = FastAPI()

# Define the data model
class AnalysisRunRequest(BaseModel):
    url: str


# A POST to create an analysis run
@app.post("/runs")
async def create_run(request: AnalysisRunRequest):
    interest_genes_1, interest_genes_2 = initial_processing()
    run_id = boolean_algebra_tool(interest_genes_1, interest_genes_2)
    # print(f"Analysis run completed. Run ID: {run_id}")
    # Return the run_id in the response
    return {"run_id": run_id, "status": "complete"}


# A GET (on run ID) to get Run status & results
@app.get("/runs/{run_id}")
async def get_run_status(run_id: str):
    status = retrieve_one_run(run_id)
    if status is None:
        raise HTTPException(status_code=404, detail="Run not found")
    return status


# A GET to retrieve all analysis runs
@app.get("/runs")
async def get_all_runs():
    # Implement logic to retrieve all analysis runs
    runs = retrieve_all_runs()
    return runs


# A DELETE (on run ID) to remove a Run
@app.delete("/runs/{run_id}")
async def cancel_run(run_id: str):
    """
    Endpoint to delete a specific analysis run.
    """
    success = delete_run(run_id)
    if not success:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": run_id, "deleted": success}


# A GET to the home page
@app.get("/")
async def home_page():
    return {"Welcome!"}



# CORS configuration for frontend communication
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
