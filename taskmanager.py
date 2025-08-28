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

con = sql.connect("tasks.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS task(
id INTEGER PRIMARY KEY AUTOINCREMENT,
title TEXT,
status TEXT,
created_at DATETIME)""")

def add_task():
    title = input("Enter the title: ").lower()
    while True:
        status = input("Enter the status (1. new/ 2. in progress/3. done): ").lower()
        if status == '1':
            status = 'new'
            break
        elif status == '2':
            status = 'in progress'
            break
        elif status == '3':
            status = 'done'
            break
        else:
            print("Invalid input. Try again!")
            continue
    created_at = dt.datetime.now().strftime("%d.%m.%y / %H:%M:%S")

    cur.execute("""INSERT INTO task(title, status, created_at)
    VALUES (?, ?, ?)""", (title, status, created_at))
    con.commit()
    task_id = cur.lastrowid
    print(f'New task succesfully added! ID: {task_id}')
    logging.info(f"New task created ID: {task_id}..")

def show_tasks():
    cur.execute("SELECT * FROM task")
    rows = cur.fetchall()

    if not rows:
        print("No tasks found!")
        logging.warning("No tasks found..")
        return

    for row in rows:
        id, title, status, created_at = row
        print(f"{id}. {title} - {status} - {created_at}")
    logging.info("All tasks displayed..")

def delete_task():
    show_tasks()
    while True:
        try:
            taskid = int(input("Enter task-id to delete: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            logging.warning("User entered non-integer task ID for deletion.")
            continue

        cur.execute("SELECT id FROM task WHERE id = ?", (taskid,))
        result = cur.fetchone()

        if result is None:
            print(f"Task with id {taskid} not found.")
            logging.warning(f"Attempt to delete non-existing task #{taskid}")
            continue

        cur.execute("DELETE FROM task WHERE id = ?", (taskid,))
        con.commit()
        print("Task successfully deleted!")
        logging.info(f"Task #{taskid} deleted.")
        break

def update_task():
    show_tasks()
    while True:
        try:
            taskid = int(input("Enter task-id to update: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            logging.warning("User entered non-integer task ID for deletion.")
            continue
            
        cur.execute("SELECT id FROM task WHERE id = ?", (taskid,))
        result = cur.fetchone()

        if result is None:
            print(f"Task with id {taskid} not found.")
            logging.warning(f"Attempt to update non-existing task #{taskid}")
            continue

        q = input("What would you like to update (1: title, 2: status)?: ")
        if q == '1':
            new_title = input("Enter new title: ").lower()
            cur.execute("UPDATE task SET title = ? WHERE id = ?", (new_title, taskid))
            con.commit()
            print("You succesfully updated title!")
            logging.info(f"Task #{taskid} updated title to {new_title}..")
            break
        elif q == '2':
            while True:
                new_status = input("Enter new status (1. new/ 2. in progress/3. done): ")
                if new_status == '1':
                    new_status = 'new'
                    break
                elif new_status == '2':
                    new_status = 'in progress'
                    break
                elif new_status == '3':
                    new_status = 'done'
                    break
                else:
                    print("Invalid input. Try again!")
                    continue
            cur.execute("UPDATE task SET status = ? WHERE id = ?", (new_status, taskid))
            con.commit()
            print("You succesfully updated status!")                
            logging.info(f"Task #{taskid} updated status to {new_status}..")
            break
        else:
            print("Invalid option. Try again!")
            continue

while True:
    print("Welcome to the Console-Task-Manager!")
    print("1. Add task\n2. Show tasks\n3. Update task\n4. Delete task\n5. Exit")
    choice = input("Select an action: ")
    if choice == '1':
        add_task()
    elif choice == '2':
        show_tasks()
    elif choice == '3':
        update_task()
    elif choice == '4':
        delete_task()
    elif choice == '5':
        con.close()
        break
    else:
        print('Invalid option. Try again!')
        continue
