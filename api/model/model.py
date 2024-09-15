import numpy as np
import pickle
import joblib
from model.preprocessor import PreProcessor

class Model:
    
    @staticmethod
    def load_model(path: str):
        """
        Loads the model based on the file extension. Supports .pkl and .joblib formats.

        Args:
            path (str): Path to the model file.

        Returns:
            The loaded model.

        Raises:
            ValueError: If the file format is not supported.
        """
        if path.endswith('.pkl'):
            with open(path, 'rb') as file:
                model = pickle.load(file)
        elif path.endswith('.joblib'):
            model = joblib.load(path)
        else:
            raise ValueError('Unsupported file format. Supported formats: .pkl, .joblib')
        
        return model
    
    @staticmethod
    def perform_prediction(model, X_input: np.ndarray):
        """
        Performs a prediction based on the trained model and input data.

        Args:
            model: Trained model used for prediction.
            X_input (np.ndarray): Input data for prediction.

        Returns:
            Diagnosis result from the model's prediction.
        """
        diagnosis = model.predict(X_input)
        return diagnosis