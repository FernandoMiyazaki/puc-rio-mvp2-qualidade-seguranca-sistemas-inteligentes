class Preprocessor:
    """
    Class for preprocessing data.

    Attributes:
        df (pd.DataFrame): The input dataset.
        target_column (str): The target column containing the labels.
        corr_threshold (float): The correlation threshold for selecting features.
    """

    def __init__(self, df, target_column, corr_threshold=0.7):
        """
        Initializes the Preprocessor with the dataset, target column, and correlation threshold.

        Args:
            df (pd.DataFrame): The input dataset.
            target_column (str): The name of the target column.
            corr_threshold (float): The threshold above which features will be kept based on correlation.
        """
        self.df = df
        self.target_column = target_column
        self.corr_threshold = corr_threshold

    def preprocess(self):
        """
        Preprocesses the dataset by encoding the target column and filtering features
        based on correlation with the target column.

        The target column is encoded as binary values (1 for 'M', 0 for 'B').
        Features that have a correlation above the given threshold with the target 
        column are retained.

        Returns:
            pd.DataFrame: The preprocessed dataset with filtered features.
        """
        # Encode the target column (1 for 'M', 0 for 'B')
        self.df[self.target_column] = self.df[self.target_column].map({'M': 1, 'B': 0})
        
        # Calculate the correlation matrix
        corr_matrix = self.df.corr()
        high_corr_features = corr_matrix[self.target_column].sort_values(ascending=False)
        
        # Select features with correlation above the threshold
        df_filtered = self.df.loc[:, high_corr_features[high_corr_features > self.corr_threshold].index]
        
        # Assign the target column back to df_filtered
        df_filtered[self.target_column] = df_filtered.pop(self.target_column)
        
        return df_filtered