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
            alpha = float(params["alpha"])
            beta = float(params["beta"])
            eps = float(params["eps"])
            gamma = float(params["gamma"])
            vac_start_day = int(params["vac_start_day"])
            uptake_per = float(params["uptake_per"])
            num_vac_days = int(params["num_vac_days"])
            vac_rate = float(params["vac_rate"])

            m.simulate_world(alpha, beta, gamma, eps, vac_start_day, uptake_per, num_vac_days, vac_rate)

            self.path = './json_io_files/model_output.json'
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

# Create an object of the above class
handler_object = VaccineModelingHttpRequestHandler

PORT = 8000
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()