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
from app.monitor import iniciar_monitor, obtener_ultima_deteccion
from app.camera import verificar_conexion_camara

def iniciar_sistema():
    """
    Inicializa el sistema de detección de placas.
    
    Esta función realiza las siguientes tareas:
    1. Verifica la conexión con la cámara de detección de placas
    2. Inicia el hilo de monitoreo para la detección de placas
    3. Muestra los resultados en consola
    
    Returns:
        None
    """
    print("\n=== VERIFICACIÓN DE COMPONENTES ===")
    
    # Verificar conexión a la cámara con reintentos automáticos
    print("\n1. Verificando conexión con la cámara...")
    conectado = False
    primer_intento = True
    contador_puntos = 0
    
    while not conectado:
        conectado, mensaje = verificar_conexion_camara()
        
        if conectado:
            if not primer_intento:
                print("\r", end="") 
            print(" ✓ Conexión con la cámara establecida correctamente")
        else:
            if primer_intento:
                print(f" ✗ Error: {mensaje}")
                print("   Reintentando conexión (Ctrl+C para cancelar)")
                print("   Intentando conectarse", end="", flush=True)
                primer_intento = False
            else:
                # Indicador de progreso
                puntos = "." * ((contador_puntos % 3) + 1)
                espacios = " " * (3 - len(puntos))
                print(f"\r   Intentando conectarse {puntos}{espacios}", end="", flush=True)
                contador_puntos += 1
            
            try:
                time.sleep(0.5)
            except KeyboardInterrupt:
                print("\n\n   Conexión cancelada por el usuario.")
                print("   El sistema se iniciará sin conexión a la cámara.")
                print("   Es posible que no detecte placas.")
                break
    
    print("\n=== INICIANDO SERVICIOS ===")
    
    # Iniciar hilo de monitoreo
    print("\nIniciando sistema de monitoreo...")
    iniciar_monitor()
    print(" Monitor de placas iniciado")
    
    print("\n Sistema listo. Mostrando detecciones en consola...")
    print("(Presione Ctrl+C para detener) \n")
    
    try:
        # Bucle principal para mostrar resultados en consola
        ultima_deteccion_completa = None
        while True:
            try:
                deteccion = obtener_ultima_deteccion()
                # Crear identificador único con placa + fecha para evitar duplicados exactos
                if deteccion:
                    deteccion_actual = f"{deteccion['placa']}_{deteccion['fecha']}"
                    if deteccion_actual != ultima_deteccion_completa:
                        ultima_deteccion_completa = deteccion_actual
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
    print("  SISTEMA DE DETECCIÓN DE PLACAS - SUZUKI")
    print("===============================================\n")
    iniciar_sistema()