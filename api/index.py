from http.server import BaseHTTPRequestHandler
import json
from urllib import parse
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        if "name" in dic:
            message = {"message": "Hello, " + dic["name"] + "!"}
        else:
            message = {"message": "Hello, stranger!"}
        
        response_json = json.dumps(message)
        self.wfile.write(response_json.encode())  # Encode the JSON response