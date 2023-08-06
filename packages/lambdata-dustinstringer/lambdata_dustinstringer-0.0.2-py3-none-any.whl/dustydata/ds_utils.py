def enlarge(n):
    """
    Param n is a number
    Function will enlarge the number
    """
    return n * 100

print(enlarge(5))


def cardinality_cutter(df, threshold=50):
    """
    Cut the cardinality of categorical data.
    """
    card = df.select_dtypes(exclude='number').nunique()
    card_cut = card[card <= threshold].index.tolist()
    return card_cut    

if __name__ == '__main__':  # run the name space when impoted in test_functions
    pass
    
    
    