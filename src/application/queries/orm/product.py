from application.models import Product


class ProductORM:
    # Добавление товара (на вход подается json, соответствующей структуре, описанной сверху).
    @staticmethod
    def add_product():
        pass

    # Удаление товара по id
    @staticmethod
    def delete_product(id: int):
        pass

    # Получение всех доступных товаров
    @staticmethod
    def get_all_available_products():
        pass

    # Получение товара по id
    @staticmethod
    def get_product(id: int):
        pass

    # Уменьшение количества товара (на вход запросу подается id товара и на сколько уменьшить)
    @staticmethod
    def reduce_product(id: int, n: int):
        pass
