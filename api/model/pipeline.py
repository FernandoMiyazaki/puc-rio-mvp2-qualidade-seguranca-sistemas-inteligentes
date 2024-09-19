import pickle


class Pipeline:

    @staticmethod
    def load_pipeline(path: str):
        """
        Load the pipeline constructed during the training phase.
        """
        with open(path, 'rb') as file:
            pipeline = pickle.load(file)
        return pipeline