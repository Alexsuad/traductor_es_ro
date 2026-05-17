# File: docs/07_tests_validacion_y_go_no_go.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Definir las pruebas de validación y criterios para el paso a producción (Go/No-Go).
# Rol: Documentación de QA y control de calidad.
# ──────────────────────────────────────────────────────────────────────
# 07 — Tests, validación y GO/NO-GO

## Proyecto

**Traductor Familiar Español-Rumano**

## Propósito de este documento

Este documento define cómo se probará el sistema, qué métricas se usarán y cómo se tomará la decisión de avanzar, reducir alcance o detener el desarrollo.

Su función es evitar decisiones basadas en intuición. El proyecto debe avanzar solo si existe evidencia suficiente de calidad, latencia, coste controlado y utilidad familiar real.

Este documento no define la arquitectura completa, la UX detallada ni la implementación paso a paso. Esos temas pertenecen a otros documentos.

---

# 1. Pregunta principal que responde este documento

```text
¿Cómo sabemos si el traductor español ↔ rumano funciona lo suficientemente bien para seguir avanzando?
```

---

# 2. Principio de validación

La validación debe seguir este principio:

```text
Probar pequeño, medir claro y decidir con evidencia.
```

No se debe avanzar a fases más costosas si las pruebas pequeñas fallan.

---

# 3. Tipos de pruebas

El proyecto tendrá cuatro tipos principales de pruebas.

## 3.1. Pruebas fake

No usan APIs reales.

Validan:

```text
estructura
configuración
flujo
caché
registro de resultados
límites de ejecución
modo simulación
```

## 3.2. Pruebas reales mínimas

Usan APIs reales con límites estrictos.

Validan:

```text
traducción real
voz real mínima
latencia real aproximada
coste controlado
fallbacks básicos
```

## 3.3. Pruebas de integración

Validan que varias piezas funcionen juntas.

Ejemplo:

```text
texto → traducción → voz
```

Más adelante:

```text
audio → transcripción → traducción → voz
```

## 3.4. Pruebas funcionales de uso

Validan si la herramienta sirve en una situación familiar real.

Ejemplo:

```text
frase breve
frase emocional
frase con ruido moderado
frase rumana real
```

---

# 4. Orden de validación

No se debe probar todo al mismo tiempo.

Orden obligatorio:

```text
1. Verificar entorno.
2. Ejecutar flujo fake sin coste.
3. Validar caché y límites.
4. Probar traducción real mínima.
5. Probar voz básica o fallback.
6. Probar voz premium mínima.
7. Probar pipeline texto → traducción → voz.
8. Probar transcripción con audios cortos.
9. Probar pipeline completo con audio.
10. Tomar decisión GO / GO parcial / NO-GO.
```

---

# 5. Pruebas iniciales sin coste

## 5.1. Prueba: verificar entorno

Script esperado:

```text
scripts/verificar_entorno.py
```

Debe validar:

```text
[ ] Existe configuración mínima.
[ ] Existen carpetas requeridas.
[ ] MODO_SIMULACION=true.
[ ] PERMITIR_APIS_REALES=false.
[ ] Existen límites de llamadas.
[ ] Existen límites de caracteres.
[ ] Existe ruta de resultados.
[ ] Existe ruta de caché.
```

Criterio de aprobación:

```text
El entorno queda validado sin llamar APIs externas.
```

---

## 5.2. Prueba: flujo fake texto → traducción → voz

Script esperado:

```text
scripts/prueba_fake_texto_traduccion_voz.py
```

Debe validar:

```text
[ ] Carga frases de prueba.
[ ] Usa traductor fake.
[ ] Usa voz fake.
[ ] Respeta límites de ejecución.
[ ] Consulta o escribe caché.
[ ] Registra mediciones.
[ ] No llama APIs reales.
```

Criterio de aprobación:

```text
El flujo completo funciona en modo simulación sin coste.
```

---

# 6. Pruebas reales mínimas

Las pruebas reales solo se permiten después de aprobar el modo fake.

Condiciones obligatorias:

```env
MODO_SIMULACION=false
PERMITIR_APIS_REALES=true
USAR_CACHE=true
MAX_FRASES_POR_PRUEBA=5
MAX_LLAMADAS_POR_EJECUCION=10
REINTENTOS_MAXIMOS=2
```

---

## 6.1. Prueba real de traducción mínima

Objetivo:

```text
Validar traducción español ↔ rumano con pocas frases.
```

Límite inicial:

```text
máximo 3 frases español → rumano
máximo 3 frases rumano → español
```

Métricas:

```text
latencia_traduccion_ms
calidad_traduccion
proveedor
uso_cache
estado
```

Criterio de aprobación:

```text
calidad_traduccion >= 4/5 en frases clave
latencia aceptable según semáforo
sin superar límites de llamadas
```

---

## 6.2. Prueba de voz básica

Objetivo:

```text
Validar que el sistema puede generar o simular audio sin romper el flujo.
```

Puede usar:

```text
gTTS
voz fake
audio local ya generado
```

Criterio de aprobación:

```text
el audio o fallback se genera/controla correctamente
el texto sigue disponible aunque el audio falle
```

---

## 6.3. Prueba de voz premium mínima

Objetivo:

```text
Validar si la voz premium aporta calidad suficiente.
```

Límite inicial:

```text
1 frase en rumano
1 frase en español
```

Criterio de aprobación:

```text
calidad_voz >= 3/5
latencia_audio dentro del semáforo
coste controlado
```

---

## 6.4. Prueba de pipeline real mínimo

Objetivo:

```text
Validar el flujo texto → traducción → voz con APIs reales controladas.
```

Límite inicial:

```text
1 frase español → rumano
1 frase rumano → español
```

Criterio de aprobación:

```text
traducción clara
audio entendible o fallback correcto
registro de mediciones completo
```

---

# 7. Pruebas de transcripción

La transcripción se valida después de traducción y voz.

## 7.1. Motivo

No tiene sentido probar voz de entrada si todavía no está validado que:

```text
texto → traducción → voz
```

funciona de manera aceptable.

## 7.2. Audios permitidos

```text
audios cortos de prueba
audios de Alex leyendo frases controladas
audios rumanos controlados o generados
```

No se permiten conversaciones familiares reales en Fase 0.

## 7.3. Límite

```text
máximo 15 segundos por audio
```

## 7.4. Criterio de aprobación

```text
transcripción español >= 4/5
transcripción rumano >= 3/5
latencia aceptable
sin guardar datos sensibles
```

---

# 8. Frases de prueba y rutas candidatas

### 8.1. Ruta Familiar Principal (Español ↔ Rumano)

*ES → RO:*
1. Estoy muy feliz de estar aquí con ustedes.
2. ¿Pueden hablar un poco más despacio, por favor?
3. La comida está muy rica, muchas gracias por recibirme.
4. Voy a usar el traductor para entenderlos mejor.
5. Para mí es importante poder comunicarme mejor con ustedes porque somos familia.

*RO → ES:*
1. Ne bucurăm că ești aici cu noi.
2. Vrei să mănânci ceva sau să bei o cafea?
3. Nu îți face griji, poți vorbi încet.
4. Familia este foarte importantă pentru noi.
5. Dacă nu înțelegi, putem repeta.

### 8.2. Rutas Candidatas de Validación (Inglés)

*ES ↔ EN:*
1. Hola, ¿cómo estás? / Hello, how are you?
2. Entiendo un poco de inglés. / I understand a little bit of English.

*RO ↔ EN:*
1. Ne bucurăm de vizită. / We enjoy the visit.
2. Vorbiți engleză? / Do you speak English?

*EN ↔ ES / RO:*
1. Welcome to our home.
2. The weather is nice today.

### 8.3. Regla de Oro
Ninguna ruta se considera "ganadora" o principal técnica hasta medir calidad, latencia y coste. El inglés se usa como punto de referencia y posible idioma puente.

## 8.4. Regla

Las frases de prueba deben ser familiares, breves y representativas.

No usar textos largos ni conversaciones reales privadas en Fase 0.

---

# 9. Métricas obligatorias

Cada prueba debe registrar como mínimo:

```text
id_prueba
tipo_prueba
modo_simulacion
proveedor_traduccion
proveedor_voz
proveedor_transcripcion, si aplica
idioma_origen
idioma_destino
uso_cache
fallback_usado
latencia_traduccion_ms
latencia_voz_ms
latencia_transcripcion_ms
latencia_total_ms
calidad_traduccion
calidad_voz
calidad_transcripcion
estado
error_resumido
```

No registrar claves, tokens, payloads completos ni conversaciones privadas.

---

# 10. Escala de calidad

## 10.1. Calidad de traducción

```text
1 = incorrecta o cambia el sentido
2 = confusa o poco natural
3 = aceptable con errores menores
4 = clara y usable
5 = natural, correcta y familiar
```

## 10.2. Calidad de voz

```text
1 = no se entiende
2 = se entiende con dificultad
3 = entendible aunque robótica
4 = clara y usable
5 = natural y cómoda
```

## 10.3. Calidad de transcripción

```text
1 = no reconoce la frase
2 = muchos errores
3 = entiende la idea general
4 = pocos errores
5 = casi exacta
```

---

# 11. Semáforo de latencia

## Semáforo de latencia

### Traducción de texto

| Estado | Tiempo |
|---|---:|
| Verde | 0 a 1.5 segundos |
| Amarillo | Más de 1.5 y hasta 3 segundos |
| Rojo | Más de 3 segundos |

### Generación de voz

| Estado | Tiempo |
|---|---:|
| Verde | 0 a 3 segundos |
| Amarillo | Más de 3 y hasta 5 segundos |
| Rojo | Más de 5 segundos |

### Transcripción

| Estado | Tiempo |
|---|---:|
| Verde | 0 a 2 segundos |
| Amarillo | Más de 2 y hasta 5 segundos |
| Rojo | Más de 5 segundos |

### Pipeline completo

| Estado | Tiempo |
|---|---:|
| Verde | 0 a 4 segundos |
| Amarillo | Más de 4 y hasta 8 segundos |
| Rojo | Más de 8 segundos |

---

# 12. Tabla de medición base

```text
| id_prueba | dirección | frase | modo | traductor | voz | transcriptor | cache | fallback | texto_ms | audio_ms | stt_ms | total_ms | calidad_traducción | calidad_voz | calidad_stt | estado | error |
|---|---|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|
```

Esta tabla puede guardarse en:

```text
resultados/mediciones_fase_0.md
```

---

# 13. Estados posibles de prueba

```text
PENDIENTE
PASA
PARCIAL
FALLA
BLOQUEADA_POR_SEGURIDAD
BLOQUEADA_POR_COSTE
```

## 13.1. PASA

La prueba cumple criterios mínimos.

## 13.2. PARCIAL

La prueba funciona parcialmente.

Ejemplo:

```text
traducción buena, audio lento
```

## 13.3. FALLA

La prueba no cumple criterios mínimos.

## 13.4. BLOQUEADA_POR_SEGURIDAD

No se ejecuta porque violaría una regla de seguridad.

## 13.5. BLOQUEADA_POR_COSTE

No se ejecuta porque supera límites configurados.

---

# 14. Matriz GO / GO parcial / NO-GO

## Fórmula de decisión GO / GO parcial / NO-GO

Cada dimensión se califica de 1 a 5.

| Dimensión | Peso |
|---|---:|
| Latencia | 30% |
| Calidad de traducción | 25% |
| Calidad de transcripción | 15% |
| Calidad de voz | 10% |
| Coste | 10% |
| Simplicidad de uso | 10% |

Fórmula:

```text
puntuacion_final =
latencia * 0.30 +
calidad_traduccion * 0.25 +
calidad_transcripcion * 0.15 +
calidad_voz * 0.10 +
coste * 0.10 +
simplicidad_uso * 0.10
```

### Decisión

```text
GO:
puntuacion_final >= 4.0

GO parcial:
puntuacion_final >= 3.0 y < 4.0

NO-GO:
puntuacion_final < 3.0
```

### Condiciones críticas

Aunque la puntuación sea aceptable, habrá NO-GO si ocurre cualquiera de estas condiciones:

* La traducción cambia el sentido de frases importantes.
* La transcripción rumana falla de forma repetida.
* La latencia total supera 8 segundos de forma frecuente.
* El coste no se puede limitar.
* El sistema exige guardar conversaciones familiares reales.
* Las API keys tendrían que exponerse en frontend.

---

# 15. Criterios de GO

La decisión es GO si:

```text
puntuacion_final >= 4.0
latencia >= 4
traduccion >= 4
transcripcion >= 3
simplicidad >= 4
```

Resultado:

```text
Construir MVP según plan.
```

---

# 16. Criterios de GO parcial

La decisión es GO parcial si:

```text
puntuacion_final entre 3.0 y 3.9
```

O si ocurre:

```text
traducción escrita funciona bien pero audio no
ES→RO funciona pero RO→ES falla parcialmente
funciona con frases cortas pero no con frases largas
funciona en modo texto pero no todavía con voz
```

Resultado:

```text
Construir MVP reducido.
```

Ejemplo de MVP reducido:

```text
texto primero + audio opcional
frases frecuentes
entrada escrita antes que voz
```

---

# 17. Criterios de NO-GO

La decisión es NO-GO si:

```text
puntuacion_final < 3.0
```

O si aparece una condición crítica.

Resultado:

```text
No construir app propia completa en esta etapa.
```

Alternativas:

```text
usar Google Translate
usar DeepL
usar ChatGPT para preparar frases
crear kit familiar español-rumano
```

---

# 18. Condiciones críticas automáticas

## 18.1. NO-GO automático

```text
[ ] La traducción cambia el sentido de frases familiares importantes.
[ ] La transcripción rumana falla en más del 50% de pruebas.
[ ] La latencia total supera 7 segundos de forma frecuente.
[ ] El coste no se puede limitar.
[ ] Se requiere guardar conversaciones familiares completas.
[ ] La API key tendría que exponerse en frontend.
```

## 18.2. GO parcial automático

```text
[ ] La traducción escrita funciona bien, pero la voz no.
[ ] Un sentido funciona mejor que el otro.
[ ] Funciona en WiFi, pero no en datos móviles.
[ ] Funciona con frases cortas, pero no con frases largas.
```

---

# 19. Plantilla de decisión final

```text
# Decisión Fase 0

Fecha:
Responsable:
Pipeline probado:

Transcriptor:
Traductor:
Generador de voz:

Resultados:
- Latencia: __/5
- Traducción: __/5
- Transcripción: __/5
- Voz: __/5
- Coste: __/5
- Simplicidad: __/5

Puntuación final:
__/5

Condiciones críticas detectadas:
[ ] Sí
[ ] No

Decisión:
[ ] GO
[ ] GO parcial
[ ] NO-GO

Motivo de la decisión:

Arquitectura recomendada para la siguiente fase:

Siguiente acción:
```

---

# 20. Checklist antes de pruebas reales

```text
[ ] Fase fake aprobada.
[ ] MODO_SIMULACION=false.
[ ] PERMITIR_APIS_REALES=true.
[ ] USAR_CACHE=true.
[ ] MAX_LLAMADAS_POR_EJECUCION definido.
[ ] MAX_CARACTERES_POR_FRASE definido.
[ ] REINTENTOS_MAXIMOS definido.
[ ] Timeouts definidos.
[ ] API keys configuradas localmente.
[ ] .env no versionado.
[ ] No se usarán audios sensibles.
```

---

# 21. Checklist después de pruebas

```text
[ ] Se guardaron mediciones.
[ ] Se registró si hubo fallback.
[ ] Se registró si se usó caché.
[ ] Se evaluó calidad manualmente.
[ ] No se expusieron claves.
[ ] No se guardaron datos sensibles.
[ ] No se superaron límites.
[ ] Se actualizó la decisión de fase si aplica.
```

---

# 22. Relación con otros documentos

Para contexto funcional:

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

Para frontend y UX:

```text
05_frontend_y_experiencia_usuario.md
```

Para proveedores y fallbacks:

```text
06_proveedores_adaptadores_y_fallbacks.md
```

Para implementación por fases:

```text
08_plan_implementacion_desarrolladores.md
```

---

# 23. Criterio de calidad de este documento

Este documento se considera correcto si:

```text
[ ] Define tipos de pruebas.
[ ] Define orden de validación.
[ ] Define pruebas fake.
[ ] Define pruebas reales mínimas.
[ ] Define métricas obligatorias.
[ ] Define escala de calidad.
[ ] Define semáforo de latencia.
[ ] Define tabla de medición.
[ ] Define matriz GO / GO parcial / NO-GO.
[ ] Define condiciones críticas.
[ ] Define checklists antes y después de pruebas.
[ ] No repite arquitectura completa.
[ ] No repite proveedores en detalle.
[ ] No repite plan de implementación completo.
```

---

# 24. Estado

```text
Estado: Borrador inicial aprobado para revisión.
```
