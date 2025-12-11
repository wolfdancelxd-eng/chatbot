const chatBot = document.getElementById('ChatBot');
const inputMensaje = document.getElementById('mensaje');

// Generar ID de sesión
let sessionId = localStorage.getItem('chatbot_session_id');
if (!sessionId) {
    sessionId = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    localStorage.setItem('chatbot_session_id', sessionId);
}

// Agregar mensajes al chat
function agregarMensaje(texto, tipo) {
    const mensaje = document.createElement('div');
    mensaje.className = tipo === 'usuario' ? 'mensajeusuario' : 'mensajebot';
    
    const contenido = document.createElement('div');
    contenido.className = 'contenido';
    contenido.innerHTML = texto.replace(/\n/g, '<br>');
    
    mensaje.appendChild(contenido);
    chatBot.appendChild(mensaje);
    chatBot.scrollTop = chatBot.scrollHeight;
}

// Enviar mensaje a Flask (Python)
async function enviarMensaje(mensajeRapido = null) {
    let mensaje;
    
    if (mensajeRapido) {
        mensaje = mensajeRapido;
    } else {
        mensaje = inputMensaje.value.trim();
        if (mensaje === '') return;
    }
    
    inputMensaje.value = '';
    agregarMensaje(mensaje, 'usuario');
    
    // Mostrar "Escribiendo..."
    const escribiendo = document.createElement('div');
    escribiendo.className = 'mensajebot';
    escribiendo.id = 'escribiendo';
    escribiendo.innerHTML = '<div class="contenido">Escribiendo...</div>';
    chatBot.appendChild(escribiendo);
    chatBot.scrollTop = chatBot.scrollHeight;
    
    try {
        // Conectar con Flask (Python)
        const response = await fetch('/chat',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                mensaje: mensaje,
                session_id: sessionId
            })
        });
        
        if (!response.ok) {
            throw new Error('Error en Flask');
        }
        
        const data = await response.json();
        
        // Quitar "Escribiendo..."
        const escribiendoEl = document.getElementById('escribiendo');
        if (escribiendoEl) escribiendoEl.remove();
        
        // Mostrar respuesta de Flask
        setTimeout(() => {
            if (data.respuesta) {
                agregarMensaje(data.respuesta, 'bot');
            } else {
                agregarMensaje('Error al recibir respuesta', 'bot');
            }
        }, 300);
        
    } catch (error) {
        console.error('Error:', error);
        
        const escribiendoEl = document.getElementById('escribiendo');
        if (escribiendoEl) escribiendoEl.remove();
        
        agregarMensaje('❌ No puedo conectarme con el servidor. Asegúrate de ejecutar: python app.py', 'bot');
    }
}

// Función alternativa
function Mensaje() {
    enviarMensaje();
}

// Mensaje de bienvenida
setTimeout(() => {
    agregarMensaje('Puedo ayudarte con información sobre nuestros planes de internet. Pregúntame lo que necesites 😊', 'bot');
}, 2000);