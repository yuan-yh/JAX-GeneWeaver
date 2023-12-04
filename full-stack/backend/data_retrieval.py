from data_base import AnalysisRun, Session


def retrieve_all_runs():
    """
    Retrieves all analysis runs from the database.
    Returns a list of dictionaries, each containing run_id and other details.
    """
    session = Session()
    try:
        # Query the database to get all analysis runs
        runs = session.query(AnalysisRun).all()

        # Convert the SQLAlchemy objects to dictionaries
        runs_list = [{"run_id": run.run_id, "status": "complete"} for run in runs]

    finally:
        session.close()

    return runs_list


def retrieve_one_run(run_id: str):
    """
    Retrieves the status of a specific analysis run from the database.
    """
    session = Session()
    try:
        # Query the database for the specific run
        run = session.query(AnalysisRun).filter_by(run_id=run_id).first()

        if run:
            run_status = {"run_id": run.run_id, "status": "complete", "geneset_values": run.geneset_values}
        else:
            run_status = None

    finally:
        session.close()

    return run_status


# Example usage
# runs = retrieve_all_runs()
# print(f"All Analysis runs: \n{runs}")
#
# run = retrieve_one_run('2d6fa50a-5853-45b3-b818-da8134d59c25')
# print(f"One Analysis run: \n{run}")