import sys
from time import sleep
import unittest
from database.services import ElasticsearchCRUDClient, ElasticsearchSearchClient
from database.utils import ElasticsearchUtility
from database.index_mappings import INDEXES

class TestElasticsearchCRUDClient(unittest.TestCase):

    def setUp(self):
        self.index_mapping = INDEXES['TEST_INDEX']
        self.client = ElasticsearchCRUDClient(self.index_mapping, log_file='test.log')
        self.utility_client = ElasticsearchUtility()


    def test_connection_to_base(self):
        self.utility_client.check_elasticsearch_status()
        self.utility_client.check_index(self.index_mapping)

    def test_create_document(self):
        test_document = {
            "test_title": "Test Note",
            "test_content": "This is a test note"
        }
        self.client.create_document(test_document)
        sleep(3)

    def test_get_all_documents(self):
        self.client.get_all_documents()

    def test_get_document_by_id(self):
        all_docs = self.client.get_all_documents()
        doc_id = all_docs[0]['_id']

        self.client.get_document_by_id(doc_id)

    def test_update_document_by_id(self):
        all_docs = self.client.get_all_documents()
        doc_id = all_docs[0]['_id']

        updated_fields = {
            "doc": {
                "test_title": "Updated Note",
                "test_content": "This note has been updated"
            }
        }
        self.client.update_document_by_id(doc_id, updated_fields)

    # def test_delete_document_by_id(self):
    #     all_docs = self.client.get_all_documents()
    #     doc_id = all_docs[0]['_id']
    #     self.client.delete_document_by_id(doc_id)


class TestElasticsearchSearchClient(unittest.TestCase):

    def setUp(self):
        self.index_mapping = INDEXES['TEST_INDEX']
        self.client = ElasticsearchSearchClient(self.index_mapping, log_file='test.log')
        self.crud_client = ElasticsearchCRUDClient(self.index_mapping, log_file='test.log')

    def test_search(self):
        query = {
            "match": {
                "test_title": "Updated Note"
            }
        }
        results = self.client.search(query)

    def test_match_all(self):
        results = self.client.match_all()

    def test_delete_document_by_id(self):
        all_docs = self.crud_client.get_all_documents()
        doc_id = all_docs[0]['_id']
        self.crud_client.delete_document_by_id(doc_id)



if __name__ == "__main__":
    unittest.main()
