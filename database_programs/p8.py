# search a row in the table
import pymysql

def connectDb():
    connectionObj = pymysql.Connect(
            host='localhost', port=3306,
            user='root', password='password',
            db='lakshmi_db', charset='utf8')
    print('Database connected successfully')
    return connectionObj

def disconnectDb(conn):
    conn.close()
    print('Database disconnected successfully')

def searchRow():
    query = 'select * from  mobiles where id = %s'
    id = int(input('Enter Id of mobile to be searched:'))  
    connectionObject = connectDb()
    cursor = connectionObject.cursor()
    cursor.execute(query, (id))
    row = cursor.fetchone()
    if row == None:
        print(f"mobile with id={id} not found")
    else:
        print(f"ID:{row[0]},Name:{row[1]},Price:{row[2]},")
    cursor.close()
    disconnectDb(connectionObject)

searchRow()