# File: docs/adr/adr_009_control_de_turnos_y_simultaneidad_experimental.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Registrar la decisión de utilizar una conversación por turnos como modo principal en el MVP para evitar solapamientos de audio.
# Rol: Registro de Decisión Arquitectónica (ADR)
# ──────────────────────────────────────────────────────────────────────

# ADR-009 — Control de turnos y simultaneidad experimental

## Estado

Aprobado

## Contexto

Durante las pruebas exploratorias con OpenAI Playground y modelos de voz en tiempo real, se detectó que la traducción simultánea puede provocar solapamiento de voces.

Cuando una persona habla y la traducción empieza a reproducirse antes de que termine su intervención, se generan problemas de experiencia familiar:

- la voz traducida puede sonar encima de la voz original;
- la otra persona puede no saber a quién prestar atención;
- el micrófono puede captar la traducción generada por el propio sistema;
- la conversación puede sentirse menos natural;
- el uso familiar cara a cara puede volverse incómodo.

La simultaneidad real puede ser técnicamente atractiva, pero no necesariamente es la mejor interacción para una conversación familiar presencial.

## Decisión

El modo principal del MVP será una conversación por turnos, usando interacción tipo push-to-talk o entrada controlada.

La app debe priorizar este flujo:

```text
persona habla
↓
termina su intervención
↓
el sistema traduce
↓
muestra texto
↓
reproduce audio si está disponible
```

Se definen tres modos de conversación:

```text
1. Por turnos / push-to-talk:
   Modo principal del MVP.

2. Semi-simultáneo con pausa:
   Modo candidato para pruebas posteriores, basado en detección de pausas claras.

3. Simultáneo real:
   Modo experimental de laboratorio, no recomendado como flujo principal familiar.
```

Regla principal:

```text
La app no debe reproducir audio traducido mientras la persona todavía está hablando,
salvo que el modo simultáneo experimental esté activado explícitamente.
```

## Consecuencias positivas

* Reduce solapamiento de voces.
* Mejora la claridad de la conversación familiar.
* Evita que la traducción compita con la voz original.
* Reduce riesgo de que el micrófono capture el audio generado por la propia app.
* Mantiene bajo control el coste y el procesamiento.
* Refuerza la decisión de texto primero y audio después.
* Permite probar simultaneidad sin convertirla en el corazón del proyecto.

## Consecuencias negativas o trade-offs

* La experiencia puede ser menos “impresionante” que una traducción simultánea pura.
* La conversación puede sentirse más pausada.
* El usuario debe respetar turnos o usar un botón de grabación.
* El modo simultáneo requerirá pruebas separadas para validar si realmente aporta valor.

## Alternativas consideradas

### Alternativa 1 — Traducción simultánea como modo principal

Se descartó como modo principal porque puede generar solapamiento, confusión de atención e incomodidad social en conversaciones familiares cara a cara.

### Alternativa 2 — Solo texto sin audio

Se mantiene como fallback, pero no como única experiencia deseada porque el audio puede ayudar en situaciones familiares si funciona con latencia aceptable.

### Alternativa 3 — Conversación por turnos

Se adopta como modo principal porque es más simple, más controlable y más adecuado para el contexto familiar inicial.

## Documentos relacionados

* docs/01_contexto_y_objetivo_funcional.md
* docs/02_arquitectura_tecnica.md
* docs/05_frontend_y_experiencia_usuario.md
* docs/07_tests_validacion_y_go_no_go.md
* docs/08_plan_implementacion_desarrolladores.md
* docs/adr/adr_004_texto_primero_audio_despues.md
