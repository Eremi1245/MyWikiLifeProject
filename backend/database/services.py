from abc import ABC
import datetime
from urllib.parse import urljoin
import requests
import logging
from database.index_mappings import BASE_URL
from database.utils import ElasticsearchLogger
from database.exceptions import IndexCRUDOperationsError,IndexSearchError

class ElasticsearchClient(ABC):

    def __init__(self,index_mapping:dict, log_file:str='app.log') -> None:
        self.base_url = BASE_URL
        self.base_index_url = urljoin(BASE_URL,index_mapping['index_name']) + '/'
        self.index_mapping = index_mapping
        self.index_name = index_mapping['index_name']
        self.mapping = index_mapping['mapping']
        self.logger = ElasticsearchLogger(log_file).logger
      

class ElasticsearchCRUDClient(ElasticsearchClient):

    def __init__(self, index_mapping: dict, log_file: str = 'app.log') -> None:
        super().__init__(index_mapping, log_file)
    
    def create_index(self, index_name):
        try:
            response = requests.put(f'http://localhost:9200/{index_name}', json=self.index_mapping)
            response.raise_for_status()
            self.logger.info(f'Index "{index_name}" created successfully')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to create index: {e}')
            raise IndexCRUDOperationsError("Failed to create index")
    
    def delete_index(self, index_name):
        try:
            response = requests.delete(f'http://localhost:9200/{index_name}')
            response.raise_for_status()
            self.logger.info(f'Index "{index_name}" deleted successfully')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to delete index: {e}')
            raise IndexCRUDOperationsError("Failed to delete index")
    
    def create_document(self, document:dict):
        if not self._validate_document(document):
            self.logger.error(f'Document is not created')
        else:
            document = self._datetime_validate_document(document)    
            try:
                url = urljoin(self.base_index_url,'_doc')
                response = requests.post(url, json=document)
                _id = response.json()["_id"]
                document["id"] = _id
                response.raise_for_status()
                self.logger.info('Document indexed successfully')
                return document
            except requests.exceptions.RequestException as e:
                self.logger.error(f'Failed to index document: {e}')
                raise IndexCRUDOperationsError("Failed to index document")

    def get_all_documents(self)->list:
        try:
            url = urljoin(self.base_index_url,'_search?size=10000')
            response = requests.get(url)
            response.raise_for_status()
            documents = response.json().get('hits', {}).get('hits', [])
            self.logger.info(f'Got all documents from index "{self.index_name}": {documents}')
            return documents
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to get all documents: {e}')
            raise IndexCRUDOperationsError("Failed to get all document")
    
    def get_document_by_id(self, doc_id:str)->dict:
        try:
            response = requests.get(f'{self.base_index_url}_doc/{doc_id}')
            response.raise_for_status()
            document = response.json()
            self.logger.info(f'Got document with ID "{doc_id}": {document}')
            return document
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to get document: {e}')
            raise IndexCRUDOperationsError("Failed to get document")
    
    def update_document_by_id(self, doc_id:str, updated_fields:dict):
        if not self._validate_document(updated_fields['doc']):
            self.logger.error(f'Document is not updated')
        else:
            updated_fields = self._datetime_validate_document(updated_fields['doc'])
            del updated_fields['created_at']
            updated_fields = {'doc': updated_fields}
            try:
                response = requests.post(f'{self.base_index_url}_doc/{doc_id}/_update', json=updated_fields)
                response.raise_for_status()
                self.logger.info(f'Document with ID "{doc_id}" updated successfully')
                updated_document = self.get_document_by_id(doc_id)
                print(updated_document)
                return updated_document
            except requests.exceptions.RequestException as e:
                self.logger.error(f'Failed to update document: {e}')
                raise IndexCRUDOperationsError("Failed to update document")
    
    def delete_document_by_id(self, doc_id:str):
        try:
            response = requests.delete(f'{self.base_index_url}_doc/{doc_id}')
            response.raise_for_status()
            self.logger.info(f'Document with ID "{doc_id}" deleted successfully')
        except requests.exceptions.RequestException as e:
            self.logger.error(f'Failed to delete document: {e}')
            raise IndexCRUDOperationsError("Failed to delete document")

    def _datetime_validate_document(self,document:dict)->dict:
        now = datetime.datetime.now()
        date_string = now.strftime('%Y-%m-%dT%H:%M:%S')
        
        if 'created_at' not in document or (document['created_at'] == ''):
            document['created_at'] = date_string

        document['updated_at'] = date_string

        return document

    def _validate_document(self, document:dict)->bool:
        # Проверяем соответствие полей документа полям индекса
        for field in document:
            if field not in self.mapping['mappings']['properties']:
                self.logger.warning(f'Field "{field}" is not defined in the index: {self.index_name})')
                raise IndexCRUDOperationsError("Failed to validate document")
        return True

class ElasticsearchSearchClient(ElasticsearchClient):

    def __init__(self, index_mapping: dict, log_file: str = 'app.log') -> None:
        super().__init__(index_mapping, log_file)
        self.search_url = urljoin(self.base_index_url,'_search')

    def search(self, query):
        headers = {"Content-Type": "application/json"}
        body = {"query": query}

        try:
            response = requests.get(self.search_url, headers=headers, json=body)
            response.raise_for_status()
            results = response.json()
            self.logger.info(f'Найденно по запросу: {query} , result: {results}')
            return results
        except requests.exceptions.RequestException as e:
            print(f"Error during search: {e}")
            raise IndexSearchError("Failed to validate document")

    def match_all(self):
        query = {"match_all": {}}
        return self.search(query)
    
# Пример использования
if __name__ == '__main__':
    from index_mappings import NOTE_INDEX
    from time import sleep

    note_index_client = ElasticsearchCRUDClient(NOTE_INDEX)
    client = ElasticsearchSearchClient(NOTE_INDEX)
    results = client.match_all()
    print(results)

    # new_document = {'title': 'Тест 2', 'content': 'This is my second note', 'user_id': 'user1'}
    # note_index_client.create_document(new_document)
    # note_index_client.get_document_by_id('WbQuxIgB9ZrQdZ-cJQsg')
    # note_index_client.update_document_by_id('WbQuxIgB9ZrQdZ-cJQsg', {'doc': {'content': 'super duper update content'}})
    sleep(2)
    note_index_client.get_all_documents()
    # note_index_client.delete_document_by_id('5e8-wIgBOGl8Sd4BBtEO')
