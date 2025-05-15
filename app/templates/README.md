# Plantillas HTML del Sistema de Detección de Placas

Este directorio contiene las plantillas HTML utilizadas por el sistema para generar las interfaces web. A continuación se describe el propósito y estructura de cada archivo:

## index.html

Esta es la plantilla principal que se muestra en la pantalla de entrada del sistema. Está diseñada para mostrar en tiempo real la última placa detectada y su estado de cita.

### Características principales:

- **Visualización de placa**: Muestra la última placa detectada en un formato destacado y legible.
- **Estado de cita**: Indica claramente si el vehículo tiene una cita programada.
  - Si tiene cita: Muestra "CITA CONFIRMADA" en verde con los datos completos del cliente y la cita.
  - Si no tiene cita: Muestra "NO TIENE CITA" o "NO SE ENCONTRARON RESULTADOS" en rojo.
- **Información de cliente**: Cuando hay una cita, muestra los datos del cliente como nombre, cédula, etc.
- **Información del vehículo**: Muestra datos del vehículo cuando están disponibles.
- **Estados de espera**: Muestra un indicador visual cuando está esperando datos o hay problemas de conexión.
- **Actualización automática**: La página se actualiza cada pocos segundos mediante peticiones AJAX al endpoint `/datos`.

### Secciones de código:

- **Estilos CSS**: Define la apariencia visual de todos los elementos de la interfaz.
- **Contenido HTML**: Estructura para mostrar la información de placas y citas.
- **JavaScript**: Funcionalidad para actualización en tiempo real y manejo de diferentes estados.

## admin.html

Esta plantilla proporciona una interfaz de administración para monitorear el sistema y ver el historial completo de detecciones.

### Características principales:

- **Estado de la cámara**: Muestra información detallada sobre la cámara IP y su estado de conexión.
- **Verificación de conexión**: Permite verificar la conexión con la cámara en tiempo real.
- **Historial de detecciones**: Muestra una tabla paginada con todas las detecciones de placas registradas.
- **Filtrado**: Permite filtrar el historial por número de placa específico.
- **Paginación**: Implementa controles de navegación para recorrer grandes conjuntos de datos.

### Secciones de código:

- **Estilos CSS**: Define la apariencia de la interfaz de administración.
- **Panel de información de cámara**: Muestra datos técnicos de la cámara.
- **Tabla de historial**: Muestra los registros de placas detectadas.
- **Controles de paginación**: Permiten navegar entre diferentes páginas de resultados.
- **JavaScript**: Implementa la verificación de conexión y actualización de datos en tiempo real.

## Características comunes

Ambas plantillas comparten algunas características:

- **Diseño responsivo**: Se adaptan a diferentes tamaños de pantalla.
- **Identidad visual de Casabaca**: Utilizan los colores y el logotipo de la empresa.
- **Iconos de Font Awesome**: Para mejorar la experiencia visual.
- **Bootstrap 5**: Como framework CSS base para el diseño.
- **Feedback visual**: Códigos de colores e iconos para comunicar diferentes estados. 