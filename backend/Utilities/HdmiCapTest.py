import cv2

def main():
    # キャプチャデバイスのインデックス（通常は0または1）
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("キャプチャデバイスを開けませんでした")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("フレームを取得できませんでした")
            break

        # フレームをリサイズ
        new_width, new_height = 1280, 720
        frame = cv2.resize(frame, (new_width, new_height))

        # フレームを表示
        cv2.imshow('HDMI Capture', frame)

        # 'q'キーが押されたらループを終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()