"""This is a data wrangling/feature engineering module:"""
import random
from sklearn.model_selection import train_test_split


class JohnWayne:
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
        if self.check_null is True:
            self.__check_nulls__()

        if self.check_data_types is True:
            self.__check_data_types__()

    def __check_nulls__(self):
        """
        Checks for null values in a data frame and
        returns the sum of nulls in a column.
        """
        null_dictionary = {}
        for _e, _i in enumerate(self.dataframe.isnull().sum()):
            if _i > 0:
                null_dictionary[_e] = _i
        print("\n")
        print("Index Position: Null value sums\n")
        print(null_dictionary)
        print("---------------------------------")

    def __check_data_types__(self):
        """
        Returns the datatypes of each series in a data frame.
        """
        print("\n")
        print("Data types of each series in the dataframe:\n")
        print(self.dataframe.dtypes)
        print("-----------------------------------------------")

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
        train, val = train_test_split(
            self.dataframe,
            test_size=val_size,
            random_state=random_state)
        val, test = train_test_split(
            val, test_size=test_size,
            random_state=random_state)
        return train, val, test


# class PocketWatch:
#     """
#     Class to handle time data
#     """


class SafeCracker:
    """Test function to see if import and installation worked....for now"""
    # def __init__(self, goal_arr, curr_arr):
    #     self.goal_arr = list(input("Enter a string of letters: ").lower())
    #     self.curr_arr = [' '] * len(goal_arr)

    def main(self):
        """main function"""
        goal_arr = list(input("Enter a string of letters: ").lower())
        curr_arr = [' '] * len(goal_arr)
        while curr_arr != goal_arr:
            self.compare_arrays(
                goal_arr,
                guess_arr=self.generate_array(len(goal_arr)),
                curr_arr=curr_arr)
            print(''.join(curr_arr))

    def generate_array(self, length) -> int:
        """Generate Random String of a specific length"""
        alphabet = 'abcdefghijklmnopqrstuvwxyz '
        res = []
        for _ in range(length):
            res.append(alphabet[random.randrange(27)])
        return res

    def compare_arrays(self, goal_arr, guess_arr, curr_arr):
        """Compare and updated array"""
        for i, _ in enumerate(goal_arr):
            if goal_arr[i] == guess_arr[i]:
                curr_arr.__setitem__(i, guess_arr[i])
        return curr_arr
