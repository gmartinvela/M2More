# This Python file is the basic file to create the web services with Tornado
# Author: Gustavo Martin Vela

import tornado.ioloop
import tornado.web
import datetime

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        now = datetime.datetime.now()
        pretty_now = now.strftime("%d-%m-%Y %H:%M")
        self.write("<p>RPI Bilbao</p><p>" + pretty_now  + "</p>")

application = tornado.web.Application([
    (r"/", MainHandler),
])

if __name__ == "__main__":
    application.listen(80)
    tornado.ioloop.IOLoop.instance().start()
