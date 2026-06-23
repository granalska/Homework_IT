import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.metrics import r2_score
from sklearn.impute import SimpleImputer

#завантаження даних
train_url = 'https://raw.githubusercontent.com/goitacademy/MACHINE-LEARNING-NEO/main/datasets/mod_04_hw_train_data.csv'
train_data = pd.read_csv(train_url, sep= ',', on_bad_lines='skip')
valid_url = 'https://raw.githubusercontent.com/goitacademy/MACHINE-LEARNING-NEO/main/datasets/mod_04_hw_valid_data.csv'
valid_data = pd.read_csv(valid_url, sep= ',', on_bad_lines='skip')

print(train_data.info())
print(train_data.head())
print(train_data.isnull().sum())
print(train_data.describe())
print('----------------------------------')

x_train = train_data.drop('Salary', axis= 1)
y_train = train_data['Salary']

x_valid = valid_data.drop('Salary', axis= 1)
y_valid = valid_data['Salary']

#пошук числових і текстових колонок
number_columns = x_train.select_dtypes(include= ['int64', 'float64']).columns
category_columns = x_train.select_dtypes(include= ['object', 'string']).columns

print(number_columns)
print(category_columns)
print('----------------------------------')

#обробку числових ознак та кодування категоріальних
number_pipe = make_pipeline(SimpleImputer(strategy= 'median'), StandardScaler())
category_pipe = make_pipeline(SimpleImputer(strategy='most_frequent'), OneHotEncoder(handle_unknown= 'ignore'))

#
transform = make_column_transformer((number_pipe, number_columns), (category_pipe, category_columns))

#побудова моделі
model = make_pipeline(transform, KNeighborsRegressor(n_neighbors=5, weights='distance'))
model.fit(x_train, y_train)
model_predict = model.predict(x_valid)

#обчислення метрик
mae = mean_absolute_error(y_valid, model_predict)
print('MAE =', mae)
print('----------------------------------')
mse = mean_squared_error(y_valid, model_predict)
print('MSE =', mse)
print('----------------------------------')
rmse = np.sqrt(mse)
print('RMSE =', rmse)
print('----------------------------------')
r2 = r2_score(y_valid, model_predict)
print('R2 =', r2)
print('----------------------------------')
mape = mean_absolute_percentage_error(y_valid, model_predict)
print(f'Validation MAPE: {mape:.2%}')
print('----------------------------------')

#результат
result = pd.DataFrame({'real_salary' : y_valid, 'predict_salary' : model_predict})

print(result.head(10))
print('----------------------------------')


