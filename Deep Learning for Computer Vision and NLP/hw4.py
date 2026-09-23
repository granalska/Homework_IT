import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
import torch
import torch.nn as nn
from torch.utils.data import TensorDataset, DataLoader
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OrdinalEncoder
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

#завантажуємо дані
url = 'https://raw.githubusercontent.com/goitacademy/MACHINE-LEARNING-NEO/main/datasets/mod_05_topic_10_various_data.pkl'

with urllib.request.urlopen(url) as response:
    data = pickle.load(response)

autos = data['autos']

#робимо нову ознаку
autos['stroke_ratio'] = autos['stroke'] / autos['bore']

#вибираємо що будемо прогнозувати
y = autos['price']

#забираємо ціну з даних
X = autos.drop('price', axis=1)

#знаходимо колонки з текстом
cat = X.select_dtypes(include='object').columns

#перетворюємо текст в числа
encoder = OrdinalEncoder(handle_unknown='use_encoded_value', unknown_value=-1)
X[cat] = encoder.fit_transform(X[cat])

#ділимо дані
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#нормалізуємо дані
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

#нормалізуємо ціну
y_scaler = StandardScaler()
y_train = y_scaler.fit_transform(y_train.values.reshape(-1, 1))
y_test = y_scaler.transform(y_test.values.reshape(-1, 1))

#робимо тензори
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train, dtype=torch.float32)
y_test = torch.tensor(y_test, dtype=torch.float32)

#створюємо нейронну мережу
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(nn.Linear(X_train.shape[1], 32), nn.ReLU(), nn.Linear(32, 16), nn.ReLU(), nn.Linear(16, 1))

    def forward(self, x):
        return self.model(x)

#створюємо модель
model = Net()

#функція помилки
loss_func = nn.MSELoss()

#оптимізатор
optimizer = torch.optim.SGD(model.parameters(), lr=0.001)

#робимо батчі
data = TensorDataset(X_train, y_train)
loader = DataLoader(data, batch_size=32, shuffle=True)

#кількість епох
epochs = 100
losses = []

#навчаємо модель
for epoch in range(epochs):
    total_loss = 0

    for xb, yb in loader:
        pred = model(xb)
        loss = loss_func(pred, yb)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    loss = total_loss / len(loader)
    losses.append(loss)

    if (epoch + 1) % 10 == 0:
        print('епоха:', epoch + 1, 'помилка:', loss)

#робимо прогноз
model.eval()

with torch.no_grad():
    pred = model(X_test).numpy()

#повертаємо нормальні ціни
pred = y_scaler.inverse_transform(pred)
y_test = y_scaler.inverse_transform(y_test.numpy())

#рахуємо результати
mse = mean_squared_error(y_test, pred)
mae = mean_absolute_error(y_test, pred)
r2 = r2_score(y_test, pred)

print('\nрезультати:')
print('MSE:', mse)
print('MAE:', mae)
print('R2:', r2)

#малюємо помилку
plt.plot(losses)
plt.xlabel('епоха')
plt.ylabel('помилка')
plt.title('зміна помилки під час навчання')
plt.show()

#малюємо справжні і прогнозовані ціни
plt.scatter(y_test, pred)
plt.xlabel('справжня ціна')
plt.ylabel('прогнозована ціна')
plt.title('справжні та прогнозовані значення')
plt.show()