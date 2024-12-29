import json


class JsonData:
    """
    Синглтон-класс для работы с JSON-данными.
    Этот класс обеспечивает загрузку данных из указанного JSON-файла и предоставляет методы
    для извлечения данных по ключу.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        Создает единственный экземпляр класса (паттерн Синглтон).
        Если экземпляр уже существует, возвращает его.
        """
        if cls._instance is None:
            cls._instance = super(JsonData, cls).__new__(cls)
        return cls._instance

    def _is_not_initialized(self) -> bool:
        """
        Проверяет, был ли инициализирован объект.
        Возвращает True, если объект еще не инициализирован.
        """
        if not hasattr(self, "_initialized"):
            self._initialized = True
            return True
        return False

    def __init__(self, json_path="data.json"):
        """
        Инициализация класса и загрузка данных из JSON-файла.

        :param json_path: Путь к JSON-файлу (по умолчанию "data.json").
        """
        if self._is_not_initialized():
            self._json_path = json_path
            self._data: dict = {}
            self._load_json()

    def _load_json(self):
        """
        Загружает данные из JSON-файла и сохраняет их в атрибут _data.
        """
        with open(self._json_path, "r", encoding="utf-8") as f:
            self._data = json.load(f)

    def get_data(self, data_key: str):
        """
        Получает значение по ключу из загруженных данных.

        :param data_key: Ключ для извлечения значения из данных.
        :return: Значение, соответствующее ключу.
        :raises ValueError: Если ключ не найден в данных.
        """
        data_value = self._data.get(data_key, None)
        if not data_value:
            raise ValueError(f"There is no key or value for key: {data_key}")
        return data_value
