# File: scripts/verificar_entorno.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Script de verificación del entorno, límites y control de seguridad de la Fase 1.
# Rol: Aseguramiento de calidad previo al experimento.
# ──────────────────────────────────────────────────────────────────────

import sys
import os

# Asegurar que el directorio raíz del laboratorio esté en el PATH de Python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src_lab.config.settings_lab import get_settings


def verificar_entorno() -> bool:
    """Verifica de forma determinista la seguridad y dependencias del entorno de la Fase 1."""
    print("=== [INICIO DE VERIFICACIÓN DE ENTORNO FASE 1] ===")

    todo_ok = True

    # 1. Verificar dependencias prohibidas
    dependencias_prohibidas = [
        "fastapi",
        "uvicorn",
        "jinja2",
        "sqlmodel",
        "sqlalchemy",
        "openai",
        "deepl",
        "elevenlabs",
        "google.cloud.translate",
        "gtts",
        "pydub",
        "soundfile"
    ]

    print("\n1. Comprobando ausencia de dependencias prohibidas en runtime...")
    for dep in dependencias_prohibidas:
        try:
            __import__(dep)
            print(f"  [ALERTA] Se detectó la librería prohibida: {dep}")
            todo_ok = False
        except ImportError:
            # Es el comportamiento esperado
            pass
    if todo_ok:
        print("  [OK] No se detectó ninguna dependencia prohibida en runtime.")

    # 2. Cargar variables con Pydantic Settings
    print("\n2. Cargando y validando variables de configuración...")
    try:
        settings = get_settings()
        print("  [OK] Variables de entorno cargadas con éxito.")
        print(f"  - MODO_SIMULACION: {settings.modo_simulacion}")
        print(f"  - PERMITIR_APIS_REALES: {settings.permitir_apis_reales}")
        print(f"  - IDIOMAS_HABILITADOS: {settings.idiomas_habilitados}")
        print(f"  - MAX_CARACTERES_POR_FRASE: {settings.max_caracteres_por_frase}")

        # 3. Validar estado seguro estricto (ADR-002)
        if not settings.modo_simulacion or settings.permitir_apis_reales:
            print("  [ALERTA] ¡ATENCIÓN!: El laboratorio no está configurado en modo simulación seguro.")
            todo_ok = False
        else:
            print("  [OK] Estado seguro confirmado (MODO_SIMULACION=true y PERMITIR_APIS_REALES=false).")

    except Exception as e:
        print(f"  [ERR] Error al cargar o validar variables con Pydantic: {e}")
        todo_ok = False

    # 4. Verificar carpetas físicas obligatorias
    print("\n3. Validando estructura física de carpetas...")
    carpetas = ["resultados", "audios_salida"]
    for carpeta in carpetas:
        ruta = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), carpeta)
        if os.path.exists(ruta):
            print(f"  [OK] Carpeta encontrada: {carpeta}/")
        else:
            print(f"  [AVISO] Carpeta no encontrada. Se creará automáticamente: {carpeta}/")
            os.makedirs(ruta, exist_ok=True)

    print("\n=== [FIN DE VERIFICACIÓN] ===")
    if todo_ok:
        print("RESULTADO: TODO CORRECTO. Listo para ejecutar pruebas de simulación.")
    else:
        print("RESULTADO: FALLO DE VERIFICACIÓN. Revisa las alertas anteriores antes de continuar.")

    return todo_ok


if __name__ == "__main__":
    exito = verificar_entorno()
    sys.exit(0 if exito else 1)
