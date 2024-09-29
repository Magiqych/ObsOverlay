from pydantic import BaseModel
from typing import Optional, List
import sqlite3

class SongDetail(BaseModel):
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

class SongLevelDetail(BaseModel):
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

class SongMetaData(BaseModel):
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

class Record(BaseModel):
    Name: str
    Level: str
    Perfect: float
    Great: float
    Nice: float
    Bad: float
    Miss: float
    Combo: float
    Score: float
    HighScore: float
    Prp: Optional[str] = None
    UPrp: Optional[str] = None
    Date: Optional[str] = None

def get_song_details_from_db(db_path: str, name: str) -> Optional[SongDetail]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SongDetail WHERE Name = ?", (name,))
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

def get_song_level_details_from_db(db_path: str, levelUri: str) -> Optional[SongLevelDetail]:
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

def get_song_meta_data_from_db(db_path: str, name: str) -> Optional[SongMetaData]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM SongMetaData WHERE Name = ?", (name,))
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

def get_records_from_db(db_path: str, name: str, level: str) -> List[Record]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Records WHERE Name = ? AND Level = ?", (name, level))
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