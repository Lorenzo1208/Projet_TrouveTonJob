from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import SGDRegressor, LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder

from data_cleaning import *
import time

start_time = time.time()

df = get_dataset_3().drop(columns='origine')

df.dropna(inplace=True)
df = df[df['Salaire minimum'] < 300000]
df.dropna(subset=['Salaire minimum', 'Salaire maximum'], inplace=True)

df['competences'] = df['competences'].apply(lambda x : x.replace(', ', ' ').replace(',', ' '))

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
        ('data_comp', transfo_text , 'competences'),
        ('data_poste', transfo_text , 'Intitulé du poste')

])

models = {
    'SGDRegressor': SGDRegressor(max_iter=100000),
    'LinearRegression': LinearRegression(),
    'Ridge': Ridge(max_iter=100000),
    'Lasso': Lasso(max_iter=100000),
    'ElasticNet': ElasticNet(max_iter=100000)
}

scores = {}
best = -100
best_random_state = 0
best_model = ''

for name_model in models:

    scores[name_model] = []

    for random_state in range(1, 100):

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)

        print(f"X_train = {X_train.shape} - X_test = {X_test.shape} - model = {name_model} - random_state = {random_state}", end='')

        model = MultiOutputRegressor(models[name_model])
        pipe_model = Pipeline([('preparation', preparation), ('model',model)])

        pipe_model.fit(X_train, y_train)

        y_pred = pipe_model.predict(X_test)

        score = r2_score(y_test, y_pred)

        scores[name_model].append(score)

        best_model = name_model if best < score else best_model
        best_random_state = random_state if best < score else best_random_state
        best = score if best < score else best

        print(" - score => ", round(score, 5), end='\n\n')

print(f"Best = {best} - Best random_state = {best_random_state} - Best model = {best_model}", end='\n\n')
print('\n'.join([f" - {n:20} moy : {sum(scores[n]) / len(scores[n])}" for n in models]))

duree = time.time() - start_time

print(f"{int(duree/3600)} h {int((duree%3600)/60)} m {duree%3600%60}")
