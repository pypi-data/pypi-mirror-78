"""This module is for testing functions."""

import pandas as pd
import numpy as np
from dustydata.wild_west import JohnWayne

if __name__ == '__main__':

    df = pd.DataFrame({
        0: [1, 2.9, 3, 4, 5, 6, 7],
        1: ['a', 'a', 'a', 'a', 'a', 'a', 'a'],
        2: ['b', 'b', np.NaN, 'b', 'b', 'b', 'b'],
        3: ['t', np.NaN, 'f', 'f', 't', 'h', 'j'],
        4: ['f', 'h', 'd', 'k', 'j', 'y', 'j']})

    jw = JohnWayne(df)
    jw.cardinality_cutter(threshold=5)
    X_train, X_val, X_test = jw.tri_split(.25, .25)
    print(X_train)
    print(X_val)
    print(X_test)
