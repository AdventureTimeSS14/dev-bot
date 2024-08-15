import json


class JsonData:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(JsonData, cls).__new__(cls)        
        return cls._instance
    
    def _is_not_initialized(self) -> bool:
        if not hasattr(self, '_initialized'):
            self._initialized = True
            return True        
        return False
    
    def __init__(self, json_path='data.json'):
        if self._is_not_initialized():
            self._json_path = json_path
            self._data: dict = {}
            self._load_json()

    def _load_json(self):
        with open(self._json_path, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

    def get_data(self, data_key : str):
        data_value = self._data.get(data_key, None)
        if not data_value:
            raise ValueError(f'There is no key or value for key: {data_key}')
        return data_value
