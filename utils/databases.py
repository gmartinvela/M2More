#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as mdb

db_name = 'DHT11'

db_creation_connection = mdb.connect('localhost', 'root', '221186')
db_creation_cursor = db_creation_connection.cursor()
db_creation_sql = 'CREATE DATABASE IF NOT EXISTS ' + db_name
db_creation_cursor.execute(db_creation_sql)
db_creation_connection.close()
db_creation_cursor.close()


tables_creation_connection = mdb.connect('localhost', 'root', '221186', db_name)
tables_creation_cursor = tables_creation_connection.cursor()
tables_creation_sql = '''CREATE TABLE log (
       id INT PRIMARY KEY AUTO_INCREMENT,       
       temp FLOAT(5,2),
       humi FLOAT(5,2),
       time DATETIME,
       device CHAR(50) 
       ) ENGINE=MyISAM DEFAULT CHARSET=latin1
       '''
tables_creation_cursor.execute(tables_creation_sql)
tables_creation_connection.close()
tables_creation_cursor.close()
