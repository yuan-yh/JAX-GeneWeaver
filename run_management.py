from typing import Dict
from uuid import uuid4, UUID

class AnalysisRun:
    def __init__(self, gene_data, status='pending', result=None):
        self.id = uuid4()
        self.gene_data = gene_data
        self.status = status  # 'pending', 'complete', 'cancelled'
        self.result = result

class RunManager:
    def __init__(self):
        self.runs: Dict[UUID, AnalysisRun] = {}

    def create_run(self, gene_data):
        new_run = AnalysisRun(gene_data)
        self.runs[new_run.id] = new_run
        return new_run.id

    def get_run(self, run_id):
        return self.runs.get(run_id)

    def get_all_runs(self):
        return list(self.runs.values())

    def delete_run(self, run_id):
        if run_id in self.runs:
            self.runs[run_id].status = 'cancelled'
            return True
        return False

run_manager = RunManager()
