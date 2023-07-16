

from elasticsearch import Elasticsearch


es = Elasticsearch(['localhost:9200'])

# Создание индекса
index_name = 'my_index'
es.indices.create(index=index_name)

# Добавление документа в индекс
doc = {
    'title': 'Заголовок документа',
    'content': 'Текст документа'
}
res = es.index(index=index_name, body=doc)
print(res)

# Поиск документов
search_query = {
    'query': {
        'match': {
            'content': 'Текст'
        }
    }
}
res = es.search(index=index_name, body=search_query)
print(res)

# Удаление индекса
es.indices.delete(index=index_name)