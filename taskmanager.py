import os
import taskmanagerlib as lib
import sqlite3 as sql
import logging

logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s | %(levelname)s | %(message)s",
    datefmt = "%d.%m.%y - %H:%M:%S",
    handlers = [
        logging.FileHandler('logs.txt')
      # logging.StreamHandler()
    ]
)

class Tasks:
    def __init__(self, dbpath):
        self.dbpath = dbpath
        self.con = sql.connect(self.dbpath)
        self.cur = self.con.cursor()
        self.cur.execute("""CREATE TABLE IF NOT EXISTS task(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            status TEXT,
            created_at DATETIME)""")
        self.con.commit()

    def __str__(self):
        return f"DB - {self.dbpath}"
    
    def close(self):
        self.con.close()
        logging.info("Connection closed..")

    def menu(self):  
        while True:
            print(f"You working with {self.dbpath}")
            print("1. Add task\n2. Show tasks\n3. Update task\n4. Delete task\n5. Exit")
            choice = input("Select an action: ")
            if choice == '1':
                lib.add_task(self)
            elif choice == '2':
                lib.show_tasks(self)
            elif choice == '3':
                lib.update_task(self)
            elif choice == '4':
                lib.delete_task(self)
            elif choice == '5':
                self.close()
                print("Connection closed!")
                return
            else:
                print('Invalid option. Try again!')
                continue

def create_db():
    dbfolder = "databases"
    os.makedirs(dbfolder, exist_ok=True)
    name = input("Enter the name of a new DB: ")
    dbpath = os.path.join(dbfolder, f"{name}.db")

    if os.path.exists(dbpath):
        logging.info(f"DB {dbpath} already exists. Opening it..")
        print("DB already exists. Opening it!")
    else:
        logging.info("Database created..")
        print("DB succesfully created!")
    return Tasks(dbpath)

def select_db():
    dbfolder = 'databases'
    os.makedirs(dbfolder, exist_ok=True)
    dbfiles = [f for f in os.listdir(dbfolder) if f.endswith(".db")]

    if not dbfiles:
        print("No file found. Creating new..")
        return create_db()
    
    print("Select DB to work with or create new: ")
    for i, db in enumerate(dbfiles, start=1):
        print(f"{i}. {db}")

    while True:
        try:
            choice = int(input("Enter number (999 to create new DB) | (0 to exit): "))
            if 1 <= choice <= len(dbfiles):
                dbchoice = os.path.join(dbfolder, dbfiles[choice - 1])
                return Tasks(dbchoice)
            elif choice == 999:
                return create_db()
            elif choice == 0:
                return None
        except ValueError:
            pass
        print("Invalid option. Try again!")

while True:
    db = select_db()
    if db is None:
        print("Exiting program..")
        break
    db.menu()
