import cv2
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import uuid

# 保存先ディレクトリの設定
save_dir = 'CapturedImages'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 難易度のリスト
difficulties = ['DEBUT', 'REGULAR', 'PRO', 'MASTER', 'MASTER+']

# キャプチャデバイスIDを固定
device_id = 2

# GUIの作成
root = tk.Tk()
root.title("難易度選択と画像保存")

# 画像表示用のラベル
image_label = tk.Label(root)
image_label.pack()

# 難易度選択用のドロップダウンメニュー
selected_difficulty = tk.StringVar()
selected_difficulty.set(difficulties[0])
difficulty_menu = ttk.OptionMenu(root, selected_difficulty, *difficulties)
difficulty_menu.pack()

# キャプチャデバイスの設定
cap = cv2.VideoCapture(device_id)
# 解像度を設定
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # 幅を1920に設定
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # 高さを1080に設定
# フレームレートを設定
cap.set(cv2.CAP_PROP_FPS, 5)  # フレームレートを5FPSに設定

# 画像を保存する関数
def save_image(event=None):
    ret, frame = cap.read()
    if ret:
        difficulty = selected_difficulty.get()
        difficulty_dir = os.path.join(save_dir, difficulty)
        if not os.path.exists(difficulty_dir):
            os.makedirs(difficulty_dir)
        filename = os.path.join(difficulty_dir, f'{uuid.uuid4()}.jpg')
        cv2.imwrite(filename, frame)

# 保存ボタン
save_button = tk.Button(root, text="画像を保存", command=save_image)
save_button.pack()

# エンターキーで画像を保存するバインディング
root.bind('<Return>', save_image)

# 画像を更新する関数
def update_image():
    ret, frame = cap.read()
    if ret:
        # 表示用に解像度を半分に縮小
        display_frame = cv2.resize(frame, (960, 540))
        cv2image = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        image_label.imgtk = imgtk
        image_label.configure(image=imgtk)
    root.after(200, update_image)  # 更新間隔を200msに設定（5FPS）

# 初期キャプチャデバイスの設定
update_image()

# GUIのメインループ
root.mainloop()

# キャプチャデバイスの解放
if cap is not None:
    cap.release()
cv2.destroyAllWindows()