# This Python file is the basic file to create the web services with Tornado
# Author: Gustavo Martin Vela

import tornado.ioloop
import tornado.web
import datetime
import MySQLdb as mdb
import json
import time
from collections import OrderedDict

import RGB

def start_RGB():
    ''' Configure the GPIO 11, 13 and 15 to manage the RGB LED'''
    RGB.setup()
    RGB.clear()
    return

def database_connect():
    con = mdb.connect('localhost', 'root', '221186', 'DHT11')
    return con

def normalized_datetime():
    ''' Returns the datetime in a normalized format'''
    now = datetime.datetime.now()
    pretty_now = now.strftime("%d-%m-%Y %H:%M")
    return pretty_now

class StatisticsHandler(tornado.web.RequestHandler):
    def get(self):
        pretty_now = normalized_datetime()
        con = database_connect()        
        with con:    
            cur = con.cursor()
            rows = cur.execute("SELECT COUNT(*) FROM log")
            rows_number = cur.fetchone()
            invalids = cur.execute("SELECT COUNT(*) FROM log WHERE data = 0")
            invalids_number = cur.fetchone()            
            valids = cur.execute("SELECT COUNT(*) FROM log WHERE data = 1")
            valids_number = cur.fetchone()
        #valids_percent = (float(valids_number[0]) / float(rows_number[0]) * 100)
        #invalids_percent = (float(invalids_number[0]) / float(rows_number[0]) * 100)
        statistics_dict = [ { 'total':rows_number[0], 'valids':valids_number[0], 
                              'invalids':invalids_number[0], 'time': pretty_now } ]
        statistics_json = json.dumps(statistics_dict, indent = 4, separators=(',', ': '), sort_keys=True) 
        self.write(statistics_json)

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        con = database_connect()
        with con:
            cur = con.cursor()
            rows = cur.execute("SELECT DISTINCT time, temp, humi  FROM log WHERE data = 1 ORDER BY time")
            data = cur.fetchall()
	# TODO: Data to string is not the better solution!
        data_json = json.dumps(str(data), sort_keys=True)
        self.write(data_json)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        pretty_now = normalized_datetime()
        main_dict = [ { 'device':'RPi Bilbao', 'time': pretty_now } ]
        main_json = json.dumps(main_dict, indent = 4, separators=(',', ': '), sort_keys=True)
        self.write(main_json)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/statistics", StatisticsHandler),
    (r"/data", DataHandler),    
])

if __name__ == "__main__":
    start_RGB()
    RGB.activate(RGB.RGB_BLUE)
    time.sleep(1)
    RGB.deactivate(RGB.RGB_BLUE)
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
