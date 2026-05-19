# File: .agents/workflows/validar_laboratorio.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Definir el workflow determinista de validación del laboratorio.
# Rol: Workflow operativo de Antigravity.
# ──────────────────────────────────────────────────────────────────────

# Workflow de Validación del Laboratorio

Este flujo procedimental es de ejecución obligatoria para validar que el entorno y los cambios en el laboratorio `traductor_rumano_lab` se mantienen estables.

## Orden Obligatorio de Ejecución

El agente debe situarse en el directorio del laboratorio y ejecutar secuencialmente los siguientes pasos:

1.  **Verificar Entorno:**
    Confirmar que las variables de configuración local, caché y directorios son válidos.
    ```bash
    cd traductor_rumano_lab
    uv run python scripts/verificar_entorno.py
    ```

2.  **Validar Estilo y Calidad (Ruff):**
    Comprobar que el código cumple con las reglas de Ruff.
    ```bash
    uv run ruff check .
    ```

3.  **Ejecutar Suite de Pruebas (Pytest):**
    Asegurar que todas las pruebas pasan sin errores.
    ```bash
    uv run pytest
    ```

## Evidencia y Cierre
Una vez completados los pasos anteriores, se debe registrar el resultado y el estado final de las pruebas en el reporte entregado al usuario.
