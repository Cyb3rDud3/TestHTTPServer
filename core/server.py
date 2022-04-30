try:
    import orjson as json
except ImportError as e:
    import json
from http.server import BaseHTTPRequestHandler
import cgi
from decorator.url import URLS



class BaseServer(BaseHTTPRequestHandler):
    urls = URLS
    has_query = False
    query_length = None
    query = None
    method = None
    post_data = None
    post_is_json = False

    def send_error(self, code: int, message: str | None = ..., explain: str | None = ...) -> None:
        if code == 404:
            self.error_message_format = "Not Found!"
            return BaseHTTPRequestHandler.send_error(self, code, message)
        return BaseHTTPRequestHandler.send_error(self,code,message)

    def json_response(self, status_code, json_data):
        if not json_data:
            json_data = {}
        json_data = json.dumps(json_data)
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json_data)

    def raw_html_response(self, status_code, html):
        if not html:
            html = "<h1> Hello World! </h1>"
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())

    def html_response(self, status_code: int, html_file: str):
        """
        :param status_code: status code to return
        :type status_code: int
        :param html_file: relative path to html file to server
        :type html_file: str
        :return: None
        :rtype: None
        """
        try:
            with open(html_file, 'r') as html:
                html_file = html.read()
        except FileNotFoundError:
            raise Exception("File Not Exist!")
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(html_file.encode())

    def do_GET(self):
        self.method = "GET"
        if '?' in self.path:
            if '=' in self.path:
                url_params = {j.split('=')[0]: j.split('=')[1] for j in self.path.split('?')[1].split('&')}
                self.has_query = True
                self.query_length = len(url_params)
                self.query = url_params
            pure_route = self.path.split('?')[0] if not self.path.split('?')[0].endswith('/') else self.path.split('?')[
                                                                                                       0][:-1:]
            self.path = pure_route
        if self.path not in self.urls:
            return self.send_error(code=404, message="Not Found!")
        if self.urls[self.path]["method"] != self.method:
            return self.send_error(code=405,message="Method Not Allowed!")
        return self.urls[self.path]["handler"](self)

    def sanitize_post_path(self):
        if '?' in self.path:
            pure_route = self.path.split('?')[0] if not self.path.split('?')[0].endswith('/') else self.path.split('?')[ 0][:-1:]
            self.path = pure_route

    def parse_post_json(self):
        try:
            length = int(self.headers.get('Content-Length', None))
            self.post_data = json.loads(self.rfile.read(length))
            self.post_is_json = True
            return True
        except Exception as e:
            print(e,Exception)
            return self.send_error(code=400,message="Bad Request")

    def do_POST(self):
        self.method = "POST"
        if self.path not in self.urls:
            return self.send_error(code=404, message="Not Found!")
        self.sanitize_post_path()
        if self.urls[self.path]["method"] != self.method:
            return self.send_error(code=405,message="Method Not Allowed!")
        content_type = self.headers.get_content_type()
        if content_type != 'application/json':
            return self.send_error(code=400,message="Bad Request")

        self.parse_post_json()
        return self.urls[self.path]["handler"](self)

    def log_request(self, code: int | str = ..., size: int | str = ...) -> None:
        return

