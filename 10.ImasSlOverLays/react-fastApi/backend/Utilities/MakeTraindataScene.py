'''
シーンディレクションのトレーニングデータを収集するためのスクリプト
'''

import os
import cv2
import uuid
import numpy as np
import keyboard  # キーボード入力を監視するためのライブラリ
from PIL import Image, ImageChops

# スクリプト自身のパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# トレーニングデータのディレクトリを設定
train_data_dirs = {
    '1':os.path.join(script_dir, '..', 'train_data', 'SceanDetect','Tire1'),
    '2':os.path.join(script_dir, '..', 'train_data', 'SceanDetect','Tire2'),
    '3':os.path.join(script_dir, '..', 'train_data', 'SceanDetect','Tire3'),
    '4':os.path.join(script_dir, '..', 'train_data', 'SceanDetect','Score')
}

# マスク画像のパスを設定
mask_paths = {
    '1': os.path.join(script_dir, '..', 'Assets', 'Tire1Mask.png'),
    '2': os.path.join(script_dir, '..', 'Assets', 'Tire2Mask.png'),
    '3': os.path.join(script_dir, '..', 'Assets', 'Tire3Mask.png'),
    '4': os.path.join(script_dir, '..', 'Assets', 'ScoreMask.png')
}

# キャプチャデバイスの設定
cap = cv2.VideoCapture(4, 700)
if not cap.isOpened():
    raise Exception("Failed to open capture device")

def apply_mask(frame, mask_path):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise Exception(f"Failed to load mask image: {mask_path}")
    # マスクを反転
    mask = cv2.bitwise_not(mask)
    # マスクを二値化
    _, binary_mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)
    # アルファチャンネルを追加
    b, g, r = cv2.split(frame)
    alpha = binary_mask
    frame = cv2.merge([b, g, r, alpha])
    # バウンディングボックスを取得
    x, y, w, h = cv2.boundingRect(binary_mask)
    return frame[y:y+h, x:x+w]  # トリミング

def save_frame(frame, tire_type):
    uid = str(uuid.uuid4())
    save_path = os.path.join(train_data_dirs[tire_type], f'{uid}.png')
    cv2.imwrite(save_path, frame)
    print(f"Saved frame to {save_path}")

recording = False
tire_type = None

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to capture frame")
        break

    if keyboard.is_pressed('q'):
        break
    elif keyboard.is_pressed('1'):
        tire_type = '1'
        recording = True
    elif keyboard.is_pressed('2'):
        tire_type = '2'
        recording = True
    elif keyboard.is_pressed('3'):
        tire_type = '3'
        recording = True
    elif keyboard.is_pressed('4'):
        tire_type = '4'
        recording = True
    if recording and tire_type:
        masked_frame = apply_mask(frame, mask_paths[tire_type])
        save_frame(masked_frame, tire_type)

cap.release()