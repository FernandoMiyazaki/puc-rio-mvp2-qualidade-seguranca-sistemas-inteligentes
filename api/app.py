from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError

from model import *
from logger import logger
from schemas import *
from flask_cors import CORS

# Initialize the OpenAPI object
info = Info(title="My API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Define tags for route grouping
home_tag = Tag(name="Documentation", description="Documentation selection: Swagger, Redoc, or RapiDoc")
patient_tag = Tag(name="Patient", description="Add, view, remove, and predict patients with breast cancer")


# Home route
@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi, the page that allows selecting the documentation style."""
    return redirect('/openapi')


# Route for listing patients
@app.get('/patients', tags=[patient_tag],
         responses={"200": PatientViewSchema, "404": ErrorSchema})
def get_patients():
    """Lists all patients registered in the database.

    Returns:
        list: List of registered patients
    """
    logger.debug("Fetching data about all patients")
    # Create a database session
    session = Session()
    # Query all patients
    patients = session.query(Patient).all()
    
    if not patients:
        # No patients found
        return {"patients": []}, 200
    else:
        logger.debug(f"{len(patients)} patients found")
        return present_patients(patients), 200


# Route for adding a patient
@app.post('/patient', tags=[patient_tag],
          responses={"200": PatientViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def add_patient(form: PatientSchema):
    """Adds a new patient to the database and returns a representation of the patient and associated diagnosis.

    Args:
        form (PatientSchema): Patient data

    Returns:
        dict: Representation of the patient and associated diagnosis
    """
    # Extract data from the form
    name = form.name
    concave_points_worst = form.concave_points_worst
    perimeter_worst = form.perimeter_worst
    concave_points_mean = form.concave_points_mean
    radius_worst = form.radius_worst
    perimeter_mean = form.perimeter_mean
    area_worst = form.area_worst
    radius_mean = form.radius_mean
    area_mean = form.area_mean
        
    # Prepare data for the model
    X_input = PreProcessor.prepare_form(form)
    # Load the model
    model_path = './MachineLearning/pipelines/rf_diabetes_pipeline.pkl'
    pipeline = Pipeline.load_pipeline(model_path)
    # Make prediction
    diagnosis = int(Model.predict(pipeline, X_input)[0])
    
    patient = Patient(
        name=name,
        concave_points_worst=concave_points_worst,
        perimeter_worst=perimeter_worst,
        concave_points_mean=concave_points_mean,
        radius_worst=radius_worst,
        perimeter_mean=perimeter_mean,
        area_worst=area_worst,
        radius_mean=radius_mean,
        area_mean=area_mean,
        diagnosis=diagnosis
    )
    logger.debug(f"Adding patient with name: '{patient.name}'")
    
    try:
        # Create a database session
        session = Session()
        
        # Check if the patient already exists
        if session.query(Patient).filter(Patient.name == form.name).first():
            error_msg = "Patient already exists in the database :/"
            logger.warning(f"Error adding patient '{patient.name}': {error_msg}")
            return {"message": error_msg}, 409
        
        # Add patient
        session.add(patient)
        # Commit the transaction
        session.commit()
        logger.debug(f"Added patient with name: '{patient.name}'")
        return present_patient(patient), 200
    
    except Exception as e:
        error_msg = "Unable to save the new item :/"
        logger.warning(f"Error adding patient '{patient.name}': {error_msg}")
        return {"message": error_msg}, 400
    

# Route for searching a patient by name
@app.get('/patient', tags=[patient_tag],
         responses={"200": PatientViewSchema, "404": ErrorSchema})
def get_patient(query: PatientSearchSchema):
    """Searches for a registered patient in the database by name.

    Args:
        query (PatientSearchSchema): Patient search query with name

    Returns:
        dict: Representation of the patient and associated diagnosis
    """
    patient_name = query.name
    logger.debug(f"Fetching data for patient #{patient_name}")
    # Create a database session
    session = Session()
    # Search for the patient
    patient = session.query(Patient).filter(Patient.name == patient_name).first()
    
    if not patient:
        # Patient not found
        error_msg = f"Patient {patient_name} not found in the database :/"
        logger.warning(f"Error searching for patient '{patient_name}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Patient found: '{patient.name}'")
        # Return patient representation
        return present_patient(patient), 200


# Route for deleting a patient by name
@app.delete('/patient', tags=[patient_tag],
            responses={"200": PatientViewSchema, "404": ErrorSchema})
def delete_patient(query: PatientSearchSchema):
    """Removes a registered patient from the database by name.

    Args:
        query (PatientSearchSchema): Patient search query with name

    Returns:
        dict: Success or error message
    """
    patient_name = unquote(query.name)
    logger.debug(f"Deleting data for patient #{patient_name}")
    
    # Create a database session
    session = Session()
    
    # Search for the patient
    patient = session.query(Patient).filter(Patient.name == patient_name).first()
    
    if not patient:
        error_msg = "Patient not found in the database :/"
        logger.warning(f"Error deleting patient '{patient_name}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        session.delete(patient)
        session.commit()
        logger.debug(f"Deleted patient #{patient_name}")
        return {"message": f"Patient {patient_name} removed successfully!"}, 200
    
if __name__ == '__main__':
    app.run(debug=True)