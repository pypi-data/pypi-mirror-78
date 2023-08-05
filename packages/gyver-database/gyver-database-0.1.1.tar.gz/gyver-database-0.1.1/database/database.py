import sqlite3


class DB():
    
    def __init__(self,dbname:str,debug=False):
        
        self.db = sqlite3.connect(dbname+'.db')
        self.sql = self.db.cursor()
        self.debug = debug
        if self.debug == True:
            print('init good')
        

    def createTable(self, table: str,structure: dict):
        self.table = table
        self.columns = structure
        query = 'CREATE TABLE IF NOT EXISTS '
        query += table + ' ('
        lenth = len(structure)
        loop = 0
        for key in structure:
            loop += 1
            if loop == lenth:
                query += key + ' ' + structure[key] + ''
            else:
              query += key + ' ' + structure[key] + ','

        query += ')'

        self.sql.execute(query)
        if self.debug == True:
            print(query)
        self.db.commit()

    def havewrite(self, column:str,value,table=None):
        if table == None:
            table = self.table
        query = 'SELECT ' + column + ' FROM ' + table + ' WHERE ' + column + ' = "{}"'.format(value)
        self.sql.execute(query)
        if self.sql.fetchone() is None:
            if self.debug == True:
                print(query)
                print(False)
            return False
        else:
            if self.debug == True:
                print(query)
                print(True)
            return True

    def write(self,data:list,table=None):
        if table == None:
            table = self.table
        
        query = 'INSERT INTO '+ table
        
        query += ' VALUES ('
        lenth2 = len(data)
        loop = 0
        for obj in data:
            loop += 1
            if loop == lenth2:
                query += "'" + str(obj) + "')"
            else:
              query += "'" + str(obj) + "', "
        
        
        if self.debug == True:
            print(query)
        self.sql.execute(query)
        self.db.commit()

    def edit(self,value,idvalue,column,idcolumn=None,table=None):
        if table == None:
            table = self.table
        if idcolumn == None:
            idcolumn = column
        query = 'UPDATE {0} SET {1} = "{2}" WHERE {3} = "{4}"'.format(table, column,value, idcolumn,idvalue)
        self.sql.execute(query)
        if self.debug == True:
            print(query)
        self.db.commit()

    def delete(self,idvalue,idcolumn,table=None):
        if table == None:
            table = self.table
        query = 'DELETE FROM {0} WHERE {1} = "{2}"'.format(table,idcolumn,idvalue)
        self.sql.execute(query)
        if self.debug == True:
            print(query)
        self.db.commit()

    def getall(self,table=None):
        if table == None:
            table = self.table
        self.sql.execute('SELECT * FROM '+table)
        return self.sql.fetchall()

    def getline(self,idvalue,idcolumn,getval=None,returnone = True,table = None):
        if table == None:
            table = self.table
        if getval == None:
            getval = '*'
        query = 'SELECT {0} FROM {1} WHERE {2} = "{3}"'.format(getval,table,idcolumn,idvalue)

        self.sql.execute(query)
        if returnone == True:
            return self.sql.fetchone()
        else:
            return self.sql.fetchall()
    def getcolumns(self,table = None):
        if table == None:
            table = self.table
        names = list(map(lambda x: x[0], self.sql.description))
        return names

    

