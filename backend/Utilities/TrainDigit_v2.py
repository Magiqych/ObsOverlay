import os
import random
import cv2
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torchvision import models, transforms
from torch.utils.data import Dataset, DataLoader
from torch.utils.tensorboard.writer import SummaryWriter
import torch.optim as optim

# 定数の定義
NUM_CLASSES = 11  # 0-9の数字と空白文字
LABELS = [str(i) for i in range(10)] + [' ']  # 0-9の数字と空白文字

# スクリプトのパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, '..', 'train_data', 'Digits')

# データセットフォルダ内のすべての画像を読み込む関数
def load_all_images(data_dir):
    images = []
    labels = []
    for folder in os.listdir(data_dir):
        folder_path = os.path.join(data_dir, folder)
        for filename in os.listdir(folder_path):
            if filename.endswith('.png'):
                image_path = os.path.join(folder_path, filename)
                image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # 二値化画像として読み込む
                _, binary_image = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY)
                images.append(binary_image)
                if folder == 'Other':
                    labels.append(10)
                else:
                    labels.append(int(folder))
    return images, labels

# 縦に65にリサイズし、縦横比を維持する関数
def resize_image(image, target_height=65):
    height, width = image.shape
    aspect_ratio = width / height
    new_width = int(target_height * aspect_ratio)
    resized_image = cv2.resize(image, (new_width, target_height), interpolation=cv2.INTER_LANCZOS4)
    return resized_image, new_width, height

# ランダムに左右に数字の切れ端を追加する関数
def add_random_edge(image, all_images):
    image, new_width, original_height = resize_image(image)
    height, width = image.shape
    new_image = np.zeros((65, 40), dtype=np.uint8)
    edge_width = random.randint(1, 10)  # ランダムな切れ端の幅
    random_image = random.choice(all_images)  # ランダムな画像を選択
    random_image, _, _ = resize_image(random_image)
    
    if random.choice([True, False]):
        # 左側に切れ端を追加
        edge = random_image[:, :edge_width]
        new_image[:, :edge_width] = edge
        new_image[:, edge_width:edge_width + width] = image[:, :min(width, 40 - edge_width)]
    else:
        # 右側に切れ端を追加
        edge = random_image[:, -edge_width:]
        new_image[:, :min(width, 40 - edge_width)] = image[:, :min(width, 40 - edge_width)]
        new_image[:, min(width, 40 - edge_width):min(width, 40 - edge_width) + edge_width] = edge
    return new_image

# カスタムデータセットクラス
class DigitDataset(Dataset):
    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        return image, label

# データの準備
images, labels = load_all_images(data_dir)
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.Resize((65, 40)),
    transforms.ToTensor(),
    transforms.Normalize((0.5,), (0.5,))
])

# データ拡張を適用
augmented_images = [add_random_edge(image, images) for image in images]
augmented_labels = labels * 2  # 拡張した分ラベルも増やす

# オリジナルと拡張データを結合
all_images = images + augmented_images
all_labels = labels + augmented_labels

dataset = DigitDataset(all_images, all_labels, transform=transform)
dataloader = DataLoader(dataset, batch_size=32, shuffle=True)

# MobileNetV2の定義
def create_mobilenetv2_model(num_classes):
    model = models.mobilenet_v2(weights='IMAGENET1K_V1')
    # 最初の畳み込み層を変更して、1チャンネルの入力を受け取るようにする
    model.features[0][0] = nn.Conv2d(1, model.features[0][0].out_channels, kernel_size=3, stride=2, padding=1, bias=False)
    model.classifier[1] = nn.Linear(model.last_channel, num_classes)  # 出力層を指定されたクラス数に変更
    return model

model = create_mobilenetv2_model(NUM_CLASSES)

# 損失関数と最適化アルゴリズムの設定
num_epochs = 25
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)
scheduler = optim.lr_scheduler.OneCycleLR(
    optimizer=optimizer,
    max_lr=1e-3,
    total_steps=len(dataloader) * num_epochs
)
# TensorBoardの設定
writer = SummaryWriter('runs/digit_classification')

# 学習ループ
for epoch in range(num_epochs):
    running_loss = 0.0
    for i, data in enumerate(dataloader, 0):
        inputs, labels = data
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        scheduler.step()
        running_loss += loss.item()
    # 検証ループ
    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for i, data in enumerate(dataloader, 0):
            inputs, labels = data
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            val_loss += loss.item()
    # エポックごとにログを出力
    avg_train_loss = running_loss / len(dataloader)
    avg_val_loss = val_loss / len(dataloader)
    current_lr = optimizer.param_groups[0]['lr']
    print(f'[Epoch {epoch + 1}] train loss: {avg_train_loss:.3f}, val loss: {avg_val_loss:.3f}, lr: {current_lr:.6f}')
    writer.add_scalar('training loss', avg_train_loss, epoch)
    writer.add_scalar('validation loss', avg_val_loss, epoch)
    writer.add_scalar('learning rate', current_lr, epoch)


print('Finished Training')

# モデルとラベルのマッピングを保存
model_save_path = 'model.pth'
torch.save({
    'model_state_dict': model.state_dict(),
    'label_mapping': LABELS
}, model_save_path)
print(f'Model and label mapping saved to {model_save_path}')

writer.close()