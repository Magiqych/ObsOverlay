import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import pytesseract

# Tesseractのパスを設定（必要に応じて変更）
pytesseract.pytesseract.tesseract_cmd =  r'D:\00.Software\Tesseract\tesseract.exe'

def select_image():
    # ファイルダイアログを開いて画像ファイルを選択
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            # 画像を開いて表示
            img = Image.open(file_path)
            img.thumbnail((400, 400))
            img_tk = ImageTk.PhotoImage(img)
            panel.config(image=img_tk)
            panel.image = img_tk

            # 画像からテキストを認識
            text = pytesseract.image_to_string(img, lang='jpn')
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, text)
        except Exception as e:
            messagebox.showerror("エラー", f"画像の処理中にエラーが発生しました: {e}")

# GUIのセットアップ
root = tk.Tk()
root.title("画像テキスト認識")

# 画像表示用のラベル
panel = tk.Label(root)
panel.pack()

# テキスト表示用のテキストボックス
text_box = tk.Text(root, height=10, width=50)
text_box.pack()

# 画像選択ボタン
btn = tk.Button(root, text="画像を選択", command=select_image)
btn.pack()

# GUIのメインループを開始
root.mainloop()