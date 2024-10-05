import time
import cv2
import sys
import os

class SelectedItem:
    '''
    選択された曲と難易度を保持するクラス
    member: song_name: str, difficulty: str
    '''
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
    
def template_matching(image, template, threshold=0.8, return_result=False):
    """
    テンプレートマッチングを行う関数。
    
    :param image: 入力画像
    :param template: テンプレート画像
    :param threshold: マッチングの閾値
    :param return_result: Trueの場合、マッチング結果の詳細を返す
    :return: 閾値を超えたかどうかのブール値、またはマッチング結果の詳細
    """
    # 画像をグレースケールに変換
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if len(template.shape) == 3:
        template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # データ型を確認
    if image.dtype != template.dtype:
        template = template.astype(image.dtype)

    # テンプレートマッチングを実行
    result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 閾値を超えたかどうかを判定
    match = max_val >= threshold

    if return_result:
        return match, result, max_val, max_loc
    else:
        return match

def load_templates(template_dir):
    """
    テンプレート画像を読み込み、辞書に格納します。

    :param template_dir: テンプレート画像が保存されているディレクトリ
    :return: テンプレート画像の辞書
    """
    templates = {}
    for filename in os.listdir(template_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            template_path = os.path.join(template_dir, filename)
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is not None:
                templates[filename] = template
            else:
                print(f"Failed to load template: {filename}")
    return templates

FrameSkipper = 0
templates = []
selectedItem = SelectedItem(None, None)

def initialize_capture_device(device_id):
    """
    キャプチャデバイスを初期化します。

    :param device_id: キャプチャデバイスのID
    :return: キャプチャオブジェクト
    """
    cap = cv2.VideoCapture(device_id)
    if not cap.isOpened():
        raise Exception(f"Failed to open capture device with ID {device_id}")
    return cap

def process_frame(frame):
    """
    フレームを処理します。将来的にOCR解析などの処理を追加します。

    :param frame: キャプチャしたフレーム
    :return: 処理結果
    """
    global FrameSkipper
    
    # ここにOCR解析などの処理を追加
    
    # 画像保存用
    # cv2.imwrite("MVSelected.png", frame)
    # print("frame.png saved")
    # time.sleep(10000000000000)
    
    
    if FrameSkipper != 0:
        FrameSkipper -= 1
        return
    # 例: グレースケール変換
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #MVボタンのテンプレートマッチング
    if template_matching(gray_frame, templates['MVSelected.png']):
        # MVボタンが見つかった場合
        selectedItem.set(difficulty=None, song_name=None)
        return gray_frame
    # イベントボックスのテンプレートマッチング
    if template_matching(gray_frame, templates['EventBox.png']):
        # イベントボックスが見つかった場合
        selectedItem.set(difficulty=None, song_name=None)
        return gray_frame
    # # レベル選択画面のテンプレートマッチング
    if template_matching(gray_frame, templates['ComfirmButton.png']):
        # Basicボタンのテンプレートマッチング
        if template_matching(gray_frame, templates['Basic.png']):     
            # Debut,Regular,Pro,Masterの判別
            # 描写領域切り出し
            template = templates['LevelZone1.png']
            match, result, max_val, max_loc = template_matching(gray_frame, template, return_result=True)
            croptop = max_loc[1] + template.shape[0]
            cropleft = max_loc[0]
            template = templates['MV.png']
            match, result, max_val, max_loc = template_matching(gray_frame, template, return_result=True)
            cropright = max_loc[0]
            cropbottom = max_loc[1] + template.shape[0]
            cropedimage = frame[croptop:cropbottom, cropleft:cropright]
            cv2.imshow("Matched Template", cropedimage)
            cv2.waitKey(0)
            

        
    
    # 処理結果を返す（ここでは単にグレースケール画像を返す）
    return gray_frame

def process_video(video_path):
    """
    動画ファイルを処理します。

    :param video_path: 動画ファイルのパス
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise Exception(f"Failed to open video file {video_path}")
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            processed_frame = process_frame(frame)
            time.sleep(1)
            # cv2.imshow('Processed Frame', processed_frame)
            # if cv2.waitKey(1) & 0xFF == ord('q'):
            #     break
    finally:
        cap.release()
        cv2.destroyAllWindows()

def process_image(image_path):
    """
    画像ファイルを処理します。

    :param image_path: 画像ファイルのパス
    """
    image = cv2.imread(image_path)
    if image is None:
        raise Exception(f"Failed to open image file {image_path}")
    processed_image = process_frame(image)
    cv2.imshow('Processed Image', processed_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def main(input_source):
    """
    メイン関数。入力ソースに応じて処理を行います。

    :param input_source: 入力ソース（動画ファイル、画像ファイル、デバイスID）
    """
    if os.path.isfile(input_source):
        # ファイルの場合
        file_ext = os.path.splitext(input_source)[1].lower()
        if file_ext in ['.mp4', '.avi', '.mov', '.mkv']:
            process_video(input_source)
        elif file_ext in ['.png', '.jpg', '.jpeg', '.bmp', '.gif']:
            process_image(input_source)
        else:
            raise Exception(f"Unsupported file type: {file_ext}")
    else:
        # デバイスIDの場合
        source = input_source
        cap = None
        if not source.isdigit():
            index, backend = map(int, source.split('-'))
            cap = cv2.VideoCapture(index, backend)
        else:
            cap = cv2.VideoCapture(source)


        try:
            while True:
                ret, frame = cap.read()
                if frame is None:
                    time.sleep(1)
                else:
                    processed_frame = process_frame(frame)
        finally:
            cap.release()
            cv2.destroyAllWindows()

if __name__ == "__main__":
    # if len(sys.argv) != 2:
    #     print("Usage: python OcrCli.py <input_source>")
    #     sys.exit(1)
    # input_source = sys.argv[1]
    script_dir = os.path.dirname(os.path.abspath(__file__))
    template_source = os.path.join(script_dir, "Assets", "UiElements")
    templates = load_templates(template_source)
    input_source = os.path.join(script_dir, "Assets", "TestData2", "fraaaaaaaaaaaaaaaaaame.png")
    input_source = "4-700"
    main(input_source)