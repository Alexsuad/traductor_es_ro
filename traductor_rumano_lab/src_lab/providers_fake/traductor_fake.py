# File: src_lab/providers_fake/traductor_fake.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Adaptador simulado para la traducción de textos.
# Rol: Adaptador secundario simulado de PuertoTraductorTexto.
# ──────────────────────────────────────────────────────────────────────

import asyncio
from typing import Dict, Tuple
from src_lab.ports.puerto_traductor_texto import PuertoTraductorTexto
from src_lab.config.settings_lab import SettingsLab


class TraductorFake(PuertoTraductorTexto):
    """Implementación simulada de traductor para pruebas rápidas y seguras."""

    def __init__(self, settings: SettingsLab):
        self.settings = settings
        # Catálogo predefinido oficial de traducciones de prueba (para consistencia)
        self._catalogo: Dict[Tuple[str, str, str], str] = {
            # ES -> RO
            ("estoy muy feliz de estar aquí con ustedes.", "es", "ro"): 
                "Sunt foarte fericit să fiu aici cu voi.",
            ("¿pueden hablar un poco más despacio, por favor?", "es", "ro"): 
                "Puteți vorbi puțin mai rar, vă rog?",
            ("la comida está muy rica, muchas gracias por recibirme.", "es", "ro"): 
                "Mâncarea este foarte gustoasă, mulțumesc mult pentru găzduire.",
            ("voy a usar el traductor para entenderlos mejor.", "es", "ro"): 
                "Voi folosi traducătorul pentru a vă înțelege mai bine.",
            ("para mí es importante poder comunicarme mejor con ustedes porque somos familia.", "es", "ro"): 
                "Pentru mine este important să pot comunica mai bine cu voi pentru că suntem o familie.",
            
            # RO -> ES
            ("ne bucurăm că ești aici cu noi.", "ro", "es"): 
                "Nos alegra que estés aquí con nosotros.",
            ("vrei să mănânci ceva sau să bei o cafea?", "ro", "es"): 
                "¿Quieres comer algo o tomar un café?",
            ("nu îți face griji, poți vorbi încet.", "ro", "es"): 
                "No te preocupes, puedes hablar despacio.",
            ("familia este foarte importantă pentru noi.", "ro", "es"): 
                "La familia es muy importante para nosotros.",
            ("dacă nu înțelegi, putem repeta.", "ro", "es"): 
                "Si no entiendes, podemos repetir.",

            # ES -> EN
            ("hola, ¿cómo estás?", "es", "en"): "Hello, how are you?",
            ("entiendo un poco de inglés.", "es", "en"): "I understand a little bit of English.",

            # EN -> ES
            ("hello, how are you?", "en", "es"): "Hola, ¿cómo estás?",
            ("i understand a little bit of english.", "en", "es"): "Entiendo un poco de inglés.",

            # RO -> EN
            ("ne bucurăm de vizită.", "ro", "en"): "We enjoy the visit.",
            ("vorbiți engleză?", "ro", "en"): "Do you speak English?",

            # EN -> RO
            ("we enjoy the visit.", "en", "ro"): "Ne bucurăm de vizită.",
            ("do you speak english?", "en", "ro"): "Vorbiți engleză?",
            ("welcome to our home.", "en", "ro"): "Bun venit în casa noastră.",
            ("the weather is nice today.", "en", "ro"): "Vremea este frumoasă astăzi.",

            # EN -> ES (adicionales)
            ("welcome to our home.", "en", "es"): "Bienvenidos a nuestra casa.",
            ("the weather is nice today.", "en", "es"): "El clima está agradable hoy."
        }

    async def traducir(self, texto: str, origen: str, destino: str) -> str:
        """Simula la traducción de texto aplicando controles de seguridad y velocidad.

        Args:
            texto: Frase original.
            origen: Idioma origen.
            destino: Idioma destino.

        Returns:
            Texto traducido simulado.
        """
        # Validación de límites de caracteres
        if len(texto) > self.settings.max_caracteres_por_frase:
            raise ValueError(
                f"Límite de caracteres excedido: {len(texto)} > {self.settings.max_caracteres_por_frase}"
            )

        # Regla de doble confirmación
        if self.settings.permitir_apis_reales and not self.settings.modo_simulacion:
            # En Fase 1 esto es un comportamiento de simulación simulado para futuras integraciones.
            # Aquí actuamos como un fake simulado.
            pass

        # Latencia mínima simulada (Ajuste 3: latencia extremadamente pequeña para no ralentizar)
        await asyncio.sleep(0.01)

        # Búsqueda en catálogo (normalizada a minúsculas y sin espacios extras)
        texto_norm = texto.strip().lower()
        origen_norm = origen.strip().lower()
        destino_norm = destino.strip().lower()

        llave = (texto_norm, origen_norm, destino_norm)
        if llave in self._catalogo:
            return self._catalogo[llave]

        # Fallback si no está en catálogo
        return f"[FAKE-{origen_norm.upper()}->{destino_norm.upper()}] {texto}"
