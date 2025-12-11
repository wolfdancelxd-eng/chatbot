from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Almacenar conversaciones por session_id
conversaciones = {}

# ==========================================
# RESPUESTAS DEL CHATBOT
# ==========================================

RESPUESTAS = {
    "hola": [
        "¡Hola! ¿En qué puedo ayudarte hoy? 😊",
        "¡Hola! Estoy aquí para ayudarte con nuestros planes de internet.",
        "¡Qué tal! ¿Buscas información sobre nuestros servicios?",
        "¡Bienvenido! Cuéntame qué necesitas 🙌"
    ],
    "planes": [
        "Tenemos 4 planes disponibles:\n\n📶 Plan BÁSICO: 30 Mbps — S/ 59.90/mes\n⚡ Plan HOGAR: 80 Mbps — S/ 79.90/mes\n🚀 Plan GAMER: 150 Mbps — S/ 109.90/mes\n💼 Plan NEGOCIOS: 200 Mbps — S/ 149.90/mes\n\n¿Necesitas ayuda para elegir el mejor plan?",
        "Mira nuestros planes:\n📶 Básico S/59.90 | ⚡ Hogar S/79.90 | 🚀 Gamer S/109.90 | 💼 Negocios S/149.90\n\n¿Cuál te interesa?"
    ],
    "precio": [
        "Nuestros precios van desde S/ 59.90/mes hasta S/ 149.90/mes. ¿Quieres que te muestre todos los planes?",
        "Tenemos opciones desde S/ 59.90 al mes. ¿Te muestro los planes completos?"
    ],
    "ayuda_elegir": [
        "¡Te ayudo a elegir! ¿Para qué usarás principalmente el internet?\n\n📶 BÁSICO - Navegar y redes sociales\n🏠 FAMILIAR - Streaming en HD\n🎮 GAMING - Juegos online\n💼 TRABAJO - Videollamadas, home office"
    ],
    "uso_basico": [
        "Para uso básico te recomiendo:\n\n📶 Plan BÁSICO (S/ 59.90/mes - 30 Mbps)\nIdeal para 1-2 personas navegando y redes sociales.\n\n¿Te interesa este plan?"
    ],
    "uso_familia": [
        "Para uso familiar te recomiendo:\n\n⚡ Plan HOGAR (S/ 79.90/mes - 80 Mbps)\nPerfecto para 3-5 personas viendo streaming.\n\n¿Cuántas personas son en casa?"
    ],
    "uso_gaming": [
        "¡Para gaming necesitas velocidad! 🎮\n\nTe recomiendo el Plan GAMER (150 Mbps - S/ 109.90/mes):\n✅ Sin lag\n✅ Ping bajo\n✅ Descargas rápidas\n\n¿Te interesa este plan?"
    ],
    "uso_trabajo": [
        "Para trabajo remoto te recomiendo el Plan NEGOCIOS (200 Mbps - S/ 149.90/mes):\n✅ Videollamadas HD\n✅ Subida rápida de archivos\n✅ Estable y confiable\n✅ Ideal para empresas\n\n¿Te interesa este plan?"
    ],
    "confirmar_contratacion": [
        "¡Excelente! 🎉\n\nPara contratar:\n📧 requenaangle61@gmail.com\n📱 WhatsApp: +51 973 550 595\n🌐 Web: https://www.aeronet.com\n\nCódigo de descuento: CHAT10 (10% OFF primer mes)\n\n¿Necesitas algo más?"
    ],
    "no_contratar": [
        "No hay problema. ¿Tienes alguna otra pregunta sobre los planes?",
        "Está bien. Si cambias de opinión o tienes dudas, aquí estoy 😊"
    ],
    "pocas_personas": [
        "Para 1-2 personas el Plan BÁSICO (S/ 59.90) es perfecto. ¿Te interesa?"
    ],
    "medianas_personas": [
        "Para 3-5 personas te recomiendo el Plan HOGAR (S/ 79.90). ¿Qué dices?"
    ],
    "muchas_personas": [
        "Para 6-10 personas necesitas el Plan GAMER (S/ 109.90). ¿Te interesa?"
    ],
    "empresa": [
        "Para una empresa te recomiendo el Plan NEGOCIOS (S/ 149.90). ¿Te interesa?"
    ],
    "ayuda": [
        "Puedo ayudarte con: planes, precios, recomendaciones. ¿Qué necesitas? 😊",
        "Estoy aquí para asistirte. Pregúntame sobre planes, precios o instalación."
    ],
    "gracias": [
        "¡De nada! ¿Hay algo más en lo que pueda ayudarte?",
        "¡Para servirte! 👍",
        "¡Con gusto! Si tienes más dudas, pregúntame 😊"
    ],
    "adios": [
        "¡Hasta luego! Que tengas un excelente día 👋",
        "¡Nos vemos! No dudes en volver si necesitas algo 😊",
        "¡Adiós! Fue un placer ayudarte 🙌"
    ],
    "horarios": [
        "Atendemos de lunes a viernes de 9:00 AM a 8:00 PM 🕐",
        "Nuestro horario es de 9am a 8pm, de lunes a viernes"
    ],
    "instalacion": [
        "La instalación es GRATIS y tarda 24-48 horas ✅",
        "Instalamos gratis en 1-2 días hábiles después de contratar"
    ],
    "soporte": [
        "Soporte técnico 24/7 al 01-555-9999 o soporte@aeronet.com 🛠️",
        "Tenemos asistencia las 24 horas. Llámanos al 01-555-9999"
    ],
    "cobertura": [
        "Tenemos cobertura en toda la ciudad. ¿En qué zona vives?",
        "Cubrimos todas las zonas urbanas. Dime tu distrito"
    ],
    "wifi": [
        "Incluimos router WiFi de última generación sin costo extra 📶",
        "Router WiFi 6 incluido en todos los planes"
    ],
    "velocidad": [
        "Nuestras velocidades son: 30 Mbps, 80 Mbps, 150 Mbps y 200 Mbps",
        "Ofrecemos desde 30 hasta 200 Mbps según el plan"
    ],
    "contacto": [
        "📧 Correo: requenaangle61@gmail.com\n📞 Teléfono: 01-555-1234\n📱 WhatsApp: +51 973 550 595"
    ]
}

def detectar_numero(mensaje):
    numeros = {
        "1": 1, "2": 2, "3": 3, "4": 4, "5": 5,
        "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
        "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
        "seis": 6, "siete": 7, "ocho": 8, "nueve": 9, "diez": 10
    }
    for palabra, num in numeros.items():
        if palabra in mensaje:
            return num
    return None

def responder(mensaje, session_id):
    texto = mensaje.lower().strip()
    
    if session_id not in conversaciones:
        conversaciones[session_id] = {
            "contexto": "inicial",
            "historial": []
        }
    
    sesion = conversaciones[session_id]
    contexto = sesion["contexto"]
    sesion["historial"].append({"rol": "usuario", "texto": mensaje})
    
    if contexto == "pregunta_ver_planes":
        if any(palabra in texto for palabra in ["si", "sí", "ok", "dale", "claro"]):
            sesion["contexto"] = "pregunta_ayuda_elegir"
            return random.choice(RESPUESTAS["planes"])
        else:
            sesion["contexto"] = "inicial"
            return "Está bien. ¿En qué más puedo ayudarte?"
    
    if contexto == "pregunta_ayuda_elegir":
        if any(palabra in texto for palabra in ["basico", "básico", "el basico", "plan basico", "uno", "1", "primero"]):
            sesion["contexto"] = "pregunta_contratar_basico"
            return "El Plan BÁSICO (S/ 59.90/mes - 30 Mbps) es perfecto para uso ligero. ¿Te interesa contratarlo?"
        elif any(palabra in texto for palabra in ["hogar", "familiar", "el hogar", "plan hogar", "dos", "2", "segundo"]):
            sesion["contexto"] = "pregunta_contratar_hogar"
            return "El Plan HOGAR (S/ 79.90/mes - 80 Mbps) es ideal para familias. ¿Te interesa contratarlo?"
        elif any(palabra in texto for palabra in ["gamer", "gaming", "el gamer", "plan gamer", "tres", "3", "tercero"]):
            sesion["contexto"] = "pregunta_contratar_gamer"
            return "El Plan GAMER (S/ 109.90/mes - 150 Mbps) es perfecto para gaming. ¿Te interesa contratarlo?"
        elif any(palabra in texto for palabra in ["negocio", "negocios", "empresarial", "empresa", "cuatro", "4", "cuarto"]):
            sesion["contexto"] = "pregunta_contratar_negocios"
            return "El Plan NEGOCIOS (S/ 149.90/mes - 200 Mbps) es ideal para empresas. ¿Te interesa contratarlo?"
        elif any(palabra in texto for palabra in ["si", "sí", "ayuda", "claro", "dale"]):
            sesion["contexto"] = "esperando_tipo_uso"
            return random.choice(RESPUESTAS["ayuda_elegir"])
        elif "no" in texto:
            sesion["contexto"] = "inicial"
            return "Perfecto. Si tienes dudas, pregúntame."
    
    if contexto == "esperando_tipo_uso":
        if any(palabra in texto for palabra in ["basico", "básico", "navegar", "redes sociales", "1", "uno"]):
            sesion["contexto"] = "pregunta_contratar_basico"
            return random.choice(RESPUESTAS["uso_basico"])
        elif any(palabra in texto for palabra in ["familiar", "familia", "hogar", "streaming", "2", "dos"]):
            sesion["contexto"] = "esperando_num_personas"
            return random.choice(RESPUESTAS["uso_familia"])
        elif any(palabra in texto for palabra in ["gaming", "gamer", "juegos", "3", "tres"]):
            sesion["contexto"] = "pregunta_contratar_gamer"
            return random.choice(RESPUESTAS["uso_gaming"])
        elif any(palabra in texto for palabra in ["trabajo", "office", "negocio", "empresa", "4", "cuatro"]):
            sesion["contexto"] = "pregunta_contratar_negocios"
            return random.choice(RESPUESTAS["uso_trabajo"])
    
    if contexto == "esperando_num_personas":
        num = detectar_numero(texto)
        if num:
            if num <= 2:
                sesion["contexto"] = "pregunta_contratar_basico"
                return random.choice(RESPUESTAS["pocas_personas"])
            elif num <= 5:
                sesion["contexto"] = "pregunta_contratar_hogar"
                return random.choice(RESPUESTAS["medianas_personas"])
            elif num <= 10:
                sesion["contexto"] = "pregunta_contratar_gamer"
                return random.choice(RESPUESTAS["muchas_personas"])
            else:
                sesion["contexto"] = "pregunta_contratar_negocios"
                return random.choice(RESPUESTAS["empresa"])
        else:
            return "No entendí el número. ¿Cuántas personas son? (escribe un número)"
    
    if contexto in ["pregunta_contratar_basico", "pregunta_contratar_hogar", "pregunta_contratar_gamer", "pregunta_contratar_negocios"]:
        if any(palabra in texto for palabra in ["si", "sí", "quiero", "contratar", "dale", "ok", "claro"]):
            sesion["contexto"] = "pregunta_necesita_mas"
            return random.choice(RESPUESTAS["confirmar_contratacion"])
        elif "no" in texto:
            sesion["contexto"] = "inicial"
            return random.choice(RESPUESTAS["no_contratar"])
    
    if contexto == "pregunta_necesita_mas":
        if any(palabra in texto for palabra in ["si", "sí", "claro", "ok", "dale", "ayuda", "necesito"]):
            sesion["contexto"] = "inicial"
            return "¿En qué más puedo ayudarte? 😊"
        elif any(palabra in texto for palabra in ["no", "nada", "eso es todo", "gracias"]):
            sesion["contexto"] = "inicial"
            return "Estoy aquí de todos modos para ayudarte. Si necesitas algo, pregúntame 😊"
    
    if any(palabra in texto for palabra in ["hola", "buenos", "buenas", "hey", "que tal", "mucho gusto", "saludos", "wenas", "hi", "ola"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["hola"])
    
    if any(palabra in texto for palabra in ["plan", "planes", "paquete", "opciones", "que planes tienen"]):
        sesion["contexto"] = "pregunta_ayuda_elegir"
        return random.choice(RESPUESTAS["planes"])
    
    if any(palabra in texto for palabra in ["precio", "costo", "cuanto", "vale"]):
        sesion["contexto"] = "pregunta_ver_planes"
        return random.choice(RESPUESTAS["precio"])
    
    if any(frase in texto for frase in ["ayuda para elegir", "ayudame", "cual me conviene", "no se cual", "cual me recomiendas"]):
        sesion["contexto"] = "esperando_tipo_uso"
        return random.choice(RESPUESTAS["ayuda_elegir"])
    
    if any(palabra in texto for palabra in ["horario", "hora", "cuando atienden", "abierto"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["horarios"])
    
    if any(palabra in texto for palabra in ["instalar", "instalacion", "instalación", "cuanto tarda"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["instalacion"])
    
    if any(palabra in texto for palabra in ["soporte", "ayuda tecnica", "problema", "falla"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["soporte"])
    
    if any(palabra in texto for palabra in ["cobertura", "zona", "llegan", "disponible"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["cobertura"])
    
    if any(palabra in texto for palabra in ["wifi", "wi-fi", "router", "señal"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["wifi"])
    
    if any(palabra in texto for palabra in ["velocidad", "rapido", "rápido", "mbps", "megas"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["velocidad"])
    
    if any(palabra in texto for palabra in ["contacto", "contactar", "correo", "telefono", "whatsapp"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["contacto"])
    
    if any(palabra in texto for palabra in ["ayuda", "duda", "en que me puedes asistir"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["ayuda"])
    
    if any(palabra in texto for palabra in ["gracias", "thanks", "agradezco"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["gracias"])
    
    if any(palabra in texto for palabra in ["adios", "adiós", "chao", "bye", "hasta luego"]):
        sesion["contexto"] = "inicial"
        return random.choice(RESPUESTAS["adios"])
    
    sesion["contexto"] = "inicial"
    return "No estoy seguro de eso. Pregúntame sobre: planes, precios, horarios, instalación o soporte 😊"



@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se envió JSON"}), 400
    
    mensaje = data.get("mensaje", "").strip()
    session_id = data.get("session_id")
    
    if not mensaje:
        return jsonify({"error": "Mensaje vacío"}), 400
    if not session_id:
        return jsonify({"error": "Falta session_id"}), 400
    
    texto_respuesta = responder(mensaje, session_id)
    conversaciones[session_id]["historial"].append({
        "rol": "bot", 
        "texto": texto_respuesta
    })
    
    return jsonify({"respuesta": texto_respuesta})
@app.route('/')
def index():
    return render_template('chatbot.html')

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000)
