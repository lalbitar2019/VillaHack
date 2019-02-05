import pyodbc
import configparser

config = configparser.ConfigParser()
config.read('conf.ini')
# Some other example server values are
# server = 'localhost\sqlexpress' # for a named instance
# server = 'myserver,port' # to specify an alternate port
cnxn = pyodbc.connect(config['Default']['DB'])
cursor = cnxn.cursor()
#Sample select query
cursor.execute("SELECT * from images") 
row = cursor.fetchone() 
while row: 
    print row 
    row = cursor.fetchone()

cnxn.close
