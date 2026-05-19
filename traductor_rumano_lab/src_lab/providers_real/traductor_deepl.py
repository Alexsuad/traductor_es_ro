# File: src_lab/providers_real/traductor_deepl.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Adaptador real para la traducción de textos utilizando DeepL.
# Rol: Adaptador secundario real de PuertoTraductorTexto.
# ──────────────────────────────────────────────────────────────────────

import asyncio
import deepl
from src_lab.ports.puerto_traductor_texto import PuertoTraductorTexto
from src_lab.config.settings_lab import SettingsLab


class TraductorDeepL(PuertoTraductorTexto):
    """Adaptador de producción para traducir texto a través de la API oficial de DeepL.

    Este adaptador ejecuta consultas HTTP controladas de forma asíncrona mediante hilos
    para no bloquear el event loop. Cuenta con validaciones estrictas de seguridad.
    """

    def __init__(self, settings: SettingsLab):
        """Inicializa el traductor real validando la configuración de seguridad.

        Args:
            settings: Instancia de configuración robusta del laboratorio.
        """
        self.settings = settings
        self._translator = None

        # ! [ALERTA]: Bloqueo preventivo de inicialización en modo simulación estricto
        if self.settings.modo_simulacion or not self.settings.permitir_apis_reales:
            raise RuntimeError(
                "¡BLOQUEO DE SEGURIDAD!: No se permite instanciar el adaptador real "
                "mientras el modo simulación esté habilitado o las APIs reales estén desactivadas."
            )

        # ? [PREGUNTA]: ¿La API Key está presente en el entorno?
        if not self.settings.deepl_api_key:
            raise ValueError(
                "¡ERROR DE CONFIGURACIÓN!: La variable DEEPL_API_KEY no puede estar vacía "
                "para instanciar el adaptador real de traducción."
            )

        # Inicialización del cliente oficial de DeepL
        # * [NOTA]: El cliente maneja reintentos automáticos con backoff exponencial.
        self._translator = deepl.Translator(self.settings.deepl_api_key)

    async def traducir(self, texto: str, origen: str, destino: str) -> str:
        """Traduce una frase mediante la API real de DeepL de forma segura.

        Args:
            texto: Frase original a traducir.
            origen: Código ISO del idioma origen (ej. 'es').
            destino: Código ISO del idioma destino (ej. 'ro').

        Returns:
            Texto traducido por la API de DeepL.

        Raises:
            ValueError: Si el texto excede los límites locales de caracteres.
            RuntimeError: Si ocurre un error de autenticación, cuota o fallo de red en DeepL.
        """
        # 1. Validación de límites locales de caracteres en el laboratorio
        caracteres = len(texto)
        if caracteres > self.settings.max_caracteres_por_frase:
            raise ValueError(
                f"Límite local de caracteres excedido: {caracteres} > {self.settings.max_caracteres_por_frase}"
            )

        # 2. Doble confirmación dinámica antes de la llamada de red
        if self.settings.modo_simulacion or not self.settings.permitir_apis_reales:
            raise RuntimeError(
                "¡BLOQUEO DINÁMICO DE RED!: Intento abortado de llamada real a DeepL "
                "porque las variables de seguridad del entorno fueron modificadas en caliente."
            )

        # 3. Mapeo de códigos de idioma de DeepL (DeepL requiere mayúsculas para algunos destinos)
        # DeepL maneja inglés americano 'EN-US' o británico 'EN-GB', pero acepta 'EN' para traducciones estándar.
        # Para Español es 'ES' y Rumano es 'RO'.
        origen_upper = origen.strip().upper()
        destino_upper = destino.strip().upper()

        # Corrección especial para inglés en DeepL
        if destino_upper == "EN":
            destino_upper = "EN-US"

        # 4. Delegación de la llamada síncrona a un hilo asíncrono secundario
        try:
            # Se ejecuta deepl.Translator.translate_text en un hilo del sistema
            resultado = await asyncio.to_thread(
                self._translator.translate_text,
                texto,
                source_lang=origen_upper,
                target_lang=destino_upper
            )
            return resultado.text

        except deepl.AuthorizationException as e:
            # ! [ALERTA]: Error grave de credenciales
            raise RuntimeError(
                f"Error de Autorización en DeepL: La API Key proporcionada es inválida o expiró. Detalles: {e}"
            ) from e

        except deepl.QuotaExceededException as e:
            # ! [ALERTA]: Límite económico/consumo superado en DeepL
            raise RuntimeError(
                f"Límite Excedido en DeepL: Se superó la cuota mensual de caracteres o el límite de coste. Detalles: {e}"
            ) from e

        except deepl.DeepLException as e:
            # Fallback general de fallos de red o problemas en servidores de DeepL
            raise RuntimeError(
                f"Error General en la API de DeepL durante la traducción. Detalles: {e}"
            ) from e
