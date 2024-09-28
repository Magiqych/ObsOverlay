import cv2
import numpy as np
from tkinter import StringVar, Tk, Label, Button, filedialog
from PIL import Image, ImageTk
import os
from datetime import datetime

# グローバル変数
capture = None
selected_folder = None
recording = False

# キャプチャデバイスの設定
def get_capture_device(device_str):
    index, backend = map(int, device_str.split('-'))
    return cv2.VideoCapture(index, backend)

# フレームの更新処理
def update_frame():
    global cv2_image
    ret, frame = capture.read()
    if not ret:
        capture.release()

    # フレームを RGB に変換
    cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 完全な黒の領域を検出して取り除く
    gray = cv2.cvtColor(cv2_image, cv2.COLOR_RGB2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
    
    # 黒以外の領域の輪郭を取得
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 最大の輪郭を取得
    if contours:
        x_min, y_min, x_max, y_max = float('inf'), float('inf'), float('-inf'), float('-inf')
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x + w)
            y_max = max(y_max, y + h)

        # 黒の領域を取り除いた画像を取得
        cv2_image = cv2_image[y_min:y_max, x_min:x_max]

        # GUI表示処理
        pil_image = Image.fromarray(cv2_image)
        imgtk = ImageTk.PhotoImage(image=pil_image)
        image_label.imgtk = imgtk
        image_label.configure(image=imgtk)

        # レコード中であれば画像を保存
        if recording and selected_folder:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")
            filename = os.path.join(selected_folder, f"{timestamp}.png")
            pil_image.save(filename)

    root.after(100, update_frame)  # フレームレートを落とすために100msの間隔を設定

# デバイス変更時の処理
def on_device_change(event):
    global capture
    capture.release()
    capture = get_capture_device(selected_device.get())

# フォルダピッカーの処理
def select_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    folder_label.config(text=f"保存先フォルダ: {selected_folder}")

# レコード開始の処理
def start_recording():
    global recording
    recording = True

# レコード停止の処理
def stop_recording():
    global recording
    recording = False

# GUIの設定
root = Tk()
root.title("GUI Debug")

# フォルダピッカーボタン
folder_button = Button(root, text="フォルダを選択", command=select_folder)
folder_button.pack()

# 保存先フォルダラベル
folder_label = Label(root, text="保存先フォルダ: 未選択")
folder_label.pack()

# レコード開始ボタン
record_button = Button(root, text="レコード開始", command=start_recording)
record_button.pack()

# レコード停止ボタン
stop_button = Button(root, text="レコード停止", command=stop_recording)
stop_button.pack()

# 画像表示ラベル
image_label = Label(root)
image_label.pack()

# キャプチャデバイスの初期化
selected_device = StringVar(root)
selected_device.set("0-700")  # デフォルトのデバイスを設定
capture = get_capture_device(selected_device.get())

# フレームの更新を開始
update_frame()

# GUIのメインループ
root.mainloop()