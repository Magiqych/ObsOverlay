import json
import os
import sqlite3

def search_song_by_name(name):
    """
    指定されたNameでSongDetailテーブルを検索し、結果を返すメソッド。
    
    :param name: 検索する曲の名前
    :return: 検索結果のリスト
    """
    # データベースファイルの相対パス
    base_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = '../../../00.DataStorage/cinderella.idolmaster.sl-stage.sqlite'
    db_path = os.path.normpath(os.path.join(base_dir, relative_path))
    
    # データベースに接続
    conn = sqlite3.connect(db_path)
    
    try:
        # カーソルを作成
        cursor = conn.cursor()
        
        # クエリを実行
        query = "SELECT * FROM SongDetail WHERE Name = ?"
        cursor.execute(query, (name,))
        
        # 結果を取得
        results = cursor.fetchall()
        injectResult(results)
        return
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # 接続を閉じる
        conn.close()

def injectResult(results):
    """
    frontend側に送信するためのデータを加工するメソッド。
    """
    # 保存するディレクトリ
    base_dir = os.path.dirname(os.path.abspath(__file__))
    relative_path = '../frontend/public/Assets'
    AssetsDir = os.path.normpath(os.path.join(base_dir, relative_path))
    os.makedirs(AssetsDir, exist_ok=True)
    
    # 画像ファイルのパス
    image_path = os.path.join(AssetsDir, "Song.png")
    # 画像を保存
    with open(image_path, "wb") as image_file:
        image_file.write(results[0][1])

    json_path = os.path.join(AssetsDir, "song_detail.json")
    result_list = list(results[0])
    del result_list[1]
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(result_list, json_file, ensure_ascii=False, indent=4)
    return