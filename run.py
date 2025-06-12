#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Sistema de Detección de Placas Vehiculares - Casabaca

Este es el punto de entrada principal del sistema de detección de placas vehiculares.
El script inicializa todos los componentes necesarios y verifica las conexiones.
La salida se muestra en una interfaz gráfica.

Autor: Edison02m
Fecha: 2025
Versión: 1.0
"""

import os
import time
import tkinter as tk
from tkinter import scrolledtext, font
import threading
from app.monitor import iniciar_monitor, obtener_ultima_deteccion
from app.camera import verificar_conexion_camara

# Variable global para la ventana principal
ventana = None
area_texto = None

def agregar_mensaje(mensaje, tipo="normal"):
    """
    Agrega un mensaje al área de texto de la interfaz gráfica.
    
    Args:
        mensaje (str): El mensaje a mostrar
        tipo (str): El tipo de mensaje (normal, error, destacado)
    """
    if not area_texto:
        return
        
    area_texto.config(state=tk.NORMAL)
    
    if tipo == "error":
        area_texto.insert(tk.END, mensaje + "\n", "error")
    elif tipo == "destacado":
        area_texto.insert(tk.END, mensaje + "\n", "destacado")
    elif tipo == "titulo":
        area_texto.insert(tk.END, mensaje + "\n", "titulo")
    else:
        area_texto.insert(tk.END, mensaje + "\n")
    
    area_texto.config(state=tk.DISABLED)
    area_texto.see(tk.END)  # Desplazar al final

def iniciar_sistema():
    """
    Inicializa el sistema de detección de placas.
    
    Esta función realiza las siguientes tareas:
    1. Verifica la conexión con la cámara de detección de placas
    2. Inicia el hilo de monitoreo para la detección de placas
    3. Muestra los resultados en la interfaz gráfica
    
    Returns:
        None
    """
    agregar_mensaje("=== VERIFICACIÓN DE COMPONENTES ===", "titulo")
    
    # Verificar conexión a la cámara
    agregar_mensaje("\n1. Verificando conexión con la cámara...")
    conectado, mensaje = verificar_conexion_camara()
    if conectado:
        agregar_mensaje(" Conexión con la cámara establecida correctamente")
    else:
        agregar_mensaje(f" Advertencia: {mensaje}", "error")
        agregar_mensaje("   El sistema se iniciará pero es posible que no detecte placas.")
    
    agregar_mensaje("\n=== INICIANDO SERVICIOS ===", "titulo")
    
    # Iniciar hilo de monitoreo
    agregar_mensaje("\nIniciando sistema de monitoreo...")
    iniciar_monitor()
    agregar_mensaje(" Monitor de placas iniciado")
    
    agregar_mensaje("\n Sistema listo. Monitoreando placas...")
    
    # Iniciar el hilo de monitoreo de placas
    hilo_monitor = threading.Thread(target=monitorear_placas)
    hilo_monitor.daemon = True  # El hilo se cerrará cuando el programa principal termine
    hilo_monitor.start()

def monitorear_placas():
    """
    Función que se ejecuta en un hilo separado para monitorear las placas detectadas
    y mostrarlas en la interfaz gráfica.
    """
    ultima_placa = None
    while True:
        try:
            deteccion = obtener_ultima_deteccion()
            if deteccion and deteccion["placa"] != ultima_placa:
                ultima_placa = deteccion["placa"]
                agregar_mensaje("\n" + "="*50)
                agregar_mensaje(f"PLACA DETECTADA: {deteccion['placa']}", "destacado")
                agregar_mensaje(f"FECHA: {deteccion['fecha']}")
                agregar_mensaje(f"ESTADO: {deteccion['mensaje']}")
                
                if deteccion["tiene_cita"]:
                    datos_cita = deteccion["datos_cita"]
                    agregar_mensaje("\nDATOS DE LA CITA:", "destacado")
                    agregar_mensaje(f"  Cliente: {datos_cita.get('nombreCliente', 'N/A')}")
                    agregar_mensaje(f"  Vehículo: {datos_cita.get('descripcionVeh', 'N/A')}")
                    agregar_mensaje(f"  Fecha: {datos_cita.get('fechaCita', 'N/A')}")
                    agregar_mensaje(f"  Hora: {datos_cita.get('horaCita', 'N/A') if 'horaCita' in datos_cita else datos_cita.get('fechaCita', 'N/A').split(' ')[1] if ' ' in datos_cita.get('fechaCita', 'N/A') else 'N/A'}")
                    agregar_mensaje(f"  Asesor: {datos_cita.get('nombreAsesor', datos_cita.get('asesor', 'N/A'))}")
                    agregar_mensaje(f"  OT: {datos_cita.get('ordenrepld', 'N/A')}")
                    if 'descripcionAlterna' in datos_cita and datos_cita['descripcionAlterna']:
                        agregar_mensaje(f"  Servicio: {datos_cita['descripcionAlterna']}")
                    if 'agencia' in datos_cita and datos_cita['agencia']:
                        agregar_mensaje(f"  Agencia: {datos_cita['agencia']}")
                
                agregar_mensaje("="*50)
        except Exception as e:
            agregar_mensaje(f"\nError al procesar detección: {e}", "error")
            agregar_mensaje("El sistema continuará monitoreando...")
            time.sleep(5)
        
        time.sleep(1)

def crear_interfaz():
    """
    Crea la interfaz gráfica del sistema.
    """
    global ventana, area_texto
    
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Sistema de Detección de Placas - SUZUKI")
    ventana.geometry("800x600")
    
    # Configurar fuentes
    fuente_normal = font.Font(family="Consolas", size=10)
    fuente_titulo = font.Font(family="Consolas", size=12, weight="bold")
    
    # Crear área de texto con scroll
    area_texto = scrolledtext.ScrolledText(ventana, wrap=tk.WORD, font=fuente_normal)
    area_texto.pack(expand=True, fill="both", padx=10, pady=10)
    
    # Configurar etiquetas para diferentes tipos de texto
    area_texto.tag_configure("error", foreground="red")
    area_texto.tag_configure("destacado", foreground="blue", font=font.Font(family="Consolas", size=10, weight="bold"))
    area_texto.tag_configure("titulo", foreground="green", font=fuente_titulo)
    
    # Botón para salir
    boton_salir = tk.Button(ventana, text="Salir", command=ventana.destroy)
    boton_salir.pack(pady=10)
    
    # Deshabilitar edición en el área de texto
    area_texto.config(state=tk.DISABLED)
    
    # Mostrar cabecera
    agregar_mensaje("===============================================", "titulo")
    agregar_mensaje("  SISTEMA DE DETECCIÓN DE PLACAS - SUZUKI", "titulo")
    agregar_mensaje("===============================================", "titulo")
    
    # Iniciar el sistema en un hilo separado
    threading.Thread(target=iniciar_sistema, daemon=True).start()
    
    # Iniciar el bucle principal de la interfaz gráfica
    ventana.mainloop()

if __name__ == "__main__":
    crear_interfaz()