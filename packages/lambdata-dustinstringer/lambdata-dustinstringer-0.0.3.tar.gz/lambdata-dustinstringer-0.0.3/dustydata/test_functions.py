from dustydata.ds_utils import cardinality_cutter

import pandas as pd
df = pd.DataFrame({0: ['g', 'g', 'g', 'y', 't', 'u', 'o'],
                    1: ['a', 'a', 'a', 'a', 'a', 'a', 'a'],
                    2: ['b', 'b', 'b', 'b', 'b', 'b', 'b'],
                    3: ['t', 'f', 'f', 'f', 't', 'h', 'j'],
                    4: ['f', 'h', 'd', 'k', 'j', 'y', 'j']})
df = cardinality_cutter(df, 4)
print(df)