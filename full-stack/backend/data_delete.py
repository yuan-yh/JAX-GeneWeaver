from data_base import AnalysisRun, Session


def delete_run(run_id: str):
    """
    Deletes a specific analysis run from the database based on the run_id.
    """
    session = Session()
    try:
        # Attempt to find the run with the given run_id
        run = session.query(AnalysisRun).filter_by(run_id=run_id).first()

        if run:
            # If found, delete the run and commit the changes
            session.delete(run)
            session.commit()
            success = True
        else:
            success = False  # Run not found

    except Exception as e:
        # Handle any exceptions that occur
        print(f"Error occurred: {e}")
        success = False

    finally:
        session.close()

    return success
