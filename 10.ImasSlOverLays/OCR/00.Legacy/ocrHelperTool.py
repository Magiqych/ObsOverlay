import cv2
from PIL import Image, ImageTk
import pytesseract
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

# Tesseractのパスを設定
pytesseract.pytesseract.tesseract_cmd = r'D:\00.Software\Tesseract\tesseract.exe'

def load_image(image_path):
    # Pillowを使用して画像を読み込む
    pil_image = Image.open(image_path)
    # 画像を半分のサイズにリサイズ
    pil_image = pil_image.resize((pil_image.width // 2, pil_image.height // 2))
    # OpenCV形式に変換
    open_cv_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    return open_cv_image

def crop_image(image, x, y, w, h):
    return image[y:y+h, x:x+w]

def get_difficulty_color(cropped_image):
    average_color = cv2.mean(cropped_image)[:3]
    return average_color

def ocr_image(cropped_image, lang='eng+jpn'):
    pil_image = Image.fromarray(cv2.cvtColor(cropped_image, cv2.COLOR_BGR2RGB))
    text = pytesseract.image_to_string(pil_image, lang=lang)
    return text.strip()

def select_image():
    global panelA, image, img_path, canvas, image_tk
    img_path = filedialog.askopenfilename(initialdir=r'D:\VideoAssets\00.OBSフッテージ\ObsOverlay\10.ImasSlOverLays\OCR\SampleData')
    if len(img_path) > 0:
        try:
            image = load_image(img_path)
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image_pil = Image.fromarray(image_rgb)
            image_tk = ImageTk.PhotoImage(image_pil)
            canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
            canvas.config(scrollregion=canvas.bbox(tk.ALL))
        except FileNotFoundError as e:
            messagebox.showerror("File Not Found", str(e))
        except Exception as e:
            messagebox.showerror("Error", str(e))

def crop_and_show():
    global image, entry_x, entry_y, entry_w, entry_h
    try:
        x = int(entry_x.get())
        y = int(entry_y.get())
        w = int(entry_w.get())
        h = int(entry_h.get())
        if x < 0 or y < 0 or w <= 0 or h <= 0 or x + w > image.shape[1] or y + h > image.shape[0]:
            raise ValueError("Invalid crop dimensions")
        cropped_image = crop_image(image, x, y, w, h)
        cv2.imshow('Cropped Image', cropped_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", str(e))

def process_image():
    global image
    try:
        # 難易度部分をクロップ (例: x=10, y=10, w=100, h=50)
        difficulty_cropped = crop_image(image, 10, 10, 100, 50)
        difficulty_color = get_difficulty_color(difficulty_cropped)
        print(f'Difficulty Color: {difficulty_color}')

        # 楽曲名部分をクロップ (例: x=10, y=70, w=300, h=50)
        song_name_cropped = crop_image(image, 10, 70, 300, 50)
        song_name = ocr_image(song_name_cropped, lang='eng+jpn')
        print(f'Song Name: {song_name}')
    except Exception as e:
        messagebox.showerror("Error", str(e))

def show_coordinates(event):
    x, y = event.x, event.y
    coordinates_label.config(text=f"Coordinates: ({x}, {y})")

# GUIのセットアップ
root = tk.Tk()
panelA = None

btn_select = tk.Button(root, text="Select an image", command=select_image)
btn_select.pack(side="top", fill="both", expand="yes", padx="10", pady="10")

label_x = tk.Label(root, text="X:")
label_x.pack(side="left")
entry_x = tk.Entry(root)
entry_x.pack(side="left")

label_y = tk.Label(root, text="Y:")
label_y.pack(side="left")
entry_y = tk.Entry(root)
entry_y.pack(side="left")

label_w = tk.Label(root, text="Width:")
label_w.pack(side="left")
entry_w = tk.Entry(root)
entry_w.pack(side="left")

label_h = tk.Label(root, text="Height:")
label_h.pack(side="left")
entry_h = tk.Entry(root)
entry_h.pack(side="left")

btn_crop = tk.Button(root, text="Crop and Show", command=crop_and_show)
btn_crop.pack(side="top", fill="both", expand="yes", padx="10", pady="10")

btn_process = tk.Button(root, text="Process Image", command=process_image)
btn_process.pack(side="top", fill="both", expand="yes", padx="10", pady="10")

coordinates_label = tk.Label(root, text="Coordinates: (0, 0)")
coordinates_label.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")

canvas = tk.Canvas(root, width=800, height=600)
canvas.pack(side="top", fill="both", expand="yes")
canvas.bind("<Motion>", show_coordinates)

root.mainloop()