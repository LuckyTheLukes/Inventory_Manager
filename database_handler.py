def connect_to_database():  # sourcery skip: extract-method

    import mysql.connector

    return mysql.connector.connect(
        host="localhost", user="root", password="admin"
    )

def create_database_and_tables():    
    workshop_inventory = connect_to_database()
    
    if workshop_inventory.is_connected():
        print('Connected to the Database Server')
        dbCursor = workshop_inventory.cursor()

        dbCursor.execute("SHOW DATABASES")

        if [database for  database in dbCursor if 'workshop_inventory' in database]:
            print('Database "workshop_inventory" already exists.')
        else:
            dbCursor.execute("CREATE DATABASE workshop_inventory")
            print('Database "workshop_inventory" has been created.')

        workshop_inventory.config(database='workshop_inventory')
        workshop_inventory.reconnect()

        dbCursor.execute("SHOW TABLES")

        if [table for table in dbCursor if 'users' in table]:
            print('Table "users" already exists.')
        else:
            dbCursor.execute("CREATE TABLE users (emp_id INT PRIMARY KEY, user_name VARCHAR(255) NOT NULL, is_active BOOLEAN NOT NULL)")
            print('Table "users" has been created.')

        dbCursor.execute("SHOW TABLES")

        if [table for table in dbCursor if 'inventory' in table]:
            print('Table "inventory" already exists.')
        else:
            dbCursor.execute("CREATE TABLE inventory (item_id INT PRIMARY KEY, item_name VARCHAR(255) NOT NULL, remaining_amount INT NOT NULL)")
            print('Table "inventory" has been created.')

        workshop_inventory.close()

    else:
        print('Connection Failed')


def read_from_database(table):
    workshop_inventory = connect_to_database()
    workshop_inventory.config(database='workshop_inventory')
    workshop_inventory.reconnect()
    dbCursor = workshop_inventory.cursor()

    dbCursor.execute(f"SELECT * FROM {table}")
    data = dbCursor.fetchall()
    workshop_inventory.close()
    print(data)


def write_to_database(table, data):
    workshop_inventory = connect_to_database()
    workshop_inventory.config(database='workshop_inventory')
    workshop_inventory.reconnect()
    dbCursor = workshop_inventory.cursor()

    empID = data[0]
    userName = data[1]
    isActive = data[2]

    dbCursor.execute(f'INSERT INTO {table} (emp_id, user_name, is_active) VALUES ({empID}, "{userName}", {isActive})')
    workshop_inventory.commit()
    workshop_inventory.close()