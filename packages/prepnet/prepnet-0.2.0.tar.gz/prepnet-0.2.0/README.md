[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Build Status](https://travis-ci.org/elda27/prepnet.svg?branch=master)](https://travis-ci.org/elda27/prepnet)
[![codecov](https://codecov.io/gh/elda27/prepnet/branch/master/graph/badge.svg)](https://codecov.io/gh/elda27/prepnet)

# Prepnet
Reconstructable preprocessor library.

There are concepts of this library.
- All pre-processes can save as a pickle.
- Reconstructable pre-processes for feature analysis

# Example
A simple example is see examples/01_iris.ipynb
There is pre-process using prepnet for iris dataset in a part of example.

```python
import prepnet 
from sklearn import datasets

# Load dataset.
iris = datasets.load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target_names[iris.target]

# Scale by std and mean, and split 5 folds.
context = prepnet.FunctionalContext()
with context.enter('normalize'):
    # All pre-process method allow method chain.
    context[
        'sepal length (cm)',
        'sepal width (cm)',
        'petal length (cm)',
        'petal width (cm)',
    ].standardize()

# context.post is execute always after other preprocesses.
with context.enter('post'):
    context.split()

# convert python list object from prepnet.DataFrameArray.
preprocessed_df_list = list(context.encode(df))
# Concat first 4 element for train dataset.
train_df = pd.concat(preprocessed_df_list[:4], axis=0) 
# Use last element for test dataset.
test_df = preprocessed_df_list[-1]
```

And above preprocessor context can disable normalize easily

```python
new_context = context.disable()
preprocessed_df_list = list(context.encode(df))
# Concat first 4 element for train dataset
nonnorm_train_df = pd.concat(preprocessed_df_list[:4], axis=0) 
# Use last element for test dataset
nonnorm_test_df = preprocessed_df_list[-1]
```

# Do you ever remember this?
Boss: Hey, what's the difference between the new results and the old ones?

Someone: Well, some preprocesses are different.

Boss: Okay. Let me see the dataset.

Someone: Yes, sir. It's this and this.

Boss: What's the difference two datasets? The value that comes out of the difference is slightly, what's the difference in the preprocess?

Someone: Well, I just don't know.

Boss: Why? The dataset contains a commit idand you're managing source codes with git.

Someone: Even if I knew what version of the dataset it was created from. I would have commented out the details and preprocessed it...

Boss: Hey you...

# Install
```shell
pip install prepnet
```

or

```shell
git clone https://github.com/elda27/prepnet
cd prepnet
python setup.py install
```

# Test
```shell
python -m pytest --cov=prepnet
```
