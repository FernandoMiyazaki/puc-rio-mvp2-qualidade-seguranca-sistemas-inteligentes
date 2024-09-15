import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

# Importing model elements
from model.base import Base
from model.patient import Patient
from model.model import Model
from model.pipeline import Pipeline
from model.preprocessor import PreProcessor
from model.evaluator import Evaluator
from model.loader import Loader

# Define the database path
DB_PATH = "database/"
DB_FILE = "patients.sqlite3"
DB_URL = f'sqlite:///{DB_PATH}{DB_FILE}'

# Ensure the database directory exists
if not os.path.exists(DB_PATH):
    os.makedirs(DB_PATH)

# Create the database engine
engine = create_engine(DB_URL, echo=False)

# Create a session maker bound to the engine
Session = sessionmaker(bind=engine)

# Create the database if it doesn't exist
if not database_exists(engine.url):
    create_database(engine.url)

# Create all tables in the database (if they don't exist)
Base.metadata.create_all(engine)