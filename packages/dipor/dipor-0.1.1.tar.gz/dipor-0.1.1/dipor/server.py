import http.server
import socketserver
from os import listdir
import os
import pathlib
import sys
import webbrowser


def runserver(app_name, settings_path):
    sys.path.append(os.path.dirname(settings_path))
    print(settings_path)
    import dipor_settings
    settings_tmp = dipor_settings.instance
    settings = { key: settings_tmp[key] for key in settings_tmp.keys() if key.startswith("DIPOR_")}
    print(settings)
    PORT = settings['DIPOR_PORT']
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


