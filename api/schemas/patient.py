import json # necessary?

import numpy as np  # necessary?
from pydantic import BaseModel
from typing import List, Optional

from model.patient import Patient


class PatientSchema(BaseModel):
    """
    Schema that defines how a patient's medical diagnosis data should be represented.

    Attributes:
        name (str): The name of the patient.
        concave_points_worst (float): Largest (mean of the three largest values) number of concave portions.
        perimeter_worst (float): Largest (mean of the three largest values) perimeter of the cell nucleus.
        concave_points_mean (float): Mean number of concave portions of the contour.
        radius_worst (float): Largest (mean of the three largest values) radius of the cell nucleus.
        perimeter_mean (float): Mean perimeter of the cell nucleus.
        area_worst (float): Largest (mean of the three largest values) area of the cell nucleus.
        radius_mean (float): Mean of distances from center to points on the perimeter.
        area_mean (float): Mean area of the cell nucleus.
    """
    name: str = "Maria"
    concave_points_worst: float = 0.2654
    perimeter_worst: float = 184.6
    concave_points_mean: float = 0.1471
    radius_worst: float = 25.38
    perimeter_mean: float = 122.8
    area_worst: float = 2019.0
    radius_mean: float = 17.99
    area_mean: float = 1001.0


class PatientViewSchema(BaseModel):
    """
    Schema that defines how a patient's details will be returned.

    Attributes:
        id (int): The unique identifier of the patient.
        name (str): The name of the patient.
        concave_points_worst (float): Largest (mean of the three largest values) number of concave portions.
        perimeter_worst (float): Largest (mean of the three largest values) perimeter of the cell nucleus.
        concave_points_mean (float): Mean number of concave portions of the contour.
        radius_worst (float): Largest (mean of the three largest values) radius of the cell nucleus.
        perimeter_mean (float): Mean perimeter of the cell nucleus.
        area_worst (float): Largest (mean of the three largest values) area of the cell nucleus.
        radius_mean (float): Mean of distances from center to points on the perimeter.
        area_mean (float): Mean area of the cell nucleus.
        diagnosis (Optional[int]): The diagnostic outcome (e.g., 0 or 1, can be None).
    """
    id: int = 1
    name: str = "Maria"
    concave_points_worst: float = 0.2654
    perimeter_worst: float = 184.6
    concave_points_mean: float = 0.1471
    radius_worst: float = 25.38
    perimeter_mean: float = 122.8
    area_worst: float = 2019.0
    radius_mean: float = 17.99
    area_mean: float = 1001.0
    diagnosis: int = None


class PatientSearchSchema(BaseModel):
    """
    Schema that defines how a search for a patient is represented.

    The search is based on the patient's name.

    Attributes:
        name (str): The name of the patient to search for.
    """
    name: str = "Maria"


class PatientListSchema(BaseModel):
    """
    Schema that defines how a list of patients is represented.

    Attributes:
        patients (List[PatientSchema]): A list of patient representations.
    """
    patients: List[PatientSchema]


class PatientDeleteSchema(BaseModel):
    """
    Schema that defines how a patient for deletion is represented.

    Attributes:
        name (str): The name of the patient to be deleted.
    """
    name: str = "Maria"


def present_patient(patient: Patient) -> dict:
    """
    Returns a dictionary representation of a patient following the PatientViewSchema.

    Args:
        patient (Patient): A Patient object containing patient information.

    Returns:
        dict: A dictionary containing the patient's details formatted as per PatientViewSchema.
    """
    return {
        "id": patient.id,
        "name": patient.name,
        "concave_points_worst": patient.concave_points_worst,
        "perimeter_worst": patient.perimeter_worst,
        "concave_points_mean": patient.concave_points_mean,
        "radius_worst": patient.radius_worst,
        "perimeter_mean": patient.perimeter_mean,
        "area_worst": patient.area_worst,
        "radius_mean": patient.radius_mean,
        "area_mean": patient.area_mean,
        "diagnosis": patient.diagnosis
    }


def present_patients(patients: List[Patient]) -> dict:
    """
    Returns a dictionary representation of a list of patients following the PatientViewSchema.

    Args:
        patients (List[Patient]): A list of Patient objects containing patient information.

    Returns:
        dict: A dictionary with a key "patients", containing a list of patient details.
    """
    result = []
    for patient in patients:
        result.append({
            "id": patient.id,
            "name": patient.name,
            "concave_points_worst": patient.concave_points_worst,
            "perimeter_worst": patient.perimeter_worst,
            "concave_points_mean": patient.concave_points_mean,
            "radius_worst": patient.radius_worst,
            "perimeter_mean": patient.perimeter_mean,
            "area_worst": patient.area_worst,
            "radius_mean": patient.radius_mean,
            "area_mean": patient.area_mean,
            "diagnosis": patient.diagnosis
        })

    return {"patients": result}