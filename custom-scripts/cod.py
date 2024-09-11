import time
from http.server import BaseHTTPRequestHandler,HTTPServer

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

def read_file(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except Exception as e:
        return str(e)

def get_system_info():
    info = {}
    info['uptime'] = read_file('/proc/uptime')

    return info

HOST_NAME = '127.0.0.1' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000

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
        
        info = get_system_info()

        html_content = f"""
        <!DOCTYPE html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Laboratório de Sistemas Operacionais</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                .container {{
                    width: 80%;
                    margin: 0 auto;
                    padding: 20px;
                    background: #fff;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .title {{
                    text-align: center;
                    margin-bottom: 20px;
                }}
                .project-info {{
                    text-align: left;
                    margin-bottom: 20px;
                }}
                .info-table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                .info-table th, .info-table td {{
                    padding: 10px;
                    border: 1px solid #ddd;
                    text-align: left;
                }}
                .info-table th {{
                    background-color: #f2f2f2;
                }}
                .info-table td {{
                    background-color: #fff;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="title">
                    <h1>Laboratório de Sistemas Operacionais - Trabalho Prático I</h1>
                </div>
                <div class="project-info">
                    <p><strong>Informações sobre o trabalho:</strong></p>
                    <p>O objetivo deste trabalho é gerar uma distribuição Linux que possua um servidor Web e escrever uma página HTML para que esta forneca informações básicas sobre o funcionamento do sistema (target).</p>
                    <p><b>Integrantes: Gabriel W. Piazenski, Gustavo W. da Silva e Lorenzo D. More</b></p>
                </div>
                <table class="info-table">
                    <tr>
                        <th>Informação</th>
                        <th>Valor</th>
                    </tr>
                    <tr>
                        <td>Uptime (segundos)</td>
                        <td>{info['uptime']}</td>
                    </tr>
                    <!-- Add other rows here similarly -->
                </table>
            </div>
        </body>
        </html>
        """

        # If someone went to "http://something.somewhere.net/foo/bar/",
        # then s.path equals "/foo/bar/".
        #s.wfile.write(f"<p>You accessed path: {s.path}</p>".encode())
        s.wfile.write(html_content.encode())

if __name__ == '__main__':
    httpd = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print("Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

