import json
import time
import cv2
import numpy as np
from tkinter import END, Listbox, Tk, Label, Button, filedialog
from PIL import Image, ImageTk
import os
import imagehash

# スクリプト自身のディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# 選択された難易度
class SelectedItem:
    def __init__(self, song_name=None, level=None,image=None):
        self.song_name = song_name
        self.level = level
        self.Image = image
    def __str__(self):
        return f"Song: {self.song_name}, Difficulty: {self.difficulty}"

# グローバル変数
# 選択されたレベルのインスタンスを作成
selectedItem = SelectedItem(None, None, None)
SearchingSong = False
# キャプチャデバイス
capture = None
# テンプレート画像
template_images = []
# キャプチャデバイスの設定
SourceHeight = 1080
SourceWidth = 1920
resizeRatio = 1
frame_counter = 0  # フレームカウンター


# キャプチャデバイスの設定
def get_capture_device(source):
    cap = None
    if source.isdigit():
        index, backend = map(int, source.split('-'))
        cap = cv2.VideoCapture(index, backend)
    else:
        cap = cv2.VideoCapture(source)
    return cap

# テンプレート画像を読み込む
def load_Uitemplates(template_dir):
    templates = []
    for filename in os.listdir(template_dir):
        if filename.endswith(".png") or filename.endswith(".jpg"):
            template_path = os.path.join(template_dir, filename)
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            # サイズを整数に変換
            new_width = int(template.shape[1] * resizeRatio)
            new_height = int(template.shape[0] * resizeRatio)
            template = cv2.resize(template, (new_width, new_height))
            templates.append((filename, template))
    return templates

# レベル選択状態のテンプレートマッチング
def template_matching(cv2_image, template,threshold=0.85):
    result = cv2.matchTemplate(cv2_image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # 閾値を設定
    threshold = 0.85
    if max_val >= threshold:
        return True
    else:  
        return False

# テンプレート名からテンプレート画像を取得
def get_template_by_name(template_name):
    for name, image in template_images:
        if name == template_name:
            return image
    return None  # 画像が見つからない場合

# ハッシュ値と最も近い画像を検索する関数
def find_closest_image(frame_hash, song_images):
    min_distance = float('inf')
    closest_image = None
    for uid, data in song_images.items():
        image_hash = imagehash.hex_to_hash(data['hash'])
        distance = frame_hash - image_hash
        if distance < min_distance:
            min_distance = distance
            closest_image = uid
    return closest_image

# JSONファイルを読み込む関数
def load_song_images(json_path):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)
# JSONファイルのパス
json_path = os.path.join(script_dir, 'Assets','SongImageHash.json')
# JSONファイルを読み込む
song_images = load_song_images(json_path)

# フレームの更新処理
def update_frame():
    # グローバル変数を使用するための宣言
    global frame_counter
    global selectedItem
    global SearchingSong
    global find_closest_image
    
    ret, frame = capture.read()
    if not ret:
        capture.release()
        return
    
    # フレームをスキップ
    frame_counter += 1
    if frame_counter % 30!= 0:
        root.after(1, update_frame)
        return
    elif ret:
        # フレームを RGB に変換
        # サイズを整数に変換
        new_width = int(frame.shape[1] * resizeRatio)
        new_height = int(frame.shape[0] * resizeRatio)
        frame = cv2.resize(frame, (new_width, new_height))
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 選択された難易度によって処理を分岐
        if template_matching(cv2_image, get_template_by_name("ComfirmButton.png"),0.8):
            #まず難易度を選択
            if template_matching(cv2_image, get_template_by_name("Basic.png"),0.8):
                #Debut/Regular/Pro/Master
                if not template_matching(cv2_image, get_template_by_name("NotRegular.png"),0.9):
                    selectedItem.level = "Regular"
                elif not template_matching(cv2_image, get_template_by_name("NotPro.png"),0.8):
                    selectedItem.level = "Pro"
                elif not template_matching(cv2_image, get_template_by_name("NotMaster.png"),0.8):
                    selectedItem.level = "Master"
                elif not template_matching(cv2_image, get_template_by_name("NotDebut.png"),1):
                    selectedItem.level = "Debut"
                else:
                    selectedItem.level = None
            elif template_matching(cv2_image, get_template_by_name("Master+.png"),0.8):
                selectedItem.level = "Master+"
            elif template_matching(cv2_image, get_template_by_name("Witch.png"),0.8):
                selectedItem.level = "Witch"
            elif template_matching(cv2_image, get_template_by_name("Grand.png"),0.8):
                selectedItem.level = "Grand"
            selectedItem.Image = cv2_image
            selectedItem.song_name = None
        else:
            #ゲスト選択エレメントが現れたら楽曲選択を行う
            if template_matching(cv2_image, get_template_by_name("SelectGuest.png"),0.8)\
                and selectedItem.song_name == None:
                #曲名を選択
                cv2_image = selectedItem.Image
                # テンプレートマッチ
                res = cv2.matchTemplate(cv2_image,  get_template_by_name("Information.png"), cv2.TM_CCOEFF_NORMED)
                # しきい値以上のものだけを残す
                left,right,top,bottom = 0,0,0,0
                loc = np.where (res > 0.9)
                for pt in zip(*loc[::-1]):
                    left = pt[0]
                    top = pt[1]
                res = cv2.matchTemplate(cv2_image,  get_template_by_name("AutoLive.png"), cv2.TM_CCOEFF_NORMED)
                loc = np.where (res > 0.9)
                for pt in zip(*loc[::-1]):
                    right = pt[0]
                    bottom = pt[1]
                    break
                cv2_image = cv2_image[top : bottom, right:left]
                pil_image = Image.fromarray(cv2_image)  # ここで変換
                frame_hash = imagehash.phash(pil_image)
                selectedItem.song_name = find_closest_image(frame_hash, song_images)
            #リボンとOKボタンが表示されたらスコアOCRを行う
            if(template_matching(cv2_image, get_template_by_name("Ribun.png"),0.8) \
                and template_matching(cv2_image, get_template_by_name("OkButton.png"),0.8)):
                hoge = 0
                
    # GUI表示処理
    cv2_image = cv2.resize(cv2_image,(490, 270))
    pil_image = Image.fromarray(cv2_image)
    imgtk = ImageTk.PhotoImage(image=pil_image)
    image_label.imgtk = imgtk
    image_label.configure(image=imgtk)
    result_label.config(text="")
    # Noneチェックを追加
    song_name = selectedItem.song_name if selectedItem.song_name is not None else ""
    level = selectedItem.level if selectedItem.level is not None else ""
    result_label.config(text=song_name + ":" + level)
    root.after(500, update_frame)

# GUIの設定
root = Tk()
root.title("テンプレートマッチングGUI")

# 画像表示ラベル
image_label = Label(root)
image_label.pack()


# # キャプチャデバイスの初期化
# capture = get_capture_device("4-700")
# キャプチャデバイスの初期化
video_path = os.path.join(script_dir, 'Assets', 'TestData', 'songlevelSelectedScore.mp4')
capture = get_capture_device(video_path)


# テンプレート画像の読み込み
template_dir = os.path.join(script_dir, 'Assets', 'UiElements')
template_images = load_Uitemplates(template_dir)

# 結果表示ラベル
result_label = Label(root, text="Matched Templates: None")
result_label.pack()

# フレームの更新を開始
update_frame()

# GUIのメインループ
root.mainloop()