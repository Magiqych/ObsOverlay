import os
import cv2
import numpy as np

# スクリプト自身のパスを取得
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)

# テンプレート画像取得
template = []
template_path = os.path.join(script_dir, 'CapturedImages', 'Assets')
for filename in os.listdir(template_path):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        img_path = os.path.join(template_path, filename)
        template.append(cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY))

# 比較画像取得
main_image = []
main_image_path = os.path.join(script_dir, 'CapturedImages', 'SampleData')
for filename in os.listdir(main_image_path):
    if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
        img_path = os.path.join(main_image_path, filename)
        main_image.append(cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2GRAY))

# テンプレートマッチングメソッド
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
           'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

# テンプレートマッチング
for i, main_gray in enumerate(main_image):
    for j, template_gray in enumerate(template):
        for method in methods:
            # テンプレートマッチングを実行
            method_eval = eval(method)
            result = cv2.matchTemplate(main_gray, template_gray, method_eval)
            
            # マッチング結果の最大値とその位置を取得
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # マッチング結果が閾値を超えた場合、テンプレートが存在すると判断
            threshold = 0.8
            if method in ['cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']:
                match_val = min_val
                match_loc = min_loc
                match_type = 'min'
            else:
                match_val = max_val
                match_loc = max_loc
                match_type = 'max'
            
            if (match_type == 'max' and match_val >= threshold) or (match_type == 'min' and match_val <= threshold):
                print(f"テンプレート {j} がメイン画像 {i} に存在します。メソッド: {method}")
                # マッチング結果を描画
                h, w = template_gray.shape
                top_left = match_loc
                main_gray_copy = main_image[i].copy()
                bottom_right = (top_left[0] + w, top_left[1] + h)
                cv2.rectangle(main_gray_copy, top_left, bottom_right, (0, 0, 255), 2)  # 赤色で矩形を描画
                # ウィンドウサイズを固定
                window_name = f'Matching Result {i}-{j} - {method}'
                cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                cv2.resizeWindow(window_name, 800, 600)
                cv2.imshow(f'Matching Result {i}-{j} - {method}', main_gray_copy)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            else:
                print(f"テンプレート {j} はメイン画像 {i} に存在しません。メソッド: {method}")