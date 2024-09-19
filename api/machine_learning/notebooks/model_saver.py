import pickle

import pandas as pd


class ModelSaver:
    """
    A class for saving models, scalers, pipelines, and test data to disk.
    """

    @staticmethod
    def save_model(model, filename):
        """
        Save a trained model to a file.

        Parameters:
        model: The model to be saved.
        filename (str): The name of the file where the model will be saved.
        """
        file_path = f"../models/{filename}"
        with open(file_path, 'wb') as file:
            pickle.dump(model, file)

    @staticmethod
    def save_scaler(scaler, filename):
        """
        Save a scaler to a file.

        Parameters:
        scaler: The scaler to be saved.
        filename (str): The name of the file where the scaler will be saved.
        """
        file_path = f"../scalers/{filename}"
        with open(file_path, 'wb') as file:
            pickle.dump(scaler, file)

    @staticmethod
    def save_pipeline(pipeline, filename):
        """
        Save a pipeline to a file.

        Parameters:
        pipeline: The pipeline to be saved.
        filename (str): The name of the file where the pipeline will be saved.
        """
        file_path = f"../pipelines/{filename}"
        with open(file_path, 'wb') as file:
            pickle.dump(pipeline, file)

    @staticmethod
    def save_test_data(X_test, y_test, df):
        """
        Save the test data to CSV files.

        Parameters:
        X_test (array-like): The feature test data.
        y_test (array-like): The target test data.
        df (DataFrame): The DataFrame used to derive column names for X_test and y_test.
        """
        X_test_df = pd.DataFrame(X_test, columns=df.columns[:-1])
        y_test_df = pd.DataFrame(y_test, columns=[df.columns[-1]])

        X_test_file_path = "../data/X_test_dataset_breast_cancer.csv"
        y_test_file_path = "../data/y_test_dataset_breast_cancer.csv"

        X_test_df.to_csv(X_test_file_path, index=False)
        y_test_df.to_csv(y_test_file_path, index=False)