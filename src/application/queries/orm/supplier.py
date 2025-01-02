from application.database import get_db_session
from application.models import Supplier


class SupplierORM:
    # Добавление поставщика (на вход подается json, соответствующей структуре, описанной сверху).
    @staticmethod
    def add_supplier():
        pass

    @staticmethod
    def delete_supplier(supplier_id: int):
        with get_db_session() as db_session:
            supplier_to_delete = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            if supplier_to_delete:
                db_session.delete(supplier_to_delete)
                db_session.commit()
            else:
                raise Exception(f'Client with id {supplier_id} not found')

    # Получение всех поставщиков
    @staticmethod
    def get_all_suppliers():
        pass

    @staticmethod
    def get_supplier_by_id(supplier_id: int):
        with get_db_session() as db_session:
            supplier = db_session.query(Supplier).filter(Supplier.id == supplier_id).one_or_none()
            if not supplier:
                raise Exception(f'Supplier with id {supplier_id} not found')
            return supplier

    # Изменение адреса поставщика (параметры: Id и новый адрес в виде json в соответствии с выше описанным форматом)
    @staticmethod
    def change_supplier_address(id: int, new_address):
        pass
