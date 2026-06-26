import kagglehub

#завантаження файлів
path = kagglehub.competition_download('ml-fundamentals-and-applications-2026-06')

print('Завантаження файлових даних:\n', path)
print('----------------------------------\n')

import pandas as pd
import os

#завантаження database
train = pd.read_csv(os.path.join(path, 'final_proj_data.csv'))
test = pd.read_csv(os.path.join(path, 'final_proj_test.csv'))
sample = pd.read_csv(os.path.join(path, 'final_proj_sample_submission.csv'))

print('Завантаження бази даних:\n')
print('Навчальна база:\n', train.shape)
print('----------------------------------\n')
print('Тестова база:\n', test.shape)
print('----------------------------------\n')

#ознайомлення з базою
print(train.head())
print('----------------------------------\n')
print(train.info())
print('----------------------------------\n')
passes = train.isnull().sum().sort_values(ascending= False)
print(train.head(20))
print('----------------------------------\n')

