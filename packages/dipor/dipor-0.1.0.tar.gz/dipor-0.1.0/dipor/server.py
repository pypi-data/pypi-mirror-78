import http.server
import socketserver
from os import listdir
import os
import pathlib
import webbrowser

PORT = 5050

def runserver(app_name):
    web_dir = os.path.join(pathlib.Path().absolute(), app_name, 'public')
    os.chdir(web_dir)
    class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):            
        def do_GET(self):
            path = self.path.strip('/')
            if os.path.isfile(os.path.join(web_dir, path+".html")):
                self.path = path+".html"
                
            return http.server.SimpleHTTPRequestHandler.do_GET(self)
    handler = CustomHttpRequestHandler
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print("server is revving up...")
        print("woohoo! check out this awesome page @ http://localhost:5050")
        print("you can keep track of your requests here")
        print("see you on the actual url next time :)")
        webbrowser.open(f"http://localhost:{PORT}")
        httpd.serve_forever()


