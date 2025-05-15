import requests
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET
from datetime import datetime
import time
import threading
import json
from flask import Flask, render_template, jsonify
import mysql.connector
from mysql.connector import Error

# === CONFIGURACIÓN ===
URL = "http://192.168.20.45/ISAPI/Traffic/channels/1/vehicleDetect/plates"
USERNAME = "admin"
PASSWORD = "Telcomexpert01"
URL_CITAS = "http://192.168.20.138/casabacaWebservices/agendamientoCitas/consultaPorPlaca"
NO_CIA = "08"
COD_AGENCIA = "05"
INTERVALO_CONSULTA = 1  # segundos entre consultas

# Configuración de la base de datos MySQL
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # Actualiza con tu contraseña
    "database": "placas"
}

# XML con la fecha de inicio de búsqueda (ajústala si quieres)
BODY_XML = """
<AfterTime>
    <picTime>20250415T000000-500</picTime>
</AfterTime>
"""

HEADERS = {
    "Content-Type": "application/xml",
    "Accept": "application/xml"
}

# Datos para la interfaz web
ultima_consulta = {
    "placa": None,
    "fecha": None,
    "tiene_cita": False,
    "datos_cita": None,
    "mensaje": None,
    "actualizado": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

# Conjunto para almacenar los eventos exactos ya procesados
eventos_exactos_procesados = set()

# Inicializar Flask
app = Flask(__name__)

def conectar_db():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None

def guardar_placa_en_db(placa, fecha, origen="Cámara IP"):
    try:
        conn = conectar_db()
        if conn is None:
            return False
        
        cursor = conn.cursor()
        # Extraer fecha y hora por separado del objeto datetime
        fecha_str = fecha.strftime("%Y-%m-%d")
        hora_str = fecha.strftime("%H:%M:%S")
        
        # Ejecutar la consulta para insertar la placa
        query = """
        INSERT INTO registro_placas (placa, fecha, hora, origen)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (placa, fecha_str, hora_str, origen))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print(f"Placa guardada: {placa}, Fecha: {fecha_str}, Hora: {hora_str}")
        return True
    except Error as e:
        print(f"Error al guardar en la base de datos: {e}")
        return False

def get_plates():
    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            data=BODY_XML.encode('utf-8'),
            auth=HTTPDigestAuth(USERNAME, PASSWORD),
            timeout=10
        )
        response.raise_for_status()

        root = ET.fromstring(response.content)
        plates = []

        # Detectar el namespace correcto del XML
        namespace = root.tag.split('}')[0].strip('{') if '}' in root.tag else None
        ns = {'ns': namespace} if namespace else None

        # Buscar todas las placas
        xpath = ".//ns:Plate" if namespace else ".//Plate"
        for plate in root.findall(xpath, ns):
            # Función auxiliar para obtener texto con o sin namespace
            def get_text(element, tag):
                return (element.findtext(f"ns:{tag}", namespaces=ns) if namespace 
                       else element.findtext(tag))

            plate_number = get_text(plate, "plateNumber")
            capture_time = get_text(plate, "captureTime")
            country = get_text(plate, "country")

            if plate_number and capture_time:
                # Convertir el formato de hora a uno que Python pueda entender
                capture_time = capture_time.replace("-500", "-0500")
                try:
                    dt = datetime.strptime(capture_time, "%Y%m%dT%H%M%S%z")
                    if plate_number.lower() != "unknown":
                        plates.append({
                            "placa": plate_number,
                            "fecha": dt,
                            "país": country
                        })
                except ValueError:
                    continue

        plates.sort(key=lambda x: x["fecha"], reverse=True)
        return plates

    except Exception:
        return []

def consultar_cita(placa):
    try:
        params = {
            "noCia": NO_CIA,
            "placa": placa,
            "codAgencia": COD_AGENCIA
        }
        response = requests.get(URL_CITAS, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None

def crear_id_evento_exacto(placa, fecha):
    return f"{placa}_{fecha.strftime('%Y%m%d%H%M%S')}"

def actualizar_datos(resultado_cita, placa, fecha):
    global ultima_consulta
    
    # Actualizar los datos para la web
    ultima_consulta["placa"] = placa
    ultima_consulta["fecha"] = fecha.strftime("%Y-%m-%d %H:%M:%S")
    ultima_consulta["actualizado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    if resultado_cita and "codigo" in resultado_cita:
        if resultado_cita["codigo"] == "0" and resultado_cita["listadoDatosAgendamiento"]:
            cita = resultado_cita["listadoDatosAgendamiento"][0]
            ultima_consulta["tiene_cita"] = True
            ultima_consulta["datos_cita"] = cita
            ultima_consulta["mensaje"] = "CITA ENCONTRADA"
        else:
            ultima_consulta["tiene_cita"] = False
            ultima_consulta["datos_cita"] = None
            ultima_consulta["mensaje"] = resultado_cita.get("mensaje", "NO SE ENCONTRARON RESULTADOS")
    else:
        ultima_consulta["tiene_cita"] = False
        ultima_consulta["datos_cita"] = None
        ultima_consulta["mensaje"] = "ERROR DE CONEXIÓN"

def procesar_ultimo_evento():
    placas = get_plates()
    if not placas:
        return

    ultimo_evento = placas[0]
    id_evento_exacto = crear_id_evento_exacto(ultimo_evento["placa"], ultimo_evento["fecha"])
    
    if id_evento_exacto not in eventos_exactos_procesados:
        # Guardar la placa en la base de datos
        guardar_placa_en_db(ultimo_evento["placa"], ultimo_evento["fecha"])
        
        # Consultar cita y actualizar datos para la web
        resultado_cita = consultar_cita(ultimo_evento["placa"])
        actualizar_datos(resultado_cita, ultimo_evento["placa"], ultimo_evento["fecha"])
        
        # Marcar como procesado
        eventos_exactos_procesados.add(id_evento_exacto)

def monitor_thread():
    while True:
        procesar_ultimo_evento()
        time.sleep(INTERVALO_CONSULTA)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/datos')
def datos():
    return jsonify(ultima_consulta)

def crear_templates():
    # Crear carpeta templates si no existe
    import os
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # Crear el archivo de plantilla HTML
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema de Detección de Placas - Casabaca</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        body {
            background-color: #f8f9fa;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .logo-container {
            text-align: center;
            margin-bottom: 20px;
        }
        .logo {
            max-height: 80px;
        }
        .main-container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .card {
            border-radius: 15px;
            box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
            margin-bottom: 30px;
            border: none;
        }
        .card-header {
            background-color: #e10600;
            color: white;
            border-radius: 15px 15px 0 0 !important;
            font-weight: bold;
            font-size: 1.5rem;
            padding: 15px 20px;
        }
        .client-info {
            background-color: #ffffff;
            border-radius: 15px;
            padding: 25px;
            margin-bottom: 20px;
        }
        .plate {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            padding: 15px;
            background-color: #ffdd00;
            color: #333;
            border-radius: 10px;
            margin-bottom: 20px;
            border: 2px solid #333;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        .info-label {
            font-weight: bold;
            color: #666;
        }
        .info-value {
            font-size: 1.1rem;
            color: #333;
        }
        .timestamp {
            font-size: 0.9rem;
            color: #777;
            text-align: right;
            font-style: italic;
            margin-top: 15px;
        }
        .status-indicator {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 8px;
        }
        .status-active {
            background-color: #28a745;
            animation: pulse 2s infinite;
        }
        .status-inactive {
            background-color: #dc3545;
        }
        .vehicle-details {
            background-color: #f8f8f8;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        }
        .no-appointment {
            text-align: center;
            padding: 30px;
            background-color: #f8f8f8;
            border-radius: 10px;
            margin: 20px 0;
        }
        .waiting-data {
            text-align: center;
            padding: 80px 30px;
            background-color: #f5f5f5;
            border-radius: 10px;
            margin: 40px 0;
            color: #666;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        .appointment-icon {
            font-size: 4rem;
            margin-bottom: 20px;
            color: #28a745;
        }
        .no-appointment-icon {
            font-size: 4rem;
            margin-bottom: 20px;
            color: #dc3545;
        }
        .waiting-icon {
            font-size: 5rem;
            margin-bottom: 30px;
            color: #007bff;
            animation: spin 2s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .footer {
            margin-top: 20px;
            padding: 15px 0;
            color: #777;
            font-size: 0.9rem;
            text-align: center;
            border-top: 1px solid #eee;
        }
    </style>
</head>
<body>
    <div class="main-container">
        <div class="logo-container mt-3">
            <img src="https://www.casabaca.com/wp-content/uploads/2021/07/logo-casabaca-toyota-ec.png" alt="Casabaca Toyota" class="logo">
        </div>
        
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <span>
                    <i class="fas fa-car"></i> Sistema de Detección de Vehículos
                </span>
                <span>
                    <span class="status-indicator status-active" id="status-indicator"></span>
                    <span id="status-text">Monitoreando</span>
                </span>
            </div>
            <div class="card-body p-4">
                <div id="waiting-content" class="waiting-data">
                    <i class="fas fa-sync waiting-icon"></i>
                    <h2>Esperando detección de vehículos</h2>
                    <p>El sistema está activo y monitoreando la entrada de vehículos.</p>
                </div>
                
                <div id="data-content" style="display: none;">
                    <div class="row">
                        <div class="col-md-12 mb-4">
                            <h3 class="plate" id="plate-number">ABC-1234</h3>
                            <div class="timestamp" id="detection-time">
                                Detectado: 2023-05-15 15:30:45
                            </div>
                        </div>
                    </div>
                    
                    <div id="appointment-found" style="display: none;">
                        <div class="text-center mb-4">
                            <i class="fas fa-calendar-check appointment-icon"></i>
                            <h2>¡Cita Encontrada!</h2>
                        </div>
                        
                        <div class="client-info">
                            <div class="row mb-2">
                                <div class="col-md-3 info-label">Cliente:</div>
                                <div class="col-md-9 info-value" id="client-name">Juan Pérez</div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-md-3 info-label">Cédula:</div>
                                <div class="col-md-9 info-value" id="client-id">0923456789</div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-md-3 info-label">Fecha de Cita:</div>
                                <div class="col-md-9 info-value" id="appointment-date">2023-05-15</div>
                            </div>
                        </div>
                        
                        <div class="vehicle-details">
                            <div class="row mb-2">
                                <div class="col-md-3 info-label">Vehículo:</div>
                                <div class="col-md-9 info-value" id="vehicle-model">Toyota Hilux 4x4</div>
                            </div>
                            <div class="row mb-2">
                                <div class="col-md-3 info-label">Descripción:</div>
                                <div class="col-md-9 info-value" id="vehicle-desc">Pickup doble cabina</div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-6 mb-2">
                                <div class="info-label">Agencia:</div>
                                <div class="info-value" id="agency">AGQ</div>
                            </div>
                            <div class="col-md-6 mb-2">
                                <div class="info-label">Orden:</div>
                                <div class="info-value" id="order">ORD123456</div>
                            </div>
                        </div>
                        
                        <div class="row">
                            <div class="col-md-12">
                                <div class="info-label">Asesor:</div>
                                <div class="info-value" id="advisor">Jeanpierre Aguilar</div>
                            </div>
                        </div>
                    </div>
                    
                    <div id="no-appointment" style="display: none;">
                        <div class="no-appointment">
                            <i class="fas fa-calendar-times no-appointment-icon"></i>
                            <h2>No Se Encontró Cita</h2>
                            <p id="no-appointment-message" class="mt-3">No hay citas programadas para este vehículo.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2023 Casabaca Toyota - Sistema de Detección de Vehículos v1.0</p>
            <p>Última actualización: <span id="last-update">2023-05-15 15:30:45</span></p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Función para actualizar los datos cada 2 segundos
        function actualizarDatos() {
            fetch('/datos')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('last-update').textContent = data.actualizado;
                    
                    // Si no hay placa detectada, mostrar pantalla de espera
                    if (!data.placa) {
                        document.getElementById('waiting-content').style.display = 'block';
                        document.getElementById('data-content').style.display = 'none';
                        return;
                    }
                    
                    // Mostrar datos de detección
                    document.getElementById('waiting-content').style.display = 'none';
                    document.getElementById('data-content').style.display = 'block';
                    document.getElementById('plate-number').textContent = data.placa;
                    document.getElementById('detection-time').textContent = 'Detectado: ' + data.fecha;
                    
                    // Mostrar información según si tiene cita o no
                    if (data.tiene_cita && data.datos_cita) {
                        document.getElementById('appointment-found').style.display = 'block';
                        document.getElementById('no-appointment').style.display = 'none';
                        
                        // Llenar datos de la cita
                        const cita = data.datos_cita;
                        document.getElementById('client-name').textContent = cita.nombreCliente;
                        document.getElementById('client-id').textContent = cita.cedulaCliente;
                        document.getElementById('vehicle-model').textContent = cita.descripcionVeh;
                        document.getElementById('vehicle-desc').textContent = cita.descripcionAlterna;
                        document.getElementById('appointment-date').textContent = cita.fechaCita;
                        document.getElementById('agency').textContent = cita.agencia;
                        document.getElementById('advisor').textContent = cita.nombreAsesor;
                        document.getElementById('order').textContent = cita.ordenrepld;
                    } else {
                        document.getElementById('appointment-found').style.display = 'none';
                        document.getElementById('no-appointment').style.display = 'block';
                        document.getElementById('no-appointment-message').textContent = data.mensaje;
                    }
                })
                .catch(error => {
                    console.error('Error al obtener datos:', error);
                    document.getElementById('status-indicator').classList.remove('status-active');
                    document.getElementById('status-indicator').classList.add('status-inactive');
                    document.getElementById('status-text').textContent = 'Error de conexión';
                });
        }
        
        // Actualizar datos inmediatamente y luego cada 2 segundos
        actualizarDatos();
        setInterval(actualizarDatos, 2000);
    </script>
</body>
</html>
        ''')

def iniciar_servidor():
    # Crear plantillas antes de iniciar
    crear_templates()
    
    # Verificar conexión a la base de datos
    conn = conectar_db()
    if conn:
        print("Conexión a la base de datos exitosa")
        conn.close()
    else:
        print("ADVERTENCIA: No se pudo conectar a la base de datos MySQL")
    
    # Iniciar hilo de monitoreo
    t = threading.Thread(target=monitor_thread, daemon=True)
    t.start()
    
    # Iniciar el servidor web
    app.run(host='0.0.0.0', port=5000)

if __name__ == "__main__":
    iniciar_servidor()
