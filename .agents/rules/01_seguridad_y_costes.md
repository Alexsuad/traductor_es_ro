# File: .agents/rules/01_seguridad_y_costes.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Establecer las reglas de control presupuestario y de seguridad para la IA.
# Rol: Capa operativa de seguridad y costes de Antigravity.
# ──────────────────────────────────────────────────────────────────────

# Reglas de Seguridad y Costes para Antigravity

Este documento rige las restricciones de seguridad y costes en el repositorio para evitar gastos accidentales y filtraciones de credenciales.

## 1. Reglas de Control de Costes and APIs
*   **Modo Simulación:** La variable `MODO_SIMULACION=true` debe estar activa por defecto.
*   **Llamadas Reales:** La variable `PERMITIR_APIS_REALES=false` impide cualquier consumo de API de producción. Solo se activará tras validación y consentimiento explícito en tareas puntuales.
*   **Límites Diarios:** Antes de realizar llamadas reales, consulte y respete los límites de coste y caracteres detallados en la fuente oficial: [04_seguridad_privacidad_y_costes.md](../../docs/04_seguridad_privacidad_y_costes.md).

## 2. Gestión de Secretos y Privacidad
*   **Filtros de Secretos:** Nunca escribir API Keys, tokens ni credenciales en el código fuente, la documentación viva, comentarios ni logs.
*   **Archivo .env:** El archivo local `.env` nunca debe versionarse ni agregarse a Git. Toda plantilla de variables seguras se mantiene en `.env.example`.
*   **Conservación:** No almacenar audios familiares reales ni datos personales de prueba en el repositorio.
