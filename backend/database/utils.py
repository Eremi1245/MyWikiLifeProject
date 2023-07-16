# Cодержит утилитарные службы и функции, которые не влияют он общую работу приложения

import logging
from urllib.parse import urljoin
import requests
from database.exceptions import ElasticsearchConnectioneError, IndexCRUDOperationsError
from database.index_mappings import BASE_URL

class ElasticsearchUtility:
    def __init__(self, log_file:str = 'app.log'):
        # Настройка логирования
        self.logger = ElasticsearchLogger(log_file).logger
        self.base_url = BASE_URL
    
    def check_elasticsearch_status(self):
        # Проверка статуса Elasticsearch
        try:
            response = requests.get(self.base_url)
            response.raise_for_status()
            self.logger.info('Elasticsearch is running')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to connect to Elasticsearch: {e}')
            raise ElasticsearchConnectioneError('Failed to connect to Elasticsearch')

    
    def check_index(self, index:dict):
        index_name = index['index_name']
        # Проверка наличия индекса
        try:
            response = requests.head(f'{BASE_URL}/{index_name}')
            if response.status_code == 200:
                self.logger.info(f'Index "{index_name}" already exists')
                self.check_index_mapping(index)
            else:
                self.logger.warning(f'Index "{index_name}" does not exist')
                self.create_index(index)
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to check index: {e}')
            raise ElasticsearchConnectioneError('Failed to check index')
    
    def check_index_mapping(self, index:dict):
        # Проверка соответствия структуры индекса
        index_name = index['index_name']
        expected_mapping = index['mapping']['mappings']['properties']
        
        try:
            response = requests.get(f'{BASE_URL}/{index_name}/_mapping')
            response.raise_for_status()
            
            mapping = response.json()
            if 'properties' in mapping[index_name]['mappings'] and mapping[index_name]['mappings']['properties'] == expected_mapping:
                self.logger.info(f'Index "{index_name}" has correct mapping')
            else:
                self.logger.warning(f'Index "{index_name}" has incorrect mapping')
                self.delete_index(index)
                self.create_index(index)
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to check index mapping: {e}')
            raise ElasticsearchConnectioneError('Failed to check index mapping')
    
    def create_index(self, index):
        # Создание индекса
        index_name = index['index_name']
        mapping = index['mapping']
        
        try:
            response = requests.put(f'{BASE_URL}/{index_name}', json=mapping)
            response.raise_for_status()
            self.logger.info(f'Index "{index_name}" created successfully')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to create index: {e}')
            raise IndexCRUDOperationsError("Failed to create index")
    
    def delete_index(self, index):
        index_name = index['index_name']
        # Удаление индекса
        try:
            response = requests.delete(f'{BASE_URL}/{index_name}')
            response.raise_for_status()
            self.logger.info(f'Index "{index_name}" deleted successfully')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to delete index: {e}')
            raise IndexCRUDOperationsError("Failed to delete index")

class SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class ElasticsearchLogger(metaclass=SingletonMeta):
    def __init__(self, log_file):
        self.logger = self._configure_logger(log_file)

    def _configure_logger(self, log_file):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # Создание обработчика для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter('%(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)

        # Создание обработчика для записи в файл
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
        file_handler.setFormatter(file_formatter)

        # Установка propagate в False для каждого обработчика
        console_handler.propagate = False
        file_handler.propagate = False

        # Добавление обработчиков к логгеру
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

        return logger


# Пример использования
if __name__ == '__main__':
    from index_mappings import NOTE_INDEX

    utility = ElasticsearchUtility()
    utility.check_elasticsearch_status()
    utility.check_index(NOTE_INDEX)