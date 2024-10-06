# coding: utf-8
import json
import os
from paddleocr import PaddleOCR
from PIL import Image, ImageEnhance, ImageFont, ImageDraw
import numpy as np
import cv2

def run_ocr(img_path):
    """ OCRメイン関数"""
    #PaddleOCRを定義
    ocr = PaddleOCR(
        use_gpu=False, #GPUあるならTrue
        lang = "japan", #英語OCRならen
        det_limit_side_len=1920, #画像サイズが960に圧縮されないように必須設定
        max_text_length = 30, #検証してないがテキスト最大長のパラメータ。今回は不要だが紹介
        )

    directory = 'data'
    for filename in os.listdir(directory):
            if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                img_path = os.path.join(directory, filename)
                #画像読み込み＋前処理(適当)+PaddleOCR入力用にnpへ
                im = Image.open(img_path).convert('L')
                enhancer= ImageEnhance.Contrast(im) #コントラストを上げる
                im_con = enhancer.enhance(2.0) #コントラストを上げる
                np_img = np.asarray(im_con)
                #PaddleOCRでOCR ※cls(傾き設定)は矩形全体での補正なので1文字1文字の補正ではない為不要
                result = ocr.ocr(img = np_img, det=True, rec=True, cls=False)
                save_result_to_json(result,img_path+'.json') #結果をjsonで保存

# result の内容を JSON ファイルに保存する関数
def save_result_to_json(result, filename='data/result.json'):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
        print(f"結果が {filename} に保存されました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == '__main__':
    img_path = "data/test.png"
    run_ocr(img_path)