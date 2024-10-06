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
    def __init__(self, song_name=None, difficulty=None):
        self.song_name = song_name
        self.difficulty = difficulty
        self.Image = None
    def set(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    def getImage(self):
        return self.Image
    def get(self):
        return  f"Song: {self.song_name}, Difficulty: {self.difficulty}"
    def __str__(self):
        return f"Song: {self.song_name}, Difficulty: {self.difficulty}"

# グローバル変数
capture = None
template_images = []
SourceHeight = 1080
SourceWidth = 1920
ResizeHeight = 1080
ResizeWidth = 1920
frame_counter = 0  # フレームカウンター
# 選択されたレベルのインスタンスを作成
selectedItem = SelectedItem("Unknown", "Unknown")
SearchingSong = False

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
            closest_image = data['name']
    return closest_image

# JSONファイルを読み込む関数
def load_song_images(json_path):
    with open(json_path, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)
# JSONファイルのパス
json_path = os.path.join(script_dir, 'ImageAssets','SongImage','song_images.json')
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
    
    if SearchingSong:
        # GUI表示処理
        cv2_image = selectedItem.getImage()
        pil_image = Image.fromarray(cv2_image)
        frame_hash = imagehash.phash(pil_image)
        selectedItem.set(song_name = find_closest_image(frame_hash, song_images))
        SearchingSong = False
    elif ret:
        # フレームを RGB に変換
        frame = cv2.resize(frame, (ResizeWidth, ResizeHeight))
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # 選択された難易度によって処理を分岐
        if template_matching(cv2_image, get_template_by_name("ComfirmButton.png"),0.8):
            #まず難易度を選択
            if template_matching(cv2_image, get_template_by_name("Basic.png"),0.8):
                #Debut/Regular/Pro/Master
                if not template_matching(cv2_image, get_template_by_name("NotDebut.png"),0.99):
                    selectedItem.set(difficulty="Debut",Image=cv2_image)
                elif not template_matching(cv2_image, get_template_by_name("NotRegular.png"),0.8):
                    selectedItem.set(difficulty="Regular",Image=cv2_image)
                elif not template_matching(cv2_image, get_template_by_name("NotPro.png"),0.8):
                    selectedItem.set(difficulty="Pro",Image=cv2_image)
                elif not template_matching(cv2_image, get_template_by_name("NotMaster.png"),0.8):
                    selectedItem.set(difficulty="Master",Image=cv2_image)
                else:
                    selectedItem.set(difficulty="Selecting",Image=cv2_image)
            elif template_matching(cv2_image, get_template_by_name("Master+.png"),0.8):
                selectedItem.set(difficulty="Master+",Image=cv2_image)
            elif template_matching(cv2_image, get_template_by_name("Witch.png"),0.8):
                selectedItem.set(difficulty="Witch",Image=cv2_image)
            elif template_matching(cv2_image, get_template_by_name("Grand.png"),0.8):
                selectedItem.set(difficulty="Grand",Image=cv2_image)
            # GUI表示処理
            cv2_image = cv2.resize(cv2_image,(490, 270))
            pil_image = Image.fromarray(cv2_image)
            imgtk = ImageTk.PhotoImage(image=pil_image)
            image_label.imgtk = imgtk
            image_label.configure(image=imgtk)
            if selectedItem.get() != (None, None):
                result_label.config(text=selectedItem.get())
        else:
            if template_matching(cv2_image, get_template_by_name("SelectGuest.png"),0.8):
                #曲名を選択
                SearchingSong = True
                cv2_image = selectedItem.getImage()
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
                selectedItem.set(Image=cv2_image)
        
    root.after(1, update_frame)

# GUIの設定
root = Tk()
root.title("テンプレートマッチングGUI")

# 画像表示ラベル
image_label = Label(root)
image_label.pack()


# # キャプチャデバイスの初期化
# capture = get_capture_device("4-700")
# キャプチャデバイスの初期化
video_path = os.path.join(script_dir, 'ImageAssets', 'TestData', 'testVideoEdited.mp4')
capture = get_capture_device(video_path)


# テンプレート画像の読み込み
template_dir = os.path.join(script_dir, 'ImageAssets', 'UiElements')
template_images = load_Uitemplates(template_dir)

# 結果表示ラベル
result_label = Label(root, text="Matched Templates: None")
result_label.pack()

# フレームの更新を開始
update_frame()

# GUIのメインループ
root.mainloop()