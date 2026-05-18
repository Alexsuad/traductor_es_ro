# File: scripts/prueba_fake_texto_traduccion_voz.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Script principal para ejecutar el pipeline simulado del laboratorio.
# Rol: Pipeline de pruebas de integración con caché y registro de métricas.
# ──────────────────────────────────────────────────────────────────────

import sys
import os
import asyncio

# Asegurar que el directorio raíz del laboratorio esté en el PATH de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src_lab.config.settings_lab import get_settings
from src_lab.providers_fake.traductor_fake import TraductorFake
from src_lab.providers_fake.voz_fake import VozFake
from src_lab.cache.cache_frases_simple import CacheFrasesSimple
from src_lab.utils.normalizar_texto import normalizar_frase
from src_lab.utils.medir_tiempos import medir_tiempo_async
from src_lab.utils.guardar_resultados import guardar_medicion, guardar_error


async def ejecutar_pipeline(
    texto_original: str,
    origen: str,
    destino: str,
    traductor: TraductorFake,
    generador_voz: VozFake,
    cache: CacheFrasesSimple,
    id_prueba: str
) -> None:
    """Ejecuta el ciclo de vida completo de traducción, síntesis de voz y persistencia."""
    settings = get_settings()
    frase_saneada = normalizar_frase(texto_original)

    # 1. Validación de longitud máxima
    if len(frase_saneada) > settings.max_caracteres_por_frase:
        mensaje_err = f"Longitud de frase excede el límite permitido ({len(frase_saneada)} > {settings.max_caracteres_por_frase})"
        print(f"  [ERR] {mensaje_err}")
        guardar_error(settings, id_prueba, "LímiteExcedido", mensaje_err, "Detener pipeline de forma segura")
        guardar_medicion(
            settings=settings,
            id_prueba=id_prueba,
            direccion=f"{origen.upper()}->{destino.upper()}",
            frase=texto_original,
            modo="SIMULACION",
            traductor="FAKE",
            voz="FAKE",
            transcriptor="NINGUNO",
            cache="NO_APLICA",
            fallback="NINGUNO",
            texto_ms=0.0,
            audio_ms=0.0,
            stt_ms=0.0,
            total_ms=0.0,
            calidad_traduccion=1,
            calidad_voz=1,
            calidad_stt=0,
            estado="FALLIDO",
            error=mensaje_err
        )
        return

    # 2. Consulta a caché
    usado_cache = "NO"
    traduccion = cache.obtener(frase_saneada, origen, destino)

    texto_ms = 0.0
    if traduccion:
        usado_cache = "SI"
        print(f"  [CACHE HIT] Clave encontrada en caché. Traducción: {traduccion}")
    else:
        print("  [CACHE MISS] Traduciendo de forma simulada...")
        try:
            # Medimos latencia de traducción
            traduccion, texto_ms = await medir_tiempo_async(
                traductor.traducir, frase_saneada, origen, destino
            )
            # Guardar en caché
            cache.guardar(frase_saneada, origen, destino, traduccion)
        except Exception as e:
            mensaje_err = f"Error durante la traducción simulada: {e}"
            print(f"  [ERR] {mensaje_err}")
            guardar_error(settings, id_prueba, "ErrorTraduccion", mensaje_err, "Registrar fallo y abortar")
            return

    # 3. Generación de voz
    audio_ms = 0.0
    ruta_audio = ""
    try:
        print("  [TTS] Generando audio de voz de forma simulada...")
        ruta_audio, audio_ms = await medir_tiempo_async(
            generador_voz.generar_voz, traduccion, destino, settings.ruta_audios_salida
        )
        print(f"  [TTS SUCCESS] Audio generado en: {ruta_audio}")
    except Exception as e:
        mensaje_err = f"Error durante la generación de voz simulada: {e}"
        print(f"  [ERR] {mensaje_err}")
        guardar_error(settings, id_prueba, "ErrorTTS", mensaje_err, "Registrar fallo de audio")
        # Anotar medición de texto exitoso con audio fallido
        guardar_medicion(
            settings=settings,
            id_prueba=id_prueba,
            direccion=f"{origen.upper()}->{destino.upper()}",
            frase=frase_saneada,
            modo="SIMULACION",
            traductor="FAKE",
            voz="FAKE",
            transcriptor="NINGUNO",
            cache=usado_cache,
            fallback="NINGUNO",
            texto_ms=texto_ms,
            audio_ms=0.0,
            stt_ms=0.0,
            total_ms=texto_ms,
            calidad_traduccion=4,  # clara y usable
            calidad_voz=1,        # no se entiende/fallido
            calidad_stt=0,
            estado="PARCIAL",
            error=mensaje_err
        )
        return

    # 4. Registrar medición exitosa
    total_ms = round(texto_ms + audio_ms, 2)
    guardar_medicion(
        settings=settings,
        id_prueba=id_prueba,
        direccion=f"{origen.upper()}->{destino.upper()}",
        frase=frase_saneada,
        modo="SIMULACION",
        traductor="FAKE",
        voz="FAKE",
        transcriptor="NINGUNO",
        cache=usado_cache,
        fallback="NINGUNO",
        texto_ms=texto_ms,
        audio_ms=audio_ms,
        stt_ms=0.0,
        total_ms=total_ms,
        calidad_traduccion=5,  # natural y correcta
        calidad_voz=5,        # natural y cómoda
        calidad_stt=0,
        estado="EXITOSO"
    )
    print(f"  [PIPELINE SUCCESS] Total tiempo: {total_ms}ms (Texto: {texto_ms}ms, Audio: {audio_ms}ms)\n")


async def main():
    settings = get_settings()
    print("=== [INICIANDO PRUEBAS FAKE DE INTEGRACIÓN] ===")
    print(f"Modo Simulación: {settings.modo_simulacion}")
    print(f"Permitir APIs Reales: {settings.permitir_apis_reales}")

    # Inicializar componentes del pipeline
    traductor = TraductorFake(settings)
    generador_voz = VozFake(settings)
    cache = CacheFrasesSimple(settings)

    # Catálogo oficial de frases para probar el flujo de ida y vuelta
    frases_prueba = [
        # ES -> RO
        ("Estoy muy feliz de estar aquí con ustedes.", "es", "ro"),
        ("¿Pueden hablar un poco más despacio, por favor?", "es", "ro"),
        ("La comida está muy rica, muchas gracias por recibirme.", "es", "ro"),
        ("Voy a usar el traductor para entenderlos mejor.", "es", "ro"),
        ("Para mí es importante poder comunicarme mejor con ustedes porque somos familia.", "es", "ro"),
        
        # RO -> ES
        ("Ne bucurăm că ești aici cu noi.", "ro", "es"),
        ("Vrei să mănânci ceva sau să bei o cafea?", "ro", "es"),
        ("Nu îți face griji, poți vorbi încet.", "ro", "es"),
        ("Familia este foarte importantă pentru noi.", "ro", "es"),
        ("Dacă nu înțelegi, putem repeta.", "ro", "es"),
        
        # Caso de error: Frase excesivamente larga para validar límites de seguridad
        ("Esta es una frase artificialmente larga diseñada para exceder por completo el límite de caracteres impuesto por la configuración de seguridad para evitar consumos de coste excesivos o de denegación de servicio por payload grande en los adaptadores del traductor rumano familiar del laboratorio.", "es", "ro")
    ]

    # Ejecutar primera tanda (Cache Miss esperados)
    print("\n>>> EJECUTANDO PRIMERA PASADA (SIN CACHÉ)...")
    for i, (frase, orig, dest) in enumerate(frases_prueba, 1):
        id_prueba = f"PRUEBA-1-{i:03d}"
        print(f"[{id_prueba}] {orig.upper()} -> {dest.upper()}: '{frase}'")
        await ejecutar_pipeline(frase, orig, dest, traductor, generador_voz, cache, id_prueba)

    # Ejecutar segunda tanda (Cache Hit esperados en las frases correctas)
    print("\n>>> EJECUTANDO SEGUNDA PASADA (DEBERÍA DAR HIT EN CACHÉ)...")
    for i, (frase, orig, dest) in enumerate(frases_prueba, 1):
        id_prueba = f"PRUEBA-2-{i:03d}"
        print(f"[{id_prueba}] {orig.upper()} -> {dest.upper()}: '{frase}'")
        await ejecutar_pipeline(frase, orig, dest, traductor, generador_voz, cache, id_prueba)

    print("=== [PRUEBAS COMPLETADAS] ===")


if __name__ == "__main__":
    asyncio.run(main())
