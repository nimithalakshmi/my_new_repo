import sys
import pymysql

class DbOperationException(Exception):
    pass



class GameDataOperations:
    def connectDb(self):
        try:
            conn = pymysql.connect(
                host='localhost', port=3306,
                user='root', password='password',
                db='lakshmi_db', charset='utf8')
            print('Database connected successfully')
            return conn
        except pymysql.MySQLError as e:
            print(f'Error connecting to the database: {e}')
            raise

    def disConnectDb(self, connection):
        try:
            connection.close()
            print('Database disconnected')
        except pymysql.MySQLError as e:
            print(f'Error disconnecting from the database: {e}')

    def createTable(self):
        createTableQuery = '''
        CREATE TABLE IF NOT EXISTS games (
            id INT PRIMARY KEY AUTO_INCREMENT, 
            name VARCHAR(50) NOT NULL, 
            price INT, 
            CONSTRAINT price_check CHECK(price % 100 = 0), 
            minimum_players INT DEFAULT 1, 
            maximum_players INT DEFAULT 11, 
            description VARCHAR(1000)
        );
        '''
        try:
            connection = self.connectDb()
            with connection.cursor() as cursor:
                cursor.execute(createTableQuery)
                connection.commit()
                print('Table created successfully')
        except pymysql.MySQLError as e:
            print(f'Error while creating the table: {e}')
        finally:
            self.disConnectDb(connection)

    def createDb(self):
        createDbQuery = 'CREATE DATABASE IF NOT EXISTS nmamit_db'
        try:
            connection = self.connectDb()
            with connection.cursor() as cursor:
                cursor.execute(createDbQuery)
                print('Database created successfully')
        except pymysql.MySQLError as e:
            print(f'Error while creating the database: {e}')
        finally:
            self.disConnectDb(connection)

    def readGameData(self, operation):
        name = input('Enter name of the Game: ')
        price = int(input('Enter Price of the Game (per head): '))
        minPlayers = int(input('Enter minimum number of players: '))
        maxPlayers = int(input('Enter maximum number of players: '))
        if operation == 'insert':
            print('Enter Description of the Game, Use Ctrl+Z to stop: ')
            sys.stdin.flush()
            description = sys.stdin.read()
            description = description.replace('\n', ' ').strip()
            return (name, price, minPlayers, maxPlayers, description)
        id = int(input('Enter Id of the Game to update: '))
        return (name, price, minPlayers, maxPlayers, id)

    def createGame(self):
        insertQuery = '''
        INSERT INTO games (name, price, minimum_players, maximum_players, description)
        VALUES (%s, %s, %s, %s, %s)
        '''
        gameObject = self.readGameData('insert')
        try:
            connection = self.connectDb()
            with connection.cursor() as cursor:
                returnValue = cursor.execute(insertQuery, gameObject)
                if returnValue != 1:
                    raise DbOperationException
                connection.commit()
                print('Row inserted successfully')
        except DbOperationException:
            print('Error while inserting a row')
        except pymysql.MySQLError as e:
            print(f'Error while inserting a row: {e}')
        finally:
            self.disConnectDb(connection)

    def updateGame(self):
        updateQuery = '''
        UPDATE games 
        SET name = %s, price = %s, minimum_players = %s, maximum_players = %s 
        WHERE id = %s
        '''
        gameObject = self.readGameData('update')
        try:
            connection = self.connectDb()
            with connection.cursor() as cursor:
                returnValue = cursor.execute(updateQuery, gameObject)
                connection.commit()
                if returnValue != 1:
                    print(f'Game with id = {gameObject[4]} not found')
                else:
                    print('Row updated successfully')
        except pymysql.MySQLError as e:
            print(f'Error while updating the row: {e}')
        finally:
            self.disConnectDb(connection)

    def deleteGame(self):
        id = int(input('Enter Id of the Game to be deleted: '))
        deleteQuery = 'DELETE FROM games WHERE id = %s'
        try:
            connection = self.connectDb()
            with connection.cursor() as cursor:
                returnValue = cursor.execute(deleteQuery, (id,))
                connection.commit()
                if returnValue != 1:
                    print(f'Game with id = {id} not found')
                else:
                    print('Row deleted successfully')
        except pymysql.MySQLError as e:
            print(f'Error while deleting the row: {e}')
        finally:
            self.disConnectDb(connection)

    def searchGame(self):
        id = int(input('Enter Id of the Game to be searched: '))
        searchQuery = 'SELECT * FROM games WHERE id = %s'
        try:
            connection = self.connectDb()
            with connection.cursor() as cursor:
                numberOfRows = cursor.execute(searchQuery, (id,))
                if numberOfRows == 0:
                    print(f'Game with id = {id} not found')
                else:
                    row = cursor.fetchone()
                    print('Game Details is: \n', str(row))
        except pymysql.MySQLError as e:
            print(f'Error while searching the row: {e}')
        finally:
            self.disConnectDb(connection)

    def listGames(self):
        query = 'SELECT * FROM games'
        try:
            connection = self.connectDb()
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                if not rows:
                    print('No games found')
                else:
                    for row in rows:
                        print('Game Details is: \n', str(row))
        except pymysql.MySQLError as e:
            print(f'Error while listing the rows: {e}')
        finally:
            self.disConnectDb(connection)

class Menu:
    def __init__(self, gameOperations):
        self.gameOperations = gameOperations

    def exitProgram(self):
        print('End of the program')
        exit()

    def invalidInput(self):
        print('Invalid input entered')

    def getMenu(self):
        menu = {
            1: self.gameOperations.createGame,
            2: self.gameOperations.searchGame,
            3: self.gameOperations.updateGame,
            4: self.gameOperations.deleteGame,
            5: self.gameOperations.listGames,
            6: self.exitProgram
        }
        return menu

    def runMenu(self):
        menu = self.getMenu()
        while True:
            print('\n1: Create 2: Search 3: Update 4: Delete 5: ListAll 6: Exit\nYour choice: ')
            try:
                choice = int(input())
                menu.get(choice, self.invalidInput)()
            except ValueError:
                self.invalidInput()

def startApp():
    operations = GameDataOperations()
    menu = Menu(operations)
    menu.runMenu()

if __name__ == '__main__':
    startApp()
