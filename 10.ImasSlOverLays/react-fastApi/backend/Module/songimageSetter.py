# このスクリプトは、データベースから曲の画像を取得し、ファイルに保存するスクリプトです。
import os
import sqlite3
import shutil
import json
import uuid

def save_song_images(db_path, output_dir):
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
    
    song_list = []
    
    for row in rows:
        image_blob, name = row
        if image_blob:
            # UIDを生成
            uid = str(uuid.uuid4())

            image_path = os.path.join(output_dir, f"{uid}.png")
            
            # 画像BLOBをファイルに保存
            with open(image_path, 'wb') as image_file:
                image_file.write(image_blob)
            
            # 曲名とUIDファイル名のリストに追加
            song_list.append({"song_name": name, "file_name": f"{uid}.png"})
    
    # 曲名とUIDファイル名のリストをJSONファイルに保存
    list_file_path = os.path.join(output_dir, 'song_list.json')
    with open(list_file_path, 'w', encoding='utf-8') as list_file:
        json.dump(song_list, list_file, ensure_ascii=False, indent=4)
    
    # データベース接続を閉じる
    conn.close()

# 使用例
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, '..', '..', '..','..', "00.DataStorage", "cinderella.idolmaster.sl-stage.sqlite")
    output_dir = os.path.join(script_dir, '..', 'public', 'songimage')
    
    save_song_images(db_path, output_dir)