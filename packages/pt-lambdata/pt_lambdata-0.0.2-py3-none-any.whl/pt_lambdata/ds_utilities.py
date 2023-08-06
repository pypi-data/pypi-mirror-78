'''
This module is to assist in cleaning out data and simple wrangling.
'''

# from pdb import set_trace as breakpoint
import pandas as pd
from sklearn.model_selection import train_test_split


class Nose:
    """
    This class helps to identify ripe boogers for picking.
    """
    def __init__(self, dataframe, features=None, target=None):
        self.dataframe = dataframe
        self.features = features
        self.target = target

    def booger_picker(self, date_column_name):
        """
        Takes a passed in dataframe and converts the date feature into
        a Datetime column, then extracts the years, months and days to
        separate features.
        """
        self.dataframe[date_column_name] = pd.to_datetime(
                                    self.dataframe[date_column_name],
                                    infer_datetime_format=True)
        self.dataframe['Year'] = self.dataframe[date_column_name].dt.year
        self.dataframe['Month'] = self.dataframe[date_column_name].dt.month
        self.dataframe['Day'] = self.dataframe[date_column_name].dt.day
        self.dataframe.drop(date_column_name, axis=1, inplace=True)
        return self.dataframe

    def nostril_population(
            self,
            train_size=0.7,
            val_size=0.1,
            test_size=0.2,
            random_state=None,
            shuffle=True):
        '''
        This function is a utility wrapper around the Scikit-Learn
        train_test_split that splits arrays or matrices into train,
        validation, and test subsets.

        Args:
            X (list): This is a list of features.

            y (str): This is a string with target column.

            train_size (float or int): Proportion of the dataset to
            include in the train split (0 to 1).

            val_size (float or int): Proportion of the dataset to
            include in the validation split (0 to 1).

            test_size (float or int): Proportion of the dataset to
            include in the test split (0 to 1).

            random_state (int): Controls the shuffling applied to
            the data before applying the split for reproducibility.

            shuffle (bool): Whether or not to shuffle the data before
            splitting

        Returns:
            Train, test, and validation dataframes for features (X)
            and target (y).
        '''
        X = self.dataframe[self.features]
        y = self.dataframe[self.target]

        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state,
            shuffle=shuffle)
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val,
            test_size=val_size / (train_size + val_size),
            random_state=random_state, shuffle=shuffle)
        return X_train, X_val, X_test, y_train, y_val, y_test

class PiercedNose(Nose):
    def __init__(self, dataframe):
        super().__init__(dataframe)

    def piercing_cleaner(self):
        print(self.dataframe)
        