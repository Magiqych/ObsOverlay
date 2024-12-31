"""
このモジュールは、楽曲の詳細情報を格納するためのモデルを提供します。
"""
import ulid
from sqlalchemy import BLOB, Column, String


class SongDetail(Base):
    """
    SongDetailクラスは、楽曲の詳細情報を格納するためのモデルです。
    属性:
        id (str): 楽曲の一意の識別子。
        name (str): 楽曲の名前。
        image (BLOB): 楽曲の画像。
        type (str): 楽曲のタイプ。
        length (str): 楽曲の長さ。
        bpm (str): 楽曲のBPM（テンポ）。
        release_date (str): 楽曲のリリース日。
        credits (str): 楽曲のクレジット情報。
        debut (str): デビュー難易度の情報。
        regular (str): レギュラー難易度の情報。
        pro (str): プロ難易度の情報。
        master (str): マスター難易度の情報。
        master_plus (str): MASTER+難易度の情報。
        legacy_master_plus (str): レガシーMASTER+難易度の情報。
        witch (str): WITCH難易度の情報。
        piano (str): PIANO難易度の情報。
        forte (str): FORTE難易度の情報。
        light (str): LIGHT難易度の情報。
        trick (str): TRICK難易度の情報。
    """

    __tablename__ = "song_detail"
    __table_args__ = {"schema": "cinderella.idolmaster.sl-stage"}

    id = Column(String, primary_key=True, default=lambda: ulid.new().str)
    name = Column(String)
    image = Column(BLOB)
    type = Column(String)
    length = Column(String)
    bpm = Column(String)
    release_date = Column(String)
    credits = Column(String)
    debut = Column(String)
    regular = Column(String)
    pro = Column(String)
    master = Column(String)
    master_plus = Column("MASTER+", String)
    legacy_master_plus = Column("レガシーMASTER+", String)
    witch = Column(String)
    piano = Column(String)
    forte = Column(String)
    light = Column(String)
    trick = Column(String)
