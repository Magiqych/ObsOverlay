"""
このモジュールは、楽曲のレベル詳細を表すモデルを提供します。
"""
import ulid
from sqlalchemy import Column, String

from .base import Base


class SongLevelDetail(Base):
    """
    SongLevelDetailクラスは、楽曲のレベル詳細を表します。
    属性:
        id (str): 一意の識別子。
        level (str): 楽曲のレベル。
        cost (str): 楽曲のコスト。
        notes (str): 楽曲のノーツ数。
        tap_icon (str): タップアイコンの数。
        long_icon (str): ロングアイコンの数。
        flick_icon (str): フリックアイコンの数。
        slide_icon (str): スライドアイコンの数。
        damage_icon (str): ダメージアイコンの数。
        density (str): ノーツの密度。
        tap_icon_ratio (str): タップアイコンの割合。
        long_icon_ratio (str): ロングアイコンの割合。
        flick_icon_ratio (str): フリックアイコンの割合。
        slide_icon_ratio (str): スライドアイコンの割合。
        level_uri (str): レベルのURI。
    """
    __tablename__ = "SongLevelDetail"
    __table_args__ = {"schema": "cinderella.idolmaster.sl-stage"}

    id = Column(String, primary_key=True, default=lambda: ulid.new().str)
    level = Column(String)
    cost = Column(String)
    notes = Column(String)
    tap_icon = Column(String)
    long_icon = Column(String)
    flick_icon = Column(String)
    slide_icon = Column(String)
    damage_icon = Column(String)
    density = Column(String)
    tap_icon_ratio = Column(String)
    long_icon_ratio = Column(String)
    flick_icon_ratio = Column(String)
    slide_icon_ratio = Column(String)
    level_uri = Column(String)
