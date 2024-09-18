from sklearn.model_selection import train_test_split
import pickle
import numpy as np


class PreProcessor:

    def split_train_test(self, dataset, test_percentage: float, seed: int = 7):
        """
        Handles all preprocessing steps including data cleaning, feature selection,
        and splitting the dataset into training and testing sets.
        """
        # Data cleaning and outlier removal

        # Feature selection

        # Train-test split
        X_train, X_test, Y_train, Y_test = self.__prepare_holdout(
            dataset, test_percentage, seed
        )

        # Normalization/standardization
        return X_train, X_test, Y_train, Y_test

    def __prepare_holdout(self, dataset, test_percentage: float, seed: int):
        """
        Splits the data into training and testing sets using the holdout method.
        Assumes the target variable is in the last column.
        The test_size parameter specifies the percentage of data used for testing.
        """
        data = dataset.values
        X = data[:, :-1]
        Y = data[:, -1]
        return train_test_split(X, Y, test_size=test_percentage, random_state=seed)

    @staticmethod
    def prepare_form(form):
        """
        Prepares the data received from the front-end for use in the model.
        """
        X_input = np.array([
            form.concave_points_worst,
            form.perimeter_worst, 
            form.concave_points_mean, 
            form.radius_worst, 
            form.perimeter_mean, 
            form.area_worst, 
            form.radius_mean, 
            form.area_mean
        ])

        # Reshape the input so the model understands we are passing a single instance
        X_input = X_input.reshape(1, -1)
        return X_input

    @staticmethod
    def scale_data(X_train):
        """
        Normalizes the data.
        """
        # Load the scaler for normalization/standardization
        scaler = pickle.load(open('./machine_learning/scalers/standard_scaler_breast_cancer.pkl', 'rb'))
        rescaled_X_train = scaler.transform(X_train)
        return rescaled_X_train