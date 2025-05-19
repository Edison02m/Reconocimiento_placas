#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema de Detección de Placas Vehiculares - Suzuki

Este es el punto de entrada principal del sistema de detección de placas vehiculares.
El script inicializa todos los componentes necesarios, verifica las conexiones
y arranca el servidor web Flask que proporciona la interfaz de usuario.

Autor: Edison02m
Fecha: 2025
Versión: 1.0
"""

import os
# Configurar para evitar que Flask intente cargar archivos .env
os.environ['FLASK_SKIP_DOTENV'] = '1'

from app import create_app
from app.database import conectar_db, probar_conexion_servidor
from app.templates import crear_templates
from app.monitor import iniciar_monitor
from app.camera import verificar_conexion_camara

def iniciar_servidor():
    """
    Inicializa y arranca el servidor web.
    
    Esta función realiza las siguientes tareas:
    1. Crea los archivos de plantillas HTML necesarios
    2. Verifica la conexión con la cámara de detección de placas
    3. Verifica la conexión con el servidor remoto para almacenamiento de datos
    4. Verifica la conexión con la base de datos local (solo diagnóstico)
    5. Inicia el hilo de monitoreo para la detección de placas
    6. Crea e inicia la aplicación web Flask
    
    Returns:
        None
    """
    # Crear plantillas antes de iniciar
    crear_templates()
    
    print("\n=== VERIFICACIÓN DE COMPONENTES ===")
    
    # Verificar conexión a la cámara
    print("\n1. Verificando conexión con la cámara...")
    conectado, mensaje = verificar_conexion_camara()
    if conectado:
        print(" Conexión con la cámara establecida correctamente")
    else:
        print(f" Advertencia: {mensaje}")
        print("   El sistema se iniciará pero es posible que no detecte placas.")
    
    # Verificar conexión al servidor remoto
    print("\n2. Verificando conexión con el servidor remoto...")
    servidor_conectado = probar_conexion_servidor()
    if not servidor_conectado:
        print(" ERROR CRÍTICO: No hay conexión con el servidor remoto!")
        print("   Las placas detectadas NO serán almacenadas")
    
    # Verificar conexión a la base de datos local (solo para diagnóstico)
    print("\n3. Verificando conexión a la base de datos local...")
    conn = conectar_db()
    if conn:
        print(" Conexión a la base de datos local exitosa (solo para diagnóstico)")
        print("   Nota: Los datos se almacenarán ÚNICAMENTE en el servidor remoto")
        conn.close()
    else:
        print(" No se pudo conectar a la base de datos local")
        print("   Nota: Esto no afecta el funcionamiento, los datos se envían al servidor remoto")
    
    print("\n=== INICIANDO SERVICIOS ===")
    
    # Iniciar hilo de monitoreo
    print("\nIniciando sistema de monitoreo...")
    iniciar_monitor()
    print(" Monitor de placas iniciado")
    
    # Crear y configurar la aplicación Flask
    app = create_app()
    
    # Iniciar el servidor web
    print("\n Sistema listo. Iniciando servidor web...")
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    print("\n===============================================")
    print("  SISTEMA DE DETECCIÓN DE PLACAS - SUZUKI")
    print("===============================================\n")
    iniciar_servidor() 