# File: AGENTS.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Definir la instrucción operativa común para agentes autónomos de IA.
# Rol: Gobierno agéntico común del repositorio.
# ──────────────────────────────────────────────────────────────────────

# Instrucción Operativa Común para Agentes de IA

Este documento regula el comportamiento, las responsabilidades y la interacción de los agentes autónomos de Inteligencia Artificial (IA) en este repositorio. Su cumplimiento es obligatorio para cualquier agente que opere en este proyecto.

## 1. Estado Actual del Proyecto
El proyecto se encuentra en el siguiente estado normativo y operativo:
*   **Planeación documental:** Cerrada.
*   **ADR (Decisiones de Arquitectura):** ADR-001 a ADR-009 cerrados.
*   **Fase 1 (Entorno y Estructura Básica):** Cerrada.
*   **Fase 2 (Traducción con Proveedor Ficticio/DeepL):** Cerrada técnicamente.
*   **Fase 3 (Traductor Real Integrado):** No iniciada.

## 2. Fuentes de Verdad Oficiales
Los agentes deben consultar únicamente los siguientes documentos normativos y nunca basarse en archivos generados temporalmente:
*   [00_indice_y_mapa_documental.md](docs/00_indice_y_mapa_documental.md) — Índice maestro de documentación.
*   [04_seguridad_privacidad_y_costes.md](docs/04_seguridad_privacidad_y_costes.md) — Políticas de seguridad, tokens y presupuestos de APIs.
*   [07_tests_validacion_y_go_no_go.md](docs/07_tests_validacion_y_go_no_go.md) — Protocolo de validación y criterios de aceptación.
*   [08_plan_implementacion_desarrolladores.md](docs/08_plan_implementacion_desarrolladores.md) — Hoja de ruta técnica de las fases.
*   [09_modelo_operativo_chats_y_equipos.md](docs/09_modelo_operativo_chats_y_equipos.md) — Modelo organizativo y de gobernanza humana.
*   Carpeta de Decisiones de Arquitectura: [docs/adr/](docs/adr/)

## 3. Reglas Operativas Comunes (Guardrails para todos los Agentes)
Cualquier agente que actúe en el repositorio debe respetar de forma estricta los siguientes límites:
1.  **Protección de Secretos:** No modificar el archivo `.env` ni añadir claves reales o tokens en el código, comentarios, documentación o logs. Toda plantilla debe actualizarse únicamente en `.env.example`.
2.  **Consumo Seguro de APIs:** Prohibido realizar llamadas a APIs reales sin autorización y consentimiento explícito del usuario.
3.  **Control de Dependencias:** No instalar ni registrar nuevas librerías o dependencias sin aprobación del usuario.
4.  **Control de Cambios:** No realizar commits, push ni despliegues (deploy) sin autorización explícita previa.
5.  **Delimitación del Alcance:** No modificar archivos que estén fuera del alcance aprobado para la tarea actual.
6.  **Control de Fases:** No declarar una fase como completada ni avanzar a la siguiente sin antes generar y depositar las evidencias correspondientes (logs de verificación, pruebas superadas) en la carpeta `/output`.
7.  **No Autorreferencialidad:** No utilizar archivos generados temporalmente o logs como fuentes normativas para tomar decisiones técnicas o de arquitectura.

## 4. Validación Base del Laboratorio
Si se realiza cualquier modificación sobre el código de la carpeta `traductor_rumano_lab`, es obligatorio situarse en ese directorio y ejecutar la suite completa de validación determinista en el siguiente orden estricto:
```bash
cd traductor_rumano_lab
uv run python scripts/verificar_entorno.py
uv run ruff check .
uv run pytest
```
Cualquier fallo en estos pasos bloquea el avance de la tarea inmediatamente.

## 5. Coordinación de Agentes y Roles
*   **Antigravity:** Lidera la fase de planificación previa de tareas, auditorías de calidad documental, control de fase, generación de reportes y creación de artifacts.
*   **Codex:** Lidera la implementación técnica del código y diseño de pruebas/adaptadores, operando únicamente cuando existe una tarea específica previamente planificada y aprobada por Antigravity.
*   **Regla de Concurrencia:** Los agentes nunca deben operar sobre los mismos archivos simultáneamente para evitar problemas de sincronización de contexto y conflictos en el historial de Git.
