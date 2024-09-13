# search a row in the table
import pymysql

def connectDb():
    connectionObj = pymysql.Connect(
            host='localhost', port=3306,
            user='root', password='root123',
            db='nimitha_db', charset='utf8')
    print('Database connected successfully')
    return connectionObj

def disconnectDb(conn):
    conn.close()
    print('Database disconnected successfully')

def searchRow():
    query = 'select *from mobiles where id = %s'
    id = int(input('Enter Id of mobile to be searched: '))  
    connectionObject = connectDb()
    cursor = connectionObject.cursor()
    cursor.execute(query, (id))
    row=cursor.fetchone()
    if row==None:
        print("mobile.with id={id} not found")
    else:
        print(f'id:{row[0]},Name:{row[1]},price:{row[2]}')
        cursor.close()
    disconnectDb(connectionObject)

searchRow()