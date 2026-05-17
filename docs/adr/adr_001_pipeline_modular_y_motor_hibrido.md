# ADR-001 — Pipeline modular y motor híbrido

## Estado

Aprobado.

## Contexto

El sistema necesita ser flexible para soportar diferentes idiomas y calidades de servicio. Confiar en un único modelo de speech-to-speech directo limita la capacidad de ajuste fino, control de costes y soporte de idiomas menos comunes como el rumano.

## Decisión

*   El sistema no dependerá de un único modelo speech-to-speech.
*   Se usará `MODO_MOTOR=AUTO` para gestionar dinámicamente la ruta de procesamiento.
*   **Camino A (Realtime):** Se usará cuando el idioma de destino esté soportado por modelos de traducción directa de baja latencia.
*   **Camino B (Pipeline modular):** Se usará cuando se requiera más control, mayor calidad o el idioma de destino no esté soportado por el motor realtime.
*   El pipeline modular seguirá la secuencia: transcripción → traducción de texto → síntesis de voz (TTS).
*   La arquitectura debe permitir cambiar proveedores en cada paso del pipeline sin afectar el núcleo del sistema.

## Consecuencias positivas

*   Máxima flexibilidad para optimizar calidad, coste y latencia por idioma.
*   Capacidad de fallback inmediato si un proveedor falla.
*   Independencia de modelos específicos "todo en uno".

## Consecuencias negativas o trade-offs

*   Mayor complejidad en la orquestación del pipeline modular.
*   Latencia acumulada potencialmente mayor en el Camino B frente a modelos integrados.

## Alternativas consideradas

*   Uso exclusivo de modelos speech-to-speech (descartado por falta de soporte robusto para rumano y falta de control granular).

## Documentos relacionados

*   docs/02_arquitectura_tecnica.md
*   docs/06_proveedores_adaptadores_y_fallbacks.md
