import sqlite3

def search_song_by_name(name):
    """
    指定されたNameでSongDetailテーブルを検索し、結果を返すメソッド。
    
    :param name: 検索する曲の名前
    :return: 検索結果のリスト
    """
    # データベースファイルのパス
    db_path = r'D:\VideoAssets\00.OBSフッテージ\ObsOverlay\00.DataStorage\cinderella.idolmaster.sl-stage.sqlite'
    
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
        
        return results
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # 接続を閉じる
        conn.close()