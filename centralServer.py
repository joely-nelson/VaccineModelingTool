import http.server
import socketserver
import urllib.parse as p
import json
import models.models as m
import cgi

class VaccineModelingHttpRequestHandler(http.server.SimpleHTTPRequestHandler):    
    
    def do_POST(self):
        # error checking
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        
        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
            
        # read the custom country by country params into dictionary
        length = int(self.headers.get('content-length'))
        customParams = json.loads(self.rfile.read(length))

        # extract num days for simulation
        url_query = p.parse_qs(p.urlparse(self.path).query)
        numDays = url_query["numDays"][0]


        # TODO: simulationResults = m.simulate_world(customParams, numDays)

        simulationResults = {'hello': 'world', 'received': 'ok'}
        resultBytes = bytes(json.dumps(simulationResults), "utf8")
        
        # return data
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(resultBytes))
        self.send_header("Content-Type", "application/json; charset=UTF-8")
        self.end_headers()

        self.wfile.write(resultBytes)
        return

# Create an object of the above class
handler_object = VaccineModelingHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)

print('Starting Server on port 8000')

# Star the server
my_server.serve_forever()
