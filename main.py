from http.server import ThreadingHTTPServer
from decorator.url import TestServer
from core.server import BaseServer
app = TestServer()

hostName = "localhost"
serverPort = 8080

@app.get("/try_it")
@app.validate_required_params(["hey","to","you"])
def first(request: BaseServer):
    return request.raw_html_response(200, "<h1> hello to you </h1>")


if __name__ == "__main__":
    webServer = ThreadingHTTPServer((hostName, serverPort), BaseServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
