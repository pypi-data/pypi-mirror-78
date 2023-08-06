from sklearn.model_selection import train_test_split

def cardinality_cutter(df, threshold=50):
    """
    Cut the cardinality of categorical data.
    Return a list of features that made the cut.
    """
    card = df.select_dtypes(exclude='number').nunique()
    card_cut = card[card <= threshold].index.tolist()
    return card_cut    


def tri_split(data):
    x, y = train_test_split(data)
    x, z = train_test_split(x)
    return x, y, z


# if __name__ == '__main__':  # run the name space when impoted in test_functions
#     pass
    
    
    