[![PyPI version](https://badge.fury.io/py/pandashape.svg)](https://badge.fury.io/py/pandashape)

# pandashape: a simpleish Python package for easy data cleanup and preparation of Pandas dataframes

I made `pandashape` because I've been finding I do a lot of the same repetitive cleanup for simple modeling with scikit-learn.
I've intentionally designed it to make data preparation expressive, concise, and easily repeatable - just put your use of 

## Getting started

Just install with pip!

`pip install pandashape`

## Using pandashape
Create your dataframe however you choose - from a CSV, `.txt.` file, random generation, whatever. Then wrap your frame in a `PandaShaper`. 

```python
# import packages
import numpy as np
import pandas as pd
from pandashape import PandaShaper, Columns
from pandashape.transformers import CategoricalEncoder, NullColumnsDropper

# create your frame
my_df = pd.read_csv('./my_data.csv')

# wrap it in a shaper
shaper = PandaShaper(my_df)
```

From here, you can use PandaShape to inspect and transform your data.

### Data inspection

PandaShape provides an automatic `.describe()` method similar to the one provided by `pandas`, but with more feature richness
and extensibility.

```python
shaper.describe()
```

```
#########################################
###         PANDASHAPE REPORT         ###
#########################################

### General frame info ###
-----------------------------------------
Shape: (1000, 12)
Columns with one or more null values: ['History']
Columns of type "object" (may need label encoding): ['Age' 'Gender' 'OwnHome' 'Married' 'Location' 'History']

### Data types ###
-----------------------------------------
Columns by data type
- Numeric: 6
- Objects/strings: 6

### Distribution ###
-----------------------------------------
These columns have significant outlier values (more than +/- 2 standard deviations from the mean).
- Salary (34)
- AmountSpent (42)
- AmountSpent_HighCorrelation (42)
- Salary_HighCorr (34)

These columns are skewed beyond the threshold of 1 +/- 0.4. You may want to scale them somehow.
 - Salary (0.41909498781999727)
 - Catalogs (0.0920540150758884)
 - AmountSpent (1.4692769120373967)
 - AmountSpent_HighCorrelation (1.4692769120373967)
 - Salary_HighCorr (0.41909498781999727)

### Correlated columns ###
-----------------------------------------
The following columns are highly correlated (r² > 0.8): ['AmountSpent_HighCorrelation', 'Salary_HighCorr']
```

If you have questions that you often ask about your datasets, you can encapsulate them in classes that inherit PandaShape's `Describer` for reuse. See the wiki for documentation.

### Data transformation

PandaShape's data preparation and cleanup features are where it really shines. It provides an expressive syntax that you can use to describe, order, and even dynamically modify transformations to your data:

```python
# import packages
import numpy as np
import pandas as pd
from pandashape import PandaShaper, Columns
from pandashape.transformers import 
    CategoricalEncoder,
    MassScaler, 
    NullColumnsDropper

# create your frame
my_df = pd.read_csv('./my_data.csv')

# wrap it in a shaper
shaper = PandaShaper(my_df)

# create a pipeline of transform operations (these will happen in order)
# and assign the output to a new (transformed) frame!
transformed_df = shaper.transform(
    {
        # drop columns that have 80% or less null data
        'columns': Columns.All,
        'transformers': [
            NullColumnsDropper(null_values=[np.nan, None, ''], threshold=0.8),
            MassScaler()
        ]
    },
    {
        # CategoricalEncoder one-hot-encodes targeted categorical columns if they
        # have a number of values ≥ the breakpoint or label encodes them normally 
        'columns': ['Education', 'SES'], 
        'transformers': CategoricalEncoder(label_encoding_breakpoint=4)
    }
)

# inspect the new frame to see the fruits of your labors!
transformed_df.head()
```

## Upcoming improvements

- Allow the user to constrain describers to specific columns (by name or `Columns` enum value)
- A describer that summarizes discrete column values for columns that appear to be categorical
- Allow the user to pass types to the 'transformers' property when shaping

## Features being evaluated

- Improvements to `.describe` that returns all frames generated during transformation for inspection

## Acknowledgments

Special thanks to the other members of the [Sustainable Social Computing Lab](https://ssc-pitt.github.io/) at the University of Pittsburgh for their support, ideas, and contributions.