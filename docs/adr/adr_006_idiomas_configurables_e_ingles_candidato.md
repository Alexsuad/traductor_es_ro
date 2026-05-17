# ADR-006 — Idiomas configurables e inglés candidato

## Estado

Aprobado.

## Contexto

Aunque el objetivo principal es la comunicación Español ↔ Rumano, el sistema debe ser lo suficientemente flexible para soportar otros idiomas y utilizar idiomas puente si la calidad de la traducción directa es insuficiente.

## Decisión

*   El sistema se diseñará como un traductor familiar configurable por idiomas de entrada y salida.
*   Los idiomas habilitados inicialmente para las pruebas serán:
    *   `es` (Español)
    *   `ro` (Rumano)
    *   `en` (Inglés)
*   El inglés se incluye como ruta candidata para comparar calidades y como posible idioma puente en el pipeline de traducción.
*   Ninguna ruta de traducción se declara como "ganadora" por defecto; la selección final se basará en los resultados de las pruebas del laboratorio.

## Consecuencias positivas

*   Arquitectura escalable a cualquier par de idiomas soportados por los proveedores.
*   Capacidad de usar el inglés como referencia de calidad y latencia.

## Consecuencias negativas o trade-offs

*   Añadir el inglés como idioma configurable aumenta ligeramente la complejidad de las matrices de pruebas en el laboratorio.

## Alternativas consideradas

*   Limitación estricta a ES ↔ RO (descartado por falta de flexibilidad y visión de futuro).

## Documentos relacionados

*   docs/01_contexto_y_objetivo_funcional.md
*   docs/02_arquitectura_tecnica.md
*   docs/04_seguridad_privacidad_y_costes.md
*   docs/07_tests_validacion_y_go_no_go.md
