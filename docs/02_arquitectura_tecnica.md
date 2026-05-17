# 02 — Arquitectura técnica

## Proyecto

**Traductor Familiar Español-Rumano**

## Propósito de este documento

Este documento define la arquitectura técnica del sistema: cómo se organizará internamente, qué flujo principal seguirá, qué componentes tendrá, qué decisiones arquitectónicas se aceptan y qué límites técnicos deben respetarse.

No contiene el plan completo de pruebas, el detalle de costes, la experiencia visual del frontend ni el plan secuencial para desarrolladores. Esos temas se documentan en archivos separados para evitar duplicidad.

---

# 1. Pregunta principal que responde este documento

```text
¿Cómo estará diseñado técnicamente el sistema para traducir español ↔ rumano de forma controlada, modular y segura?
```

---

# 2. Principio arquitectónico principal

El sistema se diseñará bajo un principio LEAN:

```text
Construir primero el flujo mínimo validable y evitar arquitectura innecesaria antes de comprobar utilidad real.
```

La arquitectura debe permitir:

```text
- probar sin coste usando adaptadores fake;
- activar proveedores reales solo con límites;
- cambiar proveedores sin reescribir la lógica principal;
- mostrar texto traducido antes que audio;
- degradar funcionalmente si una API externa falla;
- mantener el sistema simple durante el laboratorio inicial.
```

---

# 3. Decisión técnica principal: Motor Híbrido

## 3.1. Modos de ejecución (MODO_MOTOR)

El sistema debe soportar una lógica de motor configurable (`MODO_MOTOR=AUTO` por defecto) que decida el camino de ejecución según el idioma de destino y el nivel de control requerido.

### Camino A: Translate Realtime
*   **Uso:** Cuando el idioma de destino está soportado por servicios de traducción en tiempo real de alta fidelidad.
*   **Ventaja:** Baja latencia y simplicidad.

### Camino B: Pipeline Modular
*   **Uso:** Cuando el destino no está soportado directamente, se requiere un tono familiar específico o mayor control en el procesamiento intermedio.
*   **Flujo:** Transcripción → Traducción Texto → Síntesis de Voz.

## 3.2. Motivo de la hibridación
Permite escalar a nuevos idiomas manteniendo la flexibilidad de intervenir en el pipeline (por ejemplo, para ajustar el tono familiar) sin perder la velocidad de los motores directos cuando sean suficientes.

---

# 4. Catálogo de idiomas y rutas candidatas

El sistema no se acopla a un par de idiomas fijo. Utiliza un catálogo modular.

## 4.1. Idiomas habilitados inicialmente
*   `es` (Español)
*   `ro` (Rumano)
*   `en` (Inglés - Candidato / Puente)

## 4.2. Rutas candidatas para pruebas
El motor debe estar preparado para procesar:
1.  **Español ↔ Rumano** (Caso de uso familiar prioritario).
2.  **Español ↔ Inglés** (Validación de latencia y calidad estándar).
3.  **Rumano ↔ Inglés** (Validación de calidad en idiomas con menos recursos).

## 4.3. Lógica de selección de ruta
El sistema recibirá `idioma_origen` e `idioma_destino` y el `MODO_MOTOR` decidirá si utiliza un servicio directo o el pipeline modular escalonado.

## 4.4. Modo degradado

Si una etapa falla, el sistema debe intentar mantener la utilidad mínima.

Ejemplos:

```text
Si falla la voz → mostrar solo texto traducido.
Si falla el proveedor principal de traducción → usar fallback si está permitido.
Si falla la transcripción → informar error claro y pedir repetir.
Si se supera el límite de coste → detener llamadas reales.
```

---

# 5. Texto primero, audio después

## 5.1. Decisión

La traducción escrita debe mostrarse antes de esperar la generación de audio.

```text
Texto traducido primero.
Audio después si está disponible.
```

## 5.2. Motivo

La generación de audio puede ser más lenta, más costosa o fallar por proveedor externo.

El usuario no debe quedar bloqueado esperando audio si el texto traducido ya está disponible.

## 5.3. Consecuencia técnica

Los servicios deben separar internamente:

```text
resultado_texto
resultado_audio
estado_audio
latencia_texto_ms
latencia_audio_ms
```

---

# 6. Arquitectura por capas

La arquitectura se organizará en capas simples.

```text
Interfaz / Entrada
↓
Servicio de aplicación
↓
Puertos de proveedores externos
↓
Adaptadores concretos
↓
Resultados, caché y archivos locales
```

## 6.1. Capa de entrada

Responsable de recibir acciones del usuario o scripts de prueba.

En laboratorio:

```text
scripts de prueba
```

En MVP web:

```text
rutas FastAPI
formularios HTMX
captura de audio con JavaScript mínimo
```

## 6.2. Servicio de aplicación

Responsable de coordinar el flujo:

```text
validar entrada
consultar caché
traducir
solicitar voz si aplica
medir tiempos
registrar resultado
responder
```

## 6.3. Puertos

Interfaces internas que definen lo que el sistema necesita de proveedores externos.

## 6.4. Adaptadores

Implementaciones concretas para proveedores externos o simulados.

## 6.5. Persistencia simple

Durante el laboratorio y primeras fases no se usará persistencia compleja.

Se usará:

```text
resultados/*.md
resultados/cache_frases.json
audios_salida/
```

---

# 7. Arquitectura hexagonal limitada

## 7.1. Decisión

La arquitectura hexagonal se aplicará solo a proveedores externos intercambiables.

Esto incluye:

```text
transcripción
traducción
generación de voz
```

No se aplicará inicialmente a persistencia, métricas simples ni archivos locales.

## 7.2. Motivo

Los proveedores externos pueden cambiar por:

```text
coste
calidad
latencia
disponibilidad
soporte de idioma
límites de uso
```

Ahí sí tiene sentido separar puertos y adaptadores.

En cambio, crear puertos complejos para guardar mediciones locales o caché simple puede generar sobreingeniería durante el laboratorio.

## 7.3. Puertos iniciales permitidos

```text
src_lab/ports/
├── puerto_traductor_texto.py
├── puerto_generador_voz.py
└── puerto_transcriptor.py
```

Durante la primera fase de laboratorio pueden implementarse solo los puertos necesarios para el flujo fake.

## 7.4. Adaptadores iniciales permitidos

```text
src_lab/providers_fake/
├── traductor_fake.py
└── voz_fake.py
```

En fases posteriores, cuando se autoricen APIs reales:

```text
src_lab/providers_real/
├── traductor_deepl.py
├── traductor_google.py
├── traductor_openai.py
├── voz_elevenlabs.py
├── voz_gtts.py
├── transcriptor_elevenlabs.py
└── transcriptor_openai.py
```

## 7.5. Regla obligatoria

```text
No crear adaptadores para persistencia hasta que exista una necesidad real.
```

---

# 8. Modo simulación por defecto

## 8.1. Decisión

El sistema debe iniciar en modo simulación.

Valores por defecto:

```env
MODO_SIMULACION=true
PERMITIR_APIS_REALES=false
```

## 8.2. Motivo

El laboratorio debe validar estructura, flujo, límites, caché y resultados sin gastar dinero ni depender de APIs externas.

## 8.3. Consecuencia técnica

Si `MODO_SIMULACION=true`, el sistema debe usar adaptadores fake.

Si `PERMITIR_APIS_REALES=false`, el sistema no debe llamar proveedores reales aunque exista una API key configurada.

Para usar APIs reales deben cumplirse ambas condiciones:

```env
MODO_SIMULACION=false
PERMITIR_APIS_REALES=true
```

---

# 9. Adaptadores fake

## 9.1. Propósito

Los adaptadores fake permiten probar el flujo completo sin coste.

Deben simular:

```text
traducción
voz
transcripción en fases posteriores
```

## 9.2. Ejemplo de comportamiento

```text
"Hola" → "Bună"
"Gracias" → "Mulțumesc"
```

Para voz fake, el adaptador puede devolver una ruta simulada o generar un archivo de texto temporal que represente el resultado.

## 9.3. Regla

Los adaptadores fake deben tener el mismo contrato que los adaptadores reales.

Esto permite cambiar de fake a real sin modificar el servicio central.

---

# 10. Caché local simple

## 10.1. Decisión

El sistema tendrá una caché local simple antes de llamar proveedores externos.

Ubicación inicial:

```text
resultados/cache_frases.json
```

## 10.2. Propósito

Evitar repetir traducciones o generación de audio para frases ya procesadas.

Esto reduce:

```text
coste
latencia
llamadas externas innecesarias
riesgo de gasto accidental
```

## 10.3. Clave recomendada

La clave de caché debe considerar:

```text
idioma_origen
idioma_destino
texto_normalizado
proveedor
modo
```

Ejemplo conceptual:

```text
es|ro|estoy_muy_feliz_de_estar_aqui|deepl
```

## 10.4. Regla

Antes de llamar a un proveedor real, el sistema debe revisar la caché si `USAR_CACHE=true`.

---

# 11. Reglas antizombi para proveedores externos

## 11.1. Problema que evita

Una API externa puede tardar demasiado, fallar o no responder.

El sistema no debe quedar congelado esperando una respuesta indefinida.

## 11.2. Regla obligatoria

Todo adaptador externo debe tener:

```text
timeout explícito
reintentos limitados
espera exponencial limitada
fallback o modo degradado
error específico
medición de latencia
```

## 11.3. Prohibido

```text
reintentos infinitos
timeouts por defecto sin revisar
esperas indefinidas
bloquear toda la app por una API lenta
capturar errores con except Exception sin manejo específico
```

## 11.4. Valores iniciales recomendados

```env
TIMEOUT_TRADUCCION_SEGUNDOS=3
TIMEOUT_VOZ_SEGUNDOS=5
TIMEOUT_TRANSCRIPCION_SEGUNDOS=5
REINTENTOS_MAXIMOS=2
```

Los valores definitivos se detallan en `04_seguridad_privacidad_y_costes.md` y `06_proveedores_adaptadores_y_fallbacks.md`.

---

# 12. Manejo de errores

## 12.1. Errores recomendados

El sistema debe distinguir tipos de error.

```text
ErrorConfiguracion
ErrorLimiteCoste
ErrorProveedorNoDisponible
ErrorAutenticacionProveedor
ErrorTraduccion
ErrorGeneracionVoz
ErrorTranscripcion
ErrorAudioInvalido
```

## 12.2. Regla

Los errores técnicos deben convertirse en mensajes comprensibles para el usuario o para el registro de laboratorio.

Ejemplo:

```text
Proveedor de voz no disponible. Se muestra solo texto traducido.
```

---

# 13. Persistencia

## 13.1. Decisión inicial

Durante Fase 0 y Fase 1, la persistencia será simple.

Se permite:

```text
resultados/mediciones_fase_0.md
resultados/errores_fase_0.md
resultados/cache_frases.json
audios_salida/
```

## 13.2. SQLite queda pospuesto

SQLite, SQLModel, SQLAlchemy o aiosqlite no entran en la primera fase.

Se evaluarán solo si existe una necesidad real de:

```text
frases favoritas persistentes
historial controlado
métricas acumuladas
uso multi-sesión
búsqueda de frases
```

## 13.3. Regla para fases futuras

Si se usa streaming, WebSockets o flujo de audio en tiempo real, la persistencia no debe bloquear la respuesta al usuario.

Regla:

```text
Primero responder al usuario.
Después guardar métricas o historial si aplica.
```

---

# 14. Frontend previsto para MVP web

## 14.1. Decisión

El frontend del MVP web se construirá con:

```text
FastAPI
Jinja2
HTMX
HTML
CSS
JavaScript mínimo para micrófono/audio
```

## 14.2. Motivo

Esta decisión mantiene la lógica principal en Python y evita un frontend pesado.

## 14.3. JavaScript permitido

```text
pedir permiso de micrófono
grabar audio
detener grabación
preparar archivo de audio
enviar audio si aplica
reproducir audio devuelto
```

## 14.4. HTMX/Jinja2

HTMX y Jinja2 deben encargarse de:

```text
mostrar traducciones
actualizar fragmentos HTML
mostrar errores
mostrar estados de carga
insertar resultados sin recargar toda la página
```

## 14.5. Referencia interna

El detalle de UX se documenta en:

```text
05_frontend_y_experiencia_usuario.md
```

---

# 15. Componentes previstos por etapa

## 15.1. Laboratorio Fase 1

Componentes permitidos:

```text
scripts
settings_lab.py
puertos mínimos
adaptadores fake
cache simple
medición de tiempos
guardado de resultados
```

No incluye:

```text
FastAPI
HTMX
APIs reales
SQLite
WebSockets
micrófono
```

## 15.2. Pruebas reales controladas

Se añaden adaptadores reales según autorización:

```text
DeepL o Google para traducción
ElevenLabs o gTTS para voz
OpenAI solo si se autoriza como apoyo
```

## 15.3. MVP web

Se añaden:

```text
FastAPI
Jinja2
HTMX
JavaScript mínimo para micrófono/audio
rutas web
plantillas
static assets
```

## 15.4. Fase posterior

Se evaluará:

```text
transcripción real
WebSockets
SQLite async
PWA
mejoras de UX
app nativa futura
```

---

# 16. Estructura conceptual inicial

La estructura exacta por fase se detalla en `08_plan_implementacion_desarrolladores.md`.

A nivel conceptual, el sistema se organizará así:

```text
traductor_rumano_lab/
├── scripts/
├── src_lab/
│   ├── config/
│   ├── ports/
│   ├── providers_fake/
│   ├── providers_real/
│   ├── cache/
│   ├── services/
│   └── utils/
├── resultados/
└── audios_salida/
```

Para el MVP web posterior:

```text
app_web/
├── main.py
├── routes/
├── templates/
└── static/
    ├── css/
    └── js/
```

---

# 17. Decisiones arquitectónicas aceptadas

```text
[ ] Pipeline modular para español ↔ rumano.
[ ] Texto traducido antes que audio.
[ ] Modo simulación por defecto.
[ ] APIs reales bloqueadas por defecto.
[ ] Arquitectura hexagonal solo para proveedores externos.
[ ] Persistencia simple durante laboratorio.
[ ] Caché local simple.
[ ] Timeouts explícitos en proveedores externos.
[ ] Reintentos limitados.
[ ] Fallback obligatorio cuando sea viable.
[ ] FastAPI + Jinja2 + HTMX para MVP web.
[ ] JavaScript solo para micrófono/audio.
```

---

# 18. Decisiones explícitamente rechazadas para el MVP inicial

```text
- App nativa con Flet desde el inicio.
- Reflex como frontend inicial.
- React/Vue para la primera interfaz.
- Traducción continua siempre encendida.
- WebSockets desde la primera fase.
- SQLite desde el laboratorio inicial.
- Guardar conversaciones familiares completas.
- Usar APIs reales antes de pasar modo simulación.
- Arquitectura hexagonal para todo.
```

Estas opciones pueden reevaluarse en fases futuras si existe una necesidad real.

---

# 19. Referencias internas

Para contexto y objetivo funcional:

```text
01_contexto_y_objetivo_funcional.md
```

Para laboratorio y validación inicial:

```text
03_plan_laboratorio_fase_0.md
```

Para seguridad, privacidad y costes:

```text
04_seguridad_privacidad_y_costes.md
```

Para frontend y UX:

```text
05_frontend_y_experiencia_usuario.md
```

Para proveedores y fallbacks:

```text
06_proveedores_adaptadores_y_fallbacks.md
```

Para pruebas y criterios GO/NO-GO:

```text
07_tests_validacion_y_go_no_go.md
```

Para implementación secuencial:

```text
08_plan_implementacion_desarrolladores.md
```

Para modelo operativo de equipos y flujo de instrucciones:

```text
09_modelo_operativo_chats_y_equipos.md
```

---

# 20. Criterio de calidad de este documento

Este documento se considera correcto si:

```text
[ ] Define el pipeline técnico principal.
[ ] Define la arquitectura por capas.
[ ] Define el alcance de arquitectura hexagonal.
[ ] Define modo simulación por defecto.
[ ] Define la estrategia texto primero / audio después.
[ ] Define reglas antizombi.
[ ] Define el enfoque de caché.
[ ] Define persistencia inicial simple.
[ ] Define frontend previsto sin detallar UX.
[ ] No repite pruebas detalladas.
[ ] No repite costes detallados.
[ ] No repite plan completo de implementación.
```

---

# 21. Estado

```text
Estado: Borrador inicial aprobado para revisión.
```
