// Sistema de Detección de Placas - Panel de Administración con Vue.js
const { createApp, ref, onMounted } = Vue;

const app = createApp({
  setup() {
    // Estado reactivo
    const deviceStatus = ref('Sin verificar');
    const isActive = ref(false);
    const recentEvents = ref(0);
    const statusMessage = ref('');
    const verificationResult = ref('');
    const showVerificationResult = ref(false);
    const resultClass = ref('');
    
    // Función para verificar la conexión con la cámara
    const verificarConexion = () => {
      verificationResult.value = 'Verificando conexión...';
      showVerificationResult.value = true;
      resultClass.value = '';
      
      fetch('/verificar-conexion')
        .then(response => response.json())
        .then(data => {
          if (data.estado === 'Activo') {
            resultClass.value = 'alert alert-success';
            verificationResult.value = `✓ ${data.mensaje}`;
            deviceStatus.value = 'Activo';
            isActive.value = true;
          } else {
            resultClass.value = 'alert alert-danger';
            verificationResult.value = `⚠ ${data.mensaje}`;
            deviceStatus.value = 'Sin conexión';
            isActive.value = false;
            statusMessage.value = data.mensaje;
          }
          recentEvents.value = data.eventos_recientes;
        })
        .catch(error => {
          resultClass.value = 'alert alert-danger';
          verificationResult.value = '⚠ Error al verificar la conexión';
          console.error('Error:', error);
        });
    };
    
    // Función para copiar detalles del error
    const copyErrorDetails = (event) => {
      const button = event.currentTarget;
      const errorDetails = button.parentNode.parentNode.textContent.trim();
      
      navigator.clipboard.writeText(errorDetails)
        .then(() => {
          const originalText = button.innerHTML;
          button.innerHTML = '<i class="fas fa-check"></i> Copiado';
          setTimeout(() => {
            button.innerHTML = originalText;
          }, 2000);
        });
    };
    
    onMounted(() => {
      // Opcionalmente, podemos verificar la conexión automáticamente al cargar
      // verificarConexion();
    });
    
    return {
      deviceStatus,
      isActive,
      recentEvents,
      statusMessage,
      verificationResult,
      showVerificationResult,
      resultClass,
      verificarConexion,
      copyErrorDetails
    };
  }
});

// Montar la aplicación cuando el documento esté listo
document.addEventListener('DOMContentLoaded', () => {
  // Solo montar la aplicación si el elemento #admin-app existe
  if (document.getElementById('admin-app')) {
    app.mount('#admin-app');
  }
}); 