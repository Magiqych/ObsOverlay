import argparse
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
from PIL import Image
import pyvirtualcam
import requests
import threading
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
from torchvision import transforms
import torchvision.models as models
#モデルロードはカプセル化されているため、直接インポートする
from Models.MobileNetV2_Digits import MobileNetV2_Digits

#region クラス定義
class OcrCli:
    '''
    OcrCliクラス
    :param digit_classifier: 数字認識モデル
    predict_digit: 数字を予測する
    '''
    def __init__(self):
        self.MobileNetV2_Digits = MobileNetV2_Digits()
        
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

class ResNet18Model(nn.Module):
    '''
    ResNet18モデルの定義
    nn.Moduleを継承して定義
    :param model: ResNet18モデル
    :param num_ftrs: 特徴量の数
    forward: 順伝播
    '''
    def __init__(self, num_classes):
        super(ResNet18Model, self).__init__()
        self.model = models.resnet18(pretrained=True)
        num_ftrs = self.model.fc.in_features
        self.model.fc = nn.Linear(num_ftrs, num_classes)
    def forward(self, x):
        return self.model(x)
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
def compare_images(targetimage, imagemask, compareimage, IsReturnValue = False, threshold = 0.6):
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

def load_ResNet18Model(model_path):
    '''
    ResNet18モデルを読み込む関数
    :param model_path: モデルのパス
    :param num_classes: クラス数
    :return: モデル
    '''
    checkpoint = torch.load(model_path)
    num_classes = checkpoint['num_classes']
    class_to_idx = checkpoint['class_to_idx']
    idx_to_class = {v: k for k, v in class_to_idx.items()}
    model = ResNet18Model(num_classes)
    # state_dict のキーにプレフィックスを追加
    state_dict = {f'model.{k}': v for k, v in checkpoint['model_state_dict'].items()}
    model.load_state_dict(state_dict)
    # model.load_state_dict(checkpoint['model_state_dict'])
    model.eval()
    return model, idx_to_class
    
def apply_mask(frame, mask_path):
    '''
    マスク画像を適用する関数
    :param frame: フレーム
    :param mask_path: マスク画像のパス
    :return: マスク画像を適用したフレーム
    '''
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
    # frame = cv2.merge([b, g, r, alpha])
    frame = cv2.merge([r,g,b, alpha])
    # バウンディングボックスを取得
    x, y, w, h = cv2.boundingRect(binary_mask)
    return frame[y:y+h, x:x+w]  # トリミング

def SceneDetect(frameCopy, model, idx_to_class, mask_path):
    '''
    シーンを検出する関数
    :param frameCopy: フレームのコピー
    :param model: モデル
    :param idx_to_class: インデックスからクラス名への辞書
    :param mask_path: マスク画像のパス
    :return: None
    '''
    masked_frame = apply_mask(frameCopy, mask_path)
    input_tensor = cv2.resize(masked_frame, (224, 224))
    input_tensor = Image.fromarray(masked_frame).convert('RGB')
    input_tensor = transformScene(input_tensor)
    input_tensor = input_tensor.unsqueeze(0)
    
    with torch.no_grad():
        outputs = model(input_tensor)
        _, predicted = torch.max(outputs, 1)
    return idx_to_class[predicted.item()]

def recognize_digits(th1,SplitterNum = 4):
    # 認識された数字を格納するリスト
    recognized_digits = []
    rev = cv2.bitwise_not(th1)
    height, width = rev.shape[:2]
    # 数字表記は固定長のため、横方向に分割して認識する
    slices = []
    # 横に n 等分
    slice_width = width // SplitterNum
    for i in range(SplitterNum):
        start_x = i * slice_width
        end_x = (i + 1) * slice_width if i < SplitterNum - 1 else width
        slice_img = rev[:, start_x:end_x]
        slices.append(slice_img)
    for slice_img in slices:
        roi = cv2.bitwise_not(slice_img)
        prediction = ocr_cli.MobileNetV2_Digits.predict(roi)
        recognized_digits.append(prediction)
    # 認識された数字を出力
    recognized_digits_str = ''.join(map(str, recognized_digits))
    return recognized_digits_str.replace(" ","")
#endregion

#region イベントハンドラ
# デバウンス用のタイマー
debounce_timer = None
def on_selected_item_property_change(property_name, value):
    '''
    selected_itemのプロパティが変更されたときに呼び出される関数
    :param property_name: プロパティ名
    :param value: 値
    '''
    global debounce_timer
    # デバウンスのインターバル（ミリ秒）
    debounce_interval = 700
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
    '''
    scoreのプロパティが変更されたときに呼び出される関数
    :param property_name: プロパティ名
    :param value: 値
    '''
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

#region グローバル変数定義
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
ocr_cli = OcrCli()
#シーン検出用のモデルの読み込み
Tire1Model_path = os.path.join(script_dir, 'Models', 'model_Tire1.pth')
Tire2Model_path = os.path.join(script_dir, 'Models', 'model_Tire2.pth')
Tire3Model_path = os.path.join(script_dir, 'Models', 'model_Tire3.pth')
ScoreModel_path = os.path.join(script_dir, 'Models', 'model_Score.pth')
# モデルの読み込み
Tire1Model,Tire1_idx_to_class = load_ResNet18Model(Tire1Model_path)
Tire2Model,Tire2_idx_to_class = load_ResNet18Model(Tire2Model_path)
Tire3Model,Tire3_idx_to_class = load_ResNet18Model(Tire3Model_path)
ScoreModel,Score_idx_to_class = load_ResNet18Model(ScoreModel_path)
# データ拡張と前処理の設定
transformScene = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])
# マスク画像のパス
mask_paths = {
    'Tire1': os.path.join(script_dir,  'Assets', 'Tire1Mask.png'),
    'Tire2': os.path.join(script_dir,  'Assets', 'Tire2Mask.png'),
    'Tire3': os.path.join(script_dir,  'Assets', 'Tire3Mask.png'),
    'Score': os.path.join(script_dir,  'Assets', 'ScoreMask.png')
}

'''
固定長の数字の長さ
0: 'Perfect'
1: 'Great'
2: 'Nice'
3: 'Bad'
4: 'Miss'
5: 'Combo'
6: 'Score'
7: 'HighScore'
8: 'UPRP'
9: 'PRP'
'''
digit_length: dict[int, int] = {
    0: 4,  # 'Perfect': パーフェクトの長さ
    1: 4,  # 'Great': グレートの長さ
    2: 4,  # 'Nice': ナイスの長さ
    3: 4,  # 'Bad': バッドの長さ
    4: 4,  # 'Miss': ミスの長さ
    5: 4,  # 'Combo': コンボの長さ
    6: 7,  # 'Score': スコアの長さ
    7: 7,  # 'HighScore': ハイスコアの長さ
    8: 2,  # 'UPRP': UPRPの長さ
    9: 4   # 'PRP': PRPの長さ
}
#マスク・テンプレート画像読み込み
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_source = os.path.join(script_dir, "Assets",'Mask')
assets = load_assets(assets_source)
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
    
    # スコア解析中は何もしない
    if IsScoreProcessing:
        return
    # フレームスキップ
    if FrameSkipper != 0:
        FrameSkipper -= 1
        return
    #　フレームをコピー
    frameCopy = frame
    
    # シーン検出
    # スコア画面
    if compare_images(frameCopy, assets['ScoreMask.png'], assets['ScoreCom.png'],False):
    # if (SceneDetect(frameCopy, ScoreModel, Score_idx_to_class, mask_paths['Score']) == "Score"):
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
            text = recognize_digits(th1,digit_length[i])
            #デバッグ用テストデータ保存
            # os.makedirs(os.path.join(script_dir,'log',re.sub(r'\D', '', text)), exist_ok=True)
            # cv2.imwrite(os.path.join(script_dir,'log',re.sub(r'\D', '', text),str(uuid.uuid4()) + '.png'),th1)
            # make_train_data(th1) #学習データ作成
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
    # Tire1　{0: 'ComfirmModal', 1: 'Live', 2: 'Other'}
    if (SceneDetect(frameCopy, Tire1Model, Tire1_idx_to_class, mask_paths['Tire1']) == "Live"):
        #　ライブ中であればTire2のシーンを検出
        # Tire2 {0: 'Basic', 1: 'ComfirmModal', 2: 'Grand', 3: 'Master+', 4: 'Other', 5: 'Witch'}
        Tire2Scene = SceneDetect(frameCopy, Tire2Model, Tire2_idx_to_class, mask_paths['Tire2'])
        #もしもTire2のシーンがBasicであれば
        if Tire2Scene == "Basic":
            # Tire3のシーンを検出
            # Tire3 {0: 'ComfirmModal', 1: 'Debut', 2: 'Forte', 3: 'GrandMv', 4: 'Master', 5: 'Mv', 6: 'Other', 7: 'Piano', 8: 'Pro', 9: 'Regular'}
            Tire3Scene = SceneDetect(frameCopy, Tire3Model, Tire3_idx_to_class, mask_paths['Tire3'])
            #もしもTire3のシーンがSelectであれば
            if Tire3Scene == "Debut":
                selected_item.difficulty = "DEBUT"
            elif Tire3Scene == "Regular":
                selected_item.difficulty = "REGULAR"
            elif Tire3Scene == "Pro":
                selected_item.difficulty = "PRO"
            elif Tire3Scene == "Master":
                selected_item.difficulty = "MASTER"
            elif Tire3Scene == "Mv":
                selected_item.difficulty = "MV"
            elif Tire3Scene == "Piano":
                selected_item.difficulty = "PIANO"
            elif Tire3Scene == "Forte":
                selected_item.difficulty = "FORTE"
            elif Tire3Scene == "GrandMv":
                selected_item.difficulty = "MV"
        elif Tire2Scene == "Master+":
            selected_item.difficulty = "MASTER+"
        elif Tire2Scene == "Witch":
            selected_item.difficulty = "WITCH"
        else:
            return
    else:
        return
    # #曲を判定する
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
    # OCRTestPath = os.path.join(script_dir, "log")
    

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
        # キャプチャデバイスのインデックス（通常は0または1）
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("キャプチャデバイスを開けませんでした")
            return
        # 解像度を設定
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1920)

        with pyvirtualcam.Camera(width=1280, height=1024, fps=30) as cam:
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("フレームを取得できませんでした")
                    break
                # フレームをリサイズ
                new_width, new_height = 640, 480
                frameToProc = cv2.resize(frame, (new_width, new_height))
                process_frame(frameToProc)
                # フレームをRGBに変換
                 #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # フレームを仮想カメラに送信
                cam.send(frame)
                cam.sleep_until_next_frame()
        cap.release()
#endregion

#region メイン処理
if __name__ == "__main__":
    # コマンドライン引数の解析
    parser = argparse.ArgumentParser(description="OCR CLI ツール")
    parser.add_argument('--Caller', type=str, required=False, help='呼び出し元')
    args = parser.parse_args()
    # デバッグモード
    IsDebug = False
    # 呼び出し元を表示
    if args.Caller:
        IsDebug = False
        input_source = "3-700"
    else:
        IsDebug = True
        input_source = os.path.join(script_dir, "log", "20241008_095446.png")
        input_source = "3-700"
        #input_source = "4-700"
    main(input_source)
#endregion