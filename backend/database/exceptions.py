class IndexCRUDOperationsError(Exception):
    pass


class ElasticsearchConnectioneError(Exception):
    pass

class IndexSearchError(Exception):
    pass
# Генерация и обработка собственной ошибки
# try:
#     raise CustomError("Это мое собственное исключение!")
# except CustomError as e:
#     print("Поймано собственное исключение:", str(e))
