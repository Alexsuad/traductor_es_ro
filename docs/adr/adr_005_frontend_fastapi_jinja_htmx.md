# ADR-005 — Frontend FastAPI + Jinja2 + HTMX

## Estado

Aprobado.

## Contexto

El proyecto requiere una interfaz web sencilla, rápida de desarrollar y fácil de mantener para un MVP, minimizando la complejidad del estado en el cliente y la necesidad de frameworks pesados de JavaScript.

## Decisión

*   El MVP web utilizará el stack **FastAPI + Jinja2 + HTMX**.
*   El uso de JavaScript se limitará exclusivamente a la integración con las APIs del navegador para el uso del micrófono (MediaRecorder API), grabación y reproducción de audio.
*   No se utilizarán frameworks de SPA (Single Page Application) como React, Vue o Angular en la fase inicial.
*   Se descarta el uso de Reflex para el MVP inicial por considerarse sobreingeniería para el alcance actual.
*   Flet se mantiene como una opción secundaria para futuras versiones multiplataforma si fuera necesario.

## Consecuencias positivas

*   Desarrollo rápido centrado en Python.
*   Baja complejidad en la gestión del estado del frontend.
*   Carga rápida de la página y simplicidad en la comunicación cliente-servidor.

## Consecuencias negativas o trade-offs

*   Menor capacidad para interfaces extremadamente dinámicas o complejas sin recurrir a JavaScript adicional.

## Alternativas consideradas

*   Reflex (descartado por complejidad).
*   Flet (mantenido como opción futura).
*   React/Vue (descartados por sobreingeniería para un MVP familiar).

## Documentos relacionados

*   docs/05_frontend_y_experiencia_usuario.md
*   docs/08_plan_implementacion_desarrolladores.md
