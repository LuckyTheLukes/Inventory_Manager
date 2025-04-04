def create_database_and_tables():  # sourcery skip: extract-method

    import mysql.connector

    workshop_inventory = mysql.connector.connect(
    host="localhost",
    user="root",
    password="admin"
    )

    if workshop_inventory.is_connected():
        print('Connected to the Database Server')
        dbCursor = workshop_inventory.cursor()

        dbCursor.execute('SHOW DATABASES')

        if [database for  database in dbCursor if 'workshop_inventory' in database]:
            print('Database "workshop_inventory" already exists.')
        else:
            dbCursor.execute('CREATE DATABASE workshop_inventory')
            print('Database "workshop_inventory" has been created.')

        workshop_inventory.config(database='workshop_inventory')
        workshop_inventory.reconnect()

        dbCursor.execute('SHOW TABLES')

        if [table for table in dbCursor if 'users' in table]:
            print('Table "users" already exists.')
        else:
            dbCursor.execute('CREATE TABLE users (user_id INT PRIMARY KEY,'
                            'user_name VARCHAR(255) NOT NULL, is_active BOOLEAN NOT NULL)')
            print('Table "users" has been created.')

        dbCursor.execute('SHOW TABLES')

        if [table for table in dbCursor if 'inventory' in table]:
            print('Table "inventory" already exists.')
        else:
            dbCursor.execute('CREATE TABLE inventory (item_id INT PRIMARY KEY,'
                            'item_name VARCHAR(255) NOT NULL, remaining_amount INT NOT NULL)')
            print('Table "inventory" has been created.')

        workshop_inventory.close()

    else:
        print('Connection Failed')

if __name__ == '__main__':
    create_database_and_tables()