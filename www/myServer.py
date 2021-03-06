#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import path, sep, curdir
import cgi
import mraa
import datetime

class myHandler(BaseHTTPRequestHandler):

    

    def do_GET(self):
        print "GET request: " + self.path
        mimetypes = {'.html' : 'text/html',
                 '.txt'  : 'text',
                 '.jpg'  : 'image/jpeg',
                 '.gif'  : 'image/gif',
                 '.png'  : 'image/png',
                 '.css'  : 'text/css',
                 '.js'   : 'application/javascript'
                 }
        
        if self.path == "/":
            self.path = "/index.html"

        ext = path.splitext(self.path)[1] 
        try:
            if ext in mimetypes:
                self.send_response(200)
                self.send_header('Content-text', mimetypes[ext])
                self.end_headers()

                with open(curdir + sep + self.path, "r") as f:
                    self.wfile.write(f.read())
        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)

    def do_POST(self):
        print "POST request: " + self.path
        form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                    'CONTENT_TYPE':self.headers['Content-type'],
        })

        self.send_response(200)
        self.end_headers()

        if 'usermsg' in form:
            u = mraa.Uart(0)
            u.setBaudRate(9600)
            u.setMode(8, mraa.UART_PARITY_NONE, 1)
            u.setFlowcontrol(False, False)

            u.writeStr(form['usermsg'].value + "\n")
            u.flush()

if __name__ == '__main__':
    try:
        serv = HTTPServer(('', 80), myHandler)
        print '%s Server started at port 80' % \
                datetime.datetime.strftime(
                        datetime.datetime.now(), "%m-%d-%y %H:%M:%S")
        serv.serve_forever()

    except KeyboardInterrupt:
        print '%s Server stopped by user, exiting' % \
                datetime.datetime.strftime(
                        datetime.datetime.now(), "%m-%d-%y %H:%M:%S")
        serv.socket.close()
