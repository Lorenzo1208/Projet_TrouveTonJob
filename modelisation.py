from os.path import exists
import pickle

from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import GridSearchCV
from sklearn import set_config

from data_cleaning import *


def cleaning_data(df: pd.DataFrame) -> tuple:

    df.drop(columns='origine', inplace=True)
    df.dropna(inplace=True)
    df = df[df['Salaire minimum'] < 300000]
    df.dropna(subset=['Salaire minimum', 'Salaire maximum'], inplace=True)

    df['competences'] = df['competences'].apply(lambda x : x.replace(', ', ' ').replace(',', ' '))

    df['Date de publication'] = df['Date de publication'].values.astype(np.int64)

    X = df.drop(['Salaire minimum', 'Salaire maximum'], axis=1)
    y = df[['Salaire minimum', 'Salaire maximum']]

    return X, y


def get_pipeline_preparation():
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
            ('data_comp', transfo_text , 'competences'),
            ('data_poste', transfo_text , 'Intitulé du poste')
    ])

    return preparation


def get_pipeline_model(prepa, model):

    return Pipeline([('preparation', prepa), ('model',model)])


def search_best_model(pipe_model, X_y):

    param_grid = {
        'model__n_estimators': [100],
        'model__max_depth': [10,20],
        'model__min_samples_split': [1,10],
        'model__min_samples_leaf': [1,5],
        'model__random_state': list(range(0, 100))
    }

    grid = GridSearchCV(pipe_model, param_grid, cv=5)
    # Fit the GridSearchCV object to the training data
    grid.fit(X_y[0], X_y[1])

    print(grid.best_score_)
    print(grid.best_params_)

    return grid


def get_diagram(pipeline):

    set_config(display='diagram')

    return pipeline


def get_best_model():

    file_name = "best_model.model"

    if not exists(file_name):

        X, y = cleaning_data(get_dataset_3())

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        model = MultiOutputRegressor(RandomForestRegressor())

        pipe_model = get_pipeline_model(get_pipeline_preparation(), model)

        pipe_model = search_best_model(pipe_model, (X_train, y_train))

        pickle.dump(pipe_model, open(file_name, 'wb'))

        return pipe_model

    else:

        return pickle.load(open(file_name, 'rb'))


def test_model(model, X_y):

    y_pred = model.predict(X_y[0])

    score = r2_score(X_y[1], y_pred)

    print(score)
