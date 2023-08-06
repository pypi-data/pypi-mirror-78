from sklearn.model_selection import train_test_split

def cardinality_cutter(df, threshold=50):
    """
    Cut the cardinality of categorical data.
    Return a list of features that made the cut.
    """
    card = df.select_dtypes(exclude='number').nunique()
    card_cut = card[card <= threshold].index.tolist()
    return card_cut    


def tri_split(data, val_size, test_size):
    """
    Split data three ways:
    train/val/test
    
    This function makes use of sklearns train_test_split.
    
    data = dataframe to split
    val_size = size of split in float value from 0.0 to 1.0
    test_size = size of split in float value from 0.0 to 1.0
    """
    x, y = train_test_split(data, test_size=val_size)
    x, z = train_test_split(x, test_size=test_size)
    return x, y, z


# if __name__ == '__main__':  # run the name space when impoted in test_functions
#     pass
    
    
    