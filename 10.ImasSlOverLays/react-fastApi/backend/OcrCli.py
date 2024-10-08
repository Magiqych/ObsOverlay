import datetime
import json
import re
import time
import uuid
import cv2
import sys
import os
import numpy as np
import imagehash
from PIL import Image, ImageTk
import pytesseract
import requests
import threading
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

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
def load_assets(source_dir):
    """
    テンプレート画像を読み込み、辞書に格納します。
    :param template_dir: テンプレート画像が保存されているディレクトリ
    :return: テンプレート画像の辞書
    """
    assets = {}
    for root, dirs, filenames in os.walk(source_dir):
        if 'Other' in dirs:
            dirs.remove('Other')
        for filename in filenames:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                asset_path = os.path.join(root, filename)
                asset = cv2.imread(asset_path)
                if asset is not None:
                    assets[filename] = asset
                else:
                    print(f"Failed to load template: {filename}")
    return assets

# ハッシュ値と最も近い画像を検索する関数
def find_closest_image(combined_hash, song_images):
    ahash, phash, dhash, whash = combined_hash
    min_distance = float('inf')
    closest_image = None
    for uid, data in song_images.items():
        image_ahash = imagehash.hex_to_hash(data['ahash'])
        image_phash = imagehash.hex_to_hash(data['phash'])
        image_dhash = imagehash.hex_to_hash(data['dhash'])
        image_whash = imagehash.hex_to_hash(data['whash'])
        distance = (ahash - image_ahash) + (phash - image_phash)\
                    +(dhash - image_dhash) + (whash - image_whash)
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

def send_request_with_retries(url, message=None, retries=3, interval=5):
    '''
    指定された回数だけリクエストを送信し、成功するかタイムアウトするまでリトライする関数
    :param url: URL
    :param message: メッセージ
    :param retries: リトライ回数
    :param interval: リトライ間隔（秒）
    :return: レスポンス
    '''
    for attempt in range(retries):
        try:
            if message is None:
                response = requests.get(url)
            else:
                response = requests.post(url, json=message)
            response.raise_for_status()  # HTTPエラーが発生した場合に例外を発生させる
            return response
        except requests.RequestException as e:
            print(f"Failed to send request (attempt {attempt + 1}/{retries}): {e}")
            if attempt < retries - 1:
                time.sleep(interval)
            else:
                print("All retry attempts failed.")
                return None
orb = cv2.ORB_create()
def compare_images(targetimage, imagemask, compareimage, IsReturnValue = False, threshold = 0.7):
    # 画像を読み込む
    MaskedFrame = cv2.subtract(targetimage, imagemask)
    # ORB検出器を作成
    global orb
    # 特徴点と記述子を検出
    kp1, des1 = orb.detectAndCompute(MaskedFrame, None)
    kp2, des2 = orb.detectAndCompute(compareimage, None)
    # BFMatcherを使用して特徴点をマッチング
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    # マッチング結果をソート
    matches = sorted(matches, key=lambda x: x.distance)
    # 類似度を計算
    similarity = len(matches) / max(len(kp1), len(kp2))
    if IsReturnValue:
        return similarity
    else:
        if similarity > threshold:
            return True
        else:
            return False
        
def make_train_data(image):
    '''
    学習用データを作成する関数
    :param image: 画像
    '''
    # dirlist = [os.path.join(script_dir,'train_data','0'),\
    #             os.path.join(script_dir,'train_data','1'),\
    #             os.path.join(script_dir,'train_data','2'),\
    #             os.path.join(script_dir,'train_data','3'),\
    #             os.path.join(script_dir,'train_data','4'),\
    #             os.path.join(script_dir,'train_data','5'),\
    #             os.path.join(script_dir,'train_data','6'),\
    #             os.path.join(script_dir,'train_data','7'),\
    #             os.path.join(script_dir,'train_data','8'),\
    #             os.path.join(script_dir,'train_data','9'),\
    #             os.path.join(script_dir,'train_data','n')]
    # for directory in dirlist:
    #     if not os.path.exists(directory):
    #         os.makedirs(directory)
    image2 = cv2.bitwise_not(image)
    contours, hierarchy = cv2.findContours(image2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        cv2.imwrite(os.path.join(script_dir,'train_data',str(uuid.uuid4()) + '.png'),image[:, x:x+w])
#endregion

#region イベントハンドラ
# デバウンス用のタイマー
debounce_timer = None
def on_selected_item_property_change(property_name, value):
    global debounce_timer
    # デバウンスのインターバル（ミリ秒）
    debounce_interval = 500
    if IsDebug:
        print(f'{selected_item.song_name} - {selected_item.difficulty}')
        return
    def post_selected_item():
        if(selected_item.song_name is not None and selected_item.difficulty is not None):
            url = "http://localhost:8000/select_song"
            message = {"SongName": selected_item.song_name, "Level": selected_item.difficulty}
            response = send_request_with_retries(url, message)
            if response:
                print("Request succeeded:", response.json())
            else:
                print("Request failed after all retries.")
    # 既存のタイマーがあればキャンセル
    if debounce_timer is not None:
        debounce_timer.cancel()
    # 新しいタイマーをセット
    debounce_timer = threading.Timer(debounce_interval / 1000, post_selected_item)
    debounce_timer.start()

def on_score_property_change(property_name, value):
    if IsDebug:
        print(f'{score.rawResult}')
        return
    global last_update_time
    current_time = datetime.datetime.now()
    if last_update_time and (current_time - last_update_time).total_seconds() < 60:
        return
    # last_update_timeを現在の時間に更新
    last_update_time = current_time
    if(score.rawResult is not None and score.rawResult != ""):
        url = "http://localhost:8000/set_score"
        message = {"RawScore": score.rawResult}
        response = send_request_with_retries(url, message)
        if response:
            print("Request succeeded:", response.json())
        else:
            print("Request failed after all retries.")
#endregion

#region 変数定義
# スクリプト自身のディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
# JSONファイルのパス
json_path = os.path.join(script_dir, 'Assets','SongImageHash.json')
# JSONファイルを読み込む
song_images = load_song_images(json_path)
FrameSkipper = 0
assets = []
selected_item = SelectedItem()
selected_item.add_listener(on_selected_item_property_change)
last_update_time = None
score = Score()
score.add_listener(on_score_property_change)
IsScoreProcessing = False
pytesseract.pytesseract.tesseract_cmd = r'D:\00.Software\Tesseract\tesseract.exe'
#endregion

#region フレーム処理
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
    global assets
    global selected_item
    global score
    global IsScoreProcessing
    
    # 画像保存用
    # imgPath = os.path.join(script_dir,'Assets','GrandMv.png')
    # cv2.imwrite(imgPath, frame)
    # print("frame.png saved")
    # sys.exit("スクリプトを終了します")
    
    # フレームスキップ
    if FrameSkipper != 0:
        FrameSkipper -= 1
        return
    #　フレームをコピー
    frameCopy = frame
    
    
    # スコア画面検出
    if compare_images(frameCopy, assets['ScoreMask.png'], assets['ScoreCom.png'],False):
        #スコア画面が出たらOCR解析
        # スコア解析中フラグを立てる
        IsScoreProcessing = True
        #トースト通知
        # url = "http://localhost:8000/set_score"
        # message = {"RawScore": "Processing"}
        # send_request_with_retries(url, message)
        # OCRを実行
        RawScoreText = ""
        MaskedImage = cv2.subtract(frameCopy, assets['ScoreInfoMask.png'])
        regions = extract_black_regions(assets['ScoreInfoMask.png'])
        # ソート
        regions_sorted = sorted(regions, key=lambda r: r[0])
        regions_sorted = sorted(regions_sorted, key=lambda r: r[1])
        for i, region in enumerate(regions_sorted):
            x1, y1, x2, y2 = region
            CropImage = MaskedImage[y1:y2,x1:x2]
            #アンチエイリアスを使用して拡大
            scale_factor = 5
            resized_CropImage = cv2.resize(CropImage, None, fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
            gray = cv2.cvtColor(resized_CropImage, cv2.COLOR_BGR2GRAY)
            # 二値化
            ret,th1 = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)
            make_train_data(th1)
            # OCRを実行（英語と数字のみ）
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789'
            # text = pytesseract.image_to_string(binary, lang='eng',config=custom_config)
            text = pytesseract.image_to_string(th1, lang='eng',config=custom_config)
            if i == len(regions_sorted) - 1:
                RawScoreText += re.sub(r'\D', '', text)
            else:
                RawScoreText += re.sub(r'\D', '', text) + ","
        # スコアチェック
        score_list = RawScoreText.split(",")
        bad_index = 0
        for i in range(len(score_list)):
            if score_list[i] == "":
                bad_index += 1
                score_list[i] = "0"
        # 変更されたリストを再度カンマで結合
        RawScoreText = ",".join(score_list)
        score.rawResult = RawScoreText
        # スコア解析中フラグを解除
        IsScoreProcessing = False
        return
    # basic,master+,witch,grandの判定を行う
    LevelTopMask = assets['LevelTopMask.png']
    threadhold = 0.5
    Basic = compare_images(frameCopy, LevelTopMask, assets['LevelTopBasicCom.png'],True)
    Master_plus = compare_images(frameCopy, LevelTopMask, assets['LevelTopMaster+Com.png'],True)
    Witch = compare_images(frameCopy, LevelTopMask, assets['LevelTopWitchCom.png'],True)
    Grand = compare_images(frameCopy, LevelTopMask, assets['LevelTopGrandCom.png'],True)
    Witch = compare_images(frameCopy, LevelTopMask, assets['LevelTopWitchCom.png'],True)
    if Basic > threadhold:
        #Basicの場合はDebut,Regular,Pro,Masterの判定を行う
        Debut = compare_images(frameCopy, assets['DebutMask.png'], assets['DebutCom.png'],True)
        Regular = compare_images(frameCopy, assets['RegularMask.png'], assets['RegularCom.png'],True)
        Pro = compare_images(frameCopy, assets['ProMask.png'], assets['ProCom.png'],True)
        Master = compare_images(frameCopy, assets['MasterMask.png'], assets['MasterCom.png'],True)
        min_distance = min(Debut, Regular, Pro, Master)
        if min_distance == Debut:
            selected_item.difficulty = "DEBUT"
        elif min_distance == Regular:
            selected_item.difficulty = "REGULAR"
        elif min_distance == Pro:
            selected_item.difficulty = "PRO"
        elif min_distance == Master:
            selected_item.difficulty = "MASTER"
        # if compare_images(frameCopy,assets['DebutMask.png'],assets['DebutCom.png'],False):
        #     selected_item.difficulty = "DEBUT"  
        # elif compare_images(frameCopy,assets['RegularMask.png'],assets['RegularCom.png'],False):
        #     selected_item.difficulty = "REGULAR"
        # elif compare_images(frameCopy,assets['ProMask.png'],assets['ProCom.png'],False):
        #     selected_item.difficulty = "PRO"
        # elif compare_images(frameCopy,assets['MasterMask.png'],assets['MasterCom.png'],False):
        #     selected_item.difficulty = "MASTER"
        # elif compare_images(frameCopy,assets['MvMask.png'],assets['MvCom.png'],False):
        #     selected_item.difficulty = "MV"
        # else:
        #     selected_item.difficulty = None
    elif Master_plus > threadhold:
        selected_item.difficulty = "MASTER+"
    elif Witch > threadhold:
        selected_item.difficulty = "WITCH"
    elif Grand > threadhold:
        if compare_images(frameCopy, assets['PianoMask.png'], assets['PianoCom.png'],False):
            selected_item.difficulty = "Piano"
        elif compare_images(frameCopy, assets['ForteMask.png'], assets['ForteCom.png'],False):
            selected_item.difficulty = "Forte"
        elif compare_images(frameCopy, assets['GrandMvMask.png'], assets['GrandMvCom.png'],False):
            selected_item.difficulty = "MV"
    else:
        return
    #曲を判定する
    CropImage = frameCopy[120:315,395:540]
    rgb_image = cv2.cvtColor(CropImage, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    ahash = imagehash.average_hash(pil_image)
    phash = imagehash.phash(pil_image)
    dhash = imagehash.dhash(pil_image)
    whash = imagehash.whash(pil_image)
    combined_hash = (ahash, phash, dhash, whash)
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
#endregion

#region メイン処理
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    #マスク・テンプレート画像読み込み
    assets_source = os.path.join(script_dir, "Assets")
    assets = load_assets(assets_source)

    # デバッグモード
    #IsDebug = True
    IsDebug = False
    # デバッグ用
    #input_source = os.path.join(script_dir, "log", "20241008_103326.png")
    # 本番用
    input_source = "4-700"
    main(input_source)
#endregion