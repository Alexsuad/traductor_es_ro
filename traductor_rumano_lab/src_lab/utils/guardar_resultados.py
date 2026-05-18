# File: src_lab/utils/guardar_resultados.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Registro determinista de mediciones y errores en archivos Markdown.
# Rol: Gestión de salida y reporte de calidad (QA).
# ──────────────────────────────────────────────────────────────────────

import os
from datetime import datetime
from src_lab.config.settings_lab import SettingsLab


def guardar_medicion(
    settings: SettingsLab,
    id_prueba: str,
    direccion: str,
    frase: str,
    modo: str,
    traductor: str,
    voz: str,
    transcriptor: str,
    cache: str,
    fallback: str,
    texto_ms: float,
    audio_ms: float,
    stt_ms: float,
    total_ms: float,
    calidad_traduccion: int,
    calidad_voz: int,
    calidad_stt: int,
    estado: str,
    error: str = ""
) -> None:
    """Anexa una fila de medición formateada al archivo Markdown mediciones_fase_0.md.

    Garantiza la consistencia e integridad del histórico en la carpeta resultados.
    """
    ruta_archivo = os.path.join(settings.ruta_resultados, "mediciones_fase_0.md")

    # Crear directorio si no existe
    os.makedirs(settings.ruta_resultados, exist_ok=True)

    # Crear archivo con cabecera si no existe
    if not os.path.exists(ruta_archivo):
        cabecera = (
            "# Reporte de Mediciones del Laboratorio — Fase 0\n\n"
            "## Tabla de Mediciones\n\n"
            "| id_prueba | dirección | frase | modo | traductor | voz | transcriptor | cache | fallback | texto_ms | audio_ms | stt_ms | total_ms | calidad_traduccion | calidad_voz | calidad_stt | estado | error |\n"
            "|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|\n"
        )
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(cabecera)

    # Limpiar posibles saltos de línea del texto para no romper la tabla MD
    frase_limpia = frase.replace("\n", " ").replace("|", "\\|")
    error_limpio = error.replace("\n", " ").replace("|", "\\|") if error else ""

    fila = (
        f"| {id_prueba} | {direccion} | {frase_limpia} | {modo} | {traductor} | {voz} | {transcriptor} | "
        f"{cache} | {fallback} | {texto_ms} | {audio_ms} | {stt_ms} | {total_ms} | "
        f"{calidad_traduccion} | {calidad_voz} | {calidad_stt} | {estado} | {error_limpio} |\n"
    )

    with open(ruta_archivo, "a", encoding="utf-8") as f:
        f.write(fila)


def guardar_error(
    settings: SettingsLab,
    id_prueba: str,
    error_tipo: str,
    mensaje_error: str,
    accion_tomada: str
) -> None:
    """Anexa una fila de error formateada al archivo Markdown errores_fase_0.md."""
    ruta_archivo = os.path.join(settings.ruta_resultados, "errores_fase_0.md")

    # Crear directorio si no existe
    os.makedirs(settings.ruta_resultados, exist_ok=True)

    # Crear archivo con cabecera si no existe
    if not os.path.exists(ruta_archivo):
        cabecera = (
            "# Reporte de Errores y Excepciones — Fase 0\n\n"
            "## Historial de Errores\n\n"
            "| timestamp | id_prueba | error_tipo | mensaje_error | accion_tomada |\n"
            "|---|---|---|---|---|\n"
        )
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(cabecera)

    timestamp = datetime.now().isoformat()
    mensaje_limpio = mensaje_error.replace("\n", " ").replace("|", "\\|")
    accion_limpia = accion_tomada.replace("\n", " ").replace("|", "\\|")

    fila = f"| {timestamp} | {id_prueba} | {error_tipo} | {mensaje_limpio} | {accion_limpia} |\n"

    with open(ruta_archivo, "a", encoding="utf-8") as f:
        f.write(fila)
