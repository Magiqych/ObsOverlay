import os
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import uuid
import threading
import time

# 保存先ディレクトリの設定
save_dir = 'CapturedImages/Scene'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# シーンのリスト（英語に翻訳）
scenes = ['Unrelated', 'Song Selection Loading', 'Song Selection', 'Live Start', 'Score']

# キャプチャデバイスIDのリストを取得
def get_device_list(max_devices=10):
    index = 0
    arr = []
    backends = [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_V4L2]  # 使用するバックエンドのリスト
    while index < max_devices:
        for backend in backends:
            cap = cv2.VideoCapture(index, backend)
            if cap.read()[0]:
                arr.append((index, backend))
                cap.release()
                break
            cap.release()
        index += 1
    return arr

device_list = get_device_list()

# GUIの作成
root = tk.Tk()
root.title("Scene Selection and Continuous Capture")

# キャプチャデバイスが見つからない場合のエラーハンドリング
if not device_list:
    messagebox.showerror("Error", "No capture devices found.")
    root.destroy()
    exit()

# 画像表示用のラベル
image_label = tk.Label(root)
image_label.pack()

# キャプチャデバイスの選択用ドロップダウンメニュー
selected_device = tk.StringVar()
selected_device.set(f"{device_list[0][0]}-{device_list[0][1]}")  # デフォルトで最初のデバイスを選択

device_menu = ttk.Combobox(root, textvariable=selected_device, values=[f"{d[0]}-{d[1]}" for d in device_list])
device_menu.pack()

# シーンの選択用ドロップダウンメニュー
selected_scene = tk.StringVar()
selected_scene.set(scenes[0])  # デフォルトで最初のシーンを選択

scene_menu = ttk.Combobox(root, textvariable=selected_scene, values=scenes)
scene_menu.pack()

# キャプチャデバイスの設定
def get_capture_device(device_str):
    index, backend = map(int, device_str.split('-'))
    return cv2.VideoCapture(index, backend)

capture = get_capture_device(selected_device.get())

# キャプチャフラグ
is_capturing = False

def update_frame():
    ret, frame = capture.read()
    if ret:
        # 解像度を1/4にリサイズして表示
        display_frame = cv2.resize(frame, (frame.shape[1] // 4, frame.shape[0] // 4))
        cv2_image = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(cv2_image)
        imgtk = ImageTk.PhotoImage(image=pil_image)
        image_label.imgtk = imgtk
        image_label.configure(image=imgtk)
    root.after(100, update_frame)  # フレームレートを落とすために100msの間隔を設定

def capture_frames():
    global is_capturing
    scene = selected_scene.get()
    scene_dir = os.path.join(save_dir, scene)
    if not os.path.exists(scene_dir):
        os.makedirs(scene_dir)
    while is_capturing:
        ret, frame = capture.read()
        if ret:
            # 解像度を1920x1080に固定
            frame = cv2.resize(frame, (1920, 1080))
            filename = os.path.join(scene_dir, f"{uuid.uuid4()}.jpg")
            cv2.imwrite(filename, frame)
            print(f"Saved {filename}")
        time.sleep(0.1)  # フレームレートを落とすために100msの間隔を設定

def start_capture():
    global is_capturing
    is_capturing = True
    capture_thread = threading.Thread(target=capture_frames)
    capture_thread.start()

def stop_capture():
    global is_capturing
    is_capturing = False

# レコードボタン
record_button = ttk.Button(root, text="Record", command=start_capture)
record_button.pack(side=tk.LEFT)

# 停止ボタン
stop_button = ttk.Button(root, text="Stop", command=stop_capture)
stop_button.pack(side=tk.LEFT)

# デバイス変更時の処理
def on_device_change(event):
    global capture
    capture.release()
    capture = get_capture_device(selected_device.get())

device_menu.bind("<<ComboboxSelected>>", on_device_change)

# フレームの更新
update_frame()

# GUIのメインループ
root.mainloop()

# キャプチャを解放
capture.release()