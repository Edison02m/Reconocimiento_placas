// Sistema de Detección de Placas - Aplicación Vue.js
const { createApp, ref, onMounted, computed, watch } = Vue;

const app = createApp({
  setup() {
    // Estado reactivo
    const statusIndicator = ref('status-inactive');
    const statusText = ref('Verificando');
    const currentView = ref('welcome-content');
    const plateNumber = ref('');
    const clientInfo = ref('');
    const vehicleInfo = ref('');
    const advisorInfo = ref('');
    const noAppointmentMessage = ref('');
    const hasAppointment = ref(false);
    
    // Variables para control de eventos
    let ultimoEvento = null;
    let temporizadorVuelta = null;
    
    // Formatear placa con guion después de las primeras 3 letras
    const formatearPlaca = (placa) => {
      if (!placa) return "";
      
      // Eliminar cualquier guion existente
      placa = placa.replace(/-/g, '');
      
      // Si la placa tiene al menos 4 caracteres, insertar un guion después del tercer carácter
      if (placa.length >= 4) {
        return placa.substring(0, 3) + '-' + placa.substring(3);
      }
      
      return placa;
    };
    
    // Función para actualizar los datos cada 2 segundos
    const actualizarDatos = () => {
      fetch('/datos')
        .then(response => response.json())
        .then(data => {
          // Actualizar el indicador de estado
          if (data.camara_conectada) {
            statusIndicator.value = 'status-active';
            statusText.value = 'Activo';
          } else {
            statusIndicator.value = 'status-inactive';
            statusText.value = 'Sin conexión';
          }
          
          // Controlar la visibilidad de las secciones según el estado
          if (!data.camara_conectada) {
            // Si no hay conexión con la cámara, mostrar mensaje de error
            currentView.value = 'error-connection';
            return;
          }
          
          // Si no hay placa detectada, mostrar pantalla de bienvenida
          if (!data.placa) {
            currentView.value = 'welcome-content';
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
          currentView.value = 'data-content';
          plateNumber.value = formatearPlaca(data.placa);
          
          // Mostrar información según si tiene cita o no
          if (data.tiene_cita && data.datos_cita) {
            hasAppointment.value = true;
            
            // Llenar datos de la cita
            const cita = data.datos_cita;
            
            // Crear información en formato de puntos
            clientInfo.value = `Estimado/a ${cita.nombreCliente} tiene cita agendada para el ${cita.fechaCita}`;
            vehicleInfo.value = `Vehículo: ${cita.descripcionVeh}`;
            advisorInfo.value = `Asesor: ${cita.nombreAsesor} - Orden: ${cita.ordenrepld}`;
          } else {
            hasAppointment.value = false;
            
            // Procesar el mensaje de la API
            let mensajeAPI = data.mensaje || "NO SE ENCONTRARON RESULTADOS";
            
            // Formatear mensaje para mostrar en mayúsculas y bien presentado
            if (mensajeAPI === "NO SE ENCONTRARON RESULTADOS") {
              mensajeAPI = "No se encontraron citas programadas";
            } else if (mensajeAPI.toLowerCase().includes("error")) {
              mensajeAPI = "Error en la consulta de citas";
            }
            
            noAppointmentMessage.value = mensajeAPI;
          }
          
          // Configurar temporizador para volver a la pantalla de bienvenida después de 1 minuto
          if (temporizadorVuelta) {
            clearTimeout(temporizadorVuelta);
          }
          
          temporizadorVuelta = setTimeout(() => {
            currentView.value = 'welcome-content';
          }, 60000); // 60000 ms = 1 minuto
        })
        .catch(error => {
          console.error('Error al obtener datos:', error);
          statusIndicator.value = 'status-inactive';
          statusText.value = 'Error de conexión';
          
          // Mostrar mensaje de error de conexión
          currentView.value = 'error-connection';
        });
    };
    
    // Iniciar la actualización de datos al montar el componente
    onMounted(() => {
      // Actualizar datos inmediatamente y luego cada 2 segundos
      actualizarDatos();
      setInterval(actualizarDatos, 2000);
      
      // Desactivar el menú contextual para evitar interacciones no deseadas
      document.addEventListener('contextmenu', event => event.preventDefault());
      
      // Desactivar selección de texto
      document.addEventListener('selectstart', event => event.preventDefault());
    });
    
    return {
      statusIndicator,
      statusText,
      currentView,
      plateNumber,
      clientInfo,
      vehicleInfo,
      advisorInfo,
      noAppointmentMessage,
      hasAppointment
    };
  }
});

// Montar la aplicación
app.mount('#app'); 