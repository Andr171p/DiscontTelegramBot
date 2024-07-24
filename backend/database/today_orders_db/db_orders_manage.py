import pymysql

from backend.database.db_connect_data import RailwayAccessDB, AccessDB

from misc.utils import format_phone_number
from misc.utils import format_order_number, format_order_time
from misc.utils import format_order_date, format_trade_card


class SuchefOrdersDB:
    def __init__(self):
        self.access_db = RailwayAccessDB()
        # self.access_db = AccessDB()
        self.connection = None
        self.users_orders_data = []

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

    def create_users_orders_table(self):
        self.db_connect()
        with self.connection.cursor() as cursor:
            create_table_query = "CREATE TABLE `users_orders`(id int AUTO_INCREMENT," \
                                 " phone_number varchar(32)," \
                                 " client longtext," \
                                 " number varchar(32)," \
                                 " date varchar(32)," \
                                 " status varchar(32)," \
                                 " sent int," \
                                 " amount int," \
                                 " pay_link longtext," \
                                 " pay_status varchar(32)," \
                                 " cooking_time_from varchar(32)," \
                                 " cooking_time_to varchar(32)," \
                                 " delivery_time_from varchar(32)," \
                                 " delivery_time_to varchar(32)," \
                                 " project varchar(32)," \
                                 " trade_point longtext," \
                                 " trade_point_card longtext," \
                                 " delivery_method varchar(32)," \
                                 " delivery_adress longtext, PRIMARY KEY (id));"
            cursor.execute(create_table_query)
            print("[SuchefOrdersDB : create_users_orders_table] :\n"
                  "Table created successfully")

    def drop_users_orders_table(self):
        self.db_connect()
        with self.connection.cursor() as cursor:
            drop_table_query = "DROP TABLE `users_orders`"
            cursor.execute(drop_table_query)
            print("[SuchefOrdersDB : drop_orders_table] :\n"
                  "Table drop successfully")

    def clear_db(self):
        self.db_connect()
        try:
            with self.connection.cursor() as cursor:
                query = "TRUNCATE TABLE `users_orders`"
                cursor.execute(query)
        except Exception as _ex:
            print(_ex)
        finally:
            self.connection.commit()
            self.connection.close()

    def db_all_data(self):
        self.db_connect()
        try:
            with self.connection.cursor() as cursor:
                sql_query = "SELECT * FROM `users_orders`"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                result = []
                for values in data:
                    result.append(list(values.values()))
        except Exception as _ex:
            print(f"def db_all_data: {_ex}")
        finally:
            cursor.close()
            self.connection.close()
            return result

    def db_insert_orders_data(self, orders_data):
        self.db_connect()
        length = len(list(orders_data.values())[0])
        try:
            with self.connection.cursor() as cursor:
                for i in range(length):
                    phone_number = format_phone_number(orders_data['phone_number'][i])
                    client = orders_data['client'][i]
                    number = format_order_number(orders_data['number'][i])
                    date = format_order_date(orders_data['date'][i])
                    status = orders_data['status'][i]
                    amount = orders_data['amount'][i]
                    pay_link = orders_data['pay_link'][i]
                    pay_status = orders_data['pay_status'][i]
                    cooking_time_from = format_order_time(orders_data['cooking_time_from'][i])
                    cooking_time_to = format_order_time(orders_data['cooking_time_to'][i])
                    delivery_time_from = format_order_time(orders_data['delivery_time_from'][i])
                    delivery_time_to = format_order_time(orders_data['delivery_time_to'][i])
                    project = orders_data['project'][i]
                    trade_point = orders_data['trade_point'][i]
                    trade_point_card = format_trade_card(orders_data['trade_point_card'][i])
                    delivery_method = orders_data['delivery_method'][i]
                    delivery_adress = orders_data['delivery_adress'][i]

                    sql_query = "INSERT INTO `users_orders`" \
                                "(phone_number, client, number, date, status, amount, pay_link, pay_status, cooking_time_from, cooking_time_to, delivery_time_from, delivery_time_to, project, trade_point, trade_point_card, delivery_method, delivery_adress)" \
                                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    parameters = (
                        phone_number, client, number, date, status, amount, pay_link, pay_status, cooking_time_from,
                        cooking_time_to, delivery_time_from, delivery_time_to, project, trade_point, trade_point_card,
                        delivery_method, delivery_adress
                    )
                    cursor.execute(sql_query, parameters)
        except Exception as _ex:
            print(f"def db_insert_orders_data: {_ex}")
        finally:
            self.connection.commit()
            self.connection.close()

    def db_order_data_from_phone_number(self, client_phone_number):
        self.db_connect()
        try:
            with self.connection.cursor() as cursor:
                sql_query = "SELECT * FROM `users_orders` WHERE phone_number = %s"
                cursor.execute(sql_query, (client_phone_number,))
                data = cursor.fetchall()
                results = []
                for values in data:
                    results.append(list(values.values()))
            return results
        except Exception as _ex:
            print(f"def db_data_from_phone_number: {_ex}")

    def db_check_update_status(self, trigger_status):
        self.db_connect()
        try:
            triggers = "', '".join(trigger_status)
            with self.connection.cursor() as cursor:
                sql_query = f"SELECT id, phone_number, client, number, date, status, amount, pay_link, pay_status, cooking_time_from, cooking_time_to, delivery_time_from, delivery_time_to, project, trade_point, trade_point_card, delivery_method, delivery_adress FROM `users_orders`" \
                            f"WHERE status IN ('{triggers}')"
                cursor.execute(sql_query)
                result = cursor.fetchall()
        except Exception as _ex:
            print(f"def db_check_update_status:\n"
                  f"{_ex}")
            return -1
        finally:
            self.connection.close()
            return result

    def db_update_and_clear_data(self, orders_at_the_time):
        self.clear_db()
        self.db_insert_orders_data(
            orders_data=orders_at_the_time
        )

    def db_update_sent_status(self, client_phone_number, trigger_status):
        self.db_connect()
        values = (
            format_phone_number(client_phone_number),
            trigger_status
        )
        try:
            with self.connection.cursor() as cursor:
                sql_query = "UPDATE `users_orders` SET sent=1 WHERE phone_number=%s AND status IN %s"
                cursor.execute(sql_query, values)
        except Exception as _ex:
            print(f"[def db_update_sent_status] :\n"
                  f"{_ex}")
        finally:
            self.connection.commit()
            self.connection.close()

    def db_check_sent_status(self, client_phone_number):
        self.db_connect()
        values = (
            format_phone_number(client_phone_number),
        )
        try:
            sql_query = " SELECT *" \
                        " FROM `users_orders`" \
                        " WHERE phone_number=%s AND sent=1"
            with self.connection.cursor() as cursor:
                cursor.execute(sql_query, values)
                result = cursor.fetchall()
        except Exception as _ex:
            print(f"[def db_check_sent_status] :\n"
                  f"{_ex}")
            return -1
        finally:
            self.connection.commit()
            self.connection.close()
            return result

    def db_update_and_set_data(self, orders_at_the_time):
        self.db_connect()
        check_order_sql_query = " SELECT *" \
                          " FROM `users_orders`" \
                          " WHERE phone_number = %s AND number = %s"
        try:
            length = len(list(orders_at_the_time.values())[0])
            with self.connection.cursor() as cursor:
                for i in range(length):
                    # unique values for checking:
                    check_values = (
                        format_phone_number(orders_at_the_time['phone_number'][i]),
                        format_order_number(orders_at_the_time['number'][i])
                    )
                    cursor.execute(check_order_sql_query, check_values)
                    # get result:
                    result = cursor.fetchall()
                    print(result)
                    if result:
                        update_data_sql_query = " UPDATE `users_orders`" \
                                                " SET status = %s WHERE number = %s"
                        update_values = (
                            orders_at_the_time['status'][i],
                            format_order_number(orders_at_the_time['number'][i])
                        )
                        cursor.execute(update_data_sql_query, update_values)
                        self.connection.commit()
                    else:
                        delete_data_sql_query = " DELETE FROM `users_orders`" \
                                                " WHERE number = %s"
                        delete_values = (
                            orders_at_the_time['number'][i]
                        )
                        cursor.execute(delete_data_sql_query, delete_values)
                        self.connection.commit()

        except Exception as _ex:
            print(f"[def db_update_and_replace_data] : {_ex}")
        finally:
            self.connection.close()

            print("[def db_update_and_set_data] : data update successfully")
