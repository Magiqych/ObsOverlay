import cv2
import numpy as np
from tkinter import END, Listbox, Tk, Label, Button, filedialog
from PIL import Image, ImageTk
import os

# グローバル変数
capture = None
template_images = []
SourceHeight = 1080
SourceWidth = 1920
ResizeHeight = 240
ResizeWidth = 480

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
            template = cv2.resize(template, (int(template.shape[1] / (SourceWidth / ResizeWidth)), int(template.shape[0] / (SourceHeight / ResizeHeight))))
            templates.append((filename, template))
    return templates

# フレームの更新処理
def update_frame():
    ret, frame = capture.read()
    if not ret:
        capture.release()
        return

    # フレームを RGB に変換
    frame = cv2.resize(frame, (ResizeWidth, ResizeHeight))
    cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # テンプレートマッチング
    matched_templates = []
    # for template_name, template in template_images:
    #     result = cv2.matchTemplate(cv2_image, template, cv2.TM_CCOEFF_NORMED)
    #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    #     # 閾値を設定
    #     threshold = 0.8
    #     if max_val >= threshold:
    #         top_left = max_loc
    #         h, w, _ = template.shape
    #         bottom_right = (top_left[0] + w, top_left[1] + h)
    #         cv2.rectangle(cv2_image, top_left, bottom_right, (0, 0, 255), 2)
    #         matched_templates.append(template_name)
    if matched_templates:
        result_label.config(text="Matched Templates: " + ", ".join(matched_templates))
    else:
        result_label.config(text="No Match Found")

    # GUI表示処理
    cv2_image = cv2.resize(cv2_image,(860, 540))
    pil_image = Image.fromarray(cv2_image)
    imgtk = ImageTk.PhotoImage(image=pil_image)
    image_label.imgtk = imgtk
    image_label.configure(image=imgtk)

    root.after(100, update_frame)

# GUIの設定
root = Tk()
root.title("テンプレートマッチングGUI")

# 画像表示ラベル
image_label = Label(root)
image_label.pack()


# # キャプチャデバイスの初期化
# capture = get_capture_device("4-700")
# キャプチャデバイスの初期化
video_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ImageAssets', 'TestData', 'testVideoEdited.mp4')
capture = get_capture_device(video_path)


# テンプレート画像の読み込み
template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ImageAssets', 'UiElements')
template_images = load_Uitemplates(template_dir)

# 結果表示ラベル
result_label = Label(root, text="Matched Templates: None")
result_label.pack()

# フレームの更新を開始
update_frame()

# GUIのメインループ
root.mainloop()