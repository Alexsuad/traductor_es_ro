# File: .agents/rules/03_python_laboratorio.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Definir las reglas de estilo y consistencia de código Python.
# Rol: Capa operativa de desarrollo de Antigravity.
# ──────────────────────────────────────────────────────────────────────

# Reglas de Estilo de Python para el Laboratorio

Este documento regula los estándares técnicos aplicables a la carpeta `traductor_rumano_lab`.

## 1. Tooling Estándar (UV)
*   Toda gestión de dependencias y entornos debe realizarse mediante `uv` (`uv run`, `uv sync`, `uv add`).
*   Está prohibido invocar `pip` directamente a menos que se trate de excepciones debidamente registradas.

## 2. Calidad de Código y Estilo
*   **Ruff:** El formateo y análisis estático debe pasar ruff sin errores (`uv run ruff check .`).
*   **Pytest:** Todas las pruebas automatizadas del laboratorio deben estar en estado verde (`uv run pytest`).
*   **Comentarios:** Los comentarios en el código deben ser profesionales, claros, útiles y preferiblemente estructurados por bloques cuando expliquen la lógica de una sección. No usar comentarios decorativos o que agreguen ruido visual innecesario.
