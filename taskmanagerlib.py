import datetime as dt
import logging

def get_status():
    while True:
        status = input("Enter status (1. new/2. in progress/3. done): ")
        variants = {'1': 'new', '2': 'in progress', '3': 'done'}
        if status in variants:
            return variants[status]
        print("Invalid input. Try again!")

def add_task(db):
    title = input("Enter the title: ")
    status = get_status()
    created_at = dt.datetime.now().strftime("%d.%m.%y / %H:%M:%S")

    db.cur.execute("""INSERT INTO task(title, status, created_at)
    VALUES (?, ?, ?)""", (title, status, created_at))
    db.con.commit()
    task_id = db.cur.lastrowid
    print(f'New task successfully added! ID: {task_id}')
    logging.info(f"New task created ID: {task_id}..")

def show_tasks(db):
    db.cur.execute("SELECT * FROM task")
    rows = db.cur.fetchall()

    if not rows:
        print("No tasks found!")
        logging.warning("No tasks found..")
        return

    for row in rows:
        id, title, status, created_at = row
        print(f"{id}. {title} - {status} - {created_at}")
    logging.info("All tasks displayed..")

def delete_task(db):
    show_tasks(db)
    while True:
        try:
            taskid = int(input("Enter task-id to delete: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            logging.warning("User entered non-integer task ID for deletion.")
            continue

        db.cur.execute("SELECT id FROM task WHERE id = ?", (taskid,))
        result = db.cur.fetchone()

        if result is None:
            print(f"Task with id {taskid} not found.")
            logging.warning(f"Attempt to delete non-existing task #{taskid}")
            continue

        db.cur.execute("DELETE FROM task WHERE id = ?", (taskid,))
        db.con.commit()
        print("Task successfully deleted!")
        logging.info(f"Task #{taskid} deleted.")
        break

def update_task(db):
    show_tasks(db)
    while True:
        try:
            taskid = int(input("Enter task-id to update: "))
        except ValueError:
            print("Invalid input! Please enter a number.")
            logging.warning("User entered non-integer task ID for deletion.")
            continue
            
        db.cur.execute("SELECT id FROM task WHERE id = ?", (taskid,))
        result = db.cur.fetchone()

        if result is None:
            print(f"Task with id {taskid} not found.")
            logging.warning(f"Attempt to update non-existing task #{taskid}")
            continue

        q = input("What would you like to update (1: title, 2: status)?: ")
        if q == '1':
            new_title = input("Enter new title: ")
            db.cur.execute("UPDATE task SET title = ? WHERE id = ?", (new_title, taskid))
            db.con.commit()
            print("You successfully updated title!")
            logging.info(f"Task #{taskid} updated title to {new_title}..")
            break
        elif q == '2':
            status = get_status()
            db.cur.execute("UPDATE task SET status = ? WHERE id = ?", (status, taskid))
            db.con.commit()
            print("You successfully updated status!")                
            logging.info(f"Task #{taskid} updated status to {status}..")
            break
        else:
            print("Invalid option. Try again!")
            continue
