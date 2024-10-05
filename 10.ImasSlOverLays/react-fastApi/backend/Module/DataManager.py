class DataManager:
    '''
    曲選択情報とスコア情報を管理するクラス
    '''
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataManager, cls).__new__(cls)
            cls._instance.song_selection = None
            cls._instance.score_data = None
            cls._instance.score_ocr_data = None
        return cls._instance
    def __setattr__(self, name, value):
        if name in ['song_selection', 'score_data','score_ocr_data']:
            super(DataManager, self).__setattr__(name, value)
        else:
            raise AttributeError(f"Cannot set attribute {name}")
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