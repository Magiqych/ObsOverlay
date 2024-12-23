import os
from PIL import Image, ImageChops

# スクリプト自身のパスを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# データセットのディレクトリを相対パスで指定
data_dirs = [
    os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Tire1'),
    os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Tire2'),
    os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Tire3'),
    os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Score')
]

# マスク画像のパス
mask_paths = {
    'Tire1': os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Tire1', 'Tire1Mask.png'),
    'Tire2': os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Tire2', 'Tire2Mask.png'),
    'Tire3': os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Tire3', 'Tire3Mask.png'),
    'Score': os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Score', 'ScoreMask.png')
}

# トリミングされた画像の保存ディレクトリ
output_dir = os.path.join(script_dir, '..', 'train_data', 'SceanDetect', 'Cropped')

def trim_image(image, mask):
    # マスクの黒い部分を除去
    mask = mask.convert('L')  # グレースケールに変換
    mask = ImageChops.invert(mask)  # マスクを反転
    image.putalpha(mask)  # アルファチャンネルとしてマスクを追加
    bbox = image.getbbox()  # バウンディングボックスを取得
    return image.crop(bbox)  # トリミング

for data_dir in data_dirs:
    category = os.path.basename(data_dir)
    mask_path = mask_paths.get(category)
    if not mask_path:
        continue

    mask = Image.open(mask_path)
    for root, _, files in os.walk(data_dir):
        for filename in files:
            if filename.endswith('.png') and 'Mask' not in filename:
                image_path = os.path.join(root, filename)
                try:
                    image = Image.open(image_path)
                except:
                    continue
                trimmed_image = trim_image(image, mask)
                
                # 出力ディレクトリを作成
                relative_path = os.path.relpath(root, data_dir)
                output_subdir = os.path.join(output_dir, category, relative_path)
                os.makedirs(output_subdir, exist_ok=True)
                
                output_path = os.path.join(output_subdir, filename)
                trimmed_image.save(output_path)

print("トリミングが完了しました。")