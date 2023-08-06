from dustydata.ds_utils import cardinality_cutter
from dustydata.ds_utils import tri_split
from dustydata.ds_utils import train_test_split

import pandas as pd
df = pd.DataFrame({0: ['g', 'g', 'g', 'y', 't', 'u', 'o'],
                    1: ['a', 'a', 'a', 'a', 'a', 'a', 'a'],
                    2: ['b', 'b', 'b', 'b', 'b', 'b', 'b'],
                    3: ['t', 'f', 'f', 'f', 't', 'h', 'j'],
                    4: ['f', 'h', 'd', 'k', 'j', 'y', 'j']})
card_feats = cardinality_cutter(df, 4)
print(card_feats)

x, y, z = tri_split(df, .25, .25)
print(x)
print(y)
print(z)

