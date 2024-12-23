import os
import cv2
import numpy as np
import random

# スクリプト自身のパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# データセットのディレクトリを相対パスで指定
input_dir = os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Score', 'Score')
output_dir = os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Score', 'Score_Modified')
os.makedirs(output_dir, exist_ok=True)

# マスク画像のパス
mask_path = os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Score', 'TargetMask.png')

def apply_random_color(image, mask_path):
    # マスク画像を読み込み
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        raise Exception(f"Failed to load mask image: {mask_path}")

    # マスクの黒い領域を検出
    black_mask = mask == 0

    # ランダムな色を生成
    random_color = [random.randint(0, 255) for _ in range(3)]

    # 黒い領域をランダムな色で塗りつぶす
    image[black_mask, :3] = random_color

    return image

# ディレクトリ内の画像を処理
for filename in os.listdir(input_dir):
    if filename.endswith('.png'):
        image_path = os.path.join(input_dir, filename)
        image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
        if image is None:
            continue

        modified_image = apply_random_color(image, mask_path)
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, modified_image)
        print(f"Saved modified image to {output_path}")

print("処理が完了しました。")