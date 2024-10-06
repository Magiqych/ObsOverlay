import cv2
import pytesseract
import json
import os
import numpy as np

# pytesseractのパスを設定
pytesseract.pytesseract.tesseract_cmd = r'D:\00.Software\Tesseract\tesseract.exe'

def load_crop_config(config_path):
    with open(config_path, 'r') as file:
        return json.load(file)

def crop_image(image, crop_config):
    x, y, w, h = crop_config['x'], crop_config['y'], crop_config['width'], crop_config['height']
    return image[y:y+h, x:x+w]

def is_grayish(color):
    return abs(color[0] - color[1]) < 20 and abs(color[1] - color[2]) < 20 and abs(color[0] - color[2]) < 20

def determine_difficulty(image, difficulties, filename):
    # まずMASTER+の判定を行う
    for difficulty in difficulties:
        if difficulty['name'] == 'MASTER+':
            cropped_image = crop_image(image, difficulty)
            avg_color = cropped_image.mean(axis=0).mean(axis=0)
            print(f'File: {filename}, Difficulty: {difficulty["name"]}, Avg Color: {avg_color}')
            if avg_color[0] > 160 and avg_color[1] < 100 and avg_color[2] > 180:
                return 'MASTER+'
    
    # 次に他の難易度の判定を行う
    for difficulty in difficulties:
        cropped_image = crop_image(image, difficulty)
        avg_color = cropped_image.mean(axis=0).mean(axis=0)
        print(f'File: {filename}, Difficulty: {difficulty["name"]}, Avg Color: {avg_color}')
        if difficulty['name'] == 'DEBUT' and avg_color[0] > 200 and avg_color[1] > 180 and avg_color[2] < 150:
            return 'DEBUT'
        elif difficulty['name'] == 'REGULAR' and abs(avg_color[0] - avg_color[1]) < 10 and abs(avg_color[1] - avg_color[2]) < 10:
            return 'REGULAR'
        elif difficulty['name'] == 'PRO' and avg_color[0] > 150 and avg_color[1] < 130 and avg_color[2] > 200:
            return 'PRO'
        elif difficulty['name'] == 'MASTER' and np.all(avg_color > 180):
            return 'MASTER'
    
    # 他の領域が灰色に近いかどうかをチェック
    for difficulty in difficulties:
        if difficulty['name'] != 'MASTER+':
            cropped_image = crop_image(image, difficulty)
            avg_color = cropped_image.mean(axis=0).mean(axis=0)
            if is_grayish(avg_color):
                return 'Unknown'
    
    return 'Unknown'

def extract_song_name(cropped_image):
    return pytesseract.image_to_string(cropped_image, lang='ja')

def main():
    sample_data_dir = 'SampleData'
    crop_config_path = 'CropConfig.json'
    crop_config = load_crop_config(crop_config_path)

    for filename in os.listdir(sample_data_dir):
        if filename.endswith('.jpg'):
            image_path = os.path.join(sample_data_dir, filename)
            image = cv2.imread(image_path)

            # 難易度判定
            difficulties = crop_config['difficulties']
            difficulty = determine_difficulty(image, difficulties, filename)

            # 楽曲名取得用のクロップ
            song_name_crop_config = crop_config['song_name']
            song_name_image = crop_image(image, song_name_crop_config)
            song_name = extract_song_name(song_name_image)

            print(f'File: {filename}, Difficulty: {difficulty}, Song Name: {song_name}')

if __name__ == '__main__':
    main()