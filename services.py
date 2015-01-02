# This Python file is the basic file to create the web services with Tornado
# Author: Gustavo Martin Vela

import tornado.ioloop
import tornado.web
import datetime
import MySQLdb as mdb
import json
import time
#from collections import OrderedDict

import RGB

# Global variables
VERSION = "0.1"
SW_NAME = "M2More"
AUTHOR = "Gustavo Martin Vela"
DEVICE = "RPi Bilbao"

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

def dict_to_json(dict):
    normalized_now = normalized_datetime()
    results_dict = {'results': dict, 'datetime': normalized_now}
    json_dict = json.dumps(results_dict, indent = 4, separators=(',', ': '), sort_keys=True)
    return json_dict

def query_DB(queries, query_types):
    ''' Query to database and return a list with the rows directly from cursor
        - query: list of strings with the complete SQL query 
        - result: list with ONE if the query is for a result or ALL for multiple results '''
    con = database_connect()
    rows_list = []
    with con:    
        for (query, query_type) in zip(queries, query_types):
            cur = con.cursor()
            cur.execute(query)
            if query_type == "ONE":                
                rows = cur.fetchone()
            else:
                rows = cur.fetchall()
            rows_list.append(rows)
    return rows_list

class StatisticsHandler(tornado.web.RequestHandler):
    def get(self):
        rows_list = query_DB(["SELECT COUNT(*) FROM log", "SELECT COUNT(*) FROM log WHERE data = 0", 
                              "SELECT COUNT(*) FROM log WHERE data = 1"], ["ONE", "ONE", "ONE"])
        dict = [{ 'total':rows_list[0][0], 'valids':rows_list[1][0], 'invalids':rows_list[2][0] }]
        json_dict = dict_to_json(dict) 
        self.write(json_dict)

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        rows_list = query_DB(["SELECT time, temp, humi FROM log WHERE data = 1 GROUP BY time ORDER BY time"], ["ALL"])
        dict = []
        for row in rows_list[0]:
            dict.append({ 'time':row[0].strftime("%d-%m-%Y %H:%M"), 'humi':row[1], 'temp':row[2]})
        json_dict = dict_to_json(dict)
        self.write(json_dict)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        dict = [{ 'software':SW_NAME, 'author': AUTHOR, 'version': VERSION , 'device':DEVICE }]
        json_dict = dict_to_json(dict)
        self.write(json_dict)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/statistics", StatisticsHandler),
    (r"/data", DataHandler),    
])

if __name__ == "__main__":
    #start_RGB()
    #RGB.activate(RGB.RGB_BLUE)
    #time.sleep(1)
    #RGB.deactivate(RGB.RGB_BLUE)
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
