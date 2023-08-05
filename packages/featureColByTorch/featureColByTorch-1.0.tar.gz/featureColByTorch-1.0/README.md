## Feature Column in Pytorch

### Description

this is a feature column tool implemented by pytorch, which has the same function compared to featurecol class in Tensorflow.

And it's also a tool for me to paricipate in some data science competition.

### Usage

```python
from features import Features
from number_feat import Number
from category_feat import Category

from transformers.NumberTransformer import NumberTransformer
from transformers.CategoryTransformer import CategoryTransformer
import pandas as pd
import numpy as np
```

- Example
```python
def make_data():
    data = pd.DataFrame(np.random.randint(1, 20, size=(3,4)), columns=['col1', 'col2', 'col3', 'col4'])
    return data

if __name__ == "__main__":
    data = make_data()
    Number_1 = Number('col1', NumberTransformer())
    Category_1 = Category('col2', CategoryTransformer())
    Category_2 = Category('col3', CategoryTransformer())
    Features_1 = Features(number_feat=[Number_1], category_feat=[Category_2], sequence_feat=[])
    print(Features_1.number_feat)
    Features_1.fit(data)
    res = Features_1.transform(data)
    print(res)
```

### Returned Data

```python
# [<number_feat.Number object at 0x0000018903E64748>]
# OrderedDict([('col1', array([-1.4048787 ,  0.8429272 ,  0.56195146], dtype=float32)), ('col3', array([1, 1, 1], dtype=int64))])
```