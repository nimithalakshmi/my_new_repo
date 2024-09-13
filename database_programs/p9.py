# List all Rows of the table
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

def printMobiles(rows):
    print('ID  NAME         PRICE ')
    print('-' * 22 )
    for row in rows:
        print('%-3s %-12s %s'%(row[0], row[1], row[2]))

def listAllRows():
    query = 'select * from mobiles'
    connectionObject = connectDb()
    cursor = connectionObject.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    if rows == None:
        print(f'No Mobiles were found')
    else:
        printMobiles(rows)
    cursor.close()
    disconnectDb(connectionObject)

listAllRows()