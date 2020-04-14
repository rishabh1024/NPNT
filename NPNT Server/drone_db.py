import sqlite3
from sqlite3 import Error

 
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return conn
 
 
def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def print_data(conn, extract_data):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(extract_data)
    except Error as e:
        print(e)

    rows = c.fetchall()
 
    for row in rows:
        print(row)

def insert_drone_reg_data(device_id,model_id, drone_op, register_date):

    database = r"C:\sqlite\db\pythonsqlite.db"

    conn = create_connection(database)

    try:
        c = conn.cursor()
        conn.commit()
        param = (device_id, model_id, drone_op, str(register_date))
        c.execute("INSERT INTO Drone_Register (Dev_id, Mod_id, Operator, reg_date)"
                    " VALUES (?,?,?,?)", param)
        conn.commit()
    except Error as e:
        print(e)
 
def main():

    database = r"C:\sqlite\db\pythonsqlite.db"
 
    sql_create_drone_database = """CREATE TABLE IF NOT EXISTS Drone_Register (
                                    Dev_id integer PRIMARY KEY,
                                    Mod_id integer NOT NULL,
                                    Operator integer NOT NULL,
                                    reg_date text NOT NULL);"""

    sql_show_data_entry = """SELECT * FROM Drone_Register"""

 
    # create a database connection
    conn = create_connection(database)
 
    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_drone_database)
    else:
        print("Error! cannot create the database connection.")

    print_data(conn, sql_show_data_entry)

if __name__ == '__main__':
    main()