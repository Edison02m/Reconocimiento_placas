#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Sistema de Detección de Placas Vehiculares - Punto de entrada principal"""

import os
import time
from app.monitor import iniciar_monitor, obtener_ultima_deteccion
from app.camera import verificar_conexion_camara
from app.supabase_client import verificar_conexion_supabase_inicial

def iniciar_sistema():
    """Inicializa sistema: verifica conexiones, inicia monitoreo y muestra detecciones"""
    print("\n=== VERIFICACIÓN DE COMPONENTES ===")
    
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
    
    print("\n2. Verificando conexión con Supabase...")
    conectado_supabase, mensaje_supabase = verificar_conexion_supabase_inicial()
    
    if conectado_supabase:
        print(" ✓ Conexión con Supabase establecida correctamente")
    else:
        print(f" ✗ Advertencia: {mensaje_supabase}")
        print("   El sistema funcionará sin guardar detecciones en Supabase")
    
    print("\n=== INICIANDO SERVICIOS ===")
    
    print("\nIniciando sistema de monitoreo...")
    iniciar_monitor()
    print(" Monitor de placas iniciado")
    
    print("\n Sistema listo. Mostrando detecciones en consola...")
    print("(Presione Ctrl+C para detener) \n")
    
    try:
        ultima_deteccion_completa = None
        while True:
            try:
                deteccion = obtener_ultima_deteccion()
                if deteccion:
                    deteccion_actual = f"{deteccion['placa']}_{deteccion['fecha']}"
                    if deteccion_actual != ultima_deteccion_completa:
                        ultima_deteccion_completa = deteccion_actual
                        print("\n" + "="*50)
                        print(f"PLACA DETECTADA: {deteccion['placa']}")
                        print(f"FECHA: {deteccion['fecha']}")
                        print(f"ESTADO: {deteccion['mensaje']}")
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