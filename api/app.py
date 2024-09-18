from flask import redirect, request
from flask_cors import CORS
from flask_openapi3 import Info, OpenAPI, Tag
from urllib.parse import unquote

from logger import logger
from model import *
from schemas import *

# Initialize the Flask app and OpenAPI
info = Info(title="My API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Define tags for route grouping
home_tag = Tag(name="Documentation", description="Documentation selection: Swagger, Redoc, or RapiDoc")
patient_tag = Tag(name="Patient", description="Add, view, remove, and predict patients with breast cancer")

class PatientService:
    """Service class to handle patient-related operations."""

    def __init__(self):
        """Initialize the PatientService with a database session and ML model."""
        self.session = Session()
        self.model_path = './machine_learning/pipelines/svc_breast_cancer_pipeline.pkl'
        self.pipeline = Pipeline.load_pipeline(self.model_path)

    def add_patient(self, form: PatientSchema):
        """Add a new patient to the database.

        Args:
            form (PatientSchema): Patient data from the request form.

        Returns:
            tuple: Response dictionary and HTTP status code.
        """
        X_input = PreProcessor.prepare_form(form)
        diagnosis = int(Model.perform_prediction(self.pipeline, X_input)[0])

        patient = Patient(
            name=form.name,
            concave_points_worst=form.concave_points_worst,
            perimeter_worst=form.perimeter_worst,
            concave_points_mean=form.concave_points_mean,
            radius_worst=form.radius_worst,
            perimeter_mean=form.perimeter_mean,
            area_worst=form.area_worst,
            radius_mean=form.radius_mean,
            area_mean=form.area_mean,
            diagnosis=diagnosis
        )
        logger.debug(f"Adding patient with name: '{patient.name}'")

        try:
            if self.session.query(Patient).filter(Patient.name == form.name).first():
                error_msg = "Patient already exists in the database :/"
                logger.warning(f"Error adding patient '{patient.name}': {error_msg}")
                return {"message": error_msg}, 409

            self.session.add(patient)
            self.session.commit()
            logger.debug(f"Added patient with name: '{patient.name}'")
            return present_patient(patient), 200

        except Exception as e:
            error_msg = f"Unable to save the new item: {str(e)}"
            logger.warning(f"Error adding patient '{patient.name}': {error_msg}")
            return {"message": error_msg}, 400

    def get_patient(self, name: str):
        """Retrieve a patient from the database by name.

        Args:
            name (str): The name of the patient to retrieve.

        Returns:
            tuple: Response dictionary and HTTP status code.
        """
        patient = self.session.query(Patient).filter(Patient.name == name).first()
        if not patient:
            error_msg = f"Patient {name} not found in the database :/"
            logger.warning(f"Error searching for patient '{name}': {error_msg}")
            return {"message": error_msg}, 404

        logger.debug(f"Patient found: '{patient.name}'")
        return present_patient(patient), 200

    def delete_patient(self, name: str):
        """Delete a patient from the database by name.

        Args:
            name (str): The name of the patient to delete.

        Returns:
            tuple: Response dictionary and HTTP status code.
        """
        patient_name = unquote(name)
        logger.debug(f"Deleting data for patient #{patient_name}")

        patient = self.session.query(Patient).filter(Patient.name == patient_name).first()
        if not patient:
            error_msg = "Patient not found in the database :/"
            logger.warning(f"Error deleting patient '{patient_name}': {error_msg}")
            return {"message": error_msg}, 404

        self.session.delete(patient)
        self.session.commit()
        logger.debug(f"Deleted patient #{patient_name}")
        return {"message": f"Patient {patient_name} removed successfully!"}, 200

# Instantiate the service class
patient_service = PatientService()

@app.get('/', tags=[home_tag])
def home():
    """Redirects to /openapi, the page that allows selecting the documentation style."""
    return redirect('/openapi')

@app.get('/patients', tags=[patient_tag],
         responses={"200": PatientViewSchema, "404": ErrorSchema})
def get_patients():
    """Lists all patients registered in the database.

    Returns:
        tuple: Response dictionary and HTTP status code.
    """
    logger.debug("Fetching data about all patients")
    try:
        patients = patient_service.session.query(Patient).all()
        if not patients:
            return {"patients": []}, 200
        logger.debug(f"{len(patients)} patients found")
        return present_patients(patients), 200
    except Exception as e:
        error_msg = f"Unable to fetch patients: {str(e)}"
        logger.warning(f"Error fetching patients: {error_msg}")
        return {"message": error_msg}, 400

@app.post('/patient', tags=[patient_tag],
          responses={"200": PatientViewSchema, "400": ErrorSchema, "409": ErrorSchema})
def add_patient(form: PatientSchema):
    """Adds a new patient to the database.

    Args:
        form (PatientSchema): Patient data from the request form.

    Returns:
        tuple: Response dictionary and HTTP status code.
    """
    return patient_service.add_patient(form)

@app.route('/patient_streamlit', methods=['POST'])
def add_patient_streamlit():
    """Adds a new patient to the database from Streamlit.

    Returns:
        tuple: Response dictionary and HTTP status code.
    """
    data = request.json
    try:
        form = PatientSchema(**data)
    except Exception as e:
        error_msg = f"Invalid input: {str(e)}"
        logger.warning(f"Error adding patient: {error_msg}")
        return {"message": error_msg}, 400

    return patient_service.add_patient(form)

@app.get('/patient', tags=[patient_tag],
         responses={"200": PatientViewSchema, "404": ErrorSchema})
def get_patient(query: PatientSearchSchema):
    """Searches for a registered patient in the database by name.

    Args:
        query (PatientSearchSchema): Patient search query with name.

    Returns:
        tuple: Response dictionary and HTTP status code.
    """
    return patient_service.get_patient(query.name)

@app.delete('/patient', tags=[patient_tag],
            responses={"200": ErrorSchema, "404": ErrorSchema})
def delete_patient(query: PatientSearchSchema):
    """Removes a registered patient from the database by name.

    Args:
        query (PatientSearchSchema): Patient search query with name.

    Returns:
        tuple: Response dictionary and HTTP status code.
    """
    return patient_service.delete_patient(query.name)

if __name__ == '__main__':
    app.run(debug=True)