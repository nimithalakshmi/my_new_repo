# delete a row in the table
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

def deleteRow():
    query = 'delete from  mobiles where id = %s'
    id = int(input('Enter Id of mobile to be deleted:'))  
    connectionObject = connectDb()
    cursor = connectionObject.cursor()
    rows_deleted=cursor.execute(query, (id))
    connectionObject.commit()
    cursor.close()
    if rows_deleted == 1:
        print('Row deleted')
    else:
        print(f"mobile with id={id} not found")
    disconnectDb(connectionObject)

deleteRow()