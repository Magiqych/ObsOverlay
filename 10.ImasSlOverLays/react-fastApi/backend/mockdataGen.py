"""
テストデータを生成するためのスクリプト
"""
import base64
from datetime import date
import json
import os
import random
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
    print("SongDtailのモックJSONファイルが作成されました")

#  テストデータを生成
def generate_test_data(start_date: date, end_date: date, num_samples: int) -> List[Record]:
    delta = (end_date - start_date) // num_samples
    records = []
    
    for i in range(num_samples):
        current_date = start_date + i * delta
        record = Record(
            Name="とどけ！アイドル",
            Level="MASTER+",
            Perfect=514 + random.randint(-10, 10),
            Great=14 + random.randint(-5, 5),
            Nice=6 + random.randint(-3, 3),
            Bad=2 + random.randint(-2, 2),
            Miss=5 + random.randint(-3, 3),
            Combo=150 + random.randint(-10, 10),
            Score=511581 + random.randint(-1000, 1000),
            HighScore=275714 + random.randint(-500, 500),
            Prp=str(831 + random.randint(-10, 10)),
            UPrp=str(59 + random.randint(-5, 5)),
            Date=current_date.isoformat()
        )
        records.append(record)
    
    return records

#  RecordオブジェクトのリストをJSONファイルとして保存
def save_records_to_json(records: List[Record], filename: str):
    # Recordオブジェクトを辞書に変換
    records_dict = [record.__dict__ for record in records]
    # JSONファイルとして保存
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(records_dict, f, ensure_ascii=False, indent=4)
    print(f"RECORDSのモックJSONファイルが作成されました: {filename}")

if __name__ == "__main__":
    # MakeSongData_json("とどけ！アイドル","MASTER")
    # テスト用データの生成
    start_date = date(2024, 9, 1)
    end_date = date(2024, 11, 30)
    num_samples = 400
    test_data = generate_test_data(start_date, end_date, num_samples)
    # JSONファイルに保存
    save_records_to_json(test_data,os.path.join(script_dir, 'Assets','json','records.json'))