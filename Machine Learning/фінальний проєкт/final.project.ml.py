import kagglehub

#завантаження файлів
path = kagglehub.competition_download('ml-fundamentals-and-applications-2026-06')

print('Завантаження файлових даних:\n', path)
print('----------------------------------\n')

import pandas as pd
import os

#завантаження database
train_database = pd.read_csv(os.path.join(path, 'final_proj_data.csv'))
test_database = pd.read_csv(os.path.join(path, 'final_proj_test.csv'))
sample_database = pd.read_csv(os.path.join(path, 'final_proj_sample_submission.csv'))

print('Завантаження бази даних:\n')
print('Навчальна база:\n', train_database.shape)
print('----------------------------------\n')
print('Тестова база:\n', test_database.shape)
print('----------------------------------\n')

#ознайомлення з базою
print(train_database.head())
print('----------------------------------\n')
print(train_database.info())
print('----------------------------------\n')
passes_values = train_database.isnull().sum().sort_values(ascending= False)
print(train_database.head(20))
print('----------------------------------\n')

#класифікація(цільова змінна)
target_variant = train_database['y']

print(target_variant.value_counts())
print(target_variant.value_counts(normalize= True))
print('----------------------------------\n')

#розподіл даних
forecast_database = train_database.drop(columns= ['y'])
target_database = train_database['y']

print('Розподіл тренувальних даних [forecast_database/target_database]')
print('----------------------------------\n')

#ознвки
number_forecast = forecast_database.select_dtypes(include= ['int64', 'float64']).columns
category_forecast = forecast_database.select_dtypes(include= ['object', 'string']).columns

print('Кількість числових ознак:\n', len(number_forecast))
print('Кількість категоріальних ознак\n', len(category_forecast))
print('----------------------------------\n')

from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

#обробка вхідних даних
number_database = SimpleImputer(strategy= 'median')
category_database = Pipeline(steps= [('passes_values_rep', SimpleImputer(strategy= 'most_frequent')), ('categor_encoding', OneHotEncoder(handle_unknown= 'ignore'))])

database_pipeline = ColumnTransformer(transformers= [('number_process', number_database, number_forecast), ('categor_process', category_database, category_forecast)])

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

#модель kогістичної регресії
log_model = Pipeline(steps= [('data_preprocess', database_pipeline), ('model_train', LogisticRegression(max_iter= 300))])
validation = StratifiedKFold(n_splits= 6, shuffle= True, random_state= 42)
log_scores = cross_val_score(log_model, forecast_database, target_database, cv= validation, scoring= 'roc_auc')

print('Результат логістичної регресії:\n', log_scores)
print('Середній результат:\n', log_scores.mean())
print('----------------------------------\n')

from sklearn.ensemble import RandomForestClassifier

#модель рандомний ліс
random_model = Pipeline(steps= [('data_preprocess', database_pipeline), ('model_train', RandomForestClassifier(n_estimators= 200, random_state= 42, n_jobs= -1))])
random_scores = cross_val_score(random_model, forecast_database, target_database, cv= validation, scoring= 'roc_auc')

print('Результат Random Forest:\n', random_scores)
print('Середній результат\n', random_scores.mean())
print('----------------------------------\n')

from catboost import CatBoostClassifier

#модель CatBoost

x = forecast_database.copy()
y = target_database
x_test = test_database.copy()

cat_feature_names = category_forecast.tolist()

for col in cat_feature_names:
    x[col] = x[col].fillna('None').astype(str)
    x_test[col] = x_test[col].fillna('None').astype(str)

cat_features = [x.columns.get_loc(col) for col in cat_feature_names]

catboost_model = CatBoostClassifier(iterations= 1500, learning_rate= 0.03, depth= 6, loss_function= 'Logloss', eval_metric= 'AUC', verbose= 200, random_state= 42)
catboost_scores = cross_val_score(catboost_model, x, y, cv= validation, scoring= 'roc_auc', params= {'cat_features': cat_features})

print('Результат CatBoost:\n', catboost_scores)
print('Середній результат\n', catboost_scores.mean())
print('----------------------------------\n')

#фінальне навчання(беремо CatBoost так як там більший результат)
rf_mean = random_scores.mean()
log_mean = log_scores.mean()
cb_mean = catboost_scores.mean()

if cb_mean > rf_mean and cb_mean > log_mean:
    final_model = catboost_model
    is_catboost = True
    print(f'Final Model CatBoost, найкращий результат: {cb_mean:.4f}')

elif rf_mean > log_mean:
    final_model = random_model
    is_catboost = False
    print(f'Final Model Random Forest (Результат: {rf_mean:.4f})')

else:
    final_model = log_model
    is_catboost = False
    print(f'Final Model Logistic Regression (Результат: {log_mean:.4f})')
    print('----------------------------------\n')

#навчвння на всіх вхідних даних
if is_catboost:
    final_model.fit(x, y, cat_features=cat_features)
else:
    final_model.fit(forecast_database, target_database)

print('ФІнальне навчання моделі завершено')
print('----------------------------------\n')

#передбачення
if is_catboost:
    test_prediction = final_model.predict_proba(x_test)[:, 1]
else:
    test_prediction = final_model.predict_proba(test_database)[:, 1]

test_prediction = (test_prediction >= 0.5).astype(int)

print('Прогноз створено', test_prediction)

#створення файлу csv
submission_database = sample_database.copy()
submission_database['y'] = test_prediction
submission_database.to_csv('submission_ml.csv', index=False)

print('Оновлений файл csv створено з колонками:', submission_database.columns.tolist())
print('----------------------------------\n')
print(submission_database.head())