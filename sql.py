from sqlite3 import *


class SQL:

    def __init__(self):
        # The file will be created if it doesn't already exist
        print("Creating db and cursor...")
        self.db = connect("data.db")
        self.cursor = self.db.cursor()
        try:
            print("Creating table...")
            # TODO Update schema to not accept empty values
            self.cursor.execute("""
            CREATE TABLE participants(id INTEGER PRIMARY KEY, name TEXT, email TEXT unique, house TEXT, postcode TEXT)
            """)
        except Exception as e:
            print(e)

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

    def delete_database(self):
        self.cursor.execute("""DROP TABLE participants""")
        self.db.commit()

    def close(self):
        self.db.close()


if __name__ == '__main__':

    # Creates a tmp db in the memory
    # db = connect(':memory:')
    # The file will be created if it doesn't already exist
    db = SQL()
    for i in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10):
        print("Adding users...")
        db.add_user("Tester", "example" + str(i) + "@email.com", "25", "BN12 4NR")

    users = db.fetch_participants()
    for u in users:
        print("User %s is %s" % (users.index(u), str(u)))

    db.close()
