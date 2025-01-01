from application.models import Supplier


class SupplierORM:
    # Добавление поставщика (на вход подается json, соответствующей структуре, описанной сверху).
    @staticmethod
    def add_supplier():
        pass

    # Удаление поставщика по id
    @staticmethod
    def delete_supplier(id: int):
        pass

    # Получение всех поставщиков
    @staticmethod
    def get_all_suppliers():
        pass

    # Получение поставщика по id
    @staticmethod
    def get_supplier_by_id(id: int):
        pass

    # Изменение адреса поставщика (параметры: Id и новый адрес в виде json в соответствии с выше описанным форматом)
    @staticmethod
    def change_supplier_address(id: int, new_address):
        pass
