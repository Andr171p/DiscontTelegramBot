import pymysql

from backend.database.db_connect_data import RailwayAccessDB
from backend.database.orders_db.db_orders_sql import OrdersSQL

from misc.row_wrapper import RowWrapper, InsertValues

from misc.utils import DataUtils


class OrdersEngineDB:
    def __init__(self):
        self.access_db = RailwayAccessDB()
        self.connection = None

    def db_connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.access_db.host,
                port=self.access_db.port,
                user=self.access_db.user,
                password=self.access_db.password,
                database=self.access_db.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("[SuchefOrdersDB : db_connect] :\n"
                  "connection successfully..")
        except Exception as _ex:
            print(f"[SuchefOrdersDB : db_connect] :\n"
                  f"{_ex}")

    def db_create_orders_table(self):
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.execute(OrdersSQL.create_table_query)

    def db_drop_orders_table(self):
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.execute(OrdersSQL.drop_table_query)

    def db_clear_table(self):
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.execute(OrdersSQL.clear_table_query)

    def db_select_all_data(self):
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.execute(OrdersSQL.select_all_data_query)
            result = cursor.fatchall()
        return result

    def db_insert_orders_data(self, orders):
        values = RowWrapper(data=orders).create_matrix()
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.executemany(
                OrdersSQL.insert_data_query,
                values
            )

    def db_insert_order_data(self, order_from_db):
        values = InsertValues(db_row_data=order_from_db).create_values_tuple()
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.executemany(
                OrdersSQL.insert_data_query,
                values
            )

    def db_order_data_from_phone_number(self, phone_number):
        value = (phone_number,)
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                OrdersSQL.data_from_phone_number_query,
                value
            )
            result = cursor.fatchall()
        return result

    def db_check_trigger_status(self, phone_number, triggers):
        triggers_status = "', '".join(triggers)
        value = (phone_number,)
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"{OrdersSQL.check_trigger_status}('{triggers_status}')",
                value
            )
            result = cursor.fatchall()
        return result

    def db_update_sent(self, phone_number, triggers):
        triggers_status = "', '".join(triggers)
        value = (phone_number,)
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                f"{OrdersSQL.update_sent_query}('{triggers_status}')",
                value
            )

    def db_check_sent(self, phone_number):
        values = (phone_number,)
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.execute(
                OrdersSQL.check_sent_query,
                values
            )
            result = cursor.fetchall()
        return bool(result)

    def db_update_orders_data(self, orders):
        data_utils = DataUtils()
        self.db_connect()
        with self.connection.cursor() as cursor:
            cursor.execute(OrdersSQL.select_all_data_query)
            orders_from_db = cursor.fetchall()
            for order in orders_from_db:
                order.pop('id')
            update_orders = data_utils.intersection_list(
                data=orders_from_db,
                new_data=orders,
                key='phone_number'
            )
            insert_orders = data_utils.subtract_list(
                data=orders_from_db,
                new_data=orders,
                key='phone_number'
            )
            delete_orders = data_utils.subtract_list(
                data=orders,
                new_data=orders_from_db,
                key='phone_number'
            )
            if len(orders_from_db) != 0:
                for order in delete_orders:
                    value = (order['phone_number'],)
                    cursor.execute(
                        OrdersSQL.delete_data_query,
                        value
                    )
            for order in update_orders:
                values = (order['status'], order['phone_number'],)
                cursor.execute(
                    OrdersSQL.update_data_query,
                    values
                )
            if len(insert_orders) != 0:
                values = RowWrapper(
                    data=insert_orders
                ).create_matrix()
                cursor.executemany(
                    OrdersSQL.insert_data_query,
                    values
                )
