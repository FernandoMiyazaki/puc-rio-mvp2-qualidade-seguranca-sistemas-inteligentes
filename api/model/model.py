import numpy as np
import pickle
from model.preprocessor import PreProcessor

class Model:
    def __init__(self, model_path: str):
        """
        Initializes the Model class by loading the model from the specified path.
        """
        self.model = self.load_model(model_path)
    
    @staticmethod
    def load_model(path: str):
        """
        Loads the model depending on the file extension. If the file ends with 
        '.pkl', loads it using pickle. Raises an exception for unsupported formats.
        """
        if path.endswith('.pkl'):
            with open(path, 'rb') as file:
                model = pickle.load(file)
        else:
            raise Exception('Unsupported file format')
        return model

    def perform_prediction(self, X_input: np.ndarray):
        """
        Performs a prediction for the input data based on the loaded model.
        
        Args:
            X_input (np.ndarray): Input data for prediction.
            
        Returns:
            The model's prediction.
        """
        diagnosis = self.model.predict(X_input)
        return diagnosis