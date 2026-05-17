# File: docs/05_frontend_y_experiencia_usuario.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Definir la interfaz y experiencia de usuario del traductor.
# Rol: Documentación de UI/UX y flujo de interacción.
# ──────────────────────────────────────────────────────────────────────
# 05 — Frontend y experiencia de usuario

## Proyecto

**Traductor Familiar Español-Rumano**

## Propósito de este documento

Este documento define cómo debe ser la experiencia de uso del traductor familiar español-rumano desde el punto de vista de la interfaz, la interacción y el flujo de usuario.

Su objetivo es asegurar que la herramienta sea simple, clara y útil en una situación familiar real, especialmente desde un teléfono móvil.

No describe en detalle proveedores externos, seguridad, costes, arquitectura completa ni plan de implementación. Esos temas pertenecen a otros documentos.

---

# 1. Pregunta principal que responde este documento

```text
¿Cómo debe interactuar el usuario con la herramienta para que la traducción sea útil y no interrumpa la conversación familiar?
```

---

# 2. Principio UX principal

La interfaz debe seguir este principio:

```text
Menos pasos, más claridad y menor interrupción de la conversación.
```

La herramienta debe ayudar a conversar, no convertirse en el centro de la conversación.

Por eso la experiencia debe ser:

```text
simple
móvil
rápida
visual
sin distracciones
con botones grandes
con texto claro
con errores comprensibles
```

---

# 3. Decisión frontend para el MVP web

## 3.1. Stack recomendado

Para el MVP web se usará:

```text
FastAPI
Jinja2
HTMX
HTML
CSS
JavaScript mínimo para micrófono/audio
```

## 3.2. Motivo

Esta decisión permite mantener la mayor parte de la lógica en Python y evitar un frontend pesado.

HTMX permite actualizar partes de la pantalla con fragmentos HTML generados desde el backend.

Jinja2 permite construir esos fragmentos desde plantillas simples.

JavaScript se reserva solo para funciones que dependen directamente del navegador.

## 3.3. Alternativas descartadas para MVP

```text
React:
se descarta por complejidad innecesaria para una interfaz simple.

Vue:
se descarta por el mismo motivo.

Reflex:
se descarta para MVP porque sería demasiado para la primera versión.

Flet:
se descarta para MVP porque implicaría pensar en app nativa, empaquetado y permisos móviles antes de validar utilidad.

JavaScript puro para toda la UI:
se evita para no duplicar estado y lógica visual en el cliente.
```

Estas alternativas pueden reevaluarse en fases futuras si el proyecto crece.

---

# 4. Reparto de responsabilidades frontend

## 4.1. Responsabilidad de HTMX + Jinja2

HTMX y Jinja2 deben encargarse de:

```text
mostrar traducciones
actualizar bloques de resultados
mostrar errores
mostrar mensajes de carga
insertar contenido sin recargar toda la página
actualizar historial visual simple si existe en fases futuras
```

## 4.2. Responsabilidad de JavaScript

JavaScript debe limitarse a:

```text
pedir permiso de micrófono
grabar audio
detener grabación
preparar archivo de audio
enviar audio al backend si aplica
reproducir audio devuelto
controlar eventos básicos del botón de grabación
```

## 4.3. Regla obligatoria

```text
No usar JavaScript para manejar toda la lógica de estado visual si puede resolverse con HTMX + fragmentos HTML.
```

---

# 5. Interfaz principal: Dos vistas

La interfaz se divide en dos niveles de profundidad para proteger la simplicidad familiar.

## 5.1. Pantalla Familiar (Vista Principal)
Diseño minimalista con botones gigantes para uso inmediato.

*   **Botón: Hablo yo (Español → Rumano)**
*   **Botón: Me hablan ellos (Rumano → Español)**
*   **Área de resultados:** Texto grande y reproducible.
*   **Estado:** Indicadores visuales simples (Escuchando, Traduciendo, Hablando).

## 5.2. Configuración Técnica (Vista Oculta/Configurable)
Para ajuste del motor y validación de rutas candidatas.

*   **Selector de Motor:**
    *   `AUTO` (Recomendado)
    *   `Translate` (Realtime)
    *   `Whisper Pipeline` (Modular)
    *   `Combined` (Experimental)
*   **Selector de Idiomas:** Habilitar/Deshabilitar rutas candidatas (Inglés).
*   **Límites de Uso:** Visualización de minutos/llamadas restantes.

---

# 6. Flujo principal: español → rumano

## 6.1. Caso texto

```text
Usuario introduce o selecciona una frase en español
↓
Pulsa traducir a rumano
↓
El sistema muestra estado de carga
↓
El sistema muestra texto rumano
↓
Si hay audio, permite reproducir audio rumano
```

## 6.2. Caso voz

```text
Usuario pulsa o mantiene botón de hablar
↓
El navegador solicita permiso de micrófono si es necesario
↓
Se graba audio
↓
El audio se envía al backend
↓
El sistema muestra texto detectado, si aplica
↓
El sistema muestra traducción rumana
↓
El sistema reproduce o permite reproducir audio rumano, si existe
```

---

# 7. Flujo principal: rumano → español

## 7.1. Caso texto

```text
Usuario introduce o selecciona una frase en rumano
↓
Pulsa traducir a español
↓
El sistema muestra estado de carga
↓
El sistema muestra texto español
↓
Si hay audio, permite reproducir audio español
```

## 7.2. Caso voz

```text
Familiar habla en rumano usando el modo correspondiente
↓
Se graba audio
↓
El audio se envía al backend
↓
El sistema muestra texto rumano detectado, si aplica
↓
El sistema muestra traducción española
↓
El sistema reproduce o permite reproducir audio español, si existe
```

---

# 8. Dirección explícita de traducción

La interfaz debe evitar depender de autodetección de idioma en el MVP.

Debe haber dos acciones claras:

```text
Español → Rumano
Rumano → Español
```

## Motivo

La dirección explícita reduce errores y hace más predecible el comportamiento.

Esto es especialmente importante en conversaciones familiares donde una mala traducción puede generar confusión.

---

# 9. Texto primero, audio después

## 9.1. Regla UX

La traducción escrita debe aparecer antes de esperar audio.

```text
Primero texto.
Después audio, si llega.
```

## 9.2. Motivo

La generación de audio puede tardar más que la traducción escrita.

El usuario debe poder leer la traducción aunque el audio todavía no esté disponible.

## 9.3. Estados posibles

```text
Traduciendo...
Traducción lista.
Generando audio...
Audio listo.
Audio no disponible, se muestra solo texto.
```

---

# 10. Push-to-talk como interacción inicial

## 10.1. Decisión

La primera versión con voz debe usar interacción tipo push-to-talk.

Ejemplo:

```text
Mantener pulsado para hablar.
Soltar para enviar.
```

O, si es más simple para el navegador:

```text
Tocar para iniciar grabación.
Tocar para detener y enviar.
```

## 10.2. Motivo

Push-to-talk evita:

```text
ruido constante
consumo innecesario
capturas accidentales
costes imprevistos
confusión entre idiomas
```

## 10.3. Regla

No usar escucha continua en el MVP.

---

# 11. Diseño móvil

La interfaz debe priorizar uso desde teléfono.

## 11.1. Requisitos visuales

```text
botones grandes
texto legible
alto contraste
espaciado cómodo
sin menús complejos
sin paneles innecesarios
```

## 11.2. Requisitos de interacción

```text
acciones claras
pocos toques
feedback inmediato
mensajes breves
posibilidad de repetir audio
```

## 11.3. Requisitos de contexto familiar

La herramienta puede usarse en una mesa, sala o conversación informal.

Debe evitar una interfaz que parezca técnica o intimidante.

---

# 12. Estados de la interfaz

La interfaz debe contemplar estados claros.

## 12.1. Estado inicial

```text
Listo para traducir.
```

## 12.2. Grabando

```text
Grabando... habla ahora.
```

## 12.3. Procesando

```text
Procesando traducción...
```

## 12.4. Traducción lista

```text
Traducción lista.
```

## 12.5. Audio en proceso

```text
Generando audio...
```

## 12.6. Audio no disponible

```text
No se pudo generar audio. Puedes leer la traducción.
```

## 12.7. Error recuperable

```text
No se pudo completar la acción. Intenta con una frase más corta.
```

---

# 13. Mensajes de error comprensibles

Los errores no deben mostrar detalles técnicos al usuario final.

## 13.1. Ejemplos correctos

```text
La conexión tardó demasiado. Intenta de nuevo.

No se pudo generar audio, pero la traducción escrita está disponible.

La frase es demasiado larga para esta prueba. Usa una frase más corta.

No se pudo acceder al micrófono. Revisa los permisos del navegador.
```

## 13.2. Ejemplos incorrectos

```text
HTTPXTimeoutException
ProviderAuthError
Traceback completo
API key inválida: sk-...
```

Los detalles técnicos deben ir al registro seguro, no a la interfaz.

---

# 14. Frases frecuentes y acceso rápido

En una fase posterior del MVP se puede incluir una sección de frases frecuentes.

Ejemplos:

```text
Hola.
Gracias.
¿Puedes repetir, por favor?
¿Puedes hablar más despacio?
La comida está muy rica.
Estoy feliz de estar aquí.
```

## 14.1. Regla

Las frases frecuentes no deben convertirse en una funcionalidad compleja al inicio.

Primero deben validarse como parte del laboratorio y caché simple.

---

# 15. Accesibilidad básica

La interfaz debe considerar:

```text
tamaño de texto legible
botones grandes
evitar depender solo del color
mensajes claros
reproducción de audio opcional
texto siempre visible
```

El texto traducido siempre debe estar disponible aunque exista audio.

---

# 16. Privacidad visible para el usuario

La interfaz debe evitar generar miedo o confusión.

Cuando aplique, se puede mostrar un mensaje simple:

```text
Esta herramienta no guarda conversaciones familiares por defecto.
```

No se debe mostrar un texto largo legalista en la pantalla principal del MVP.

Los detalles completos de privacidad pertenecen a:

```text
04_seguridad_privacidad_y_costes.md
```

---

# 17. Qué queda fuera del frontend MVP

No se incluye en el frontend inicial:

```text
login
registro de usuarios
dashboard
historial avanzado
configuración compleja
múltiples idiomas
modo reunión
subida de documentos
panel de administración
app nativa instalable
notificaciones push
```

---

# 18. Criterios UX de éxito

La experiencia se considera adecuada si:

```text
[ ] El usuario entiende qué botón usar.
[ ] La dirección español → rumano es clara.
[ ] La dirección rumano → español es clara.
[ ] El texto traducido aparece de forma visible.
[ ] El audio no bloquea la lectura.
[ ] Los errores son comprensibles.
[ ] La interfaz funciona bien desde móvil.
[ ] La herramienta no interrumpe excesivamente la conversación.
```

---

# 19. Criterios UX de fracaso

La experiencia se considera fallida si:

```text
[ ] El usuario no sabe qué botón usar.
[ ] La herramienta tarda sin mostrar feedback.
[ ] La traducción queda oculta o poco visible.
[ ] El audio bloquea todo el flujo.
[ ] Los errores son técnicos o confusos.
[ ] Se requieren demasiados pasos.
[ ] La interfaz parece más complicada que usar un traductor existente.
```

---

# 20. Relación con otros documentos

Para contexto y objetivo funcional:

```text
01_contexto_y_objetivo_funcional.md
```

Para arquitectura técnica:

```text
02_arquitectura_tecnica.md
```

Para laboratorio de validación:

```text
03_plan_laboratorio_fase_0.md
```

Para seguridad, privacidad y costes:

```text
04_seguridad_privacidad_y_costes.md
```

Para proveedores y fallbacks:

```text
06_proveedores_adaptadores_y_fallbacks.md
```

Para pruebas y GO/NO-GO:

```text
07_tests_validacion_y_go_no_go.md
```

Para implementación por fases:

```text
08_plan_implementacion_desarrolladores.md
```

---

# 21. Criterio de calidad de este documento

Este documento se considera correcto si:

```text
[ ] Define la experiencia principal del usuario.
[ ] Define la decisión FastAPI + Jinja2 + HTMX.
[ ] Limita JavaScript a micrófono/audio.
[ ] Define dirección explícita de traducción.
[ ] Define texto primero y audio después.
[ ] Define push-to-talk.
[ ] Define estados de interfaz.
[ ] Define mensajes de error comprensibles.
[ ] Define criterios UX de éxito y fracaso.
[ ] No repite proveedores en detalle.
[ ] No repite costes detallados.
[ ] No repite plan de implementación completo.
```

---

# 22. Estado

```text
Estado: Aprobado documentalmente para cierre de planeación.
```

