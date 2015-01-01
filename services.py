# This Python file is the basic file to create the web services with Tornado
# Author: Gustavo Martin Vela

import tornado.ioloop
import tornado.web
import datetime
import MySQLdb as mdb
import json
#con = mdb.connect('localhost', 'root', '221186', 'DHT11');
#with con:
#    cur = con.cursor()
#    cur.execute("SELECT * FROM log")
#    rows = cur.fetchall()
#    for row in rows:
#        print row

class StatisticsHandler(tornado.web.RequestHandler):
    def get(self):
        now = datetime.datetime.now()
        pretty_now = now.strftime("%d-%m-%Y %H:%M")
        con = mdb.connect('localhost', 'root', '221186', 'DHT11');        
        with con:    
            cur = con.cursor()
            rows = cur.execute("select count(*) from log")
            rows_number = cur.fetchone()
            invalids = cur.execute("select count(*) from log where data = 0")
            invalids_number = cur.fetchone()            
            valids = cur.execute("select count(*) from log where data = 1")
            valids_number = cur.fetchone()
            valids_percent = (float(valids_number[0]) / float(rows_number[0]) * 100)
            invalids_percent = (float(invalids_number[0]) / float(rows_number[0]) * 100)
            statistics_dict = [ { 'total':rows_number[0], 'valids':valids_number[0], 'invalids':invalids_number[0], '%valids':str(valids_percent) , '%invalids':str(invalids_percent)  } ]
            statistics_json = json.dumps(statistics_dict) 
            #self.write("<p>Statistics</p><p>Valid data: " + str(valids_percent)  + " %</p><p>Invalid data: " + str(invalids_percent)  + " %</p>")
            self.write(statistics_json)

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        now = datetime.datetime.now()
        pretty_now = now.strftime("%d-%m-%Y %H:%M")
        main_dict = [ { 'device':'RPi BILBAO', 'time': pretty_now } ]
        main_json = json.dumps(main_dict)
        #self.write("<p>RPI Bilbao</p><p>" + pretty_now  + "</p>")
        self.write(main_json)

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/statistics", StatisticsHandler),
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
