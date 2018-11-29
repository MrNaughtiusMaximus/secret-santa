from sqlite3 import *


class SQL:

    def __init__(self):
        # The file will be created if it doesn't already exist
        print("Creating db and cursor...")
        self.db = connect("data.db")
        self.cursor = self.db.cursor()
        self.create_participants_table()

    def add_user(self, name, email, house, postcode, wishlist):
        try:
            self.cursor.execute("""INSERT INTO participants(name, email, house, postcode, wishlist) VALUES(?,?,?,?,?)""",
                                (name, email, house, postcode, wishlist))
            self.db.commit()
        except Exception as e:
            print("Encountered following error: " + str(e))
            self.db.rollback()
            return e

    def fetch_participants_from_first_table(self):
        self.cursor.execute("""SELECT name FROM sqlite_master WHERE type = 'table'""")
        tb = self.cursor.fetchall()
        self.cursor.execute("""SELECT * FROM %s""" % tb[0])
        return self.cursor.fetchall()

    def fetch_participants(self):
        self.cursor.execute("""SELECT * FROM participants""")
        return self.cursor.fetchall()

    def reset_records(self):
        self.cursor.execute("""DROP TABLE participants""")
        self.db.commit()
        self.create_participants_table()
        self.db.commit()

    def close(self):
        self.db.close()

    def create_participants_table(self):
        try:
            print("Creating table...")
            # TODO Update schema to not accept empty values
            self.cursor.execute("""
            CREATE TABLE participants(id INTEGER PRIMARY KEY, 
                                      name TEXT NOT NULL, 
                                      email TEXT unique NOT NULL, 
                                      house TEXT NOT NULL, 
                                      postcode TEXT NOT NULL,
                                      wishlist TEXT
                                      )
            """)
            self.db.commit()
            print("Table created!")
        except Exception as e:
            print(e)

    # TODO Finish
    def create_nice_list(self, name):
        try:
            print("Creating nice list table %s" % name)
            self.cursor.execute("""
            CREATE TABLE %s(id INTEGER PRIMARY KEY, email TEXT unique)
            """ % name)
            self.db.commit()
            print("Table created!")

        except Exception as e:
            print(e)
