from sqlite3 import connect, IntegrityError


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
            print("Added user '%s, %s, %s, %s, %s'" % (name, email, house, postcode, wishlist))
        except IntegrityError as e:
            print("User is attempting to use an email twice")
            self.db.rollback()
            raise e
        except Exception as e:
            print("Encountered following error: " + str(e))
            self.db.rollback()
            raise e

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
