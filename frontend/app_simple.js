
const SUPABASE_URL = 'https://nghrrsfuimwuzsukdbkd.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im5naHJyc2Z1aW13dXpzdWtkYmtkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3NzQ1MDIsImV4cCI6MjA3NTM1MDUwMn0.EFj6lIFqcdU-f5-oKB4aFAcnqVZBZQ7DIssbWCVHx-Q';

const supabase = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

const statusDisplay = document.getElementById('status');
const payloadDisplay = document.getElementById('payload-display');
const btnDisconnect = document.getElementById('btn-disconnect');
const btnConnect = document.getElementById('btn-connect');

// Variable global para manejar la suscripción
let realtimeChannel = null;

document.addEventListener('DOMContentLoaded', () => {
    console.log('Monitor RAW iniciado');
    configurarRealtime();
    configurarBotones();
});

function configurarRealtime() {
    try {
        realtimeChannel = supabase.channel('custom-insert-channel')
            .on(
                'postgres_changes',
                { event: 'INSERT', schema: 'public', table: 'detecciones' },
                (payload) => {
                    console.log('Change received!', payload);
                    mostrarPayloadCompleto(payload);
                }
            )
            .subscribe((status) => {
                console.log('Status:', status);
                if (status === 'SUBSCRIBED') {
                    statusDisplay.textContent = 'Conectado - Esperando datos...';
                    btnDisconnect.disabled = false;
                    btnConnect.disabled = true;
                } else if (status === 'CHANNEL_ERROR') {
                    statusDisplay.textContent = 'Error de conexión';
                    btnDisconnect.disabled = true;
                    btnConnect.disabled = false;
                }
            });

    } catch (error) {
        console.error('Error:', error);
        statusDisplay.textContent = 'Error de configuración';
    }
}

function mostrarPayloadCompleto(payload) {
    const payloadTexto = JSON.stringify(payload, null, 2);
    payloadDisplay.textContent = payloadTexto;
    
    statusDisplay.textContent = `Última actualización: ${new Date().toLocaleTimeString('es-ES')}`;
    
    console.log('Payload completo mostrado:', payload);
}

function configurarBotones() {
    btnDisconnect.addEventListener('click', () => {
        desconectar();
    });

    btnConnect.addEventListener('click', () => {
        reconectar();
    });
}

function desconectar() {
    console.log(' Desconectando por solicitud del usuario...');
    if (realtimeChannel) {
        realtimeChannel.unsubscribe();
        realtimeChannel = null;
        statusDisplay.textContent = 'Desconectado manualmente';
        payloadDisplay.textContent = 'Conexión cerrada. Usa "Reconectar" para volver a conectar.';
        
        btnDisconnect.disabled = true;
        btnConnect.disabled = false;
        
        console.log(' Desconectado correctamente');
    }
}

function reconectar() {
    console.log(' Reconectando...');
    statusDisplay.textContent = 'Reconectando...';
    payloadDisplay.textContent = 'Estableciendo conexión...';
    
    btnDisconnect.disabled = true;
    btnConnect.disabled = true;
    
    configurarRealtime();
}

window.addEventListener('beforeunload', () => {
    console.log(' Limpiando suscripción antes de cerrar...');
    if (realtimeChannel) {
        realtimeChannel.unsubscribe();
        console.log('Suscripción limpiada correctamente');
    }
});