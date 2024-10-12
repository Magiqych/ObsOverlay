import os
import winsound
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms, models
from torch.utils.data import DataLoader, random_split
import matplotlib.pyplot as plt
from PIL import ImageFile

# トランケートされた画像を無視する設定
ImageFile.LOAD_TRUNCATED_IMAGES = True

# スクリプト自身のパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# データセットのベースディレクトリを相対パスで指定
base_data_dir = os.path.join(script_dir, '..', 'train_data', 'SceanDetect')

# データの前処理
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

# 各サブディレクトリごとにモデルを作成
for category in os.listdir(base_data_dir):
# for category in ['Tire1', 'Tire2', 'Tire3']:
    winsound.Beep(440, 2000)
    data_dir = os.path.join(base_data_dir, category)
    if not os.path.isdir(data_dir):
        continue

    # データセットの読み込み
    dataset = datasets.ImageFolder(data_dir, transform=transform)

    # データセットをトレーニングとテストに分割
    train_size = int(0.8 * len(dataset))
    test_size = len(dataset) - train_size
    train_dataset, test_dataset = random_split(dataset, [train_size, test_size])

    # データローダーの作成
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False)

    # モデルの定義（ResNet18を使用）
    model = models.resnet18(pretrained=True)
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, len(dataset.classes))

    # 損失関数とオプティマイザの定義
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    # トレーニングループ
    num_epochs = 10
    train_losses = []
    test_losses = []
    train_accuracies = []
    test_accuracies = []
    winsound.Beep(1000, 500)
    for epoch in range(num_epochs):
        model.train()
        running_loss = 0.0
        correct = 0
        total = 0
        for inputs, labels in train_loader:
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()
            
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
        train_losses.append(running_loss / len(train_loader))
        train_accuracies.append(100 * correct / total)

        model.eval()
        running_loss = 0.0
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, labels in test_loader:
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                running_loss += loss.item()
                
                _, predicted = torch.max(outputs, 1)
                total += labels.size(0)
                correct += (predicted == labels).sum().item()
        test_losses.append(running_loss / len(test_loader))
        test_accuracies.append(100 * correct / total)

        print(f'Category: {category}, Epoch {epoch+1}/{num_epochs}, Train Loss: {train_losses[-1]}, Test Loss: {test_losses[-1]}, Train Accuracy: {train_accuracies[-1]}, Test Accuracy: {test_accuracies[-1]}')
        winsound.Beep(880, 500)
    # モデルの保存
    model_save_path = os.path.join(script_dir, '..', 'Models', f'model_{category}.pth')
    torch.save({
        'model_state_dict': model.state_dict(),
        'num_classes': len(dataset.classes),
        'class_to_idx': dataset.class_to_idx
    }, model_save_path)
    winsound.Beep(440, 1000)
winsound.Beep(440, 3000)