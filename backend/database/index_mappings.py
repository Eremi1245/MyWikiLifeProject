INDEXES = {
        "NOTE_INDEX" : {
        'index_name':'notes',
        'mapping' : {
            'mappings': {
                'properties': {
                    'title': {'type': 'text'},
                    'content': {'type': 'text'},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"},
                    'user_id': {'type': 'keyword'}
                }
            }
        }
    },
    "TEST_INDEX" : {
        'index_name':'test_index',
        'mapping' : {
            'mappings': {
                'properties': {
                    'test_title': {'type': 'text'},
                    'test_content': {'type': 'text'},
                    "created_at": {"type": "date"},
                    "updated_at": {"type": "date"},
                    'test_user_id': {'type': 'keyword'}
                }
            }
        }
    }
}

# BASE_URL = 'http://localhost:9200/'
BASE_URL = 'http://elasticsearch:9200'