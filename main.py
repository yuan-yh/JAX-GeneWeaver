# @app.get("/hello")
# async def welcome():
#     return "Welcome ;)"
#
# @app.get("/")
# async def home_page():
#     return "This is the GW-API Home Page."

from fastapi import FastAPI, HTTPException
from models.preprocessed_gene_data import PreprocessedGeneData
from utils.boolean_algebra_analysis import perform_boolean_algebra_intersection
from run_management import run_manager, AnalysisRun
from uuid import UUID

app = FastAPI()

@app.post("/analysis_run/")
async def create_analysis_run(gene_data: PreprocessedGeneData):
    run_id = run_manager.create_run(gene_data)
    return {"run_id": str(run_id)}

@app.get("/analysis_runs/")
async def get_all_runs():
    runs = run_manager.get_all_runs()
    return {"runs": [{str(run.id): run.status} for run in runs]}

@app.get("/analysis_run/{run_id}/")
async def get_run_status(run_id: UUID):
    run = run_manager.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Run not found")
    return {"run_id": str(run_id), "status": run.status, "result": run.result}

@app.delete("/analysis_run/{run_id}/")
async def delete_run(run_id: UUID):
    if run_manager.delete_run(run_id):
        return {"message": "Run cancelled"}
    else:
        raise HTTPException(status_code=404, detail="Run not found")

# Run the server with: uvicorn main:app --reload
