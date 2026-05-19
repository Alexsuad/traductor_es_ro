# File: .agents/rules/02_fases_y_alcance.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Controlar el orden secuencial del desarrollo del proyecto.
# Rol: Capa operativa de fases y alcance de Antigravity.
# ──────────────────────────────────────────────────────────────────────

# Reglas de Fases y Alcance

Este documento asegura que el desarrollo del traductor se ejecute de forma ordenada y bajo el principio de "vamos despacio".

## 1. Regla de Oro de las Fases
*   Ningún agente debe iniciar el desarrollo de una fase sin haber verificado y cerrado la anterior.
*   La evidencia de cierre de cada fase (logs de pruebas, reportes de calidad) debe ser depositada en la carpeta `/output` para su validación.
*   Consulte la hoja de ruta y la lista de dependencias permitidas/prohibidas en la fuente oficial: [08_plan_implementacion_desarrolladores.md](../../docs/08_plan_implementacion_desarrolladores.md).

## 2. Incompatibilidad de Dependencias
*   No se permite la instalación de dependencias no autorizadas para la fase actual (ej. framework web, ElevenLabs en fases iniciales).
*   Cualquier desviación requiere justificación técnica y registro en un ADR si afecta la arquitectura.
