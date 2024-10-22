# Feature engineering
- model actually ingests an array of floating-point values called a **feature vector**
  eg. [2.3, 5.1]
- You must determine the best way to represent raw dataset values as trainable values in the feature vector. This process is called **feature engineering**, and it is a vital part of machine learning.
- The most common feature engineering techniques are:
    + **Normalization**: Converting numerical values into a standard range.
    + **Binning** (also referred to as bucketing): Converting numerical values into buckets of ranges.

## Numerical data
### Normalization helps:
  + converge more quickly during training
  +  infer better predictions
  +  avoid the "NaN trap" when feature values are very high. NaN is an abbreviation for not a number. When a value in a model exceeds the floating-point precision limit, the system sets the value to NaN instead of a number.
  +  learn appropriate weights for each feature. Without feature scaling, the model pays too much attention to features with wide ranges and not enough attention to features with narrow ranges
  
**Warning: If you normalize a feature during training, you must also normalize that feature when making predictions.**

- Normalization techniques:
  + Linear scaling: When the feature is uniformly distributed across a fixed range.
  + Z-score scaling: When the feature distribution does not contain extreme outliers.
  + Log scaling: When the feature conforms to the power law.
  + Clipping: When the feature contains extreme outliers.
### Binning
- Binning (also called bucketing) is a feature engineering technique that groups different numerical subranges into bins or buckets. In many cases, binning turns numerical data into categorical data
- eg:
  Bin number	Range	Feature vector  
  1   15-34   [1.0, 0.0, 0.0, 0.0, 0.0]  
  2   35-117  [0.0, 1.0, 0.0, 0.0, 0.0]

## Polynomal transform
Synthetic features can be created to model non-linear relationships between two features. These synthetic features can then be used as inputs to a linear model to enable it to represent nonlinearities.

## synthetic feature
A feature not present among the input features, but assembled from one or more of them. Methods for creating synthetic features include the following:  
  - Bucketing a continuous feature into range bins.  
  - Creating a feature cross.  
  - Multiplying (or dividing) one feature value by other feature value(s) or by itself. For example, if a and b are input features, then the following are examples of synthetic features:  
    + a*b  
    + a^2  
  - Applying a transcendental function to a feature value. For example, if c is an input feature, then the following are examples of synthetic features:  
    + sin(c)  
    + ln(c)  

## Categorical data
**Categorical data** has a _specific set_ of possible values. For example:
- The different species of animals in a national park
- The names of streets in a particular city
- Whether or not an email is spam


