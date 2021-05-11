import http.server
import socketserver
import urllib.parse as p
import json
import models.models as m

class VaccineModelingHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # parse url
        params = p.parse_qs(p.urlparse(self.path).query)
        print(params)

        if not params:
            # if url has no params, server desired file
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        else:
            alpha = float(params["alpha"][0])
            beta = float(params["beta"][0])
            eps = float(params["eps"][0])
            gamma = float(params["gamma"][0])
            vac_start_day = int(params["vac_start_day"][0])
            uptake_per = float(params["uptake_per"][0])
            num_vac_days = int(params["num_vac_days"][0])
            vac_rate = float(params["vac_rate"][0])

            m.simulate_world(alpha, beta, gamma, eps, vac_start_day, uptake_per, num_vac_days, vac_rate)

            self.path = './json_io_files/model_output.json'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
handler_object = VaccineModelingHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)

print('Starting Server on port 8000')

# Star the server
my_server.serve_forever()
