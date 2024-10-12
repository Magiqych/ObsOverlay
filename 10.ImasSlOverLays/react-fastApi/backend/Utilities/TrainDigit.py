import os
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader, random_split
from torchvision import transforms

# データセットクラスの定義
class DigitDataset(Dataset):
    def __init__(self, data_dir, transform=None):
        self.data_dir = data_dir
        self.transform = transform
        self.images = []
        self.labels = []
        self.load_data()

    def load_data(self):
        for label in os.listdir(self.data_dir):
            label_dir = os.path.join(self.data_dir, str(label))
            if not os.path.exists(label_dir):
                continue
            for filename in os.listdir(label_dir):
                if filename.endswith('.png'):
                    img_path = os.path.join(label_dir, filename)
                    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                    img = cv2.resize(img, (28, 28))
                    self.images.append(img)
                    if label == 'Other':  # Otherの場合
                        self.labels.append(10)  # 空白文字を表すラベルを10に設定
                    else:
                        self.labels.append(int(label))

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, torch.tensor(label)  # ラベルをテンソルに変換

# データ拡張と前処理の設定
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomRotation(10),
    transforms.RandomResizedCrop(28, scale=(0.8, 1.0)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# データセットの作成と分割
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'train_data','Digits')
dataset = DigitDataset(data_dir, transform=transform)
train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size
train_dataset, val_dataset = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

# シンプルなCNNモデルの定義
class SimpleCNN(nn.Module):
    def __init__(self):
        super(SimpleCNN, self).__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 11)  # クラス数を11に変更
        self.relu = nn.ReLU()
        self.softmax = nn.LogSoftmax(dim=1)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(-1, 64 * 7 * 7)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return self.softmax(x)

# モデルの初期化
model = SimpleCNN()

# 損失関数とオプティマイザの定義
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# 早期停止の設定
early_stopping_patience = 25
best_val_loss = float('inf')
patience_counter = 0

# モデルのトレーニング
num_epochs = 50  # 最大エポック数を設定
for epoch in range(num_epochs):
    model.train()
    running_loss = 0.0
    for images, labels in train_loader:
        # 勾配をリセット
        optimizer.zero_grad()

        # 順伝播
        outputs = model(images)
        loss = criterion(outputs, labels)

        # 逆伝播とオプティマイザのステップ
        loss.backward()
        optimizer.step()

        # 損失の累積
        running_loss += loss.item()

    print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {running_loss/len(train_loader):.4f}')

    # 検証データでの評価
    model.eval()
    val_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            outputs = model(images)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    val_loss /= len(val_loader)
    accuracy = 100 * correct / total
    print(f'Validation Loss: {val_loss:.4f}, Validation Accuracy: {accuracy:.2f}%')

    # 早期停止のチェック
    if val_loss < best_val_loss:
        best_val_loss = val_loss
        patience_counter = 0
        # モデルの保存
        model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'Models', 'digit_classifier_v2.pth')
        torch.save({
            'model_state_dict': model.state_dict(),
            'num_classes': 11,
            'class_to_idx': {str(i): i for i in range(10)} | {'Other': 10}
        }, model_path)
    else:
        patience_counter += 1
        if patience_counter >= early_stopping_patience:
            print("Early stopping")
            break

print('Finished Training')