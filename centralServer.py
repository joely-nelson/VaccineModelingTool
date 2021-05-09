import http.server
import socketserver
import urllib.parse as p
import json
import models.models

class VaccineModelingHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # parse url
        params = p.parse_qs(p.urlparse(self.path).query)
        print(params)

        if not params:
            # if url has no params, server desired file
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        else:
            # call model, pass appropriate params    

            self.path = 'sampleModelOutput.json'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
handler_object = VaccineModelingHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()