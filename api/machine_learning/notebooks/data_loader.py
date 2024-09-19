import pandas as pd


class DataLoader:
    """
    A class for loading datasets from a given URL.

    Attributes:
        url (str): The URL where the dataset is located.
        delimiter (str): The delimiter used in the dataset file (e.g., ',' for CSV).
        column_names (list): List of column names for the dataset.
    """

    def __init__(self, url, delimiter, column_names):
        """
        Initializes DataLoader with URL, delimiter, and column names.

        Args:
            url (str): URL of the dataset.
            delimiter (str): Delimiter used to separate values in the dataset.
            column_names (list): Column names to use for the dataset.
        """
        self.url = url
        self.delimiter = delimiter
        self.column_names = column_names

    def load_data(self):
        """
        Loads the dataset from the provided URL.

        Returns:
            pd.DataFrame: The loaded dataset as a pandas DataFrame.
        """
        return pd.read_csv(
            self.url, 
            delimiter=self.delimiter, 
            names=self.column_names, 
            header=None
        )