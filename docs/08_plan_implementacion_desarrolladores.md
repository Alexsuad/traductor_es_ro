# File: docs/08_plan_implementacion_desarrolladores.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Hoja de ruta detallada para la implementación técnica del proyecto.
# Rol: Guía de desarrollo y fases de construcción.
# ──────────────────────────────────────────────────────────────────────

# 08 — Plan de implementación para desarrolladores

## Proyecto

**Traductor Familiar Español-Rumano**

## Propósito de este documento

Este documento define el orden de implementación del proyecto para el equipo de desarrollo.

Su objetivo es evitar improvisación, sobreingeniería y gasto innecesario. El equipo debe avanzar por fases pequeñas, verificables y con criterios claros de cierre.

Este documento no repite la arquitectura completa, la UX detallada, la seguridad completa ni las plantillas completas de pruebas. Para esos temas se referencian los documentos correspondientes.

---

# 1. Pregunta principal que responde este documento

```text
¿Qué debe construir el equipo, en qué orden, con qué archivos, con qué dependencias y bajo qué criterios de cierre?
```

---

# 2. Principio de implementación

El desarrollo debe seguir este principio:

```text
Primero laboratorio sin coste. Después pruebas reales mínimas. Finalmente MVP web.
```

No se debe construir la app completa antes de validar el flujo técnico y económico.

---

# 3. Reglas generales de desarrollo

## 3.1. Regla de fases

No se debe iniciar una fase sin cerrar la anterior.

Cada fase debe tener:

```text
objetivo
alcance
archivos permitidos
dependencias permitidas
comandos de validación
criterio de cierre
```

## 3.2. Reglas de coste y variables oficiales

Las variables oficiales de entorno, límites, timeouts y reglas de coste están centralizadas en:

- `04_seguridad_privacidad_y_costes.md`

Este documento no debe duplicar la lista completa para evitar inconsistencias.

## 3.3. Regla de simplicidad

No instalar dependencias que no pertenezcan a la fase actual.

## 3.4. Regla de no duplicidad

Si una decisión técnica está definida en otro documento, no debe copiarse completa aquí. Solo se referencia.

## 3.5. Regla de validación

Toda fase debe cerrar con:

```bash
uv run ruff check .
uv run pytest
```

Si no hay tests todavía en fases iniciales, debe documentarse y agregarse el primer test tan pronto exista lógica propia.

---

# 4. Resumen de fases

```text
Fase 1 — Laboratorio con modo simulación.
Fase 2 — Pruebas reales mínimas de traducción.
Fase 3 — Pruebas de voz básica y premium.
Fase 4 — Pipeline texto → traducción → voz.
Fase 5 — Transcripción con audios cortos.
Fase 6 — MVP web con FastAPI + Jinja2 + HTMX.
Fase 7 — Endurecimiento de seguridad y privacidad.
Fase 8 — Pruebas reales de uso familiar.
```

---

# 5. Fase 1 — Laboratorio con modo simulación

## 5.1. Objetivo

Crear el laboratorio mínimo sin APIs reales, con arquitectura modular.

Debe validar:

```text
estructura modular
configuración de idiomas (es, ro, en)
modo motor (AUTO, Translate, Whisper)
modo simulación
adaptadores fake (multi-idioma)
caché simple
registro de resultados
prueba fake texto → traducción → voz
```

## 5.2. Alcance

Incluye:

```text
- proyecto con uv;
- estructura inicial;
- settings_lab.py;
- puertos mínimos;
- traductor fake;
- voz fake;
- caché simple;
- medición de tiempos;
- guardado de resultados;
- script verificar_entorno.py;
- script prueba_fake_texto_traduccion_voz.py.
```

No incluye:

```text
- APIs reales;
- DeepL;
- ElevenLabs;
- OpenAI;
- Google Cloud;
- FastAPI;
- HTMX;
- WebSockets;
- SQLite;
- micrófono;
- transcripción real.
```

## 5.3. Estructura permitida

```text
traductor_rumano_lab/
├── .env.example
├── .gitignore
├── pyproject.toml
├── README.md
├── resultados/
│   ├── mediciones_fase_0.md
│   ├── errores_fase_0.md
│   └── cache_frases.json
├── audios_salida/
│   └── README.md
├── scripts/
│   ├── verificar_entorno.py
│   └── prueba_fake_texto_traduccion_voz.py
└── src_lab/
    ├── __init__.py
    ├── config/
    │   ├── __init__.py
    │   └── settings_lab.py
    ├── ports/
    │   ├── __init__.py
    │   ├── puerto_traductor_texto.py
    │   └── puerto_generador_voz.py
    ├── providers_fake/
    │   ├── __init__.py
    │   ├── traductor_fake.py
    │   └── voz_fake.py
    ├── cache/
    │   ├── __init__.py
    │   └── cache_frases_simple.py
    └── utils/
        ├── __init__.py
        ├── medir_tiempos.py
        ├── normalizar_texto.py
        └── guardar_resultados.py
```

## 5.4. Dependencias permitidas

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

## 5.5. Dependencias prohibidas en esta fase

```text
deepl
elevenlabs
openai
google-cloud-translate
gtts
fastapi
uvicorn
jinja2
sqlmodel
sqlalchemy
aiosqlite
pydub
soundfile
```

## 5.6. Comandos iniciales

```bash
mkdir traductor_rumano_lab
cd traductor_rumano_lab
uv init
uv venv
uv add python-dotenv pydantic pydantic-settings httpx tenacity
uv add --dev pytest pytest-asyncio ruff
```

Activación en Linux / WSL:

```bash
source .venv/bin/activate
```

Activación en Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

## 5.7. Comandos de validación

```bash
uv run python --version
uv run ruff check .
uv run pytest
uv run python scripts/verificar_entorno.py
uv run python scripts/prueba_fake_texto_traduccion_voz.py
```

## 5.8. Criterio de cierre

La Fase 1 se cierra cuando:

```text
[ ] El laboratorio existe con estructura modular.
[ ] El entorno se crea con uv.
[ ] IDIOMAS_HABILITADOS=es,ro,en configurado en fake.
[ ] MODO_MOTOR=AUTO simulado correctamente.
[ ] MODO_SIMULACION=true.
[ ] PERMITIR_APIS_REALES=false.
[ ] verificar_entorno.py pasa.
[ ] prueba_fake_texto_traduccion_voz.py pasa con rutas candidatas.
[ ] Se escribe o consulta cache_frases.json.
[ ] Se registran mediciones fake.
[ ] Ruff pasa.
[ ] Pytest pasa.
[ ] No se hizo ninguna llamada real a APIs externas.
```

---

# 6. Fase 2 — Pruebas reales mínimas de traducción

## 6.1. Objetivo

Validar traducción real español ↔ rumano con pocas frases y coste controlado.

## 6.2. Precondición

Fase 1 cerrada.

Variables requeridas:

```env
MODO_SIMULACION=false
PERMITIR_APIS_REALES=true
USAR_CACHE=true
MAX_FRASES_POR_PRUEBA=5
MAX_LLAMADAS_POR_EJECUCION=10
REINTENTOS_MAXIMOS=2
```

## 6.3. Alcance

Incluye:

```text
- instalar un proveedor de traducción real;
- crear adaptador real de traducción;
- probar máximo 3 frases ES→RO;
- probar máximo 3 frases RO→ES;
- registrar latencia y calidad;
- usar caché antes de proveedor.
```

No incluye:

```text
- voz real;
- transcripción;
- frontend;
- WebSockets;
- base de datos.
```

## 6.4. Dependencias permitidas

Una de estas, según decisión:

```text
deepl
google-cloud-translate
```

No instalar ambas si la prueba inicial solo requiere una.

## 6.5. Archivos permitidos

```text
src_lab/providers_real/traductor_deepl.py
src_lab/providers_real/traductor_google.py, si aplica
scripts/prueba_real_traduccion_minima.py
```

## 6.6. Criterio de cierre

```text
[ ] La traducción ES→RO funciona con frases cortas.
[ ] La traducción RO→ES funciona con frases cortas.
[ ] Se registra latencia.
[ ] Se registra calidad manual.
[ ] Se respeta el límite de llamadas.
[ ] Se usa caché cuando aplica.
[ ] No se superan límites de coste.
[ ] Ruff pasa.
[ ] Pytest pasa.
```

---

# 7. Fase 3 — Pruebas de voz básica y premium

## 7.1. Objetivo

Validar generación de audio para rumano y español.

## 7.2. Precondición

Fase 2 cerrada.

## 7.3. Alcance

Incluye:

```text
- probar voz básica o fallback;
- probar voz premium mínima;
- generar pocos audios;
- guardar rutas de audio;
- registrar latencia y calidad de voz;
- comprobar que el texto no se bloquea si falla el audio.
```

## 7.4. Orden recomendado

```text
1. Probar voz fake o fallback.
2. Probar gTTS si se autoriza.
3. Probar ElevenLabs con 1 frase rumana y 1 frase española.
```

## 7.5. Dependencias permitidas

Según la prueba:

```text
gtts
elevenlabs
```

No instalar ElevenLabs hasta que exista autorización para prueba premium mínima.

## 7.6. Archivos permitidos

```text
src_lab/providers_real/voz_gtts.py
src_lab/providers_real/voz_elevenlabs.py
scripts/prueba_gtts_texto_voz.py
scripts/prueba_real_voz_minima.py
```

## 7.7. Criterio de cierre

```text
[ ] Se genera o simula audio español.
[ ] Se genera o simula audio rumano.
[ ] Se registra latencia de voz.
[ ] Se evalúa calidad de voz.
[ ] Si falla voz premium, se mantiene texto.
[ ] Si aplica, gTTS funciona como fallback.
[ ] No se regeneran audios innecesarios.
[ ] Ruff pasa.
[ ] Pytest pasa.
```

---

# 8. Fase 4 — Pipeline texto → traducción → voz

## 8.1. Objetivo

Validar el primer flujo real útil sin micrófono.

```text
texto → traducción → voz
```

## 8.2. Precondición

Fase 2 y Fase 3 cerradas.

## 8.3. Alcance

Incluye:

```text
- una frase ES→RO;
- una frase RO→ES;
- traducción real;
- audio real o fallback;
- medición de tiempo total;
- registro de resultados;
- uso de caché.
```

No incluye:

```text
- micrófono;
- transcripción;
- frontend web;
- WebSockets.
```

## 8.4. Archivo permitido

```text
scripts/prueba_pipeline_real_minimo.py
```

## 8.5. Criterio de cierre

```text
[ ] El pipeline ES→RO funciona.
[ ] El pipeline RO→ES funciona.
[ ] El texto aparece antes que audio.
[ ] El audio no bloquea el resultado.
[ ] Se registra latencia total.
[ ] Se registra fallback si ocurre.
[ ] Se decide si se pasa a transcripción.
[ ] Ruff pasa.
[ ] Pytest pasa.
```

---

# 9. Fase 5 — Transcripción con audios cortos

## 9.1. Objetivo

Validar voz → texto para español y rumano.

## 9.2. Precondición

Fase 4 cerrada.

## 9.3. Alcance

Incluye:

```text
- audios cortos controlados;
- transcripción español;
- transcripción rumano;
- comparación contra texto esperado;
- medición de latencia;
- evaluación manual de calidad.
```

No incluye:

```text
- conversaciones familiares reales;
- audios largos;
- escucha continua;
- streaming avanzado.
```

## 9.4. Dependencias permitidas

Según proveedor elegido:

```text
elevenlabs
openai
```

## 9.5. Archivos permitidos

```text
src_lab/providers_real/transcriptor_elevenlabs.py
src_lab/providers_real/transcriptor_openai.py
scripts/prueba_transcripcion_audio_corto.py
audios_entrada/README.md
audios_entrada/es/
audios_entrada/ro/
```

## 9.6. Criterio de cierre

```text
[ ] Transcripción español >= 4/5.
[ ] Transcripción rumano >= 3/5.
[ ] Audios no superan 15 segundos.
[ ] No se usan conversaciones familiares reales.
[ ] Se registra latencia.
[ ] Se decide si se pasa a pipeline con audio.
[ ] Ruff pasa.
[ ] Pytest pasa.
```

---

# 10. Fase 6 — MVP web con FastAPI + Jinja2 + HTMX

## 10.1. Objetivo

Crear una interfaz web móvil mínima después de validar el pipeline.

## 10.2. Precondición

Fases 1 a 5 cerradas o decisión GO parcial documentada.

## 10.3. Alcance

Incluye:

```text
- FastAPI;
- Jinja2;
- HTMX;
- HTML/CSS simple;
- JavaScript mínimo para micrófono/audio;
- pantalla con dos direcciones;
- texto traducido visible;
- audio opcional;
- errores comprensibles.
```

No incluye:

```text
- login;
- dashboard;
- multiusuario;
- base de datos avanzada;
- app nativa;
- WebSockets complejos, salvo decisión posterior.
```

## 10.4. Dependencias permitidas

```text
fastapi
uvicorn
jinja2
python-multipart
```

HTMX no requiere instalación Python; se incorporará como recurso frontend según decisión del equipo.

## 10.5. Estructura permitida

```text
app_web/
├── main.py
├── routes/
│   ├── __init__.py
│   └── traduccion_routes.py
├── templates/
│   ├── index.html
│   └── partials/
│       ├── resultado_traduccion.html
│       └── error_mensaje.html
└── static/
    ├── css/
    │   └── styles.css
    └── js/
        └── mic_recorder.js
```

## 10.6. Criterio de cierre

```text
[ ] La página carga en navegador móvil.
[ ] Existen botones ES→RO y RO→ES.
[ ] El texto traducido se muestra.
[ ] El audio es opcional.
[ ] Los errores son comprensibles.
[ ] No se exponen API keys al frontend.
[ ] JavaScript se limita a micrófono/audio.
[ ] Ruff pasa.
[ ] Pytest pasa.
```

---

# 11. Fase 7 — Endurecimiento de seguridad y privacidad

## 11.1. Objetivo

Revisar que el MVP no exponga claves, datos sensibles ni costes incontrolados.

## 11.2. Alcance

Incluye:

```text
- revisión de .env y .gitignore;
- revisión de logs;
- límites de llamadas;
- límites de tamaño de audio;
- revisión de caché;
- mensajes de error seguros;
- limpieza de archivos temporales;
- verificación de que frontend no recibe claves.
```

## 11.3. Criterio de cierre

```text
[ ] .env no está versionado.
[ ] No hay claves en docs ni código.
[ ] No hay audios familiares reales guardados.
[ ] Logs no contienen payloads sensibles.
[ ] Límites de coste activos.
[ ] Timeouts activos.
[ ] Reintentos limitados.
[ ] Fallbacks registrados.
[ ] Ruff pasa.
[ ] Pytest pasa.
```

---

# 12. Fase 8 — Pruebas reales de uso familiar

## 12.1. Objetivo

Validar si la herramienta sirve en una situación cercana al uso real.

## 12.2. Alcance

Incluye:

```text
- pruebas con frases familiares;
- pruebas desde móvil;
- pruebas con WiFi;
- pruebas con datos móviles si aplica;
- pruebas con ruido moderado;
- evaluación de comodidad;
- decisión final de MVP.
```

No incluye:

```text
- conversaciones privadas largas;
- uso sin límites;
- grabación continua;
- publicación pública.
```

## 12.3. Criterio de cierre

```text
[ ] La herramienta es usable desde móvil.
[ ] La traducción escrita es clara.
[ ] El audio aporta valor o queda como opcional.
[ ] La latencia no rompe la conversación.
[ ] El coste se mantiene controlado.
[ ] Se toma decisión GO / GO parcial / NO-GO.
```

---

# 13. Orden de instalación de dependencias

No instalar todo desde el inicio.

## 13.1. Fase 1

```bash
uv add python-dotenv pydantic pydantic-settings httpx tenacity
uv add --dev pytest pytest-asyncio ruff
```

## 13.2. Fase 2

Según proveedor:

```bash
uv add deepl
```

O:

```bash
uv add google-cloud-translate
```

## 13.3. Fase 3

Según autorización:

```bash
uv add gtts
uv add elevenlabs
```

## 13.4. Fase 5

Según proveedor de transcripción:

```bash
uv add openai
```

O reutilizar:

```bash
uv add elevenlabs
```

## 13.5. Fase 6

```bash
uv add fastapi uvicorn jinja2 python-multipart
```

---

# 14. Reglas para commits

Los commits deben ser pequeños y en español.

Ejemplos:

```text
crear estructura inicial del laboratorio
agregar configuración de modo simulación
implementar adaptador fake de traducción
agregar prueba fake de texto a voz
configurar límites de coste en settings
```

No usar commits genéricos como:

```text
cambios
update
fix
cosas varias
```

---

# 15. Reglas de revisión antes de avanzar

Antes de cerrar cada fase:

```text
[ ] Revisar que no se instalaron dependencias no autorizadas.
[ ] Revisar que no hay claves reales en archivos versionables.
[ ] Revisar que no se repitió información innecesaria en docs.
[ ] Ejecutar ruff.
[ ] Ejecutar pytest.
[ ] Revisar resultados de medición.
[ ] Actualizar estado de fase.
```

---

# 16. Relación con otros documentos

Para contexto funcional:

```text
01_contexto_y_objetivo_funcional.md
```

Para arquitectura técnica:

```text
02_arquitectura_tecnica.md
```

Para laboratorio:

```text
03_plan_laboratorio_fase_0.md
```

Para seguridad y costes:

```text
04_seguridad_privacidad_y_costes.md
```

Para frontend:

```text
05_frontend_y_experiencia_usuario.md
```

Para proveedores:

```text
06_proveedores_adaptadores_y_fallbacks.md
```

Para pruebas y GO/NO-GO:

```text
07_tests_validacion_y_go_no_go.md
```

Para modelo operativo de equipos, responsabilidades y flujo de instrucciones:

```text
09_modelo_operativo_chats_y_equipos.md
```

---

# 17. Criterio de calidad de este documento

Este documento se considera correcto si:

```text
[ ] Define fases de implementación.
[ ] Define precondiciones por fase.
[ ] Define alcance por fase.
[ ] Define dependencias permitidas.
[ ] Define dependencias prohibidas cuando aplica.
[ ] Define archivos permitidos.
[ ] Define comandos de validación.
[ ] Define criterios de cierre.
[ ] Mantiene APIs reales fuera de Fase 1.
[ ] No repite arquitectura completa.
[ ] No repite UX completa.
[ ] No repite pruebas completas.
```

---

# 18. Estado

```text
Estado: Aprobado documentalmente para iniciar Fase 1 — Laboratorio con modo simulación.
```
