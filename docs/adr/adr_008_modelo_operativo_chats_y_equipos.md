# ADR-008 — Modelo operativo de chats y equipos

## Estado

Aprobado.

## Contexto

Para evitar contraórdenes y cambios contradictorios en un entorno de desarrollo asistido por IA, es necesario definir claramente las responsabilidades y permisos de cada equipo humano y su interacción con las herramientas de desarrollo.

## Decisión

*   El proyecto se organiza en equipos/chats especializados (Arquitectura, Arnés, Backend, Frontend, Testing, Calidad y Seguridad, Experto de Usuario).
*   Este modelo operativo define la interacción humana y no la arquitectura interna de agentes de Antigravity/Codex.
*   Los equipos operativos (Arquitectura, Arnés, Backend, Frontend, Testing, Calidad y Seguridad) pueden dar instrucciones técnicas a Antigravity/Codex solo dentro de su dominio de responsabilidad.
*   El **Equipo Experto de Usuario / Cliente** no tiene permiso para dar instrucciones técnicas directas a la IA; su rol es auditar funcionalmente y reportar hallazgos a los equipos responsables.
*   El **Equipo Arnés de Desarrollo Agéntico** es el único autorizado para decidir sobre la creación de archivos de configuración agéntica (`AGENTS.md`, `GEMINI.md`, `SKILL.md`, etc.).
*   La regla de oro es evitar contraórdenes mediante la delimitación estricta de dominios.

## Consecuencias positivas

*   Orden y trazabilidad en las instrucciones dadas a la IA.
*   Prevención de conflictos técnicos causados por intervenciones de equipos ajenos al dominio.
*   Protección de la integridad de la arquitectura por parte del equipo dueño.

## Consecuencias negativas o trade-offs

*   Requiere un flujo de comunicación más formal para reportar hallazgos transversales.

## Alternativas consideradas

*   Modelo de "todos mandan sobre todo" (descartado por generar caos y deudas técnicas rápidas).

## Documentos relacionados

*   docs/09_modelo_operativo_chats_y_equipos.md
*   docs/00_indice_y_mapa_documental.md
