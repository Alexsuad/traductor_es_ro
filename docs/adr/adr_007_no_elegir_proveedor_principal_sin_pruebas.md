# ADR-007 — No elegir proveedor principal sin pruebas

## Estado

Aprobado.

## Contexto

Existen múltiples proveedores de IA para transcripción, traducción y voz (DeepL, Google, OpenAI, ElevenLabs, etc.). Elegir uno como definitivo basándose solo en su popularidad o intuición es un riesgo técnico y económico.

## Decisión

*   No se declara ningún proveedor como "principal definitivo" antes de realizar las pruebas exhaustivas en el laboratorio.
*   Todos los proveedores mencionados en la documentación se consideran candidatos en igualdad de condiciones.
*   La selección del proveedor principal para cada componente se basará exclusivamente en:
    *   Calidad (específicamente en rumano).
    *   Latencia (tiempo de respuesta).
    *   Coste por carácter/minuto.
    *   Facilidad de integración técnica.
    *   Estabilidad del servicio.
    *   Disponibilidad de un fallback robusto.

## Consecuencias positivas

*   Decisiones basadas en evidencia y datos reales del proyecto.
*   Optimización del equilibrio calidad-precio-latencia.
*   Prevención de dependencia de un único proveedor que no cumpla las expectativas en el caso de uso real.

## Consecuencias negativas o trade-offs

*   Requiere un esfuerzo mayor en la fase de laboratorio para implementar y probar múltiples adaptadores.

## Alternativas consideradas

*   Elegir OpenAI para todo por simplicidad (descartado por no garantizar la mejor calidad en síntesis de voz o traducción de rumano).

## Documentos relacionados

*   docs/06_proveedores_adaptadores_y_fallbacks.md
*   docs/07_tests_validacion_y_go_no_go.md
