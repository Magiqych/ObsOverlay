import sqlite3
import os
import json
import uuid
from PIL import Image
import io

# スクリプト自身のディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))

# データベースファイルのパス
db_path = os.path.join(script_dir,"..","..","..", '00.DataStorage', 'cinderella.idolmaster.sl-stage.sqlite')

# 画像を保存するディレクトリ
image_dir = os.path.join(script_dir, "..", 'ImageAssets', 'SongImage')
os.makedirs(image_dir, exist_ok=True)

# JSONファイルのパス
json_path = os.path.join(image_dir, 'song_images.json')

# SQLiteデータベースに接続
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# SongDetailテーブルからImageとNameカラムを取得
cursor.execute("SELECT Image, Name FROM SongDetail")
rows = cursor.fetchall()

# UIDとNameのマッピングを保存する辞書
uid_name_mapping = {}

for row in rows:
    image_blob, name = row
    if image_blob:
        # UIDを生成
        uid = str(uuid.uuid4())

        # 画像を保存
        image_path = os.path.join(image_dir, f"{uid}.png")
        image = Image.open(io.BytesIO(image_blob))
        image.save(image_path)

        # UIDとNameのマッピングを保存
        uid_name_mapping[uid] = name

# JSONファイルにUIDとNameのマッピングを保存
with open(json_path, 'w', encoding='utf-8') as json_file:
    json.dump(uid_name_mapping, json_file, ensure_ascii=False, indent=4)

# データベース接続を閉じる
conn.close()

print("画像とJSONファイルの保存が完了しました。")