import time
from http.server import BaseHTTPRequestHandler,HTTPServer


HOST_NAME = '127.0.0.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000

# /proc/driver/rtc
# /proc/uptime
# /proc/cpuinfo
# capacidade ocupada do processador
# /proc/meminfo
# /proc/version
# Lista de processos em execucao (PID e nome)
# Lista de unidades de disco, com capacidade total de cada unidade
# /sys/bus/usb/devices Lista de dispositivos USB, com a respectiva porta em que estao conectados
# /proc/net/route

class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write("<html><head><title>Title goes here.</title></head>".encode())
        s.wfile.write("<body><p>This is a test.</p>".encode())
        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        s.wfile.write(f"<p>You accessed path: {s.path}</p>".encode())
        s.wfile.write("</body></html>".encode())

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print("Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

