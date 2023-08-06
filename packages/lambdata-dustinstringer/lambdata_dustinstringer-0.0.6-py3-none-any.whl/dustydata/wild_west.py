# This is a data wrangling module:
import pandas as pd 
import numpy as np
from sklearn.model_selection import train_test_split

class johnWayne:
    """
    Data Wrangling Class
    
    ex:
    new_wrangler = johnWayne(dataframe)
    """
    
    def __init__(self, dataframe, check_null=True, 
                 check_data_types=True):
        self.dataframe = dataframe
        self.check_null = check_null
        self.check_data_types = check_data_types
        self.main()
        
    def main(self):
        """
        Main function to run when the class is instantiated.
        These functions can be enabled and disabled as params in the
        class instance.
        """
        if self.check_null == True:
            self.__check_nulls__()
            
        if self.check_data_types == True:
            self.__check_data_types__()
        
    def __check_nulls__(self):
        """
        Checks for null values in a data frame and 
        returns the sum of nulls in a column.
        """
        null_dictionary = {}
        for e, i in enumerate(self.dataframe.isnull().sum()):
            if i > 0:
                null_dictionary[e] = i
        print(null_dictionary)
        
    def __check_data_types__(self):
        """
        Returns the datatypes of each series in a data frame.
        """
        print(self.dataframe.dtypes)
        
    def cardinality_cutter(self, threshold=50):
        """
        Cut the cardinality of categorical data.
        Return a list of features that made the cut.
        """
        card = self.dataframe.select_dtypes(exclude='number').nunique()
        card_cut = card[card <= threshold].index.tolist()
        return card_cut 

    def tri_split(self, val_size, test_size, random_state=42):
        """
        Split data three ways:
        train/val/test
        
        This function makes use of sklearns train_test_split.
        
        data = dataframe to split
        val_size = size of split in float value from 0.0 to 1.0
        test_size = size of split in float value from 0.0 to 1.0
        """
        x, y = train_test_split(self.dataframe, 
                                test_size=val_size, 
                                random_state=random_state)
        x, z = train_test_split(x, test_size=test_size, 
                                random_state=random_state)
        return x, y, z
