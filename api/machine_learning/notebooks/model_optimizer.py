import numpy as np

from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

np.random.seed(7)


class ModelOptimizer:
    """
    A class to optimize machine learning models using GridSearchCV with various preprocessing steps.
    """

    def __init__(self, X_train, y_train, kfold=5, scoring='accuracy'):
        """
        Initialize the ModelOptimizer with training data, cross-validation settings, and scoring metric.
        
        Parameters:
        - X_train: array-like, shape (n_samples, n_features)
            Training data features.
        - y_train: array-like, shape (n_samples,)
            Training data labels.
        - kfold: int, default=5
            Number of folds in cross-validation.
        - scoring: str, default='accuracy'
            Scoring metric for model evaluation.
        """
        self.X_train = X_train
        self.y_train = y_train
        self.kfold = kfold
        self.scoring = scoring
        self.models = self._initialize_models()
        self.pipelines = self._create_pipelines()
        self.param_grids = self._initialize_param_grids()

    def _initialize_models(self):
        """
        Initialize the models for optimization.
        
        Returns:
        - list of tuples containing model names and instances.
        """
        return [
            ('KNN', KNeighborsClassifier()),
            ('CART', DecisionTreeClassifier()),
            ('NB', GaussianNB()),
            ('SVM', SVC())
        ]

    def _create_pipelines(self):
        """
        Create pipelines with different scalers and models.
        
        Returns:
        - list of tuples containing pipeline names and Pipeline instances.
        """
        standard_scaler = ('StandardScaler', StandardScaler())
        min_max_scaler = ('MinMaxScaler', MinMaxScaler())
        pipelines = []

        for name, model in self.models:
            pipelines.append((f"{name}-orig", Pipeline(steps=[(name, model)])))
            pipelines.append((f"{name}-std", Pipeline(steps=[standard_scaler, (name, model)])))
            pipelines.append((f"{name}-norm", Pipeline(steps=[min_max_scaler, (name, model)])))
        
        return pipelines

    def _initialize_param_grids(self):
        """
        Define parameter grids for each model.
        
        Returns:
        - dict of parameter grids for different models.
        """
        return {
            'KNN': {
                'KNN__n_neighbors': [1, 3, 5, 7, 9, 11],
                'KNN__metric': ['euclidean', 'manhattan', 'minkowski']
            },
            'CART': {
                'CART__max_depth': [None, 10, 20, 30],
                'CART__min_samples_split': [2, 5, 10],
                'CART__min_samples_leaf': [1, 2, 4]
            },
            'NB': {
                'NB__var_smoothing': [1e-9, 1e-8, 1e-7, 1e-6]
            },
            'SVM': {
                'SVM__C': [0.1, 1, 10, 100],
                'SVM__gamma': [1, 0.1, 0.01, 0.001],
                'SVM__kernel': ['rbf', 'linear']
            }
        }

    def optimize_models(self):
        """
        Run GridSearchCV for each pipeline and print the best model configurations.
        """
        for name, pipeline in self.pipelines:
            model_type = name.split('-')[0]
            if model_type in self.param_grids:
                param_grid = self.param_grids[model_type]
                grid = GridSearchCV(
                    estimator=pipeline,
                    param_grid=param_grid,
                    scoring=self.scoring,
                    cv=self.kfold
                )
                grid.fit(self.X_train, self.y_train)
                self._print_best_model(name, grid)

    @staticmethod
    def _print_best_model(name, grid):
        """
        Print the best configuration found for the model.
        
        Parameters:
        - name: str
            The name of the pipeline.
        - grid: GridSearchCV
            The fitted GridSearchCV instance.
        """
        print(f"Model: {name} - Best Score: {grid.best_score_} using {grid.best_params_}")