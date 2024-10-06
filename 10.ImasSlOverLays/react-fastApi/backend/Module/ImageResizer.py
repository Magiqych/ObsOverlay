import os
from PIL import Image

def resize_image(input_path, output_path, scale):
    """
    画像を指定された倍率でリサイズします。

    :param input_path: 入力画像のパス
    :param output_path: 出力画像のパス
    :param scale: リサイズの倍率 (例: 0.5 で元のサイズの半分)
    """
    with Image.open(input_path) as img:
        width, height = img.size
        new_size = (int(width * scale), int(height * scale))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        img.save(output_path)
        print(f"Resized image saved to {output_path}")

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # 画像が保存されているディレクトリ
    input_dir = os.path.join(script_dir, '..', 'Assets', 'UiElements')
    output_dir = os.path.join(script_dir, '..', 'Assets', 'UiElements', 'Resized')

    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # リサイズの倍率を指定
    scale = 1/3  # 例: 元のサイズの1/3

    # ディレクトリ内のすべての画像をリサイズ
    for filename in os.listdir(input_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            resize_image(input_path, output_path, scale)

if __name__ == "__main__":
    main()