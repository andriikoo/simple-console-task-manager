import os
import taskmanagerlib as lib
import sqlite3 as sql
import logging
import datetime as dt

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
        return f"DB - {self.dbpath}.db"
    
    def close(self):
        self.con.close()
        logging.info("Connection closed..")

    def menu(self):  
        while True:
            print(f"You working with {self.dbpath}.db")
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
                logging.info("Connection closed..")
                print("Connection closed!")
                select_db()
                break
            else:
                print('Invalid option. Try again!')
                continue

def create_db():
    dbfolder = "databases"
    os.makedirs(dbfolder, exist_ok=True)
    name = input("Enter the name of a new DB: ")
    dbpath = os.path.join(dbfolder, f"{name}.db")
    return Tasks(dbpath)

def select_db():
    dbfolder = 'databases'
    os.makedirs(dbfolder, exist_ok=True)
    dbfiles = [f for f in os.listdir(dbfolder) if f.endswith(".db")]

    if not dbfiles:
        while True:
            question = input("No file found. Create new? (y/n): ")
            if question == 'y':
                return create_db()
            elif question == 'n':
                print("Oki, bra.")
                continue
            print ("Wrong Input!")
    
    print("Select DB to work with or create new: ")
    for i, db in enumerate(dbfiles, start=1):
        print(f"{i}. {db}")

    while True:
        try:
            choice = int(input("Enter number (or 999 to create new): "))
            if 1 <= choice <= len(dbfiles):
                dbchoice = dbfiles[choice - 1].replace(".db", "")
                return Tasks(dbchoice)
            elif choice == 999:
                create_db()
        except ValueError:
            pass
        print("Invalid option. Try again!")

db = select_db()
db.menu()

