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

#фінальне навчання(беремо random forest так як там більший результат)
if random_scores.mean() > log_scores.mean():
    final_model = Pipeline(steps= [('data_preprogress', database_pipeline), ('model_train', RandomForestClassifier(n_estimators= 200, random_state=42, n_jobs=-1))])
    print('Final Model Random Forest')

else:
    final_model = Pipeline(steps= [('data_preprocess', database_pipeline), ('model_train', LogisticRegression(max_iter= 300))])
    print('Final Model Logistic Regression')
    print('----------------------------------\n')

#навчвння на всіх вхідних даних
final_model.fit(forecast_database, target_database)
print('ФІнальне навчання моделі завершено')
print('----------------------------------\n')

#передбачення
test_prediction = final_model.predict(test_database)

print('Прогноз створено', test_prediction)

#створення файлу csv
submission_database = pd.DataFrame({'index': test_database.index, 'y': test_prediction})
sample_database.to_csv('submission.csv', index= False)

print('Файл csv створено')
print('----------------------------------\n')
print(submission_database.head())