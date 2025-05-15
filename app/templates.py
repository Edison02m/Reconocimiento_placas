import os

def crear_templates():
    """Crea la carpeta templates y genera los archivos HTML necesarios."""
    # Crear carpeta templates si no existe
    if not os.path.exists('app/templates'):
        os.makedirs('app/templates')
    
    # Crear el archivo de plantilla index.html
    with open('app/templates/index.html', 'w', encoding='utf-8') as f:
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
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
            border-left: 5px solid #0056b3;
        }
        .plate {
            font-size: 3rem;
            font-weight: bold;
            text-align: center;
            padding: 15px 20px;
            background-color: #ffdd00;
            color: #333;
            border-radius: 10px;
            margin-bottom: 25px;
            border: 2px solid #333;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            display: inline-block;
            min-width: 200px;
        }
        .info-label {
            font-weight: 600;
            color: #555;
            font-size: 0.9rem;
            text-transform: uppercase;
            margin-bottom: 5px;
            letter-spacing: 0.5px;
        }
        .info-value {
            font-size: 1.1rem;
            color: #333;
            font-weight: 500;
        }
        .timestamp {
            font-size: 0.9rem;
            color: #666;
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
            background-color: #f9f9f9;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
            border-left: 5px solid #e10600;
        }
        .no-appointment {
            text-align: center;
            padding: 60px 30px;
            background-color: #ffeeee;
            border-radius: 15px;
            margin: 20px 0;
            border: 2px solid #dc3545;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
        }
        #no-appointment-message {
            font-weight: 500;
            color: #333;
        }
        .status-message {
            background-color: #f1f1f1;
            padding: 12px 15px;
            border-radius: 8px;
            margin: 15px auto;
            border-left: 4px solid #0056b3;
            text-align: left;
            display: inline-block;
            max-width: 80%;
        }
        .waiting-data {
            text-align: center;
            padding: 80px 30px;
            background-color: #f5f5f5;
            border-radius: 10px;
            margin: 40px 0;
            color: #666;
            border: 1px dashed #0056b3;
        }
        .error-connection {
            text-align: center;
            padding: 80px 30px;
            background-color: #f8d7da;
            border-radius: 10px;
            margin: 40px 0;
            color: #721c24;
            border: 1px dashed #dc3545;
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
            font-size: 6rem;
            margin-bottom: 20px;
            color: #dc3545;
            animation: pulse 2s infinite;
        }
        .waiting-icon {
            font-size: 5rem;
            margin-bottom: 30px;
            color: #0056b3;
            animation: spin 2s linear infinite;
        }
        .error-icon {
            font-size: 5rem;
            margin-bottom: 30px;
            color: #dc3545;
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
        .admin-link {
            position: absolute;
            top: 10px;
            right: 20px;
            color: #666;
            text-decoration: none;
            font-size: 0.9rem;
        }
        .admin-link:hover {
            color: #333;
            text-decoration: underline;
        }
        .plate-container {
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <a href="/admin" class="admin-link"><i class="fas fa-cog"></i> Administración</a>
    
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
                    <span class="status-indicator" id="status-indicator"></span>
                    <span id="status-text">Verificando</span>
                </span>
            </div>
            <div class="card-body p-4">
                <div id="waiting-content" class="waiting-data">
                    <i class="fas fa-sync waiting-icon"></i>
                    <h2>Sistema Listo</h2>
                    <p>Esperando vehículos</p>
                </div>
                
                <div id="error-connection" class="error-connection" style="display: none;">
                    <i class="fas fa-exclamation-triangle error-icon"></i>
                    <h2>Sistema en Mantenimiento</h2>
                    <p>Por favor, espere un momento mientras restablecemos el servicio.</p>
                </div>
                
                <div id="data-content" style="display: none;">
                    <div class="row">
                        <div class="col-md-12 mb-4">
                            <div class="plate-container">
                                <h3 class="plate" id="plate-number">ABC-1234</h3>
                            </div>
                        </div>
                    </div>
                    
                    <div id="appointment-found" style="display: none;">
                        <div class="text-center mb-4">
                            <i class="fas fa-check-circle appointment-icon" style="font-size: 5rem; color: #28a745;"></i>
                            <h2 style="font-size: 2.5rem; font-weight: bold; color: #28a745; margin-top: 20px;">CITA CONFIRMADA</h2>
                        </div>
                        
                        <div class="client-info">
                            <div class="row mb-4">
                                <div class="col-md-12 text-center">
                                    <div style="font-size: 1.8rem; font-weight: bold; color: #333;" id="client-name"></div>
                                    <div style="font-size: 1.2rem; color: #666;" id="client-id"></div>
                                </div>
                            </div>
                            
                            <div class="row mb-3">
                                <div class="col-md-6 text-center">
                                    <div style="font-size: 1.1rem; font-weight: bold; color: #0056b3;">FECHA DE CITA</div>
                                    <div style="font-size: 1.6rem;" id="appointment-date"></div>
                                </div>
                                <div class="col-md-6 text-center">
                                    <div style="font-size: 1.1rem; font-weight: bold; color: #0056b3;">ASESOR</div>
                                    <div style="font-size: 1.6rem;" id="advisor"></div>
                                </div>
                            </div>
                        </div>
                        
                        <div class="vehicle-details mt-4">
                            <div class="row">
                                <div class="col-md-12 text-center">
                                    <div style="font-size: 1.3rem; font-weight: bold; margin-bottom: 10px; color: #333;">
                                        <i class="fas fa-car me-2"></i>INFORMACIÓN DEL VEHÍCULO
                                    </div>
                                    <div style="font-size: 1.5rem;" id="vehicle-model"></div>
                                    <div style="font-size: 1.2rem; margin-top: 10px;">
                                        <span style="font-weight: bold;">Orden:</span> 
                                        <span id="order"></span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div id="no-appointment" style="display: none;">
                        <div class="no-appointment">
                            <i class="fas fa-times-circle no-appointment-icon" style="color: #dc3545; font-size: 5rem;"></i>
                            <h2 style="font-size: 2.5rem; font-weight: bold; margin-top: 20px; color: #dc3545;">NO TIENE CITA</h2>
                            <div style="background-color: #f8f8f8; border-radius: 8px; padding: 15px; margin: 20px auto; max-width: 80%; border-left: 4px solid #dc3545;">
                                <span id="no-appointment-message" style="font-size: 1.2rem; font-weight: 500; color: #333;"></span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 Casabaca Toyota - Sistema de Detección de Vehículos v1.0</p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Función para actualizar los datos cada 2 segundos
        function actualizarDatos() {
            fetch('/datos')
                .then(response => response.json())
                .then(data => {
                    // Actualizar el indicador de estado
                    const statusIndicator = document.getElementById('status-indicator');
                    const statusText = document.getElementById('status-text');
                    
                    if (data.camara_conectada) {
                        statusIndicator.classList.remove('status-inactive');
                        statusIndicator.classList.add('status-active');
                        statusText.textContent = 'Activo';
                    } else {
                        statusIndicator.classList.remove('status-active');
                        statusIndicator.classList.add('status-inactive');
                        statusText.textContent = 'Sin conexión';
                    }
                    
                    // Controlar la visibilidad de las secciones según el estado
                    if (!data.camara_conectada) {
                        // Si no hay conexión con la cámara, mostrar mensaje de error
                        document.getElementById('error-connection').style.display = 'block';
                        document.getElementById('waiting-content').style.display = 'none';
                        document.getElementById('data-content').style.display = 'none';
                        return;
                    } else {
                        document.getElementById('error-connection').style.display = 'none';
                    }
                    
                    // Si hay conexión pero no hay placa detectada
                    if (!data.placa) {
                        document.getElementById('waiting-content').style.display = 'block';
                        document.getElementById('data-content').style.display = 'none';
                        return;
                    }
                    
                    // Mostrar datos de detección
                    document.getElementById('waiting-content').style.display = 'none';
                    document.getElementById('data-content').style.display = 'block';
                    document.getElementById('plate-number').textContent = data.placa;
                    
                    // Mostrar información según si tiene cita o no
                    if (data.tiene_cita && data.datos_cita) {
                        document.getElementById('appointment-found').style.display = 'block';
                        document.getElementById('no-appointment').style.display = 'none';
                        
                        // Llenar datos de la cita
                        const cita = data.datos_cita;
                        document.getElementById('client-name').textContent = cita.nombreCliente;
                        document.getElementById('client-id').textContent = cita.cedulaCliente;
                        document.getElementById('vehicle-model').textContent = cita.descripcionVeh;
                        document.getElementById('appointment-date').textContent = cita.fechaCita;
                        document.getElementById('advisor').textContent = cita.nombreAsesor;
                        document.getElementById('order').textContent = cita.ordenrepld;
                    } else {
                        document.getElementById('appointment-found').style.display = 'none';
                        document.getElementById('no-appointment').style.display = 'block';
                        
                        // Procesar el mensaje de la API
                        let mensajeAPI = data.mensaje || "NO SE ENCONTRARON RESULTADOS";
                        
                        // Formatear mensaje para mostrar en mayúsculas y bien presentado
                        if (mensajeAPI === "NO SE ENCONTRARON RESULTADOS") {
                            mensajeAPI = "No se encontraron citas programadas";
                        } else if (mensajeAPI.toLowerCase().includes("error")) {
                            mensajeAPI = "Error en la consulta de citas";
                        }
                        
                        document.getElementById('no-appointment-message').textContent = mensajeAPI;
                    }
                })
                .catch(error => {
                    console.error('Error al obtener datos:', error);
                    const statusIndicator = document.getElementById('status-indicator');
                    const statusText = document.getElementById('status-text');
                    statusIndicator.classList.remove('status-active');
                    statusIndicator.classList.add('status-inactive');
                    statusText.textContent = 'Error de conexión';
                    
                    // Mostrar mensaje de error de conexión
                    document.getElementById('error-connection').style.display = 'block';
                    document.getElementById('waiting-content').style.display = 'none';
                    document.getElementById('data-content').style.display = 'none';
                });
        }
        
        // Actualizar datos inmediatamente y luego cada 2 segundos
        actualizarDatos();
        setInterval(actualizarDatos, 2000);
    </script>
</body>
</html>
        ''')
    
    # Crear la plantilla para la página de administración
    with open('app/templates/admin.html', 'w', encoding='utf-8') as f:
        f.write('''
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Administración - Sistema de Detección de Placas</title>
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
            max-height: 60px;
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
            background-color: #0056b3;
            color: white;
            border-radius: 15px 15px 0 0 !important;
            font-weight: bold;
            font-size: 1.5rem;
            padding: 15px 20px;
        }
        .section-title {
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 20px;
            color: #444;
        }
        .device-card {
            background-color: #fff;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 15px;
            padding: 15px;
        }
        .device-status {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        .status-active {
            background-color: #28a745;
        }
        .status-inactive {
            background-color: #dc3545;
        }
        .table {
            font-size: 0.95rem;
        }
        .table th {
            font-weight: bold;
            background-color: #f0f0f0;
        }
        .footer {
            margin-top: 20px;
            padding: 15px 0;
            color: #777;
            font-size: 0.9rem;
            text-align: center;
            border-top: 1px solid #eee;
        }
        .back-link {
            margin-bottom: 20px;
            display: inline-block;
        }
        .camera-info {
            background-color: #f8f8f8;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .camera-info .row {
            margin-bottom: 10px;
        }
        .camera-info .label {
            font-weight: bold;
            color: #666;
        }
        #verificar-resultado {
            display: none;
            margin-top: 15px;
            padding: 12px;
            border-radius: 8px;
            font-weight: bold;
        }
        .alert-success {
            background-color: #d4edda;
            color: #155724;
        }
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
        }
        .error-msg {
            color: #dc3545;
            font-style: italic;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="main-container">
        <a href="/" class="back-link"><i class="fas fa-arrow-left"></i> Volver al Monitor</a>
        
        <div class="logo-container">
            <img src="https://www.casabaca.com/wp-content/uploads/2021/07/logo-casabaca-toyota-ec.png" alt="Casabaca Toyota" class="logo">
        </div>
        
        <div class="card">
            <div class="card-header">
                <i class="fas fa-cog"></i> Panel de Administración
            </div>
            <div class="card-body p-4">
                <div class="row">
                    <div class="col-md-12 mb-4">
                        <h2 class="section-title"><i class="fas fa-video"></i> Dispositivos de Captura ANPR</h2>
                        
                        <div class="camera-info">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="row">
                                        <div class="col-md-4 label">Modelo:</div>
                                        <div class="col-md-8">{{ camara.modelo }}</div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-4 label">Estado:</div>
                                        <div class="col-md-8">
                                            <span class="device-status {% if camara.estado == 'Activo' %}status-active{% else %}status-inactive{% endif %}"></span> 
                                            <span id="estado-camara">{{ camara.estado }}</span>
                                            {% if camara.estado != 'Activo' %}
                                                <div class="error-msg">
                                                    {{ camara.mensaje }}
                                                    <div class="mt-2">
                                                        <small class="text-muted">
                                                            <i class="fas fa-info-circle me-1"></i> 
                                                            Información técnica: Error de conexión con la cámara IP {{ camara.url }}. 
                                                            Verifique credenciales y disponibilidad de red.
                                                        </small>
                                                    </div>
                                                </div>
                                            {% endif %}
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-4 label">Eventos recientes:</div>
                                        <div class="col-md-8" id="eventos-recientes">{{ camara.eventos_recientes }}</div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-4 label">URL:</div>
                                        <div class="col-md-8">{{ camara.url }}</div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-4 label">Usuario:</div>
                                        <div class="col-md-8">{{ camara.usuario }}</div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <img src="https://www.hikvision.com/content/dam/hikvision/products/CIUD/ITS%20Camera/License%20Plate%20Recognition%20Unit/iDS-TCV107-F1B(850)/images/1.png" 
                                         alt="Hikvision ANPR Camera" style="max-width: 100%; border-radius: 5px;">
                                </div>
                            </div>
                            <div class="row mt-3">
                                <div class="col-md-12">
                                    <button id="verificar-conexion" class="btn btn-sm btn-primary">
                                        <i class="fas fa-sync-alt"></i> Verificar Conexión
                                    </button>
                                    <div id="verificar-resultado"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-12">
                        <h2 class="section-title"><i class="fas fa-history"></i> Historial de Detecciones</h2>
                        
                        <div class="table-responsive">
                            <table class="table table-striped table-hover">
                                <thead>
                                    <tr>
                                        <th>Número de Placa</th>
                                        <th>Fecha</th>
                                        <th>Hora</th>
                                        <th>Origen</th>
                                        <th>Registrado</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% if historial %}
                                        {% for registro in historial %}
                                            <tr>
                                                <td>{{ registro.placa }}</td>
                                                <td>{{ registro.fecha }}</td>
                                                <td>{{ registro.hora }}</td>
                                                <td>{{ registro.origen }}</td>
                                                <td>{{ registro.fecha_registro }}</td>
                                            </tr>
                                        {% endfor %}
                                    {% else %}
                                        <tr>
                                            <td colspan="5" class="text-center">No hay registros disponibles</td>
                                        </tr>
                                    {% endif %}
                                </tbody>
                            </table>
                        </div>
                        
                        <div class="d-flex justify-content-between">
                            <button class="btn btn-outline-secondary">
                                <i class="fas fa-file-export"></i> Exportar Registros
                            </button>
                            <div>
                                <!-- Formulario de búsqueda -->
                                <form action="{{ url_for('main.admin') }}" method="get" class="d-flex">
                                    <input type="text" name="placa" class="form-control me-2" placeholder="Buscar placa..." 
                                           value="{{ paginacion.filtro_placa if paginacion and paginacion.filtro_placa }}">
                                    <button type="submit" class="btn btn-outline-primary">
                                        <i class="fas fa-search"></i> Buscar
                                    </button>
                                    {% if paginacion and paginacion.filtro_placa %}
                                        <a href="{{ url_for('main.admin') }}" class="btn btn-outline-secondary ms-2">
                                            <i class="fas fa-times"></i> Limpiar
                                        </a>
                                    {% endif %}
                                </form>
                            </div>
                        </div>
                        
                        <!-- Controles de paginación -->
                        {% if paginacion %}
                        <div class="d-flex justify-content-between align-items-center mt-4">
                            <div>
                                <span class="text-muted">
                                    Mostrando registros {{ (paginacion.pagina_actual - 1) * paginacion.registros_por_pagina + 1 }} 
                                    al {{ (paginacion.pagina_actual - 1) * paginacion.registros_por_pagina + historial|length }}
                                    de {{ paginacion.total_registros }} en total
                                    {% if paginacion.filtro_placa %}
                                        (Filtro: "{{ paginacion.filtro_placa }}")
                                    {% endif %}
                                </span>
                            </div>
                            <nav aria-label="Navegación de páginas">
                                <ul class="pagination">
                                    <!-- Botón Anterior -->
                                    <li class="page-item {% if paginacion.pagina_actual == 1 %}disabled{% endif %}">
                                        <a class="page-link" href="{{ url_for('main.admin', pagina=paginacion.pagina_actual-1, placa=paginacion.filtro_placa) }}" aria-label="Anterior">
                                            <span aria-hidden="true">&laquo;</span>
                                        </a>
                                    </li>
                                    
                                    <!-- Páginas -->
                                    {% for p in range(1, paginacion.total_paginas + 1) %}
                                        <li class="page-item {% if p == paginacion.pagina_actual %}active{% endif %}">
                                            <a class="page-link" href="{{ url_for('main.admin', pagina=p, placa=paginacion.filtro_placa) }}">{{ p }}</a>
                                        </li>
                                    {% endfor %}
                                    
                                    <!-- Botón Siguiente -->
                                    <li class="page-item {% if paginacion.pagina_actual == paginacion.total_paginas %}disabled{% endif %}">
                                        <a class="page-link" href="{{ url_for('main.admin', pagina=paginacion.pagina_actual+1, placa=paginacion.filtro_placa) }}" aria-label="Siguiente">
                                            <span aria-hidden="true">&raquo;</span>
                                        </a>
                                    </li>
                                </ul>
                            </nav>
                        </div>
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 Casabaca Toyota - Sistema de Detección de Vehículos v1.0</p>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Función para copiar detalles del error
        function copyErrorDetails(button) {
            const errorDetails = button.parentNode.parentNode.textContent.trim();
            navigator.clipboard.writeText(errorDetails).then(() => {
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-check"></i> Copiado';
                setTimeout(() => {
                    button.innerHTML = originalText;
                }, 2000);
            });
        }
        
        // Función para verificar la conexión con la cámara
        document.getElementById('verificar-conexion').addEventListener('click', function() {
            const resultadoDiv = document.getElementById('verificar-resultado');
            const estadoSpan = document.getElementById('estado-camara');
            const indicador = document.querySelector('.device-status');
            const eventosSpan = document.getElementById('eventos-recientes');
            
            resultadoDiv.innerHTML = 'Verificando conexión...';
            resultadoDiv.style.display = 'block';
            resultadoDiv.className = '';
            
            fetch('/verificar-conexion')
                .then(response => response.json())
                .then(data => {
                    if (data.estado === 'Activo') {
                        resultadoDiv.className = 'alert alert-success';
                        resultadoDiv.innerHTML = '<i class="fas fa-check-circle"></i> ' + data.mensaje;
                        estadoSpan.textContent = 'Activo';
                        indicador.className = 'device-status status-active';
                        // Limpiar mensaje de error si existe
                        const errorMsg = document.querySelector('.error-msg');
                        if (errorMsg) errorMsg.remove();
                    } else {
                        resultadoDiv.className = 'alert alert-danger';
                        resultadoDiv.innerHTML = `
                            <i class="fas fa-exclamation-triangle"></i> ${data.mensaje}
                            <hr>
                            <div class="mt-2 small">
                                <strong>Detalles técnicos:</strong><br>
                                - No se pudo establecer conexión con la cámara<br>
                                - Código de error: CM-${Date.now().toString().slice(-6)}<br>
                                - Tiempo de respuesta excedido<br>
                                <div class="mt-2">
                                    <button class="btn btn-sm btn-outline-secondary" onclick="copyErrorDetails(this)">
                                        <i class="fas fa-copy"></i> Copiar detalles
                                    </button>
                                </div>
                            </div>
                        `;
                        estadoSpan.textContent = 'Sin conexión';
                        indicador.className = 'device-status status-inactive';
                        
                        // Añadir mensaje de error debajo del estado
                        let errorMsg = document.querySelector('.error-msg');
                        if (!errorMsg) {
                            errorMsg = document.createElement('div');
                            errorMsg.className = 'error-msg';
                            estadoSpan.parentNode.appendChild(errorMsg);
                        }
                        errorMsg.innerHTML = `
                            ${data.mensaje}
                            <div class="mt-2">
                                <small class="text-muted">
                                    <i class="fas fa-info-circle me-1"></i> 
                                    Información técnica: Error al comunicarse con la cámara. 
                                    Verifique la configuración de red y credenciales.
                                </small>
                            </div>
                        `;
                    }
                    eventosSpan.textContent = data.eventos_recientes;
                })
                .catch(error => {
                    resultadoDiv.className = 'alert alert-danger';
                    resultadoDiv.innerHTML = '<i class="fas fa-exclamation-triangle"></i> Error al verificar la conexión';
                    console.error('Error:', error);
                });
        });
    </script>
</body>
</html>
        ''')