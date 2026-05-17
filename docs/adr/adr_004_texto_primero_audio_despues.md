# ADR-004 — Texto primero, audio después

## Estado

Aprobado.

## Contexto

En una conversación familiar en tiempo real, la latencia es el principal factor de fricción. Esperar a que el audio esté completamente generado y descargado para mostrar el resultado puede romper el ritmo de la interacción.

## Decisión

*   El sistema mostrará la traducción escrita inmediatamente después de ser procesada, sin esperar a la generación o reproducción del audio.
*   La síntesis de voz y su posterior reproducción se tratarán como un proceso de apoyo, no como un paso bloqueante.
*   En caso de fallo en el servicio de voz, el sistema debe mantener su utilidad básica mostrando el texto traducido.
*   Esta estrategia busca reducir la latencia percibida por el usuario.

## Consecuencias positivas

*   Mejor experiencia de usuario (UX) al recibir feedback visual inmediato.
*   Robustez ante fallos en los servicios de síntesis de voz (TTS).
*   Reducción de la latencia percibida en la conversación familiar.

## Consecuencias negativas o trade-offs

*   Desincronización visual-auditiva si el proceso de audio es significativamente más lento que el de texto.

## Alternativas consideradas

*   Esperar a tener el audio para mostrar todo el resultado (descartado por generar una percepción de lentitud y poca fluidez).

## Documentos relacionados

*   docs/01_contexto_y_objetivo_funcional.md
*   docs/02_arquitectura_tecnica.md
*   docs/05_frontend_y_experiencia_usuario.md
