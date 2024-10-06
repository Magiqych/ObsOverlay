import json
import re
import time
import cv2
import sys
import os
import numpy as np
import imagehash
from PIL import Image, ImageTk
import pytesseract
import requests

#region クラス定義
class SelectedItem:
    '''
    選択された難易度と曲名を保持するクラス
    :param song_name: 曲名
    :param difficulty: 難易度
    @property song_name: 曲名
    @property difficulty: 難易度
    @song_name.setter: 曲名を設定
    @difficulty.setter: 難易度を設定
    _notify_listeners: リスナーに通知
    add_listener: リスナーを追加
    remove_listener: リスナーを削除
    '''
    def __init__(self):
        self._song_name = None
        self._difficulty = None
        self._listeners = []
    @property
    def song_name(self):
        return self._song_name
    @song_name.setter
    def song_name(self, value):
        if self._song_name != value:
            self._song_name = value
            self._notify_listeners('song_name', value)
    @property
    def difficulty(self):
        return self._difficulty
    @difficulty.setter
    def difficulty(self, value):
        if self._difficulty != value:
            self._difficulty = value
            self._notify_listeners('difficulty', value)
    def _notify_listeners(self, property_name, value):
        for listener in self._listeners:
            listener(property_name, value)
    def add_listener(self, listener):
        self._listeners.append(listener)
    def remove_listener(self, listener):
        self._listeners.remove(listener)

class Score:
    '''
    スコア結果を保持するクラス
    :param rawResult: スコア結果
    @property rawResult: スコア結果
    @rawResult.setter: スコア結果を設定
    _notify_listeners: リスナーに通知
    add_listener: リスナーを追加
    remove_listener: リスナーを削除
    '''
    def __init__(self):
        self._rawResult = ""
        self._listeners = []
    @property
    def rawResult(self):
        return self._rawResult
    @rawResult.setter
    def rawResult(self, value):
        if self._rawResult != value:
            self._rawResult = value
            self._notify_listeners('rawResult', value)
    def _notify_listeners(self, property_name, value):
        for listener in self._listeners:
            listener(property_name, value)
    def add_listener(self, listener):
        self._listeners.append(listener)
    def remove_listener(self, listener):
        self._listeners.remove(listener)

#endregion

#region 関数定義
def load_templates(template_dir):
    """
    テンプレート画像を読み込み、辞書に格納します。
    :param template_dir: テンプレート画像が保存されているディレクトリ
    :return: テンプレート画像の辞書
    """
    templates = {}
    for filename in os.listdir(template_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            template_path = os.path.join(template_dir, filename)
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is not None:
                templates[filename] = template
            else:
                print(f"Failed to load template: {filename}")
    return templates

# ハッシュ値と最も近い画像を検索する関数
def find_closest_image(combined_hash, song_images):
    phash_256, dhash_256 = combined_hash
    min_distance = float('inf')
    closest_image = None
    for uid, data in song_images.items():
        image_phash = imagehash.hex_to_hash(data['phash'])
        image_dhash = imagehash.hex_to_hash(data['dhash'])
        distance = (phash_256 - image_phash) + (dhash_256 - image_dhash)
        if distance < min_distance:
            min_distance = distance
            closest_image = uid
    return closest_image

# JSONファイルを読み込む関数
def load_song_images(json_path):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)

def extract_black_regions(masked_image):
    '''
    黒い領域を抽出する関数
    :param masked_image: マスク画像
    :return: 黒い領域のリスト
    '''
    mask = cv2.inRange(masked_image, np.array([0,0,0]), np.array([0,0,0]))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    regions = []
    for contour in contours:
        x1, y1, w, h = cv2.boundingRect(contour)
        x2 = x1 + w
        y2 = y1 + h
        regions.append([x1, y1, x2, y2])
    return regions
#endregion

#region イベントハンドラ
def on_selected_item_property_change(property_name, value):
    if(selected_item.song_name is not None and selected_item.difficulty is not None):
        print(f'{selected_item.song_name} - {selected_item.difficulty}')
        url = "http://localhost:8000/select_song"
        message = {"SongName": selected_item.song_name, "Level": selected_item.difficulty}
        requests.post(url, json=message)

def on_score_property_change(property_name, value):
    if(score.rawResult is not None and score.rawResult != ""):
        url = "http://localhost:8000/set_score"
        message = {"RawScore": score.rawResult}
        requests.post(url, json=message)
        print(score.rawResult)
#endregion

#region 変数定義
# スクリプト自身のディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
# JSONファイルのパス
json_path = os.path.join(script_dir, 'Assets','SongImageHash.json')
# JSONファイルを読み込む
song_images = load_song_images(json_path)
FrameSkipper = 0
templates = []
selected_item = SelectedItem()
selected_item.add_listener(on_selected_item_property_change)
score = Score()
score.add_listener(on_score_property_change)
pytesseract.pytesseract.tesseract_cmd = r'D:\00.Software\Tesseract\tesseract.exe'
#endregion

def initialize_capture_device(device_id):
    """
    キャプチャデバイスを初期化します。

    :param device_id: キャプチャデバイスのID
    :return: キャプチャオブジェクト
    """
    cap = cv2.VideoCapture(device_id)
    if not cap.isOpened():
        raise Exception(f"Failed to open capture device with ID {device_id}")
    return cap

def process_frame(frame):
    """
    フレームを処理します。将来的にOCR解析などの処理を追加します。

    :param frame: キャプチャしたフレーム
    :return: 処理結果
    """
    global FrameSkipper
    global templates
    global selected_item
    global score
    
    # 画像保存用
    # cv2.imwrite("Mv.png", frame)
    # print("frame.png saved")
    # time.sleep(10000000000000)
    
    if FrameSkipper != 0:
        FrameSkipper -= 1
        return
    #　フレームをコピー
    frameCopy = frame
    # スコア画面検出
    Score_np = None
    Score_np = np.sum(np.array(cv2.subtract(frameCopy, templates['ScoreDetect.png'])), axis=None)
    threshold = 500000
    if Score_np < threshold:
        #スコア画面が出たらOCR解析
        RawScoreText = ""
        MaskedImage = cv2.subtract(frameCopy, templates['ScoreInfo.png'])
        regions = extract_black_regions(templates['ScoreInfo.png'])
        # ソート
        regions_sorted = sorted(regions, key=lambda r: r[0])
        regions_sorted = sorted(regions_sorted, key=lambda r: r[1])
        for i, region in enumerate(regions_sorted):
            x1, y1, x2, y2 = region
            CropImage = MaskedImage[y1:y2,x1:x2]
            gray = cv2.cvtColor(CropImage, cv2.COLOR_BGR2GRAY)
            # 二値化
            _, binary = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
            #アンチエイリアスを使用して拡大
            scale_factor = 5
            resized_binary = cv2.resize(binary, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
            # OCRを実行（英語と数字のみ）
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
            text = pytesseract.image_to_string(resized_binary, config=custom_config)
            if i == len(regions_sorted) - 1:
                RawScoreText += re.sub(r'\D', '', text)
            else:
                RawScoreText += re.sub(r'\D', '', text) + ","
        # スコアチェック
        score_list = RawScoreText.split(",")
        bad_index = 3
        for i in range(len(score_list)):
            if score_list[i].startswith("0") and score_list[i] != "0":
                score_list[i] = "8" + score_list[i][1:]
            if score_list[i] == "":
                score_list[i] = "0"
                bad_index -= 1
            if bad_index == 0:
                return
        # 変更されたリストを再度カンマで結合
        RawScoreText = ",".join(score_list)
        score.rawResult = RawScoreText
        return
    #スタミナ消費画面が出たらフレームスキップ
    Stamina = np.sum(np.array(cv2.subtract(frameCopy, templates['Stamina.png'])), axis=None)
    threshold = 1200000
    if Stamina < threshold:
        FrameSkipper = 100
        return
    # basic,master+,witch,grandの判定を行う
    Basic = np.sum(np.array(cv2.subtract(frameCopy, templates['Basic.png'])), axis=None)
    MasterPlus = np.sum(np.array(cv2.subtract(frameCopy, templates['Master+.png'])), axis=None)
    Witch = np.sum(np.array(cv2.subtract(frameCopy, templates['Witch.png'])), axis=None)
    Grand = np.sum(np.array(cv2.subtract(frameCopy, templates['Grand.png'])), axis=None)
    threshold = 140000
    if Basic > threshold and MasterPlus > threshold and Witch > threshold and Grand > threshold:
        #ライブ画面以外と判断スキップ
        return
    else:
        # 最小値を持つテンプレートを見つける
        min_value = min(Basic, MasterPlus, Witch, Grand)
        # 最小値を持つテンプレートの変数名をスイッチ
        if min_value == Basic:
            #Basicの場合はDebut,Regular,Pro,Masterの判定を行う
            Debut = np.sum(np.array(cv2.subtract(frameCopy, templates['Debut.png'])), axis=None)
            Regular = np.sum(np.array(cv2.subtract(frameCopy, templates['Regular.png'])), axis=None)
            Pro = np.sum(np.array(cv2.subtract(frameCopy, templates['Pro.png'])), axis=None)
            Master = np.sum(np.array(cv2.subtract(frameCopy, templates['Master.png'])), axis=None)
            Mv = np.sum(np.array(cv2.subtract(frameCopy, templates['Mv.png'])), axis=None)
            threshold = 140000
            if Debut < threshold and Regular < threshold and Pro < threshold \
                and Master < threshold and Mv < threshold:
                #何か違うものが描写されている場合はスキップ
                return
            min_value = min(Debut, Regular, Pro, Master, Mv)
            if min_value == Debut:
                selected_item.difficulty = "DEBUT"
            elif min_value == Regular:
                selected_item.difficulty = "REGULAR"
            elif min_value == Pro:
                selected_item.difficulty = "PRO"
            elif min_value == Master:
                selected_item.difficulty = "MASTER"
            elif min_value == Mv:
                selected_item.difficulty = None
            else:
                return
        elif min_value == MasterPlus:
            selected_item.difficulty = "MASTER+"
        elif min_value == Witch:
            selected_item.difficulty = "WITCH"
        elif min_value == Grand:
            selected_item.difficulty = "GRAND"
        else:
            return
    
    #曲を判定する
    CropImage = frameCopy[120:315,395:540]
    rgb_image = cv2.cvtColor(CropImage, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    phash_256 = imagehash.phash(pil_image, hash_size=16)
    dhash_256 = imagehash.dhash(pil_image, hash_size=32)
    combined_hash = (phash_256, dhash_256)
    selected_item.song_name = find_closest_image(combined_hash, song_images)
    return

def process_video(video_path):
    """
    動画ファイルを処理します。

    :param video_path: 動画ファイルのパス
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception(f"Failed to open video file {video_path}")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            processed_frame = process_frame(frame)
            time.sleep(1)
            # cv2.imshow('Processed Frame', processed_frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
    finally:
        cap.release()
        cv2.destroyAllWindows()

def process_image(image_path):
    """
    画像ファイルを処理します。

    :param image_path: 画像ファイルのパス
    """
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Failed to open image file {image_path}")
    process_frame(image)

def main(input_source):
    """
    メイン関数。入力ソースに応じて処理を行います。

    :param input_source: 入力ソース（動画ファイル、画像ファイル、デバイスID）
    """
    if os.path.isfile(input_source):
        # ファイルの場合
        file_ext = os.path.splitext(input_source)[1].lower()
        if file_ext in ['.mp4', '.avi', '.mov', '.mkv']:
            process_video(input_source)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
            process_image(input_source)
        else:
            raise Exception(f"Unsupported file type: {file_ext}")
    else:
        # デバイスIDの場合
        source = input_source
        cap = None
        if not source.isdigit():
            index, backend = map(int, source.split('-'))
            cap = cv2.VideoCapture(index, backend)
        else:
            cap = cv2.VideoCapture(source)


        try:
            while True:
                ret, frame = cap.read()
                if frame is None:
                    time.sleep(1)
                else:
                    process_frame(frame)
        finally:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python OcrCli.py <input_source>")
    #     sys.exit(1)
    # input_source = sys.argv[1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_source = os.path.join(script_dir, "Assets", "Mask")
    templates = load_templates(template_source)
    #input_source = os.path.join(script_dir, "Assets", "TestData2", "ScoreBasicRight.png")
    input_source = "4-700"
    main(input_source)