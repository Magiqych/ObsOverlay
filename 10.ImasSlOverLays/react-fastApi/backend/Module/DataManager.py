class DataManager:
    '''
    曲選択情報とスコア情報を管理するクラス
    '''
    def __init__(self):
        self.song_selection = None
        self.score_data = None
        self.score_ocr_data = None
    def __setattr__(self, name, value):
        super().__setattr__(name, value)
    def set_song_selection(self, selection):
        self.song_selection = selection
    def get_song_selection(self):
        return self.song_selection
    def set_score_data(self, data):
        self.score_data = data
    def get_score_data(self):
        return self.score_data
    def set_score_ocr_data(self, data):
        self.score_ocr_data = data
    def get_score_ocr_data(self):
        return self.score_ocr_data