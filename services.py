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

def dict_to_json(dict, **kwargs):
    normalized_now = normalized_datetime()
    results_dict = {'results': dict, 'datetime': normalized_now}
    if kwargs:    
        results_dict.update(kwargs)
    json_dict = json.dumps(results_dict)
    return json_dict

def prepare_datetimes(date):
    start = date + ' 00:00:00'
    end = date + ' 23:59:59'
    return start, end

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
    ''' This service retrieve the quality statistics of the measures of a certain day '''
    def get(self, date):
        start, end = prepare_datetimes(date)
        rows_list = query_DB(["SELECT COUNT(*) FROM log WHERE time between '" + start + "' and '" + end  + "'", 
                              "SELECT COUNT(*) FROM log WHERE data = 0 AND time between '" + start + "' and '" + end  + "'", 
                              "SELECT COUNT(*) FROM log WHERE data = 1 AND time between '" + start + "' and '" + end  + "'"], 
                              ["ONE", "ONE", "ONE"])
        dict = [{ 'total':rows_list[0][0], 'invalids':rows_list[1][0], 'valids':rows_list[2][0] }]
        json_dict = dict_to_json(dict, records_number = rows_list[0][0]) 
        self.set_header("Content-Type", "application/json")        
        self.write(json_dict)

class DataHandler(tornado.web.RequestHandler):
    ''' This service retrieve the humidity and temperature records of the measures of a certain day '''
    def get(self, date):
        start, end = prepare_datetimes(date)
        rows_list = query_DB(["SELECT time, temp, humi FROM log WHERE data = 1 AND time between '" + start + "' and '" + end  + "' GROUP BY time ORDER BY time",
                              "SELECT COUNT(DISTINCT time) FROM log WHERE data = 1 AND time between '" + start + "' and '" + end  + "'"], ["ALL", "ONE"])
        dict = []
        for row in rows_list[0]:
            dict.append({ 'time':row[0].strftime("%d-%m-%Y %H:%M"), 'humi':row[1], 'temp':row[2]})
        json_dict = dict_to_json(dict, records_number = rows_list[1][0])
        self.set_header("Content-Type", "application/json")
        self.write(json_dict)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        dict = [{ 'software':SW_NAME, 'author': AUTHOR, 'version': VERSION , 'device':DEVICE }]
        json_dict = dict_to_json(dict)
        self.set_header("Content-Type", "application/json")
        self.write(json_dict)

class NowHandler(tornado.web.RequestHandler):
    def get(self):
        rows_list = query_DB(["SELECT time, temp, humi FROM log WHERE data=1 ORDER BY id DESC LIMIT 1"], ["ALL"])
        dict = []
        for row in rows_list[0]:
            dict.append({ 'time':row[0].strftime("%d-%m-%Y %H:%M"), 'humi':row[1], 'temp':row[2]})
        json_dict = dict_to_json(dict)
        self.set_header("Content-Type", "application/json")
        self.write(json_dict)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/statistics/([^/]+)", StatisticsHandler),
    (r"/data/([^/]+)", DataHandler),
    (r"/last", NowHandler),    
])

if __name__ == "__main__":
    #start_RGB()
    #RGB.activate(RGB.RGB_BLUE)
    #time.sleep(1)
    #RGB.deactivate(RGB.RGB_BLUE)
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
