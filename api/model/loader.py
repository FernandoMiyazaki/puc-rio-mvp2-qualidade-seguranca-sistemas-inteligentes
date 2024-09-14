import pandas as pd


class Loader:

    @staticmethod
    def load_data(url: str, attributes: list) -> pd.DataFrame:
        """
        Loads and returns a DataFrame. There are various parameters 
        in read_csv that could be used to provide additional options.
        """

        return pd.read_csv(
            url,
            names=attributes,
            header=0,
            skiprows=0,
            delimiter=','
        )