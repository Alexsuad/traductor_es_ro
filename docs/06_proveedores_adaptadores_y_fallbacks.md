# File: docs/06_proveedores_adaptadores_y_fallbacks.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Definir la estrategia de multi-proveedor, adaptadores y sistemas de respaldo (fallbacks).
# Rol: Documentación técnica de integración y resiliencia.
# ──────────────────────────────────────────────────────────────────────

# 06 — Proveedores, adaptadores y fallbacks

## Proyecto

**Traductor Familiar Español-Rumano**

## Propósito de este documento

Este documento define qué proveedores externos puede usar el proyecto, cómo se aíslan mediante adaptadores, qué fallbacks existen y bajo qué condiciones se cambia de proveedor.

Su objetivo es evitar que la lógica principal dependa directamente de una API concreta. El sistema debe poder probar proveedores, reemplazarlos o degradar funcionalmente sin romper todo el flujo.

Este documento no describe la UX, el plan completo de implementación, las plantillas de pruebas ni el detalle extenso de privacidad. Esos temas pertenecen a otros documentos.

---

# 1. Pregunta principal que responde este documento

```text
¿Qué proveedor se usa para cada función, cómo se integra y qué ocurre si falla?
```

---

# 2. Matriz de Motores y Caminos de Ejecución

El sistema decide el camino técnico según el `MODO_MOTOR` seleccionado.

| Motor | Descripción | Camino Técnico |
|---|---|---|
| `Translate` | Traducción directa en tiempo real. | Realtime Translate |
| `Whisper Pipeline` | Transcripción + Traducción + Voz. | Pipeline Modular |
| `Combined` | Uso de ambos motores para validación cruzada. | Experimental |
| `AUTO` | El sistema elige según idioma de destino. | Híbrido |

## 2.1. Rutas de idiomas
*   **Ruta Familiar:** Español ↔ Rumano (Enfoque principal).
*   **Ruta Candidata:** Español ↔ Inglés, Rumano ↔ Inglés (Para validación y comparación).

El inglés actúa como ruta de prueba, posible idioma puente y opción de comparación tecnológica, pero no es el objetivo humano final.

---

# 3. Principio de diseño

La integración con proveedores externos debe seguir esta regla:

```text
La lógica principal conoce puertos. Los adaptadores conocen proveedores.
```

Esto significa que el servicio central no debe depender directamente de DeepL, Google, ElevenLabs, OpenAI o gTTS.

Debe depender de interfaces internas como:

```text
puerto_traductor_texto
puerto_generador_voz
puerto_transcriptor
```

---

# 4. Puertos permitidos

## 4.1. Puerto de traducción de texto

Responsabilidad:

```text
recibir texto, idioma origen e idioma destino;
devolver texto traducido y metadatos mínimos.
```

Contrato conceptual:

```text
traducir(texto, idioma_origen, idioma_destino) -> resultado_traduccion
```

## 4.2. Puerto de generación de voz

Responsabilidad:

```text
recibir texto e idioma;
devolver una ruta de audio, bytes de audio o resultado simulado según el modo.
```

Contrato conceptual:

```text
generar_voz(texto, idioma_destino, nombre_salida) -> resultado_voz
```

## 4.3. Puerto de transcripción

Responsabilidad:

```text
recibir audio e idioma esperado;
devolver texto transcrito y metadatos mínimos.
```

Contrato conceptual:

```text
transcribir(ruta_audio, idioma_esperado) -> resultado_transcripcion
```

---

# 5. Adaptadores fake

## 5.1. Propósito

Los adaptadores fake permiten probar el flujo completo sin llamar APIs reales.

Deben ser usados por defecto en Fase 1 del laboratorio.

## 5.2. Adaptadores fake iniciales

```text
providers_fake/
├── traductor_fake.py
└── voz_fake.py
```

En fases posteriores se puede agregar:

```text
transcriptor_fake.py
```

## 5.3. Reglas de adaptadores fake

```text
- No deben llamar APIs externas.
- No deben requerir claves.
- Deben respetar el mismo contrato que los adaptadores reales.
- Deben devolver respuestas predecibles.
- Deben permitir probar caché, medición y guardado de resultados.
```

## 5.4. Ejemplo de respuestas fake

```text
Hola → Bună
Gracias → Mulțumesc
¿Puedes repetir? → Poți repeta?
```

Estas respuestas no buscan validar calidad lingüística. Buscan validar flujo técnico sin coste.

---

# 6. Proveedores de traducción

## 6.1. DeepL

### Uso previsto

DeepL será uno de los candidatos para las primeras pruebas reales de traducción texto. No se declara como proveedor principal definitivo hasta comparar calidad, latencia y coste frente a otros candidatos.

### Motivo

```text
- Buena calidad en idiomas europeos.
- API relativamente directa.
- Adecuado para comparar naturalidad de traducción.
```

### Cuándo usarlo

```text
- Pruebas reales mínimas de texto.
- Traducción español → rumano.
- Traducción rumano → español.
- Comparación de calidad con Google.
```

### Fallback posible

```text
Google Cloud Translation
OpenAI texto, si se requiere tono familiar
```

---

## 6.2. Google Cloud Translation

### Uso previsto

Google Cloud Translation será candidato alternativo o fallback para traducción.

### Motivo

```text
- Amplia cobertura de idiomas.
- API madura.
- Buena opción si DeepL no cumple en latencia, coste o disponibilidad.
```

### Cuándo usarlo

```text
- Comparación contra DeepL.
- Fallback si DeepL falla.
- Pruebas de cobertura y velocidad.
```

### Consideración

Puede requerir configuración adicional de credenciales de Google Cloud.

Las credenciales no deben versionarse.

---

## 6.3. OpenAI texto

### Uso previsto

OpenAI texto será candidato de comparación, especialmente para evaluar tono familiar, naturalidad y rutas con inglés. No se declara como proveedor principal hasta medir resultados y coste.

Se usará principalmente como apoyo contextual.

### Cuándo usarlo

```text
- Frases familiares delicadas.
- Adaptación de tono.
- Reformulación natural.
- Explicación de matices.
- Comparación cualitativa.
```

### Cuándo no usarlo

```text
- Traducción masiva.
- Primera prueba económica.
- Frases simples donde DeepL o Google sean suficientes.
```

---

# 7. Proveedores de generación de voz

## 7.1. ElevenLabs TTS

### Uso previsto

ElevenLabs será uno de los candidatos fuertes para voz natural.

### Motivo

```text
- Buena calidad de voz.
- Candidato fuerte para rumano y español.
- Útil para validar si el audio aporta valor familiar.
```

### Cuándo usarlo

```text
- Pruebas reales mínimas de voz.
- Validación de audio rumano.
- Validación de audio español.
- Comparación de calidad frente a gTTS.
```

### Riesgo

```text
- Puede generar coste por caracteres.
- Puede tener latencia superior a texto.
- No se debe regenerar el mismo audio innecesariamente.
```

### Fallback posible

```text
gTTS
solo texto
```

---

## 7.2. gTTS

### Uso previsto

gTTS será fallback simple y económico.

### Motivo

```text
- Fácil de probar.
- Útil para validar flujo texto → audio.
- Adecuado como respaldo básico.
```

### Cuándo usarlo

```text
- Pruebas de bajo coste.
- Fallback si ElevenLabs no está disponible.
- Validación de generación de archivos de audio.
```

### Limitación

La voz puede ser menos natural que ElevenLabs.

---

## 7.3. Solo texto

### Uso previsto

Si falla la generación de voz, el sistema debe mantener utilidad mostrando texto.

### Regla

```text
La falta de audio no debe bloquear la traducción escrita.
```

Este fallback es obligatorio.

---

# 8. Proveedores de transcripción

## 8.1. ElevenLabs Scribe

### Uso previsto

Uno de los candidatos para transcripción en fases posteriores.

### Motivo

```text
- Orientado a speech-to-text.
- Candidato para español y rumano.
- Útil para validar voz → texto.
```

### Cuándo usarlo

```text
- Después de validar texto → traducción → voz.
- Pruebas controladas con audios cortos.
- Comparación contra OpenAI Whisper.
```

---

## 8.2. OpenAI Whisper / Realtime Whisper

### Uso previsto

Candidato alternativo para transcripción.

### Cuándo usarlo

```text
- Comparación de calidad.
- Fallback si ElevenLabs Scribe falla.
- Pruebas con audios cortos.
```

---

## 8.3. Transcripción no incluida en primera fase

Durante la Fase 1 del laboratorio no se usará transcripción real.

Primero se valida:

```text
texto → traducción fake → voz fake
```

Después:

```text
texto → traducción real → voz real mínima
```

Solo luego se valida:

```text
audio → transcripción → traducción → voz
```

---

# 9. Reglas de selección de proveedores

## 9.1. Criterios principales

Cada proveedor debe evaluarse por:

```text
calidad
latencia
coste
facilidad de integración
soporte español ↔ rumano
estabilidad
capacidad de fallback
```

## 9.2. No elegir por moda

No se debe elegir un proveedor solo porque sea más reciente o tenga mejor marketing.

La decisión debe basarse en pruebas medidas.

## 9.3. Proveedor principal y fallback

Cada función debe tener:

```text
proveedor principal
proveedor fallback
modo degradado
```

Ejemplo:

```text
Voz principal: ElevenLabs
Voz fallback: gTTS
Modo degradado: solo texto
```

---

# 10. Timeouts iniciales por tipo de proveedor

Los valores iniciales aprobados son:

```env
TIMEOUT_TRADUCCION_SEGUNDOS=3
TIMEOUT_VOZ_SEGUNDOS=5
TIMEOUT_TRANSCRIPCION_SEGUNDOS=5
```

Interpretación:

* Traducción: si supera 3 segundos, se considera lenta o fallida.
* Voz: si supera 5 segundos, no debe bloquear la respuesta textual.
* Transcripción: si supera 5 segundos, debe registrarse como latencia alta.

Regla:
el texto traducido tiene prioridad sobre el audio.

---

# 11. Reintentos oficiales

Las variables oficiales de entorno, límites, timeouts y reglas de coste están centralizadas en:

- `04_seguridad_privacidad_y_costes.md`

Este documento no debe duplicar la lista completa para evitar inconsistencias.

---

# 12. Fallbacks por función

## 12.1. Traducción

Orden conceptual:

```text
1. Traductor principal autorizado.
2. Traductor fallback autorizado.
3. Mensaje de error claro.
```

Ejemplo:

```text
DeepL falla → Google si está configurado y permitido.
Google falla → mostrar error claro.
```

## 12.2. Voz

Orden conceptual:

```text
1. ElevenLabs.
2. gTTS.
3. Solo texto.
```

## 12.3. Transcripción

Orden conceptual:

```text
1. Transcriptor principal.
2. Transcriptor fallback.
3. Pedir repetir o usar entrada escrita.
```

---

# 13. Caché antes de proveedor

Antes de llamar a un proveedor externo, el sistema debe consultar caché si está activada.

```env
USAR_CACHE=true
```

## 13.1. Orden correcto

```text
1. Validar entrada.
2. Normalizar texto.
3. Revisar límite de caracteres.
4. Consultar caché.
5. Si hay caché válida, devolver resultado.
6. Si no hay caché, llamar proveedor autorizado.
7. Guardar resultado en caché si aplica.
```

## 13.2. Prohibido

```text
llamar proveedor real antes de revisar caché cuando USAR_CACHE=true.
```

---

# 14. Adaptadores reales y modo simulación

## 14.1. Regla

Los adaptadores reales solo pueden ejecutarse si:

```env
MODO_SIMULACION=false
PERMITIR_APIS_REALES=true
```

## 14.2. Si no se cumple

El sistema debe:

```text
usar adaptadores fake
o detener la ejecución según el tipo de prueba.
```

## 14.3. Prohibido

```text
llamar DeepL, Google, OpenAI o ElevenLabs con MODO_SIMULACION=true.
```

---

# 15. Errores por proveedor

Cada adaptador debe convertir errores externos en errores internos claros.

Ejemplos:

```text
ErrorAutenticacionProveedor
ErrorProveedorNoDisponible
ErrorTimeoutProveedor
ErrorLimiteCoste
ErrorTraduccion
ErrorGeneracionVoz
ErrorTranscripcion
```

No se deben propagar tracebacks crudos hacia la interfaz.

---

# 16. Métricas mínimas por llamada

Cada llamada real o fake debe registrar:

```text
id_prueba
proveedor
modo_simulacion
uso_cache
idioma_origen
idioma_destino
latencia_ms
estado
fallback_usado
error_resumido
```

No se deben registrar claves ni payloads sensibles.

---

# 17. Orden recomendado de activación de proveedores reales

No se activan todos a la vez.

## 17.1. Paso 1 — Traducción real mínima

```text
DeepL o Google
máximo 3 frases ES→RO
máximo 3 frases RO→ES
```

## 17.2. Paso 2 — Voz básica

```text
gTTS
máximo 2 frases
```

## 17.3. Paso 3 — Voz premium mínima

```text
ElevenLabs
máximo 1 frase en rumano
máximo 1 frase en español
```

## 17.4. Paso 4 — Pipeline real mínimo

```text
1 frase ES→RO
1 frase RO→ES
```

## 17.5. Paso 5 — Transcripción real

Solo después de validar texto y voz.

```text
audios cortos
máximo 15 segundos por archivo
```

---

# 18. Criterios para cambiar de proveedor

Se puede cambiar de proveedor principal si:

```text
- la latencia es demasiado alta;
- el coste es mayor de lo previsto;
- la calidad no es suficiente;
- falla con frecuencia;
- no soporta bien español ↔ rumano;
- la integración se vuelve inestable;
- otro proveedor demuestra mejor resultado en pruebas.
```

La decisión debe basarse en resultados registrados, no en impresión subjetiva.

---

# 19. Proveedores fuera del alcance inicial

No se evaluarán en la primera fase:

```text
servicios de app nativa
plataformas de videollamada
traducción de documentos
modelos locales pesados
servicios empresariales complejos
infraestructura de streaming avanzada
```

Pueden evaluarse en fases futuras si el MVP demuestra valor.

---

# 20. Relación con otros documentos

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

Para pruebas y criterios GO/NO-GO:

```text
07_tests_validacion_y_go_no_go.md
```

Para implementación por fases:

```text
08_plan_implementacion_desarrolladores.md
```

Para modelo operativo de equipos, límites de instrucción y coordinación con proveedores:

```text
09_modelo_operativo_chats_y_equipos.md
```

---

# 21. Criterio de calidad de este documento

Este documento se considera correcto si:

```text
[ ] Define funciones externas del sistema.
[ ] Define puertos permitidos.
[ ] Define adaptadores fake.
[ ] Define proveedores de traducción.
[ ] Define proveedores de voz.
[ ] Define proveedores de transcripción.
[ ] Define fallbacks.
[ ] Define timeouts y reintentos por tipo.
[ ] Define reglas de caché antes de proveedor.
[ ] Define criterios para cambiar de proveedor.
[ ] No repite seguridad completa.
[ ] No repite UX.
[ ] No repite plan de implementación completo.
```

---

# 22. Estado

```text
Estado: Aprobado documentalmente para cierre de planeación.
```

