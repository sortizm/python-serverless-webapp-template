import os
from http.server import BaseHTTPRequestHandler, HTTPServer

os.environ["SERVICE_NAME"] = "{{ cookiecutter.service_name }}"
{%- if cookiecutter.with_dynamodb_table == "y" %}
os.environ["SERVICE_TABLE_NAME"] = "{{ cookiecutter.service_name }}.table"
{%- endif %}


hostName = "localhost"
serverPort = 8080


class LocalServer(BaseHTTPRequestHandler):
    def do_GET(self):
        response = route_request(self.path, method="GET")
        self.send_response(response.status_code)
        self.send_header("Content-type", "application/json")
        for key, value in response.headers.items():
            self.send_header(key, value)
        self.end_headers()
        if response.body:
            self.wfile.write(response.body.encode(encoding="utf-8"))


if __name__ == "__main__":
    from test.utils import route_request

    webServer = HTTPServer((hostName, serverPort), LocalServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        webServer.server_close()
