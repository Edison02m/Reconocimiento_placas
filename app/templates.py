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
    <title>Sistema de Detección de Placas</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --primary-color: #1E88E5;
            --secondary-color: #333;
            --accent-color: #ffdd00;
            --light-bg: #f8f9fa;
            --dark-bg: #222;
            --success-color: #28a745;
            --error-color: #dc3545;
        }
        
        body {
            background-color: var(--light-bg);
            font-family: 'Montserrat', sans-serif;
            color: var(--secondary-color);
            line-height: 1.6;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }
        
        .header {
            background-color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 20px 0;
            position: relative;
            z-index: 100;
        }
        
        .logo-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 3rem;
        }
        
        .logo {
            height: 80px;
        }
        
        .status-container {
            display: flex;
            align-items: center;
            font-weight: 500;
            font-size: 1.2rem;
        }
        
        .status-indicator {
            width: 15px;
            height: 15px;
            border-radius: 50%;
            display: inline-block;
            margin-right: 10px;
        }
        
        .status-active {
            background-color: var(--success-color);
            animation: pulse 2s infinite;
        }
        
        .status-inactive {
            background-color: var(--error-color);
        }
        
        .main-content {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            padding: 3rem;
        }
        
        .content-container {
            width: 100%;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .plate {
            font-size: 4.5rem;
            font-weight: 700;
            text-align: center;
            padding: 1rem 2rem;
            background-color: var(--accent-color);
            color: var(--dark-bg);
            border-radius: 10px;
            margin-bottom: 3rem;
            border: 3px solid var(--dark-bg);
            display: inline-block;
            min-width: 280px;
            letter-spacing: 3px;
        }
        
        .info-section {
            background-color: white;
            border-radius: 15px;
            padding: 3rem;
            margin-bottom: 3rem;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
            width: 100%;
        }
        
        .appointment-confirmed {
            border-left: 8px solid var(--success-color);
        }
        
        .waiting-data {
            text-align: center;
            padding: 8rem 3rem;
            margin: 3rem 0;
            color: #555;
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .error-connection {
            text-align: center;
            padding: 8rem 3rem;
            background-color: #fff0f0;
            border-radius: 15px;
            margin: 3rem 0;
            color: var(--error-color);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        }
        
        .no-appointment {
            border-left: 8px solid var(--error-color);
        }
        
        h2 {
            font-size: 3rem;
            margin-bottom: 1.5rem;
            color: var(--primary-color);
            text-align: center;
        }
        
        .plate-container {
            text-align: center;
            margin-bottom: 3rem;
        }
        
        .footer {
            background-color: white;
            padding: 1.5rem 0;
            color: #888;
            font-size: 1rem;
            text-align: center;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.05);
        }
        
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.5; }
            100% { opacity: 1; }
        }
        
        .info-list {
            list-style: none;
            padding: 0;
            margin: 0;
            font-size: 1.8rem;
        }
        
        .info-list li {
            padding: 15px 0;
            border-bottom: 1px solid #eee;
            text-align: center;
        }
        
        .info-list li:last-child {
            border-bottom: none;
        }
        
        .welcome-container {
            text-align: center;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 60vh;
        }
        
        .welcome-title {
            font-size: 4rem;
            margin-bottom: 2rem;
            color: var(--primary-color);
        }
        
        .welcome-subtitle {
            font-size: 2rem;
            color: #666;
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .no-appointment-message {
            font-size: 2rem;
            text-align: center;
            padding: 2rem 0;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo-container">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzjacaReuensqCroZhbPShC0grYy7PDlMnxQ&s" alt="Suzuki" class="logo">
            <div class="status-container">
                    <span class="status-indicator" id="status-indicator"></span>
                    <span id="status-text">Verificando</span>
            </div>
        </div>
                </div>
                
    <div class="main-content">
        <div class="content-container">
            <!-- Pantalla de Bienvenida -->
            <div id="welcome-content" class="welcome-container">
                <h1 class="welcome-title">Bienvenido a Suzuki</h1>
                <p class="welcome-subtitle">Sistema de detección de vehículos activo y funcionando correctamente</p>
            </div>
            
            <!-- Esperando Vehículos -->
                <div id="waiting-content" class="waiting-data" style="display: none;">
                    <h2>Sistema Activo</h2>
                <p class="welcome-subtitle">Esperando detección de vehículos</p>
                </div>
                
            <!-- Error de Conexión -->
                <div id="error-connection" class="error-connection" style="display: none;">
                    <h2>Sistema en Mantenimiento</h2>
                <p class="welcome-subtitle">Por favor, espere un momento mientras restablecemos el servicio.</p>
                </div>
                
            <!-- Datos del Vehículo Detectado -->
                <div id="data-content" style="display: none;">
                    <div class="plate-container">
                        <h3 class="plate" id="plate-number">ABC-1234</h3>
                    </div>
                    
                <div id="appointment-found" class="info-section appointment-confirmed" style="display: none;">
                    <div class="text-center mb-4">
                            <h2>CITA CONFIRMADA</h2>
                        </div>
                        
                    <ul class="info-list">
                        <li><span id="client-info"></span></li>
                        <li><span id="vehicle-info"></span></li>
                        <li><span id="advisor-info"></span></li>
                            </ul>
                    </div>
                    
                <div id="no-appointment" class="info-section no-appointment" style="display: none;">
                    <div class="text-center mb-4">
                            <h2>NO TIENE CITA</h2>
                        </div>
                    <p class="no-appointment-message" id="no-appointment-message"></p>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
        <p>© 2025 Suzuki - Sistema de Detección de Vehículos v1.0</p>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Variable para almacenar el último evento procesado
        let ultimoEvento = null;
        // Variable para controlar el temporizador
        let temporizadorVuelta = null;
        
        // Función para formatear la placa con guion después de las primeras 3 letras
        function formatearPlaca(placa) {
            if (!placa) return "";
            
            // Eliminar cualquier guion existente
            placa = placa.replace(/-/g, '');
            
            // Si la placa tiene al menos 4 caracteres, insertar un guion después del tercer carácter
            if (placa.length >= 4) {
                return placa.substring(0, 3) + '-' + placa.substring(3);
            }
            
            return placa;
        }
        
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
                        mostrarContenido('error-connection');
                        return;
                    } else {
                        document.getElementById('error-connection').style.display = 'none';
                    }
                    
                    // Si no hay placa detectada, mostrar pantalla de bienvenida
                    if (!data.placa) {
                        mostrarContenido('welcome-content');
                        return;
                    }
                    
                    // Crear un identificador único para el evento actual (placa + hora)
                    const eventoActual = `${data.placa}-${data.fecha}`;
                    
                    // Verificar si este evento ya fue procesado (para evitar duplicados)
                    if (eventoActual === ultimoEvento) {
                        return; // No hacer nada si es el mismo evento
                    }
                    
                    // Es un nuevo evento, procesarlo
                    ultimoEvento = eventoActual;
                    
                    // Mostrar datos de detección
                    mostrarContenido('data-content');
                    document.getElementById('plate-number').textContent = formatearPlaca(data.placa);
                    
                    // Mostrar información según si tiene cita o no
                    if (data.tiene_cita && data.datos_cita) {
                        document.getElementById('appointment-found').style.display = 'block';
                        document.getElementById('no-appointment').style.display = 'none';
                        
                        // Llenar datos de la cita
                        const cita = data.datos_cita;
                        
                        // Crear información en formato de puntos
                        document.getElementById('client-info').textContent = `Estimado/a ${cita.nombreCliente} tiene cita agendada para el ${cita.fechaCita}`;
                        document.getElementById('vehicle-info').textContent = `Vehículo: ${cita.descripcionVeh}`;
                        document.getElementById('advisor-info').textContent = `Asesor: ${cita.nombreAsesor} - Orden: ${cita.ordenrepld}`;
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
                    
                    // Configurar temporizador para volver a la pantalla de bienvenida después de 1 minuto
                    if (temporizadorVuelta) {
                        clearTimeout(temporizadorVuelta);
                    }
                    
                    temporizadorVuelta = setTimeout(() => {
                        mostrarContenido('welcome-content');
                    }, 60000); // 60000 ms = 1 minuto
                })
                .catch(error => {
                    console.error('Error al obtener datos:', error);
                    const statusIndicator = document.getElementById('status-indicator');
                    const statusText = document.getElementById('status-text');
                    statusIndicator.classList.remove('status-active');
                    statusIndicator.classList.add('status-inactive');
                    statusText.textContent = 'Error de conexión';
                    
                    // Mostrar mensaje de error de conexión
                    mostrarContenido('error-connection');
                });
        }
        
        // Función auxiliar para mostrar solo el contenido especificado
        function mostrarContenido(idContenido) {
            const contenidos = ['welcome-content', 'waiting-content', 'error-connection', 'data-content'];
            
            contenidos.forEach(id => {
                document.getElementById(id).style.display = (id === idContenido) ? 'block' : 'none';
            });
        }
        
        // Actualizar datos inmediatamente y luego cada 2 segundos
        actualizarDatos();
        setInterval(actualizarDatos, 2000);
        
        // Desactivar el menú contextual para evitar interacciones no deseadas
        document.addEventListener('contextmenu', event => event.preventDefault());
        
        // Desactivar selección de texto
        document.addEventListener('selectstart', event => event.preventDefault());
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
        :root {
            --primary-color: #1E88E5;
            --secondary-color: #333;
            --light-bg: #f9f9f9;
            --border-color: #e0e0e0;
            --success-color: #28a745;
            --error-color: #dc3545;
        }
        
        body {
            background-color: var(--light-bg);
            font-family: 'Montserrat', sans-serif;
            color: var(--secondary-color);
            line-height: 1.6;
        }
        
        .logo-container {
            text-align: center;
            margin: 1.2rem 0;
        }
        
        .logo {
            max-height: 60px;
            transition: transform 0.3s ease;
        }
        
        .logo:hover {
            transform: scale(1.05);
        }
        
        .main-container {
            max-width: 1100px;
            margin: 0 auto;
            padding: 0 15px;
        }
        
        .card {
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 25px;
            overflow: hidden;
        }
        
        .card-header {
            background-color: var(--primary-color);
            color: white;
            font-weight: 600;
            font-size: 1.3rem;
            padding: 1rem 1.2rem;
        }
        
        .card-body {
            padding: 1.8rem;
        }
        
        .section-title {
            font-size: 1.3rem;
            font-weight: 600;
            margin-bottom: 1.2rem;
            color: var(--secondary-color);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .device-status {
            display: inline-block;
            width: 10px;
            height: 10px;
            border-radius: 50%;
            margin-right: 5px;
        }
        
        .status-active {
            background-color: var(--success-color);
        }
        
        .status-inactive {
            background-color: var(--error-color);
        }
        
        .camera-info {
            background-color: white;
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .label {
            font-weight: 600;
            color: #666;
        }
        
        .table {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        }
        
        .table th {
            background-color: rgba(0, 0, 0, 0.03);
            font-weight: 600;
            padding: 0.8rem;
        }
        
        .table td {
            padding: 0.8rem;
            vertical-align: middle;
        }
        
        .back-link {
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            color: #666;
            margin-bottom: 1rem;
            text-decoration: none;
            transition: color 0.2s;
        }
        
        .back-link:hover {
            color: var(--primary-color);
        }
        
        .btn {
            border-radius: 6px;
            padding: 0.5rem 1rem;
            transition: all 0.2s;
        }
        
        .btn-outline-primary:hover {
            background-color: var(--primary-color);
        }
        
        .error-msg {
            color: var(--error-color);
            font-style: italic;
            margin-top: 5px;
        }
        
        #verificar-resultado {
            display: none;
            margin-top: 1rem;
            padding: 0.75rem;
            border-radius: 6px;
            font-weight: 500;
        }
        
        .pagination {
            margin-bottom: 0;
        }
        
        .pagination .page-link {
            color: var(--primary-color);
            border-color: var(--border-color);
        }
        
        .pagination .page-item.active .page-link {
            background-color: var(--primary-color);
            border-color: var(--primary-color);
        }
        
        .footer {
            margin-top: 2rem;
            padding: 1rem 0;
            color: #888;
            font-size: 0.8rem;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="main-container">
        <a href="/" class="back-link"><i class="fas fa-arrow-left"></i> Volver al Monitor</a>
        
        <div class="logo-container">
            <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQzjacaReuensqCroZhbPShC0grYy7PDlMnxQ&s" alt="Suzuki" class="logo">
        </div>
        
        <div class="card">
            <div class="card-header">
                <i class="fas fa-cog"></i> Panel de Administración
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12 mb-4">
                        <h2 class="section-title"><i class="fas fa-video"></i> Dispositivos de Captura ANPR</h2>
                        
                        <div class="camera-info">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="row mb-2">
                                        <div class="col-md-4 label">Modelo:</div>
                                        <div class="col-md-8">{{ camara.modelo }}</div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-md-4 label">Estado:</div>
                                        <div class="col-md-8">
                                            <span class="device-status {% if camara.estado == 'Activo' %}status-active{% else %}status-inactive{% endif %}"></span> 
                                            <span id="estado-camara">{{ camara.estado }}</span>
                                            {% if camara.estado != 'Activo' %}
                                                <div class="error-msg mt-2">
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
                                    <div class="row mb-2">
                                        <div class="col-md-4 label">Eventos recientes:</div>
                                        <div class="col-md-8" id="eventos-recientes">{{ camara.eventos_recientes }}</div>
                                    </div>
                                    <div class="row mb-2">
                                        <div class="col-md-4 label">URL:</div>
                                        <div class="col-md-8">{{ camara.url }}</div>
                                    </div>
                                    <div class="row mb-2">
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
                                    <button id="verificar-conexion" class="btn btn-primary btn-sm">
                                        <i class="fas fa-sync-alt"></i> Verificar Conexión
                                    </button>
                                    <div id="verificar-resultado"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <div class="col-md-12">
                        <h2 class="section-title"><i class="fas fa-history"></i> Historial de Detecciones</h2>
                        
                        <div class="d-flex justify-content-between mb-3">
                            <button class="btn btn-outline-secondary">
                                <i class="fas fa-file-export"></i> Exportar Registros
                            </button>
                            <div>
                                <!-- Formulario de búsqueda -->
                                <form action="{{ url_for('main.admin') }}" method="get" class="d-flex">
                                    <input type="text" name="placa" class="form-control me-2" placeholder="Buscar placa..." 
                                           value="{{ paginacion.filtro_placa if paginacion and paginacion.filtro_placa }}">
                                    <button type="submit" class="btn btn-primary">
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
                        
                        {% if paginacion and paginacion.error_mensaje %}
                        <div class="alert alert-warning mb-3">
                            <i class="fas fa-exclamation-triangle me-2"></i>
                            <strong>Error al obtener registros:</strong> {{ paginacion.error_mensaje }}
                            <div class="mt-2">
                                <a href="{{ url_for('main.admin') }}" class="btn btn-sm btn-warning">
                                    <i class="fas fa-sync-alt"></i> Intentar nuevamente
                                </a>
                            </div>
                        </div>
                        {% endif %}
                        
                        <div class="table-responsive">
                            <table class="table table-hover">
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
                                    {% if historial and historial|length > 0 %}
                                        {% for registro in historial %}
                                            <tr>
                                                <td><strong>{{ registro.placa }}</strong></td>
                                                <td>{{ registro.fecha }}</td>
                                                <td>{{ registro.hora }}</td>
                                                <td>{{ registro.origen }}</td>
                                                <td>{{ registro.fecha_registro }}</td>
                                            </tr>
                                        {% endfor %}
                                    {% else %}
                                        <tr>
                                            <td colspan="5" class="text-center py-4">
                                                <div class="my-4">
                                                    <i class="fas fa-inbox text-muted mb-3" style="font-size: 2.5rem;"></i>
                                                    <p class="lead">No hay registros disponibles</p>
                                                    {% if paginacion and paginacion.filtro_placa %}
                                                        <p>No se encontraron coincidencias para "{{ paginacion.filtro_placa }}"</p>
                                                        <a href="{{ url_for('main.admin') }}" class="btn btn-outline-primary btn-sm mt-2">
                                                            <i class="fas fa-sync-alt"></i> Mostrar todos los registros
                                                        </a>
                                                    {% endif %}
                                                </div>
                                            </td>
                                        </tr>
                                    {% endif %}
                                </tbody>
                            </table>
                        </div>
                        
                        {% if historial and historial|length > 0 %}
                        <!-- Controles de paginación -->
                        {% if paginacion %}
                        <div class="d-flex justify-content-between align-items-center mt-3">
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
                        {% endif %}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>© 2025 Suzuki - Sistema de Detección de Vehículos v1.0</p>
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
                            errorMsg.className = 'error-msg mt-2';
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