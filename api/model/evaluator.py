from sklearn.metrics import accuracy_score
from model.model import Model


class Evaluator:
    @staticmethod
    def evaluate(model, X_test, Y_test):
        """
        Makes a prediction and evaluates the model. This method could be 
        extended to parameterize different evaluation types and metrics.
        """
        predictions = Model.perform_prediction(model, X_test)

        return accuracy_score(Y_test, predictions)