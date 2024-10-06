from pydantic import BaseModel
from typing import Optional, List
import sqlite3

# 曲の詳細情報のデータ構造
class SongDetail(BaseModel):
    '''
    曲の詳細情報のデータ構造を定義するクラス
    Name: str : 曲名
    Image: Optional[bytes] : 画像
    Type: Optional[str] : タイプ
    Length: Optional[str] : 長さ
    BPM: Optional[str] : BPM
    ReleaseDate: Optional[str] : リリース日
    Credits: Optional[str] : クレジット
    DEBUT: Optional[str] : DEBUT
    REGULAR: Optional[str] : REGULAR
    PRO: Optional[str] : PRO
    MASTER: Optional[str] : MASTER
    MASTER_plus: Optional[str] : MASTER+
    レガシーMASTER_plus: Optional[str] : レガシーMASTER+
    WITCH: Optional[str] : WITCH
    PIANO: Optional[str] : PIANO
    FORTE: Optional[str] : FORTE
    LIGHT: Optional[str] : LIGHT
    TRICK: Optional[str] : TRICK
    '''
    Name: str
    Image: Optional[bytes] = None
    Type: Optional[str] = None
    Length: Optional[str] = None
    BPM: Optional[str] = None
    ReleaseDate: Optional[str] = None
    Credits: Optional[str] = None
    DEBUT: Optional[str] = None
    REGULAR: Optional[str] = None
    PRO: Optional[str] = None
    MASTER: Optional[str] = None
    MASTER_plus: Optional[str] = None
    レガシーMASTER_plus: Optional[str] = None
    WITCH: Optional[str] = None
    PIANO: Optional[str] = None
    FORTE: Optional[str] = None
    LIGHT: Optional[str] = None
    TRICK: Optional[str] = None

# 曲のレベル詳細情報のデータ構造
class SongLevelDetail(BaseModel):
    '''
    曲のレベル詳細情報のデータ構造を定義するクラス
    Level: int : レベル
    Cost: int : コスト
    Notes: int : ノーツ数
    TapIcon: int : タップアイコン
    LongIcon: int : ロングアイコン
    FlickIcon: int : フリックアイコン
    SlideIcon: int : スライドアイコン
    DamageIcon: int : ダメージアイコン
    Density: float : ノーツ密度
    TapIconRatio: float : タップアイコン比率
    LongIconRatio: float : ロングアイコン比率
    FlickIconRatio: float : フリックアイコン比率
    SlideIconRatio: float : スライドアイコン比率
    LevelUri: Optional[str] : レベルURI
    '''
    Level: int
    Cost: int
    Notes: int
    TapIcon: int
    LongIcon: int
    FlickIcon: int
    SlideIcon: int
    DamageIcon: int
    Density: float
    TapIconRatio: float
    LongIconRatio: float
    FlickIconRatio: float
    SlideIconRatio: float
    LevelUri: Optional[str] = None

# 曲のメタデータのデータ構造
class SongMetaData(BaseModel):
    '''
    曲のメタデータのデータ構造を定義するクラス
    Name: str : 曲名
    Type: Optional[str] : タイプ
    Kind: Optional[str] : 種類
    Master_plus: Optional[int] : MASTER+
    Wicth: Optional[int] : WITCH
    Grand: Optional[int] : GRAND
    Smart: Optional[int] : SMART
    ReleaseDate: Optional[str] : リリース日
    Memo: Optional[str] : メモ
    DetailUri: Optional[str] : 詳細URI
    '''
    Name: str
    Type: Optional[str] = None
    Kind: Optional[str] = None
    Master_plus: Optional[int] = None
    Wicth: Optional[int] = None
    Grand: Optional[int] = None
    Smart: Optional[int] = None
    ReleaseDate: Optional[str] = None
    Memo: Optional[str] = None
    DetailUri: Optional[str] = None

# レコードのデータ構造
class Record(BaseModel):
    '''
    レコードのデータ構造を定義するクラス
    name: str : 曲名
    level: str : レベル
    perfect: float : Perfectの数
    great: float : Greatの数
    nice: float : Niceの数
    bad: float : Badの数
    miss: float : Missの数
    combo: float : コンボ数
    score: float : スコア
    highScore: float : ハイスコア
    uPrp: Optional[str] : UPRP
    prp: Optional[str] : PRP
    date: Optional[str] : 日付
    '''
    Name: str
    Level: str
    Perfect: str
    Great: str
    Nice: str
    Bad: str
    Miss: str
    Combo: str
    Score: str
    HighScore: str
    UPrp: Optional[str] = None
    Prp: Optional[str] = None
    Date: Optional[str] = None

# エスケープ処理を行う関数
def escape_string(value):
    '''
    文字列中のシングルクォートをエスケープする関数
    value: str : 文字列
    return: str : エスケープ後の文字列
    '''
    return value.replace("'", "''")

# データベースから曲の詳細情報を取得
def get_song_details_from_db(db_path: str, name: str) -> Optional[SongDetail]:
    '''
    指定された名前の曲の詳細情報をデータベースから取得する関数
    db_path: str : データベースファイルのパス
    name: str : 曲名
    return: Optional[SongDetail] : 曲の詳細情報
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    escaped_songname = escape_string(name)
    cursor.execute("SELECT * FROM SongDetail WHERE Name = ?", (escaped_songname,))
    row = cursor.fetchone()
    conn.close()

    if row:
        song_detail = SongDetail(
            Name=row[0],
            Image=row[1],
            Type=row[2],
            Length=row[3],
            BPM=row[4],
            ReleaseDate=row[5],
            Credits=row[6],
            DEBUT=row[7],
            REGULAR=row[8],
            PRO=row[9],
            MASTER=row[10],
            MASTER_plus=row[11],
            レガシーMASTER_plus=row[12],
            WITCH=row[13],
            PIANO=row[14],
            FORTE=row[15],
            LIGHT=row[16],
            TRICK=row[17]
        )
        return song_detail
    else:
        return None

# データベースから曲のレベル詳細情報を取得
def get_song_level_details_from_db(db_path: str, levelUri: str) -> Optional[SongLevelDetail]:
    '''
    指定されたレベルの曲のレベル詳細情報をデータベースから取得する関数
    db_path: str : データベースファイルのパス
    levelUri: str : レベルURI
    return: Optional[SongLevelDetail] : 曲のレベル詳細情報
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SongLevelDetail WHERE LevelUri = ?", (levelUri,))
    row = cursor.fetchone()
    conn.close()

    if row:
        song_level_detail = SongLevelDetail(
            Level=row[0],
            Cost=row[1],
            Notes=row[2],
            TapIcon=row[3],
            LongIcon=row[4],
            FlickIcon=row[5],
            SlideIcon=row[6],
            DamageIcon=row[7],
            Density=row[8],
            TapIconRatio=row[9],
            LongIconRatio=row[10],
            FlickIconRatio=row[11],
            SlideIconRatio=row[12],
            LevelUri=row[13]
        )
        return song_level_detail
    else:
        return None

# データベースから曲のメタデータを取得
def get_song_meta_data_from_db(db_path: str, name: str) -> Optional[SongMetaData]:
    '''
    指定された名前の曲のメタデータをデータベースから取得する関数
    db_path: str : データベースファイルのパス
    name: str : 曲名
    return: Optional[SongMetaData] : 曲のメタデータ
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    escaped_songname = escape_string(name)
    cursor.execute("SELECT * FROM SongMetaData WHERE Name = ?", (escaped_songname,))
    row = cursor.fetchone()
    conn.close()

    if row:
        song_meta = SongMetaData(
            Name=row[0],
            Type=row[1],
            Kind=row[2],
            Master_plus=row[3],
            Wicth=row[4],
            Grand=row[5],
            Smart=row[6],
            ReleaseDate=row[7],
            Memo=row[8],
            DetailUri=row[9]
        )
        return song_meta
    else:
        return None

# データベースからレコードを取得
def get_records_from_db(db_path: str, name: str, level: str) -> List[Record]:
    '''
    指定された名前とレベルの曲のレコードをデータベースから取得する関数
    db_path: str : データベースファイルのパス
    name: str : 曲名
    level: str : レベル
    return: List[Record] : レコードのリスト
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    escaped_songname = escape_string(name)
    cursor.execute("SELECT * FROM Records WHERE Name = ? AND Level = ?", (escaped_songname, level))
    rows = cursor.fetchall()
    conn.close()

    records = []
    for row in rows:
        record = Record(
            Name=row[0],
            Level=row[1],
            Perfect=row[2],
            Great=row[3],
            Nice=row[4],
            Bad=row[5],
            Miss=row[6],
            Combo=row[7],
            Score=row[8],
            HighScore=row[9],
            Prp=row[10],
            UPrp=row[11],
            Date=row[12]
        )
        records.append(record)
    return records

# データベースにレコードを挿入
def insert_record_into_db(db_path: str, record: Record):
    '''
    指定されたレコードをデータベースに挿入する関数
    db_path: str : データベースファイルのパス
    record: Record : 挿入するレコード
    '''
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Records (Name, Level, Perfect, Great, Nice, Bad, Miss, Combo, Score, HighScore, Prp, UPrp, Date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            escape_string(record.Name),
            record.Level,
            record.Perfect,
            record.Great,
            record.Nice,
            record.Bad,
            record.Miss,
            record.Combo,
            record.Score,
            record.HighScore,
            record.Prp,
            record.UPrp,
            record.Date
        ))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"エラーが発生しました：{e}")
    finally:
        conn.close()