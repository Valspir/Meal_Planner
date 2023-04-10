import sqlite3
from http.server import BaseHTTPRequestHandler, HTTPServer
import time

hostName = "localhost"
serverPort = 8080

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0].strip("/")
        if(len(self.path.split("?"))>1):
            args = self.path.split("?")[1].split("&")
        if(path == "search"):
            self.send_response(200)
            #self.send_header("Content-Type", "text/html")
            self.end_headers()
            f = open('index.html','r')
            html = f.read()
            self.wfile.write(bytes(html,'utf-8'))
        else:
            try:
                self.send_response(200)
                #self.send_header("Content-Type", "text/html")
                self.end_headers()
                f = open(path,'r')
                html = f.read()
                self.wfile.write(bytes(html,'utf-8'))
            except:
                self.send_response(404)

if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
