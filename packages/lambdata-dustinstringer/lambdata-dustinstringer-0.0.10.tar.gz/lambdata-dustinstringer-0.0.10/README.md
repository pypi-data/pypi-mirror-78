# lambdata-dustinstringer
A collection of datascience utility functions.

## Installation:
    pip install lambdata-dustinstringer
  
## Modules:
- **dustydata.wild_west**
    - example: import on the module level
                            
            from dustydata import wild_west

## Classes:
- **dustydata.wild_west.johnWayne(dataframe, check_null=boolean, check_data_types=boolean)**
    - example: import class and instatiate the class with its parameters
    
            from dustydata.wild_west import johnWayne
            
            new_wrangler = johnWayne(
                dataframe=dataframe,
                check_null=boolean,
                check_data_types, )
                
## Attributes/Methods/Functions:
- **dustydata.wild_west.johnWayne.cardinality_cutter(threshold=int)**
- **dustydata.wild_west.johnWayne.tri_split(val_size=float, test_size=float)**
