import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

np.random.seed(7)


class ModelTrainer:
    """
    Class for training and evaluating machine learning models.
    """

    def __init__(self, X_train, y_train, models, scoring, kfold):
        """
        Initializes the ModelTrainer with the dataset, models, scoring method, and other parameters.

        Args:
            X_train (pd.DataFrame): Training features.
            y_train (pd.Series): Training target.
            models (list of tuples): List of models to evaluate.
            scoring (str): Scoring method for evaluation.
            kfold (int): Number of folds for cross-validation.
        """
        self.X_train = X_train
        self.y_train = y_train
        self.scoring = scoring
        self.kfold = kfold
        self.models = models
        self.results = []
        self.names = []

    @staticmethod
    def _default_models():
        """
        Returns a default list of models to evaluate.

        Returns:
            list of tuples: Default models.
        """
        return [
            ('KNN', KNeighborsClassifier()),
            ('CART', DecisionTreeClassifier()),
            ('NB', GaussianNB()),
            ('SVM', SVC())
        ]

    def evaluate_models(self):
        """
        Evaluates each model using cross-validation and prints the results.
        """
        for name, model in self.models:
            cv_results = cross_val_score(model, self.X_train, self.y_train, cv=self.kfold, scoring=self.scoring)
            self.results.append(cv_results)
            self.names.append(name)
            print(f"{name}: {cv_results.mean()} ({cv_results.std()})")
        self._plot_model_comparison()

    def _plot_model_comparison(self):
        """
        Plots a boxplot comparing the performance of different models.
        """
        fig = plt.figure(figsize=(15, 10))
        fig.suptitle('Model Comparison')
        plt.boxplot(self.results)
        plt.xticks(range(1, len(self.names) + 1), self.names)
        plt.show()