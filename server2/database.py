import mysql.connector

def setConn():
    conn = mysql.connector.connect(
        user="root",
        password="",
        host="localhost",
        database="db_bukatoko"
    )
    return conn

def inup(query, val):
    conn = setConn()
    mycursor = conn.cursor()
    mycursor.execute(query,val)
    conn.commit()

def rowCount(query):
    conn = setConn()
    mycursor = conn.cursor()
    mycursor.execute(query)
    mycursor.fetchall()
    rc = mycursor.rowcount
    return rc

def getData(query):
    conn = setConn()
    if rowCount(query) > 0:
        cursor = conn.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data
    else:
        return None

def insertData(table, data):
    col = ', '.join(data.keys())
    nval = "%s" + ", %s" * (len(data)-1)
    query = f"INSERT INTO {table} ({col}) VALUES ({nval})"
    values = list(data.values())
    inup(query, values)