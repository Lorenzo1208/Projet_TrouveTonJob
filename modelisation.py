from os.path import exists
import sys
import pickle
import time

from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder
from sklearn.model_selection import RandomizedSearchCV
from sklearn import set_config
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, SGDRegressor

from data_cleaning import *


def cleaning_data(df: pd.DataFrame) -> tuple:

    df = df.copy()
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


def search_best_model(model, X_y, param_search):

    starting_time = time.time()

    search = RandomizedSearchCV(model, param_search, n_iter = 100, cv=5, verbose=3)

    pipe_model = get_pipeline_model(get_pipeline_preparation(), MultiOutputRegressor(search))

    pipe_model.fit(*X_y)

    duree = time.time() - starting_time

    search = pipe_model.named_steps['model'].estimators_[0]

    if hasattr(search, 'best_score_'):
        print("BEST SCORE :", search.best_score_)

    if hasattr(search, 'best_params_'):
        print("BEST PARAMS :", search.best_params_)

    print()
    print(f"{int(duree/3600)} H {int(duree%3600/60)} M {duree%3600%60}")

    return pipe_model


def get_diagram(pipeline):

    set_config(display='diagram')
    print(pipeline)


def get_best_model(file_name, model = None, params = None):

    file_name = "best_model_SGDRegressor.model"

    if not exists(file_name):

        if model is None or params is None:
            raise Exception(file_name + " introuvable")

        X_y = cleaning_data(get_dataset_3())

        pipe_model = search_best_model(model, X_y, params)

        pickle.dump(pipe_model, open(file_name, 'wb'))

        return pipe_model

    else:

        return pickle.load(open(file_name, 'rb'))


def test_model():

    starting_time = time.time()

    models = {
        'RandomForestRegressor': RandomForestRegressor(),
        'Lasso': Lasso(),
        'ElasticNet': ElasticNet(),
        'Ridge': Ridge(),
        'LinearRegression': LinearRegression(),
        'SGDRegressor': SGDRegressor()
    }

    best_score = None
    best_model_name = None
    best_random_state = None
    best_model = None

    for model_name in models:

        for random_state in range(100):

            X_y = cleaning_data(get_dataset_3())

            X_train, X_test, y_train, y_test = train_test_split(*X_y, test_size=0.3, random_state=random_state)

            model = get_pipeline_model(get_pipeline_preparation(), MultiOutputRegressor(models[model_name]))

            model.fit(X_train, y_train)

            y_pred = model.predict(X_test)

            score = r2_score(y_test, y_pred)

            print(f" - {model_name:25} {random_state:5} - score :{score:10.3%}", end='\n\n')

            if best_score is None or score > best_score:
                best_score = score
                best_model_name = model_name
                best_random_state = random_state
                best_model = model

    print(f"BEST : {best_model_name:25} {best_random_state:5} - score :{best_score:10.3%}")

    duree = time.time() - starting_time

    print(f"{duree//3600} H {duree%3600//60} M {duree%3600%60}")

    return best_model


def test_predict():

    file_name = "model_test.model"

    if not exists(file_name):
        model = test_model()
        pickle.dump(model, open(file_name, 'wb'))

    else:
        model = pickle.load(open(file_name, 'rb'))
        print('Model chargé')

    print('-------------')

    X = pd.DataFrame({
        'lieu': ['tours', 'paris', 'la defense', 'tours'],
        'Nom de la société': ['', 'societe general', 'edf', 'atos'],
        'Type de contrat': ['cdi', 'cdi', 'stage', 'alternance'],
        'Date de publication': time.time(),
        'Intitulé du poste': ['data scientist', 'chief business analyst', 'stage', 'alternance data ia'],
        'competences': ['python sql git', 'python sql reseau power bi', 'python', 'python sql pyspark excel git']
    })

    print(X)

    y = model.predict(X)

    print(y)


def main():

    param_SGD = {
        'max_iter': [1000000],
        'loss': ["squared_error", "huber", "epsilon_insensitive", "squared_epsilon_insensitive"],
        'penalty': ["l2", "l1", "elasticnet", None],
        'shuffle': [True, False],
        'random_state': range(10000),
        'learning_rate': ["constant", "optimal", "invscaling", "adaptive"]
    }

    model_SGD = SGDRegressor()

    get_best_model("SGDRegressor.model", model_SGD, param_SGD)


if __name__ == '__main__':
    main()
