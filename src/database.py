import psycopg2

from contextlib import contextmanager


class ConnectionDb:
    def connect(self, cursor_factory=None):
        self.conn = psycopg2.connect(
            dbname='registration', 
            user='postgres', 
            password='lola2015', 
            host='127.0.0.1', 
            port='5432',
            cursor_factory=cursor_factory
        )
        
        return self.conn
    

class SelectUser:
    @classmethod
    @contextmanager
    def context_manager(cls, connect, sql, by_data=None):
        cls.conn = connect
        cls.sql = sql
        cls.by_data = by_data

        try:
            cur = cls.conn.cursor()
            cur.execute(cls.sql, (cls.by_data,))  
            yield cur

        finally:
            cur.close()
            cls.conn.close()

    @classmethod
    def all_users(cls, connect):
        cls.conn = connect
        cls.sql = "SELECT * FROM users.profiles;"

        with cls.context_manager(cls.conn, cls.sql) as manager:
            return manager.fetchall() 
    

    @classmethod
    def by_id(cls, connect, id):
        cls.conn = connect
        cls.id = id
        cls.sql = "SELECT * FROM users.profiles WHERE id = %s;"

        with cls.context_manager(cls.conn, cls.sql, cls.id) as manager:
            return manager.fetchone() 
        
    

    @classmethod
    def by_login(cls, connect, login):
        cls.conn = connect
        cls.login = login
        cls.sql = "SELECT * FROM users.profiles WHERE login = %s;"

        with cls.context_manager(cls.conn, cls.sql, cls.login) as manager:
            return manager.fetchone()
        
    
class InsertUser:
    @classmethod
    def insert_all(cls, connect, data):
        cls.conn = connect

        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO users.profiles (
                        first_name, last_name, email, status, city,
                        address, age, floor, apartament_number, data_registratsii,
                        password, login
                    ) VALUES (
                        %(first_name)s, %(last_name)s, %(email)s,
                        %(status)s, %(city)s, %(address)s, %(age)s,
                        %(floor)s, %(apartament_number)s, %(data_registratsii)s,
                        %(login)s, %(password)s
                    )
                    """, data
                )


class DeleteUser:
    @classmethod
    def by_id(cls, connect, id):
        cls.conn = connect

        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute(f"DELETE FROM users.profiles WHERE id = {id};")


class UpdateUser:
    @classmethod
    def by_id(cls, connect, data):
        cls.conn = connect
        param = [f"{key} = %({key})s" for key in data.keys() if key != 'id']

        with cls.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    f"UPDATE users.profiles SET {', '.join(param)} WHERE id = %(id)s;", data
                )