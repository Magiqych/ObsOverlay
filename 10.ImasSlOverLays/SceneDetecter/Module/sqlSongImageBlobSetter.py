import os
import io
import uuid
import json
import sqlite3
from PIL import Image
import imagehash

# スクリプト自身のディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
# データベースファイルのパス
db_path = os.path.join(script_dir,"..","..","..", '00.DataStorage', 'cinderella.idolmaster.sl-stage.sqlite')
# JSONファイルのパス
json_path = os.path.join(script_dir,"..","Assets",'SongImageHash.json')
# SQLiteデータベースに接続
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# UIDとNameのマッピングを保存する辞書
SongHash = {}

# データベースから画像データを取得
cursor.execute("SELECT Image, Name FROM SongDetail")
rows = cursor.fetchall()

for row in rows:
    image_blob, name = row
    if image_blob:
        # UIDを生成
        uid = str(uuid.uuid4())

        # 画像を保存
        image = Image.open(io.BytesIO(image_blob))

        # 画像のハッシュ値を計算
        image_hash = str(imagehash.phash(image))

        # UID、Name、ハッシュ値のマッピングを保存
        SongHash[name] = {
            "hash": image_hash
        }

# JSONファイルにUID、Name、ハッシュ値のマッピングを保存
with open(json_path, 'w', encoding='utf-8') as json_file:
    json.dump(SongHash, json_file, ensure_ascii=False, indent=4)

# データベース接続を閉じる
conn.close()
print("SongImageHash.jsonを生成しました。")