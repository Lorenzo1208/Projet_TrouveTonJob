# Step 1:Imputation
from sklearn.impute import SimpleImputer
imputer = SimpleImputer(strategy='mean')


#Step 2 Scaling

from sklearn.preprocessing import RobustScaler
scaler = RobustScaler()




#Step 3 Modelisation

from sklearn.linear_model import LinearRegression
model = LinearRegression()

#Step 4 : Build the pipeline

from sklearn.pipeline import Pipeline
pipe = Pipeline(steps=[
                       ('imputation', imputer),
                       ('scaling', scaler),
                       ('modelisation', model)
                       ])
pipe

#Step 5 : Apply the pipeline

# Prepare data
import numpy as np
from sklearn.model_selection import train_test_split
X = np.array([[1, np.nan], [1, 2], [ np.nan, 2], [2, 3]])
y = np.array([5.,  8., 7., 11.])

# Apply pipeline
pipe.fit(X, y)

#Step 6 : Use the pipeline

pipe.score(X, y)

#Pipeline diagram

from sklearn import set_config
set_config(display='diagram')
pipe