import datetime
import psycopg2


class DBManagement:

    def create_db(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="postgres"
            )

            self.curs = self.conn.cursor()

            self.curs.execute("""SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'olx_postgres'""")
            exists = self.curs.fetchone()
            if not exists:
                self.curs.execute("""CREATE DATABASE olx_postgres;""")

            self.conn.commit()
            self.curs.close()

        except psycopg2.Error as error:
            print(error)

        finally:
            if self.conn:
                self.conn.close()

    def create_table(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="postgres",
                database="olx_postgres"
            )

            self.curs = self.conn.cursor()

            self.curs.execute("""
                CREATE TABLE IF NOT EXISTS olx(
                    id SERIAL PRIMARY KEY,
                    description VARCHAR(300),
                    "manufacture date" date,
                    location VARCHAR(100),
                    price INTEGER,
                    "date posted" date);
                    """)

            self.conn.commit()
            self.curs.close()

        except psycopg2.Error as error:
            print(error)

        finally:
            if self.conn:
                self.conn.close()

    def drop_table(self):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="postgres",
                database="olx_postgres"
            )

            self.curs = self.conn.cursor()

            self.curs.execute("""
                DROP TABLE olx;
                    """)

            self.conn.commit()
            self.curs.close()

        except psycopg2.Error as error:
            print(error)

        finally:
            if self.conn:
                self.conn.close()

    def insert_values(self, values: list):
        try:
            self.conn = psycopg2.connect(
                host="localhost",
                user="postgres",
                password="postgres",
                database="olx_postgres"
            )

            self.curs = self.conn.cursor()

            query = """INSERT INTO olx(description, "manufacture date", location, price, "date posted") VALUES (
                        %s, %s, %s, %s, %s);"""
            for value in values:
                print(value)
                desc = value[0]
                manuf_date = value[1]
                location = value[2]
                price = value[3]
                price = price if price != 0 else None
                post_date = value[4]
                manuf_date_str = manuf_date if manuf_date != datetime.date(9999, 1, 1) else None
                self.curs.execute(query, (desc, manuf_date_str, location, price, post_date))
            self.conn.commit()
            self.curs.close()
        except psycopg2.Error as error:
            print(error)

        finally:
            if self.conn:
                self.conn.close()

    def __del__(self):
        if self.curs:
            self.curs.close()
        if self.conn:
            self.conn.close()





