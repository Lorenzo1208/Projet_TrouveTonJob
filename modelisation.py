from TrouveTonJob import *

# data
import pandas as pd

# Preprocessing
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, RobustScaler, MinMaxScaler

# Pipeline and model
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.naive_bayes import CategoricalNB, GaussianNB
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.svm import SVC
from sklearn.multioutput import MultiOutputRegressor

# Score of models
from sklearn.metrics import r2_score


df = try_download_json(URL)
df = clean_data(df)

df.dropna(subset=['Salaire minimum', 'Salaire maximum'], inplace=True)

df['Date de publication'] = df['Date de publication'].values.astype(np.int64)

X = df.drop(['Salaire minimum', 'Salaire maximum'], axis=1)
y = df[['Salaire minimum', 'Salaire maximum']]

# J'ai pas mis de simple imputer parce que ça me parait pas logique de mettre un nom de société au pif quand il y en a pas
column_cat = ['lieu', 'Nom de la société', 'Type de contrat']
transfo_cat = Pipeline([
    ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output = False))
])

column_num = ['Date de publication']
transfo_num = Pipeline([
    ('imputation', SimpleImputer(strategy='median')),
    ('scaling', MinMaxScaler())
])

transfo_text = Pipeline([
    ('bow', CountVectorizer())
])

preparation = ColumnTransformer([
        ('data_cat', transfo_cat , column_cat),
        ('data_num', transfo_num , column_num),
        ('data_artist', transfo_text , 'Intitulé du poste'),
        ('data_track', transfo_text , 'competences')
])

model = MultiOutputRegressor(SGDRegressor(max_iter=100000))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=2)

pipe_model = Pipeline([('preparation', preparation),
                        ('model',model)])

pipe_model.fit(X_train, y_train)

y_pred = pipe_model.predict(X_test)

score = r2_score(y_test, y_pred)
print("score :", round(score, 5))
