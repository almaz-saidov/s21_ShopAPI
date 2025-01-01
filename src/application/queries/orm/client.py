from application.models import Client


class ClientORM:
    # Добавление клиента (на вход подается json, соответствующей структуре, описанной сверху).
    @staticmethod
    def add_client():
        pass

    # Удаление клиента (по его идентификатору)
    @staticmethod
    def delete_client(client_id: int):
        pass

    # Получение всех клиентов (В данном запросе необходимо предусмотреть опциональные параметры пагинации в строке запроса: limit и offset). В случае отсутствия эти параметров возвращать весь список.
    @staticmethod
    def get_all_clients():
        pass

    # Получение клиентов по имени и фамилии (параметры — имя и фамилия)
    @staticmethod
    def get_client_by_name_and_surname(name: str, surname: str):
        pass

    # Изменение адреса клиента (параметры: Id и новый адрес в виде json в соответствии с выше описанным форматом)
    @staticmethod
    def change_client_address(id: int, new_address):
        pass
