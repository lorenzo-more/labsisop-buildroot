import os
from time import sleep
from http.server import BaseHTTPRequestHandler,HTTPServer

# /proc/driver/rtc
# /proc/uptime
# /proc/cpuinfo
# /proc/stat capacidade ocupada do processador
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
    
def read_cpu_times():
    with open('/proc/stat', 'r') as f:
        line = f.readline()

    parts = line.split()
    return list(map(int, parts[1:9])) # see https://stackoverflow.com/questions/23367857/accurate-calculation-of-cpu-usage-given-in-percentage-in-linux

def get_system_info():
    info = {}
    
    data_hora = read_file('/proc/driver/rtc')
    lines = data_hora.splitlines()

    for line in lines[:2]:
        if line.startswith('rtc_time'):
            rtc_time = line.split(':', 1)[1].strip()
        elif line.startswith('rtc_date'):
            rtc_date = line.split(':', 1)[1].strip()

    info_rtc = rtc_date + " " + rtc_time
    info.update({'rtc': info_rtc})
    
    up_idle = read_file('/proc/uptime').split(' ')
    info.update({'uptime': up_idle[0]})

    cpu_model = read_file('/proc/cpuinfo')
    lines = cpu_model.splitlines()

    for line in lines:
        if line.startswith('model name'):
            model_name = line.split(':', 1)[1].strip()
            break
    info.update({'cpuinfo': model_name})
    
    prev_times = read_cpu_times()
    sleep(1)
    current_times = read_cpu_times()

    prev_total = sum(prev_times)
    current_total = sum(current_times)

    prev_idle = prev_times[3] 
    current_idle = current_times[3] 

    total_dif = current_total - prev_total
    idle = current_idle - prev_idle

    cpu_usage = round(((total_dif - idle) / total_dif * 100), 1)

    info.update({'cpu_capacity': cpu_usage})
        
    
    memory = read_file('/proc/meminfo')
    lines = memory.splitlines()

    for line in lines[:2]:
        if line.startswith('MemTotal'):
            memory_total = line.split(':', 1)[1].strip()[:-2]
        elif line.startswith('MemFree'):
            memory_free = line.split(':', 1)[1].strip()[:-2]
    
    m1 = int(memory_total)/1024
    m2 = int(memory_free)/1024
    m3 = m1 - m2

    memory_info = f'Memória total: {round(m1)} MB Memória usada: {round(m3)} MB'

    info.update({'meminfo': memory_info})
    
    info['version'] = read_file('/proc/version')
    
    processes = []

    for pid in os.listdir('/proc'):
        if pid.isdigit():
            try:
                with open(f'/proc/{pid}/comm', 'r') as f:
                    pname = f.readline().strip()
                processes.append((pid, pname))
            except Exception:
                continue

    html_processes = '<ul style="list-style-type: none; padding: 0;">'
    for pid, pname in processes:
        html_processes += f"<li>{pid}: {pname}</li>"
                
    html_processes += '</ul>'
    info.update({'processes': html_processes})

    lines = read_file('/proc/partitions').splitlines()

    disk_info = []

    for line in lines[2:]:
        parts = line.split()
        if len(parts) > 3:
            major, minor, blocks, name = parts
            blocks = (int(blocks) * 4096) / (1024 * 1024) # conversao de bloco pra MB

            if 'loop' in name or 'sr' in name:
                continue

            disk_info.append((name, round(blocks)))

    html_disk = '<ul style="list-style-type: none; padding: 0;">'
    for name, blocks in disk_info:
        html_disk += f"<li>{name}: {blocks} MB</li>"
    html_disk += '</ul>'

    info.update({'disk': html_disk})

    html_usb = '<ul style="list-style-type: none; padding: 0;">'
    for device in os.listdir('/sys/bus/usb/devices'):
        html_usb += f"<li>{device}</li>"
    html_usb += '</ul>'

    info.update({'usb_devices': html_usb})
    
    lines = read_file('/proc/net/route').splitlines()

    html_net = '<ul style="list-style-type: none; padding: 0;">'
    for line in lines:
        html_net += f"<li>{line}</li>"
    html_net += '</ul>'

    info.update({'route': html_net})

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
                    <p>O objetivo deste trabalho é gerar uma distribuição Linux que possua um servidor Web e escrever uma página HTML para que esta forneça informações básicas sobre o funcionamento do sistema (target).</p>
                    <p><b>Integrantes: Gabriel W. Piazenski, Gustavo W. da Silva e Lorenzo D. More</b></p>
                </div>
                <table class="info-table">
                    <tr>
                        <th>Informação</th>
                        <th>Valor</th>
                    </tr>
                    <tr>
                        <td>Data e hora</td>
                        <td>{info['rtc']}</td>
                    </tr>
                    <tr>
                        <td>Uptime (em segundos)</td>
                        <td>{info['uptime']}</td>
                    </tr>
                    <tr>
                        <td>Modelo do processador e velocidade</td>
                        <td>{info['cpuinfo']}</td>
                    </tr>
                    <tr>
                        <td>Capacidade ocupada do processador (%)</td>
                        <td>{info['cpu_capacity']}%</td>
                    </tr>
                    <tr>
                        <td>Quantidade de memória RAM total e usada (MB)</td>
                        <td>{info['meminfo']}</td>
                    </tr>
                    <tr>
                        <td>Versão do sistema</td>
                        <td>{info['version']}</td>
                    </tr>
                    <tr>
                        <td>Lista de processos em execução (PID: nome)</td>
                        <td>{info['processes']}</td>
                    </tr>
                    <tr>
                        <td>Lista de unidades de disco, com capacidade total de cada unidade (MB)</td>
                        <td>{info['disk']}</td>
                    </tr>
                    <tr>
                        <td>Lista de dispositivos USB, com a respectiva porta em que estão conectados</td>
                        <td>{info['usb_devices']}</td>
                    </tr>
                    <tr>
                        <td>Lista de adaptadores de rede, com o respectivo endereçamento IP de cada um</td>
                        <td>{info['route']}</td>
                    </tr>
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

