"""
楽曲画像をデータベースから取得し、指定されたディレクトリに保存し、画像のハッシュ値を計算してJSONファイルに保存する関数。
Args:
    db_path (str): SQLiteデータベースのパス。
    output_dir (str): 画像を保存するディレクトリのパス。
Raises:
    Exception: 既存ファイルの削除に失敗した場合に発生する例外。
"""
import os
import io
import uuid
import json
import sqlite3
from PIL import Image
import imagehash
import shutil
import hashlib

def SongImageRegister(db_path, output_dir):
    # 楽曲画像配置初期処理
    # ディレクトリが存在しない場合は作成
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # ディレクトリ内の既存ファイルを削除
    for filename in os.listdir(output_dir):
        file_path = os.path.join(output_dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    # データベース接続
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # songDetailテーブルから曲名と画像BLOBを取得
    cursor.execute("SELECT Image, Name FROM SongDetail")
    rows = cursor.fetchall()
    # songlist.json初期設定
    song_list = []
    # UIDとハッシュ値のマッピングを保存
    SongHash = {}
    for row in rows:
        image_blob, name = row
        if image_blob:
            uuid = generate_uid(name)
            # 画像セット領域
            image_path = os.path.join(output_dir, f"{uuid}.png")
            # 画像BLOBをファイルに保存
            with open(image_path, 'wb') as image_file:
                image_file.write(image_blob)
            # 曲名とUIDファイル名のリストに追加
            song_list.append({"song_name": name, "file_name": f"{uuid}.png"})
            
            # ハッシュ値計算領域
            image = Image.open(io.BytesIO(image_blob))
            #(145, 195)にリサイズ
            image = image.resize((145, 195))
            # 使用可能なすべてのハッシュアルゴリズム
            ahash = imagehash.average_hash(image)
            phash = imagehash.phash(image)
            dhash = imagehash.dhash(image)
            whash = imagehash.whash(image)
            crhash = imagehash.crop_resistant_hash(image)
            # UID、Name、ハッシュ値のマッピングを保存
            SongHash[name] = {
                'ahash': str(ahash),
                'phash': str(phash),
                'dhash': str(dhash),
                'whash': str(whash),
                'crhash': str(crhash)
            }
    
    # 曲名とUIDファイル名のリストをJSONファイルに保存
    list_file_path = os.path.join(output_dir, 'song_list.json')
    with open(list_file_path, 'w', encoding='utf-8') as list_file:
        json.dump(song_list, list_file, ensure_ascii=False, indent=4)

    # JSONファイルにUID、Name、ハッシュ値のマッピングを保存
    with open(json_path, 'w', encoding='utf-8') as json_file:
        json.dump(SongHash, json_file, ensure_ascii=False, indent=4)
    
    # データベース接続を閉じる
    conn.close()

"""
楽曲名からSHA-256ハッシュを生成する関数。
Args:
    name (str): 楽曲名。
Returns:
    str: 楽曲名のSHA-256ハッシュ値。
"""
def generate_uid(name):
    return hashlib.sha256(name.encode()).hexdigest()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path =  os.path.join(script_dir, '..','..', 'cinderella.idolmaster.sl-stage.sqlite')
    output_dir = os.path.join(script_dir, '..', 'public', 'songimage')
    json_path = os.path.join(script_dir, '..','Assets','SongImageHash.json')
    SongImageRegister(db_path, output_dir)