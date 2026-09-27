import kagglehub
import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, Subset
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay


#завантажуємо дані
path = kagglehub.dataset_download('puneet6060/intel-image-classification')

train_path = path + '/seg_train/seg_train'
test_path = path + '/seg_test/seg_test'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

image_size = 96
batch_size = 32
epochs = 5


#робимо перетворення для картинок
train_transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.RandomHorizontalFlip(),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])

test_transform = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])


#завантажуємо картинки
train_full = datasets.ImageFolder(train_path, transform=train_transform)
val_full = datasets.ImageFolder(train_path, transform=test_transform)
test_data = datasets.ImageFolder(test_path, transform=test_transform)

classes = train_full.classes
num_classes = len(classes)

print('класи:', classes)
print('кількість класів:', num_classes)


#ділимо дані на навчальні та валідаційні
generator = torch.Generator().manual_seed(42)
indices = torch.randperm(len(train_full), generator=generator)

train_size = int(0.8 * len(train_full))
train_indices = indices[:train_size]
val_indices = indices[train_size:]

train_data = Subset(train_full, train_indices)
val_data = Subset(val_full, val_indices)


#створюємо DataLoader
train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_data, batch_size=batch_size, shuffle=False)


#створюємо модель ResNet18
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

for param in model.parameters():
    param.requires_grad = False

input_features = model.fc.in_features
last_layer = nn.Linear(input_features, num_classes)

model.fc = last_layer
model = model.to(device)


#створюємо функцію помилки та оптимізатор
loss_func = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.fc.parameters(), lr=0.001)

train_losses = []
val_losses = []
train_accuracy = []
val_accuracy = []


#навчаємо модель
for epoch in range(epochs):
    model.train()

    total_loss = 0
    correct = 0
    total = 0

    for xb, yb in train_loader:
        xb = xb.to(device)
        yb = yb.to(device)

        pred = model(xb)
        loss = loss_func(pred, yb)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss = total_loss + loss.item()

        predicted = torch.argmax(pred, dim=1)
        correct = correct + (predicted == yb).sum().item()
        total = total + yb.size(0)

    train_loss = total_loss / len(train_loader)
    train_acc = correct / total

    train_losses.append(train_loss)
    train_accuracy.append(train_acc)


    #перевіряємо модель на валідаційних даних
    model.eval()

    total_val_loss = 0
    correct_val = 0
    total_val = 0

    with torch.no_grad():
        for xb, yb in val_loader:
            xb = xb.to(device)
            yb = yb.to(device)

            pred = model(xb)
            loss = loss_func(pred, yb)

            total_val_loss = total_val_loss + loss.item()

            predicted = torch.argmax(pred, dim=1)
            correct_val = correct_val + (predicted == yb).sum().item()
            total_val = total_val + yb.size(0)

    val_loss = total_val_loss / len(val_loader)
    val_acc = correct_val / total_val

    val_losses.append(val_loss)
    val_accuracy.append(val_acc)

    print('епоха:', epoch + 1, 'помилка:', round(train_loss, 4), 'val помилка:', round(val_loss, 4), 'точність:', round(train_acc, 4), 'val точність:', round(val_acc, 4))


#перевіряємо модель на тестових даних
model.eval()

all_predictions = []
all_targets = []

with torch.no_grad():
    for xb, yb in test_loader:
        xb = xb.to(device)

        pred = model(xb)
        predicted = torch.argmax(pred, dim=1)

        all_predictions.extend(predicted.cpu().numpy())
        all_targets.extend(yb.numpy())


#рахуємо результати
accuracy = accuracy_score(all_targets, all_predictions)
f1 = f1_score(all_targets, all_predictions, average='weighted')

print('\nрезультати:')
print('Accuracy:', accuracy)
print('F1:', f1)


#будуємо матрицю помилок
cm = confusion_matrix(all_targets, all_predictions)

disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classes)
disp.plot(xticks_rotation=45)
plt.title('матриця помилок')
plt.tight_layout()
plt.savefig('confusion_matrix.png')
plt.show()


#будуємо графік помилки
plt.plot(train_losses, label='навчання')
plt.plot(val_losses, label='валідація')
plt.xlabel('епоха')
plt.ylabel('помилка')
plt.title('зміна помилки під час навчання')
plt.legend()
plt.savefig('loss.png')
plt.show()


#будуємо графік точності
plt.plot(train_accuracy, label='навчання')
plt.plot(val_accuracy, label='валідація')
plt.xlabel('епоха')
plt.ylabel('точність')
plt.title('зміна точності під час навчання')
plt.legend()
plt.savefig('accuracy.png')
plt.show()


#показуємо приклади прогнозів
images, labels = next(iter(test_loader))

with torch.no_grad():
    pred = model(images.to(device))
    pred = torch.argmax(pred, dim=1).cpu()

plt.figure(figsize=(12, 6))

for i in range(6):
    image = images[i].permute(1, 2, 0).numpy()

    image = image * np.array([0.229, 0.224, 0.225])
    image = image + np.array([0.485, 0.456, 0.406])
    image = np.clip(image, 0, 1)

    plt.subplot(2, 3, i + 1)
    plt.imshow(image)
    plt.title('справжній: ' + classes[labels[i]] + '\nпрогноз: ' + classes[pred[i]])
    plt.axis('off')

plt.tight_layout()
plt.savefig('predictions.png')
plt.show()