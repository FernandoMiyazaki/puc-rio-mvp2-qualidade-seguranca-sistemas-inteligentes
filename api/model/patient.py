from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from model.base import Base


class Patient(Base):
    __tablename__ = 'patients'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    concave_points_worst = Column(Float)
    perimeter_worst = Column(Float)
    concave_points_mean = Column(Float)
    radius_worst = Column(Float)
    perimeter_mean = Column(Float)
    area_worst = Column(Float)
    radius_mean = Column(Float)
    area_mean = Column(Float)
    diagnosis = Column(Integer, nullable=True)
    insertion_date = Column(DateTime, default=datetime.now)

    def __init__(
        self, 
        name: str,
        concave_points_worst: float,
        perimeter_worst: float,
        concave_points_mean: float,
        radius_worst: float,
        perimeter_mean: float,
        area_worst: float,
        radius_mean: float,
        area_mean: float,
        diagnosis: Union[int, None] = None,
        insertion_date: Union[DateTime, None] = None
    ):
        """
        Creates a Patient object.

        Arguments:
            name: Patient's name.
            concave_points_worst: Worst concave points measurement.
            perimeter_worst: Worst perimeter measurement.
            concave_points_mean: Mean concave points measurement.
            radius_worst: Worst radius measurement.
            perimeter_mean: Mean perimeter measurement.
            area_worst: Worst area measurement.
            radius_mean: Mean radius measurement.
            area_mean: Mean area measurement.
            diagnosis: Diagnostic result (e.g., positive/negative for a condition).
            insertion_date: Date when the patient was added to the database.
        """
        self.name = name
        self.concave_points_worst = concave_points_worst
        self.perimeter_worst = perimeter_worst
        self.concave_points_mean = concave_points_mean
        self.radius_worst = radius_worst
        self.perimeter_mean = perimeter_mean
        self.area_worst = area_worst
        self.radius_mean = radius_mean
        self.area_mean = area_mean
        self.diagnosis = diagnosis

        # Set the current date/time if no insertion date is provided.
        if insertion_date is None:
            insertion_date = datetime.now()
        self.insertion_date = insertion_date