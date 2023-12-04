from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Define the path for the database file
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(BASE_DIR, "gw_anlysis_runs.db")

# Create an engine that stores data in the specified file
engine = create_engine(f'sqlite:///{db_path}')

# Base class for our class definitions
Base = declarative_base()

# Define a class which corresponds to the database table 'analysis_runs'
class AnalysisRun(Base):
    __tablename__ = 'analysis_runs'
    id = Column(Integer, primary_key=True)
    run_id = Column(String, unique=True)
    geneset_values = Column(Text)

# Create the table
Base.metadata.create_all(engine)

# Create a sessionmaker, to be used for creating sessions
Session = sessionmaker(bind=engine)
