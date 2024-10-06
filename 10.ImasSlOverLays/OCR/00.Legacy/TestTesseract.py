import sys
import pytesseract
from PIL import Image

def image_to_text(image_path):
    # 画像を読み込む
    img = Image.open(r'D:\repos\ObsOverlay\10.ImasSlOverLays\OCR\CapturedImages\SampleData\0e6232fb-a56b-4304-be0a-3713a493cf3e.jpg')
    pytesseract.pytesseract.tesseract_cmd = r'D:\00.Software\Tesseract\tesseract.exe'
    pytesseract.get_languages(config='ja')
    # TesseractでOCRを実行
    text = pytesseract.image_to_string(img, lang='jpn')

    return text

if __name__ == "__main__":
    text = image_to_text("")
    print(text)
        