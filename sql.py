from sqlite3 import *


class SQL:

    def __init__(self):
        # The file will be created if it doesn't already exist
        print("Creating db and cursor...")
        self.db = connect("data.db")
        self.cursor = self.db.cursor()
        self.create_table()

    def add_user(self, name, email, house, postcode):
        try:
            self.cursor.execute("""INSERT INTO participants(name, email, house, postcode) VALUES(?,?,?,?)""",
                                (name, email, house, postcode))
            self.db.commit()
        except Exception as e:
            print("Encountered following error: " + e)
            self.db.rollback()
            return e

    def fetch_participants(self):
        self.cursor.execute("""SELECT * FROM participants""")
        return self.cursor.fetchall()

    def reset_records(self):
        self.cursor.execute("""DROP TABLE participants""")
        self.db.commit()
        self.create_table()
        self.db.commit()

    def close(self):
        self.db.close()

    def create_table(self):
        try:
            print("Creating table...")
            # TODO Update schema to not accept empty values
            self.cursor.execute("""
            CREATE TABLE participants(id INTEGER PRIMARY KEY, name TEXT, email TEXT unique, house TEXT, postcode TEXT)
            """)
            self.db.commit()
            print("Table created!")
        except Exception as e:
            print(e)
