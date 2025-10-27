#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Servidor local simple para el frontend

Este script inicia un servidor HTTP local para servir el frontend
de manera rápida y sencilla.
"""

import http.server
import socketserver
import webbrowser
import os
import sys

def iniciar_servidor(puerto=8000):
    """
    Inicia un servidor HTTP local para el frontend
    
    Args:
        puerto (int): Puerto donde servir el frontend (default: 8000)
    """
    # Cambiar al directorio del frontend
    frontend_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(frontend_dir)
    
    print(f"📡 Iniciando servidor local en el puerto {puerto}")
    print(f"📁 Directorio: {frontend_dir}")
    
    try:
        # Configurar el servidor
        with socketserver.TCPServer(("", puerto), http.server.SimpleHTTPRequestHandler) as httpd:
            url = f"http://localhost:{puerto}"
            
            print(f"\n🚀 Servidor iniciado exitosamente!")
            print(f"🌐 URL: {url}")
            print(f"📊 Monitor de Placas: {url}/index.html")
            print(f"\n⏹️  Presiona Ctrl+C para detener el servidor\n")
            
            # Abrir automáticamente en el navegador
            try:
                webbrowser.open(url)
                print("🔍 Abriendo en el navegador...")
            except:
                print("ℹ️  Abre manualmente en tu navegador")
            
            # Servir indefinidamente
            httpd.serve_forever()
            
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ El puerto {puerto} ya está en uso")
            print(f"💡 Intenta con otro puerto: python servidor.py {puerto + 1}")
        else:
            print(f"❌ Error al iniciar servidor: {e}")
    except KeyboardInterrupt:
        print(f"\n⏹️  Servidor detenido por el usuario")
        print("👋 ¡Hasta luego!")

if __name__ == "__main__":
    # Permitir especificar puerto como argumento
    puerto = 8000
    if len(sys.argv) > 1:
        try:
            puerto = int(sys.argv[1])
        except ValueError:
            print("❌ Puerto inválido, usando 8000 por defecto")
    
    iniciar_servidor(puerto)