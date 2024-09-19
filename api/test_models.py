import pytest

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    roc_auc_score
)

from model import Loader, Model, PreProcessor

# Parameters
PATH_DATASET = "./machine_learning/data/test_dataset_breast_cancer.csv"
COLUMNS = [
    'concave_points_worst', 
    'perimeter_worst', 
    'concave_points_mean', 
    'radius_worst', 
    'perimeter_mean', 
    'area_worst', 
    'radius_mean', 
    'area_mean',
    'diagnosis'
]
PATH_MODEL = "./machine_learning/models/svc_breast_cancer_classification.pkl"

# Instantiate objects for loader and model
loader = Loader()
model = Model()
preprocessor = PreProcessor()

@pytest.fixture(scope="module")
def load_data_and_model():
    """Fixture to load dataset and model."""
    # Load dataset
    dataset = loader.load_data(PATH_DATASET, COLUMNS)
    array = dataset.values
    X_test = array[:, :-1]
    y_test = array[:, -1]
    
    # Rescale features
    rescaled_X_test = preprocessor.scale_data(X_test)
    
    # Load model
    loaded_model = model.load_model(PATH_MODEL)
    
    return loaded_model, rescaled_X_test, y_test

def test_model_predictions_binary(load_data_and_model):
    """Test if model predictions are binary (0 or 1)."""
    loaded_model, X_test, _ = load_data_and_model
    y_pred = model.perform_prediction(loaded_model, X_test)

    assert set(y_pred).issubset({0, 1}), "Predictions should be 0 or 1"

def test_predictions_no_nan(load_data_and_model):
    """Test if predictions contain no NaN values.""" 
    loaded_model, X_test, _ = load_data_and_model
    y_pred = model.perform_prediction(loaded_model, X_test)

    assert not np.isnan(y_pred).any(), "Predictions contain NaN values"

def test_confusion_matrix_non_negative(load_data_and_model):
    """Test if confusion matrix values are non-negative.""" 
    loaded_model, X_test, y_test = load_data_and_model
    y_pred = model.perform_prediction(loaded_model, X_test)
    cm = confusion_matrix(y_test, y_pred)

    assert (cm >= 0).all(), "Confusion matrix contains negative values"

def test_predictions_length_matches(load_data_and_model):
    """Test if the number of predictions matches the test data size.""" 
    loaded_model, X_test, y_test = load_data_and_model
    y_pred = model.perform_prediction(loaded_model, X_test)

    assert len(y_pred) == len(y_test), "Number of predictions does not match number of test samples"

def test_model_metrics(load_data_and_model):
    """Test model performance metrics.""" 
    loaded_model, X_test, y_test = load_data_and_model
    y_pred = model.perform_prediction(loaded_model, X_test)
    
    # If the model supports probability predictions
    if hasattr(loaded_model, "predict_proba"):
        y_pred_proba = loaded_model.predict_proba(X_test)[:, 1]
    else:
        # Assuming the model does not have predict_proba method
        y_pred_proba = None
    
    # Evaluate metrics
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred)
    recall = recall_score(y_test, y_pred)

    assert accuracy >= 0.94, f"Accuracy is too low: {accuracy:.2f}"
    assert precision >= 0, "Precision should be non-negative"
    assert recall >= 0, "Recall should be non-negative"

    if y_pred_proba is not None:
        auc = roc_auc_score(y_test, y_pred_proba)
        assert auc >= 0.9, f"AUC score is too low: {auc:.2f}"
    else:
        pytest.skip("Model does not support probability predictions, skipping AUC test.")