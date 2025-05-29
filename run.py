#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema de Detección de Placas Vehiculares - Casabaca

Este es el punto de entrada principal del sistema de detección de placas vehiculares.
El script inicializa todos los componentes necesarios y verifica las conexiones.
La salida se muestra en consola.

Autor: Edison02m
Fecha: 2025
Versión: 1.0
"""

import os
import time
from app.database import conectar_db, probar_conexion_servidor
from app.monitor import iniciar_monitor, obtener_ultima_deteccion
from app.camera import verificar_conexion_camara
from app.state import ultima_consulta

def iniciar_sistema():
    """
    Inicializa el sistema de detección de placas.
    
    Esta función realiza las siguientes tareas:
    1. Verifica la conexión con la cámara de detección de placas
    2. Verifica la conexión con el servidor remoto para almacenamiento de datos
    3. Verifica la conexión con la base de datos local (solo diagnóstico)
    4. Inicia el hilo de monitoreo para la detección de placas
    5. Muestra los resultados en consola
    
    Returns:
        None
    """
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
    
    print("\n Sistema listo. Mostrando detecciones en consola...")
    print("(Presione Ctrl+C para detener)")
    
    try:
        # Bucle principal para mostrar resultados en consola
        ultima_placa = None
        while True:
            try:
                deteccion = obtener_ultima_deteccion()
                if deteccion and deteccion["placa"] != ultima_placa:
                    ultima_placa = deteccion["placa"]
                    print("\n" + "="*50)
                    print(f"PLACA DETECTADA: {deteccion['placa']}")
                    print(f"FECHA: {deteccion['fecha']}")
                    print(f"ESTADO: {deteccion['mensaje']}")
                    
                    if deteccion["tiene_cita"]:
                        datos_cita = deteccion["datos_cita"]
                        print("\nDATOS DE LA CITA:")
                        print(f"  Cliente: {datos_cita.get('nombreCliente', 'N/A')}")
                        print(f"  Vehículo: {datos_cita.get('descripcionVeh', 'N/A')}")
                        print(f"  Fecha: {datos_cita.get('fechaCita', 'N/A')}")
                        print(f"  Hora: {datos_cita.get('horaCita', 'N/A') if 'horaCita' in datos_cita else datos_cita.get('fechaCita', 'N/A').split(' ')[1] if ' ' in datos_cita.get('fechaCita', 'N/A') else 'N/A'}")
                        print(f"  Asesor: {datos_cita.get('nombreAsesor', datos_cita.get('asesor', 'N/A'))}")
                        print(f"  OT: {datos_cita.get('ordenrepld', 'N/A')}")
                        if 'descripcionAlterna' in datos_cita and datos_cita['descripcionAlterna']:
                            print(f"  Servicio: {datos_cita['descripcionAlterna']}")
                        if 'agencia' in datos_cita and datos_cita['agencia']:
                            print(f"  Agencia: {datos_cita['agencia']}")
                    
                    print("="*50)
            except Exception as e:
                print(f"\nError al procesar detección: {e}")
                print("El sistema continuará monitoreando...")
                time.sleep(5)
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nDetención solicitada por el usuario. Cerrando sistema...")

if __name__ == "__main__":
    print("\n===============================================")
    print("  SISTEMA DE DETECCIÓN DE PLACAS - CASABACA")
    print("===============================================\n")
    iniciar_sistema() 