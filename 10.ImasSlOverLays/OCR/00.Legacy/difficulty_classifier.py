import os
import numpy as np
import cv2
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split

# ディレクトリとクラスの設定
base_dir = 'CapturedImages/Levels'
classes = ['DEBUT', 'REGULAR', 'PRO', 'MASTER', 'MASTER+']
mask_path = os.path.join(base_dir, 'Mask.jpg')

# マスク画像の読み込み
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
mask = cv2.resize(mask, (128, 128))  # マスクのリサイズ
mask = mask / 255.0  # 正規化

# 画像データとラベルのリスト
images = []
labels = []

# 画像の読み込みとマスクの適用
for label, class_name in enumerate(classes):
    class_dir = os.path.join(base_dir, class_name)
    for img_name in os.listdir(class_dir):
        img_path = os.path.join(class_dir, img_name)
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # グレースケールに変換
        img = cv2.resize(img, (128, 128))  # 画像のリサイズ
        masked_img = img * mask  # マスクの適用
        images.append(masked_img)
        labels.append(label)

# データの正規化と変換
images = np.array(images)
images = images.reshape(images.shape[0], images.shape[1], images.shape[2], 1)  # チャンネル次元を追加
images = images / 255.0  # 正規化
labels = to_categorical(labels, num_classes=len(classes))

# トレーニングとテストデータに分割
X_train, X_test, y_train, y_test = train_test_split(images, labels, test_size=0.2, random_state=42)

# モデルの構築
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(128, 128, 1)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(classes), activation='softmax')
])

# モデルのコンパイル
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# モデルの学習
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test))

# モデルの保存
model.save('Models/difficulty_classifier_model.keras')