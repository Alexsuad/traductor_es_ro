# ADR-003 — Hexagonal solo para proveedores externos

## Estado

Aprobado.

## Contexto

El sistema debe permitir el intercambio de proveedores (traducción, voz, transcripción) sin afectar la lógica de negocio. Sin embargo, aplicar arquitectura hexagonal de forma estricta a todo el sistema puede generar sobreingeniería innecesaria en las fases iniciales de laboratorio.

## Decisión

*   Se aplicará el patrón de arquitectura hexagonal (puertos y adaptadores) exclusivamente a los servicios de proveedores externos intercambiables.
*   Los dominios afectados por esta decisión son:
    *   Traducción.
    *   Voz (TTS).
    *   Transcripción (STT).
*   No se aplicará arquitectura hexagonal inicialmente a la persistencia simple, gestión de métricas locales ni lectura de archivos Markdown/JSON del sistema.
*   Se prioriza la simplicidad y velocidad de desarrollo en el laboratorio para los componentes internos estables.

## Consecuencias positivas

*   Facilidad para añadir o cambiar proveedores de IA con impacto mínimo en el código funcional.
*   Reducción de la sobreingeniería en componentes donde la volatilidad tecnológica es baja.
*   Facilita la creación de adaptadores "fake" para el modo simulación.

## Consecuencias negativas o trade-offs

*   Acoplamiento temporal de la lógica interna a ciertas utilidades de persistencia o sistema de archivos.

## Alternativas consideradas

*   Arquitectura hexagonal completa en todas las capas (descartado por complejidad excesiva para un MVP/Laboratorio).

## Documentos relacionados

*   docs/02_arquitectura_tecnica.md
*   docs/06_proveedores_adaptadores_y_fallbacks.md
