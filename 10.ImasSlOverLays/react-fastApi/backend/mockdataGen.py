import base64
import json
import os
from models import *

# スクリプト自身のディレクトリを取得
script_dir = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(script_dir, '..','..','..',"00.DataStorage","cinderella.idolmaster.sl-stage.sqlite")
songDetail = None
songLevelDetail = None
songMetaData = None

def MakeSongData_json(name:str,level:str):
    """
    指定されたNameでSongDetailテーブルを検索し、結果を返すメソッド。
    
    :param name: 検索する曲の名前
    """
    # データベースから曲の詳細情報を取得
    songDetail = get_song_details_from_db(db_path,name)
    if level == "MASTER+":
        level = "MASTER_plus"
    songLevelDetail = get_song_level_details_from_db(db_path,songDetail.__dict__[level])
    # songDetailとsongLevelDetailを辞書に変換してマージ
    songDetail_dict = songDetail.__dict__
    songLevelDetail_dict = songLevelDetail.__dict__
    # バイト型のデータを削除
    songDetail_dict = {key: value for key, value in songDetail_dict.items() if not isinstance(value, bytes)}
    songLevelDetail_dict = {key: value for key, value in songLevelDetail_dict.items() if not isinstance(value, bytes)}
    merged_data = {**songDetail_dict, **songLevelDetail_dict}
    # 新しいキーと値を追加
    merged_data["SelectedLevel"] = "MASTER+"
    # マージしたデータをJSONファイルとして保存
    with open(os.path.join(script_dir, 'Assets','json','song_detail.json'), 'w', encoding='utf-8') as f:
        json.dump(merged_data, f, ensure_ascii=False, indent=4)
    print("JSONファイルが作成されました")

if __name__ == "__main__":
    MakeSongData_json("とどけ！アイドル","MASTER")
