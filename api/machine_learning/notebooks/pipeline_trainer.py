import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

np.random.seed(7)


class PipelineTrainer:
    """
    A class for running and evaluating different pipelines with preprocessing steps and models.

    Attributes:
        X_train (pd.DataFrame): The training features.
        y_train (pd.Series): The training target variable.
        kfold (StratifiedKFold): Cross-validation strategy.
        results (list): List to store results of pipeline evaluations.
    """

    def __init__(self, X_train, y_train, kfold):
        """
        Initializes the PipelineTrainer with training data, target, and cross-validation strategy.

        Args:
            X_train (pd.DataFrame): Features for training.
            y_train (pd.Series): Target variable for training.
            kfold (StratifiedKFold): Cross-validation strategy.
        """
        self.X_train = X_train
        self.y_train = y_train
        self.kfold = kfold
        self.results = []

    def run_pipelines(self):
        """
        Runs the defined pipelines, evaluates their performance using cross-validation,
        and plots the comparison of their results.
        """
        pipelines = self._create_pipelines()
        
        for name, pipeline in pipelines:
            cv_results = cross_val_score(
                pipeline, self.X_train, self.y_train, cv=self.kfold, scoring='accuracy'
            )
            mean_score = cv_results.mean()
            std_dev = cv_results.std()
            print(f"{name}: {mean_score} ({std_dev})")
            self.results.append((name, cv_results))
        
        self._plot_pipelines_comparison()

    @staticmethod
    def _create_pipelines():
        """
        Creates a list of pipelines with various combinations of models and preprocessing steps.

        Returns:
            list: A list of tuples, each containing a name and a Pipeline object.
        """
        # Define classifiers
        knn = ('KNN', KNeighborsClassifier())
        cart = ('CART', DecisionTreeClassifier())
        naive_bayes = ('NB', GaussianNB())
        svm = ('SVM', SVC())

        # Define scalers
        standard_scaler = ('StandardScaler', StandardScaler())
        min_max_scaler = ('MinMaxScaler', MinMaxScaler())

        # Create pipelines
        pipelines = [
            ('KNN-orig', Pipeline([knn])),
            ('CART-orig', Pipeline([cart])),
            ('NB-orig', Pipeline([naive_bayes])),
            ('SVM-orig', Pipeline([svm])),

            ('KNN-std', Pipeline([standard_scaler, knn])),
            ('CART-std', Pipeline([standard_scaler, cart])),
            ('NB-std', Pipeline([standard_scaler, naive_bayes])),
            ('SVM-std', Pipeline([standard_scaler, svm])),

            ('KNN-norm', Pipeline([min_max_scaler, knn])),
            ('CART-norm', Pipeline([min_max_scaler, cart])),
            ('NB-norm', Pipeline([min_max_scaler, naive_bayes])),
            ('SVM-norm', Pipeline([min_max_scaler, svm])),
        ]

        return pipelines

    def _plot_pipelines_comparison(self):
        """
        Plots a boxplot comparing the results of the different pipelines.
        """
        fig = plt.figure(figsize=(25, 6))
        fig.suptitle('Pipeline Comparison')
        
        # Extract results and labels for plotting
        data = [result[1] for result in self.results]
        labels = [result[0] for result in self.results]
        
        plt.boxplot(data, labels=labels)
        plt.xticks(rotation=90)
        plt.show()