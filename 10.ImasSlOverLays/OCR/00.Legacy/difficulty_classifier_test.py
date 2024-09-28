import cv2
import numpy as np
from tensorflow.keras.models import load_model
import time

# モデルとカテゴリのロード
model_path = 'Models/difficulty_classifier_model.keras'
model = load_model(model_path)
categories = ['DEBUT', 'REGULAR', 'PRO', 'MASTER', 'MASTER+']
img_size = 128

# マスク画像の読み込みとリサイズ
mask_path = 'CapturedImages/Levels/Mask.jpg'
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
mask = cv2.resize(mask, (img_size, img_size))
mask = mask / 255.0  # 正規化

# キャプチャデバイスの設定
device_str="4-700"
index, backend = map(int, device_str.split('-'))
capture = cv2.VideoCapture(index, backend)

# 解像度の設定
capture.set(cv2.CAP_PROP_FRAME_WIDTH, img_size)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, img_size)

def predict_image(image):
    resized_array = cv2.resize(image, (img_size, img_size))
    masked_array = resized_array * mask  # マスクの適用
    normalized_array = masked_array.reshape(-1, img_size, img_size, 1) / 255.0
    prediction = model.predict(normalized_array)
    predicted_class = np.argmax(prediction)
    return categories[predicted_class]

while True:
    ret, frame = capture.read()
    if not ret:
        print("Failed to grab frame")
        break

    # グレースケールに変換
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 画像の難易度を予測
    predicted_difficulty = predict_image(gray_frame)
    print(f'The predicted difficulty is: {predicted_difficulty}')

    # フレームを表示
    cv2.imshow('HDMI Capture', frame)

    # フレームレートを落とすためにスリープ
    time.sleep(0.1)  # 0.1秒スリープ（約10FPS）

    # 'q'キーが押されたらループを終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# キャプチャを解放し、ウィンドウを閉じる
capture.release()
cv2.destroyAllWindows()