import os
import cv2
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import uuid
import threading
import time

import numpy as np

# スクリプト自身のパスを取得
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

LiveStartButtonTemplate = cv2.imread(os.path.join("CapturedImages","Assets","LiveStartButton.jpg"))

# テンプレートマッチング
def template_match(template, target, method=cv2.TM_CCOEFF_NORMED, threshold=0.99999):
    """
    Perform template matching 
    """
    template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    target_gray = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)

    result = cv2.matchTemplate(target_gray, template_gray, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        template_height, template_width = template_gray.shape[:2]
        
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc

        bottom_right = (top_left[0] + 260, top_left[1] + 75)
        return [(top_left, bottom_right, 0)]  
    else:
        return []

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
selected_device.set(f"{device_list[1][0]}-{device_list[1][1]}")  # デフォルトで最初のデバイスを選択

device_menu = ttk.Combobox(root, textvariable=selected_device, values=[f"{d[0]}-{d[1]}" for d in device_list])
device_menu.pack()

# キャプチャデバイスの設定
def get_capture_device(device_str):
    index, backend = map(int, device_str.split('-'))
    return cv2.VideoCapture(index, backend)

capture = get_capture_device(selected_device.get())
#解説4
width, height = 720, 480
capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# フレームの更新処理
def update_frame():
    ret, frame = capture.read()
    if ret:
        cv2_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        #ライブ開始ボタンのテンプレートマッチング
        # rectangle = template_match(cv2_image,LiveStartButtonTemplate,cv2.TM_SQDIFF_NORMED,0.99999)
        # if rectangle:
        #     top_left, bottom_right, _ = rectangle[0]
        #     cv2.rectangle(cv2_image, top_left, bottom_right, (0, 255, 0),4)
        # 2値化
        img_gray = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(img_gray,170,255,cv2.THRESH_BINARY_INV)
        kernel = np.ones((3,3),np.uint8)
        opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
        sure_bg = cv2.dilate(opening,kernel,iterations=3)
        # 距離画像
        dist_transform = cv2.distanceTransform(sure_bg,cv2.DIST_L2,3)
        # 2値化
        ret, sure_fg = cv2.threshold(dist_transform,0.28*dist_transform.max(),255,0)
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)
        # ラベリング
        ret, markers = cv2.connectedComponents(sure_fg)
        markers = markers+1
        markers[unknown==255] = 0
        markers = cv2.watershed(cv2_image, markers)
        cv2_image[markers == -1] = [255,0,0]
        contours, hierarchy = cv2.findContours(markers.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
        for i in range(len(contours)):
            if hierarchy[0][i][3] == -1:
                cv2.drawContours(cv2_image, contours, i, (255, 0, 0), 1)
        
        cv2_image = cv2.resize(cv2_image, (width//2, height//2))
        pil_image = Image.fromarray(cv2_image)
        imgtk = ImageTk.PhotoImage(image=pil_image)
        image_label.imgtk = imgtk
        image_label.configure(image=imgtk)
    root.after(100, update_frame)  # フレームレートを落とすために100msの間隔を設定

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