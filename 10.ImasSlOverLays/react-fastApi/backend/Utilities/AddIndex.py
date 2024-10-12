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
    data_dir = os.path.join(base_data_dir, category)
    if not os.path.isdir(data_dir):
        continue
    # データセットの読み込み
    train_dataset = datasets.ImageFolder(data_dir, transform=transform)
    # クラス数とクラスラベルのマッピングを取得
    num_classes = len(train_dataset.classes)
    class_to_idx = train_dataset.class_to_idx
    model_save_path = os.path.join(script_dir, '..', 'Models', f'model_{category}.pth')
    # 既存のモデルを読み込み
    checkpoint = torch.load(model_save_path)
    model_state_dict = checkpoint['model_state_dict'] if 'model_state_dict' in checkpoint else checkpoint

    # 新しいチェックポイントを作成
    new_checkpoint = {
        'model_state_dict': model_state_dict,
        'num_classes': num_classes,
        'class_to_idx': class_to_idx
    }
    
    torch.save(new_checkpoint, model_save_path)