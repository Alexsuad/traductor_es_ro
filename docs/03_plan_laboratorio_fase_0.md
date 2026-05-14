# 03 — Plan laboratorio Fase 0

## Proyecto

**Traductor Familiar Español-Rumano**

## Propósito de este documento

Este documento define cómo se validará técnicamente el proyecto antes de construir la app real.

La Fase 0 no busca crear el producto final. Busca crear un laboratorio controlado para comprobar si la idea es viable con el menor coste, menor riesgo y menor complejidad posible.

No describe la arquitectura completa del MVP web, ni el diseño visual, ni la comparación detallada de proveedores. Esos temas pertenecen a otros documentos.

---

# 1. Pregunta principal que responde este documento

```text
¿Cómo validamos el traductor español ↔ rumano antes de invertir tiempo y dinero en una app completa?
```

---

# 2. Objetivo de Fase 0

Validar si el proyecto puede funcionar de forma útil para conversaciones familiares reales entre español y rumano.

La Fase 0 debe responder:

```text
¿La traducción español → rumano funciona bien?
¿La traducción rumano → español funciona bien?
¿La voz generada es entendible?
¿La transcripción de voz es viable?
¿La latencia es tolerable?
¿El coste se puede controlar?
¿Vale la pena avanzar a MVP?
```

---

# 3. Regla principal de Fase 0

```text
Primero validar. Después construir.
```

No se permite construir una app completa antes de validar:

```text
traducción
voz
transcripción
coste
latencia
experiencia mínima de uso
```

---

# 4. Resultado esperado de Fase 0

Al terminar Fase 0 debe existir una decisión clara:

```text
GO
GO parcial
NO-GO
```

## 4.1. GO

Significa que el pipeline funciona con calidad y latencia suficiente para construir el MVP.

## 4.2. GO parcial

Significa que algunas piezas funcionan, pero se debe reducir el alcance.

Ejemplo:

```text
La traducción escrita funciona bien, pero el audio tarda demasiado.
```

Resultado:

```text
Construir MVP texto primero + audio opcional.
```

## 4.3. NO-GO

Significa que no vale la pena construir una app propia en esta etapa.

Ejemplo:

```text
La latencia es demasiado alta o la traducción cambia el sentido.
```

Resultado:

```text
Usar herramientas existentes o preparar kit de frases familiares.
```

---

# 5. Laboratorio de pruebas

## 5.1. Nombre del laboratorio

El laboratorio se llamará:

```text
traductor_rumano_lab
```

No debe confundirse con el proyecto final.

## 5.2. Motivo

El laboratorio permite:

```text
- probar sin comprometer la app final;
- mantener código experimental separado;
- medir resultados;
- evitar gasto innecesario;
- descartar decisiones antes de que sean costosas;
- validar arquitectura básica con adaptadores fake.
```

---

# 6. Alcance del laboratorio

## 6.1. Incluido

```text
- Configuración local.
- Modo simulación.
- Adaptadores fake (multi-idioma).
- Configuración de idiomas habilitados (es, ro, en).
- Configuración de motor híbrido (MODO_MOTOR).
- Caché local simple.
- Medición de tiempos.
- Registro de resultados.
- Pruebas texto → traducción → voz.
- Pruebas reales mínimas cuando se autoricen.
```

## 6.2. No incluido

```text
- App web final.
- FastAPI en la primera fase.
- HTMX en la primera fase.
- WebSockets.
- SQLite.
- Login.
- Dashboard.
- Despliegue cloud.
- App nativa.
- Traducción continua.
```

---

# 7. Principio de pruebas económicas

La Fase 0 debe ejecutarse en tres niveles.

## 7.1. Nivel 1 — Pruebas sin coste

No se usan APIs reales.

Se usan adaptadores fake:

```text
traductor_fake
voz_fake
transcriptor_fake, si aplica en fase posterior
```

Objetivo:

```text
probar estructura, flujo, configuración, caché y registros sin gastar dinero.
```

## 7.2. Nivel 2 — Pruebas de bajo coste

Se usan herramientas simples o resultados locales.

Ejemplos:

```text
gTTS
audios ya generados
traducciones preguardadas
cache_frases.json
```

Objetivo:

```text
validar nombres de archivos, flujo texto→audio, fallback y registros.
```

## 7.3. Nivel 3 — APIs reales controladas

Solo se usan APIs reales cuando el modo simulación ya pasó.

Ejemplos:

```text
DeepL
ElevenLabs
OpenAI
Google Cloud Translation
```

Con límites estrictos:

```text
máximo 5 frases por prueba
máximo 10 llamadas por ejecución
máximo 300 caracteres por frase
máximo 2 reintentos
timeouts explícitos
caché activa
```

---

# 8. Modo simulación obligatorio

## 8.1. Valores por defecto

El laboratorio debe iniciar con:

```env
MODO_SIMULACION=true
PERMITIR_APIS_REALES=false
```

## 8.2. Regla

Mientras `MODO_SIMULACION=true`, el sistema debe usar adaptadores fake.

Mientras `PERMITIR_APIS_REALES=false`, ninguna API real debe ser llamada, aunque existan claves configuradas.

## 8.3. Doble confirmación para APIs reales

Para permitir llamadas reales deben cumplirse ambas condiciones:

```env
MODO_SIMULACION=false
PERMITIR_APIS_REALES=true
```

Si una de las dos no se cumple, el sistema debe detenerse o usar adaptadores fake.

---

# 9. Estructura del laboratorio

La Fase 0 utilizará un laboratorio separado llamado `traductor_rumano_lab/`.

Este documento define el propósito del laboratorio, sus límites, las reglas de simulación y los criterios para avanzar a pruebas reales.

La estructura operativa exacta de carpetas, archivos y comandos de creación se define en:

- `08_plan_implementacion_desarrolladores.md`

Regla documental:
este documento no debe duplicar la estructura completa del laboratorio para evitar inconsistencias futuras.

---

# 10. Dependencias permitidas en Fase 1 del laboratorio

La primera fase del laboratorio solo debe instalar dependencias necesarias para validar estructura y simulación.

```text
python-dotenv
pydantic
pydantic-settings
httpx
tenacity
pytest
pytest-asyncio
ruff
```

## 10.1. Motivo

Estas dependencias permiten:

```text
- leer configuración;
- validar variables;
- preparar contratos;
- definir llamadas HTTP futuras;
- preparar reintentos limitados;
- probar código;
- aplicar lint.
```

---

# 11. Dependencias no permitidas todavía

Durante la primera fase del laboratorio no se deben instalar dependencias que impliquen APIs reales, web app o persistencia compleja.

```text
fastapi
uvicorn
jinja2
sqlmodel
sqlalchemy
aiosqlite
elevenlabs
deepl
openai
google-cloud-translate
gtts
pydub
soundfile
```

Estas dependencias entran solo después de que el modo simulación pase correctamente y exista autorización para pruebas reales controladas.

---

# 12. Scripts iniciales

## 12.1. `scripts/verificar_entorno.py`

Responsabilidad:

```text
verificar que el laboratorio está listo sin llamar APIs externas.
```

Debe comprobar:

```text
- existe .env o configuración equivalente;
- existen carpetas necesarias;
- existen variables mínimas;
- IDIOMAS_HABILITADOS=es,ro,en configurado;
- MODO_MOTOR=AUTO configurado;
- MODO_SIMULACION=true;
- PERMITIR_APIS_REALES=false;
- rutas configuradas;
- límites de coste configurados.
```

No debe:

```text
- llamar APIs reales;
- generar audios reales;
- traducir con proveedores reales;
- crear dependencias no autorizadas.
```

## 12.2. `scripts/prueba_fake_texto_traduccion_voz.py`

Responsabilidad:

```text
probar el flujo texto → traducción → voz simulada sin coste.
```

Debe comprobar:

```text
- carga de frases de prueba;
- traducción fake;
- generación fake de voz;
- medición de tiempos;
- uso de caché;
- guardado de resultados;
- respeto de límites de llamadas;
- ausencia de APIs reales.
```

---

# 13. Primer flujo permitido

La primera prueba ejecutable será:

```text
texto → traducción fake → voz fake → registro de resultado
```

No se permite todavía:

```text
micrófono
transcripción real
DeepL
ElevenLabs
OpenAI
Google Cloud
FastAPI
HTMX
WebSockets
```

---

# 14. Frases iniciales de laboratorio

### Frases de prueba — Español → Rumano

1. Estoy muy feliz de estar aquí con ustedes.
2. ¿Pueden hablar un poco más despacio, por favor?
3. La comida está muy rica, muchas gracias por recibirme.
4. Voy a usar el traductor para entenderlos mejor.
5. Para mí es importante poder comunicarme mejor con ustedes porque somos familia.

### Frases de prueba — Rumano → Español

1. Ne bucurăm că ești aici cu noi.
2. Vrei să mănânci ceva o să bei o cafea?
3. Nu îți face griji, poți vorbi încet.
4. Familia este foarte importantă para noi.
5. Dacă nu înțelegi, putem repeta.

Estas frases son suficientes para probar el flujo sin coste.

Las listas extendidas de prueba deben gestionarse en `07_tests_validacion_y_go_no_go.md`.

---

# 15. Variables oficiales del laboratorio

Las variables oficiales de entorno, límites, timeouts y reglas de coste están centralizadas en:

- `04_seguridad_privacidad_y_costes.md`

Este documento no debe duplicar la lista completa para evitar inconsistencias.

---

# 16. Comandos base con `uv`

## 16.1. Crear laboratorio

```bash
mkdir traductor_rumano_lab
cd traductor_rumano_lab
uv init
uv venv
```

## 16.2. Activar entorno

En Linux / WSL:

```bash
source .venv/bin/activate
```

En Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 16.3. Instalar dependencias permitidas

```bash
uv add python-dotenv pydantic pydantic-settings httpx tenacity
uv add --dev pytest pytest-asyncio ruff
```

## 16.4. Validar entorno

```bash
uv run python --version
uv run ruff check .
uv run pytest
```

---

# 17. Criterio de cierre de Fase 1 del laboratorio

La primera fase del laboratorio se considera completa cuando:

```text
[ ] El laboratorio se crea con uv.
[ ] El entorno se valida.
[ ] MODO_SIMULACION=true por defecto.
[ ] PERMITIR_APIS_REALES=false por defecto.
[ ] La prueba fake texto→traducción→voz funciona.
[ ] Se registran mediciones fake.
[ ] Se escribe o consulta cache_frases.json.
[ ] Ruff pasa sin errores.
[ ] Pytest pasa con tests básicos.
[ ] No se realizó ninguna llamada a API externa.
```

---

# 18. Criterio para pasar a APIs reales

No se permite usar APIs reales hasta que la fase fake haya pasado.

Para iniciar pruebas reales controladas deben cumplirse:

```text
[ ] Fase fake completada.
[ ] Límites de coste configurados.
[ ] Caché activa.
[ ] Timeouts configurados.
[ ] Reintentos limitados.
[ ] Variables de API configuradas localmente.
[ ] Autorización explícita para pruebas reales.
```

Variables requeridas para pruebas reales:

```env
MODO_SIMULACION=false
PERMITIR_APIS_REALES=true
```

---

# 19. Pruebas reales mínimas posteriores

Una vez autorizado, el orden económico será:

```text
1. prueba_real_traduccion_minima.py
2. prueba_gtts_texto_voz.py
3. prueba_real_voz_minima.py
4. prueba_pipeline_real_minimo.py
```

## 19.1. Primera prueba real de traducción

Solo debe usar pocas frases.

```text
máximo 3 frases ES→RO
máximo 3 frases RO→ES
```

## 19.2. Primera prueba real de voz

Solo debe generar pocos audios.

```text
máximo 1 frase en rumano
máximo 1 frase en español
```

## 19.3. Pipeline real mínimo

Solo debe probar:

```text
1 frase ES→RO
1 frase RO→ES
```

---

# 20. Elementos que se validan en Fase 0

La Fase 0 valida:

```text
- estructura;
- configuración;
- flujo;
- modo simulación;
- límites;
- caché;
- registro de resultados;
- traducción real mínima;
- voz real mínima;
- latencia aproximada;
- coste controlado;
- decisión GO / GO parcial / NO-GO.
```

---

# 21. Elementos que no se validan todavía

La Fase 0 no valida completamente:

```text
- UX final;
- uso continuo en móvil;
- WebSockets;
- streaming real;
- app nativa;
- uso multiusuario;
- persistencia avanzada;
- despliegue cloud;
- rendimiento bajo carga.
```

Estos temas pertenecen a fases posteriores.

---

# 22. Relación con otros documentos

Para objetivo funcional:

```text
01_contexto_y_objetivo_funcional.md
```

Para arquitectura técnica:

```text
02_arquitectura_tecnica.md
```

Para seguridad, privacidad y control de costes:

```text
04_seguridad_privacidad_y_costes.md
```

Para proveedores y fallbacks:

```text
06_proveedores_adaptadores_y_fallbacks.md
```

Para pruebas, plantillas y GO/NO-GO:

```text
07_tests_validacion_y_go_no_go.md
```

Para implementación secuencial:

```text
08_plan_implementacion_desarrolladores.md
```

---

# 23. Criterio de calidad de este documento

Este documento se considera correcto si:

```text
[ ] Define qué es Fase 0.
[ ] Define el laboratorio.
[ ] Define modo simulación.
[ ] Define adaptadores fake.
[ ] Define estructura inicial.
[ ] Define dependencias permitidas.
[ ] Define dependencias no permitidas.
[ ] Define scripts iniciales.
[ ] Define criterios para pasar a APIs reales.
[ ] No repite arquitectura completa.
[ ] No repite seguridad detallada.
[ ] No repite pruebas completas.
```

---

# 24. Estado

```text
Estado: Borrador inicial aprobado para revisión.
```
