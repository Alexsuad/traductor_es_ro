# 04 — Seguridad, privacidad y costes

## Proyecto

**Traductor Familiar Español-Rumano**

## Propósito de este documento

Este documento define las reglas de seguridad, privacidad y control de costes del proyecto.

Su objetivo es evitar tres riesgos principales:

```text
1. Exponer claves o credenciales.
2. Guardar información familiar sensible sin control.
3. Generar gastos innecesarios en APIs externas.
```

Este documento no describe la arquitectura completa, la experiencia visual del frontend ni el plan de implementación paso a paso. Esos temas pertenecen a otros documentos.

---

# 1. Pregunta principal que responde este documento

```text
¿Cómo protegemos las claves, los datos personales y el presupuesto durante las pruebas y el desarrollo?
```

---

# 2. Principio general de seguridad

El proyecto debe funcionar bajo el principio:

```text
Seguro por defecto, económico por defecto y privado por defecto.
```

Esto significa:

```text
- Las APIs reales están bloqueadas por defecto.
- Las claves no se suben al repositorio.
- Los audios familiares reales no se guardan por defecto.
- Las llamadas externas tienen límites.
- Los logs no contienen información sensible.
- El sistema debe poder fallar sin filtrar datos ni generar gastos inesperados.
```

---

# 3. Variables de control obligatorias

El archivo `.env.example` debe incluir variables de control económico y de seguridad.

```env
# --- CONTROL GLOBAL ---
MODO_SIMULACION=true
PERMITIR_APIS_REALES=false

# --- CONFIGURACIÓN DE IDIOMAS ---
IDIOMAS_HABILITADOS=es,ro,en
IDIOMA_PRINCIPAL_USUARIO=es
IDIOMA_FAMILIA_PRINCIPAL=ro
IDIOMA_PUENTE=en
USAR_IDIOMA_PUENTE=false
PERMITIR_PRUEBAS_CON_INGLES=true

# --- CONFIGURACIÓN DE MOTORES ---
MODO_MOTOR=AUTO
PERMITIR_TRANSLATE_REALTIME=false
PERMITIR_WHISPER_REALTIME=false
PERMITIR_PIPELINE_MODULAR=true
PERMITIR_MODO_COMBINADO=false

# --- LÍMITES DE USO (DIARIOS/POR EJECUCIÓN) ---
MAX_LLAMADAS_POR_EJECUCION=10
MAX_CARACTERES_POR_FRASE=300
MAX_FRASES_POR_PRUEBA=5

MAX_MINUTOS_TRANSLATE_DIA=10
MAX_MINUTOS_WHISPER_DIA=10
MAX_MINUTOS_MODO_COMBINADO_DIA=5
MAX_LLAMADAS_PIPELINE_DIA=50

# --- OPERACIÓN Y CACHÉ ---
USAR_CACHE=true
RUTA_CACHE_FRASES=resultados/cache_frases.json
RUTA_RESULTADOS=resultados
RUTA_AUDIOS_SALIDA=audios_salida

REINTENTOS_MAXIMOS=2
TIMEOUT_TRADUCCION_SEGUNDOS=3
TIMEOUT_VOZ_SEGUNDOS=5
TIMEOUT_TRANSCRIPCION_SEGUNDOS=5

DETENER_SI_SUPERA_LIMITE=true
```

Las claves reales de proveedores se agregan solo en el archivo `.env` local, nunca en `.env.example` con valores reales.

---

# 4. Gestión de claves y credenciales

## 4.1. Archivo permitido para claves reales

Las claves reales solo deben guardarse en:

```text
.env
```

## 4.2. Archivos prohibidos para claves reales

No se deben colocar claves reales en:

```text
README.md
docs/
scripts/
src_lab/
resultados/
audios_salida/
capturas de pantalla
mensajes de chat
commits de Git
```

## 4.3. `.env.example`

El archivo `.env.example` sí puede estar versionado, pero solo con nombres vacíos.

Ejemplo:

```env
DEEPL_API_KEY=
ELEVENLABS_API_KEY=
OPENAI_API_KEY=
GOOGLE_APPLICATION_CREDENTIALS=
```

## 4.4. Credenciales JSON de Google

Si en fases posteriores se usa Google Cloud, cualquier archivo de credenciales JSON debe quedar fuera del repositorio.

Patrones recomendados para `.gitignore`:

```gitignore
*credentials*.json
google_*.json
service_account*.json
```

---

# 5. `.gitignore` obligatorio

El proyecto debe excluir archivos sensibles y temporales.

Contenido mínimo recomendado:

```gitignore
.env
.venv/
__pycache__/
*.pyc

.pytest_cache/
.ruff_cache/

*.mp3
*.wav
*.m4a

audios_salida/*.mp3
audios_salida/*.wav
audios_salida/*.m4a

resultados/*.jsonl
resultados/*.log

*credentials*.json
google_*.json
service_account*.json
```

## 5.1. Archivos que sí pueden versionarse

```text
.env.example
README.md
docs/*.md
scripts/*.py
src_lab/**/*.py
resultados/mediciones_fase_0.md
resultados/errores_fase_0.md
audios_salida/README.md
```

## 5.2. Archivos que no deben versionarse

```text
.env
audios familiares reales
audios generados con contenido sensible
logs con payloads completos
credenciales de proveedores
archivos temporales con datos personales
```

---

# 6. Modo simulación y APIs reales

## 6.1. Valores por defecto

El sistema debe iniciar con:

```env
MODO_SIMULACION=true
PERMITIR_APIS_REALES=false
```

## 6.2. Regla de seguridad

Si `MODO_SIMULACION=true`, el sistema debe usar adaptadores fake.

Si `PERMITIR_APIS_REALES=false`, el sistema no debe llamar APIs reales aunque existan claves configuradas.

## 6.3. Doble confirmación para uso real

Para llamar APIs reales deben cumplirse ambas condiciones:

```env
MODO_SIMULACION=false
PERMITIR_APIS_REALES=true
```

Si una de las dos condiciones no se cumple, el sistema debe:

```text
- detener la ejecución, o
- usar adaptadores fake, según el tipo de prueba.
```

## 6.4. Motivo

La doble confirmación evita gasto accidental y protege al equipo de ejecutar pruebas reales sin intención.

---

# 7. Control de costes

## 7.1. Riesgo principal

El mayor riesgo económico es ejecutar scripts que llamen APIs externas muchas veces sin control.

Ejemplos peligrosos:

```text
- procesar 50 frases sin confirmación;
- regenerar audios ya existentes;
- repetir pruebas con las mismas frases;
- usar reintentos excesivos;
- procesar audios largos;
- dejar un bucle llamando APIs por error.
```

## 7.2. Límites obligatorios

El sistema debe respetar:

```env
MAX_LLAMADAS_POR_EJECUCION=10
MAX_CARACTERES_POR_FRASE=300
MAX_FRASES_POR_PRUEBA=5
REINTENTOS_MAXIMOS=2
DETENER_SI_SUPERA_LIMITE=true
```

## 7.3. Regla de parada

Si se supera un límite configurado, la ejecución debe detenerse.

No se debe continuar automáticamente.

## 7.4. Confirmación antes de pruebas grandes

Si una prueba requiere procesar más frases que el límite configurado, debe tratarse como una fase nueva y requerir autorización explícita.

---

# 8. Reintentos y timeouts

## 8.1. Timeouts obligatorios

Toda llamada externa debe tener timeout explícito.

Valores iniciales recomendados:

```env
TIMEOUT_TRADUCCION_SEGUNDOS=3
TIMEOUT_VOZ_SEGUNDOS=5
TIMEOUT_TRANSCRIPCION_SEGUNDOS=5
```

## 8.2. Reintentos limitados

Valor inicial aprobado:

```env
REINTENTOS_MAXIMOS=2
```

Regla:
ningún adaptador puede reintentar indefinidamente.

Si se alcanza el límite de reintentos, el sistema debe:

1. registrar el error técnico,
2. devolver un mensaje comprensible,
3. usar fallback si existe,
4. detener la ejecución si `DETENER_SI_SUPERA_LIMITE=true`.

## 8.3. Prohibido

```text
- reintentos infinitos;
- timeouts por defecto sin revisar;
- llamadas externas sin límite;
- esperar indefinidamente a un proveedor;
- bloquear la app completa por una API lenta.
```

## 8.4. Relación con arquitectura

Los detalles de adaptadores y fallbacks se documentan en:

```text
06_proveedores_adaptadores_y_fallbacks.md
```

---

# 9. Caché local simple

## 9.1. Decisión

El sistema debe usar caché local cuando `USAR_CACHE=true`.

Ubicación inicial:

```env
RUTA_CACHE_FRASES=resultados/cache_frases.json
```

## 9.2. Objetivo

Evitar gastar dinero y tiempo repitiendo traducciones o audios ya generados.

## 9.3. Qué puede guardar la caché

```text
texto_original
texto_normalizado
idioma_origen
idioma_destino
texto_traducido
proveedor_usado
ruta_audio_generado, si existe
fecha_generacion
```

## 9.4. Qué no debe guardar la caché

```text
conversaciones familiares reales completas
datos médicos
datos económicos
direcciones
teléfonos
documentos personales
API keys
tokens
payloads completos de proveedores
```

## 9.5. Regla

Antes de llamar a una API real, revisar la caché.

Si existe resultado válido:

```text
usar caché
no llamar API
```

---

# 10. Privacidad de audios

## 10.1. Audios permitidos en Fase 0

Durante las pruebas iniciales solo se permiten audios controlados.

Ejemplos:

```text
Alex leyendo frases de prueba.
Una voz TTS leyendo frases rumanas.
Una persona rumana leyendo frases neutrales con permiso.
```

## 10.2. Audios prohibidos en Fase 0

No se deben usar ni guardar:

```text
conversaciones familiares reales
discusiones privadas
datos médicos
datos económicos
datos personales de terceros
audio de personas sin aviso
audio de menores sin autorización explícita
```

## 10.3. Duración máxima recomendada

```text
Audio recomendado: 3 a 8 segundos.
Máximo por archivo: 15 segundos.
```

## 10.4. Consentimiento

Si una persona colabora grabando frases en rumano, debe saber:

```text
- que el audio se usará para probar una herramienta de traducción;
- que no debe subirse al repositorio;
- que puede eliminarse cuando termine la prueba;
- que no se usará para entrenar modelos propios.
```

---

# 11. Privacidad de texto

## 11.1. Texto permitido

Se puede guardar:

```text
frases de prueba
traducciones generadas
tiempos de ejecución
proveedor usado
estado de prueba
observaciones técnicas
```

## 11.2. Texto prohibido

No se debe guardar:

```text
nombres completos de familiares
direcciones
teléfonos
documentos oficiales
datos médicos reales
temas íntimos
conversaciones completas
correos electrónicos
credenciales
```

## 11.3. Resultados de pruebas

Los resultados deben ser técnicos y no sensibles.

Ejemplo correcto:

```text
ES_RO_01 | deepl_fake | 14 ms | OK
```

Ejemplo incorrecto:

```text
Transcripción completa de una conversación familiar privada.
```

---

# 12. Política de logs

## 12.1. Logs permitidos

Se permite registrar:

```text
fecha
id de prueba
proveedor
latencia en ms
estado
error técnico resumido
modo_simulacion
uso_cache
```

## 12.2. Logs prohibidos

No se debe registrar:

```text
API keys
tokens
headers completos
payloads completos
audios en base64
conversaciones privadas completas
respuestas completas de proveedores si contienen datos sensibles
```

## 12.3. Niveles de log recomendados

```text
INFO: ejecución normal.
WARNING: latencia alta, fallback usado o caché faltante.
ERROR: fallo de proveedor, configuración inválida o límite superado.
```

No usar `DEBUG` con payloads completos durante pruebas con APIs reales.

---

# 13. Política de conservación de datos

## 13.1. Durante Fase 0

```text
Audios de salida: temporales.
Audios de entrada: solo frases controladas.
Resultados: se conservan si no contienen datos sensibles.
Errores: se conservan si no contienen payloads privados.
Caché: se conserva si contiene solo frases de prueba.
```

## 13.2. Después de cada sesión de pruebas

Revisar:

```text
[ ] No se generaron archivos fuera de carpetas previstas.
[ ] No se guardaron claves.
[ ] No se guardaron conversaciones privadas.
[ ] Los audios generados innecesarios fueron eliminados.
[ ] Los logs no contienen payloads sensibles.
[ ] Se registró el número aproximado de llamadas.
```

## 13.3. Al cerrar Fase 0

```text
[ ] Borrar audios de salida innecesarios.
[ ] Revisar audios de entrada.
[ ] Conservar solo frases de prueba no sensibles.
[ ] Conservar mediciones limpias.
[ ] Borrar logs temporales.
[ ] Verificar que no hay claves en Git.
```

---

# 14. Errores críticos de seguridad

Los siguientes errores deben detener la ejecución:

```text
falta .env cuando es obligatorio;
MODO_SIMULACION=false y PERMITIR_APIS_REALES=false;
intento de usar API real sin autorización;
límite de llamadas superado;
límite de caracteres superado;
audio supera duración o tamaño máximo;
proveedor devuelve error de autenticación;
archivo de credenciales no encontrado;
clave API vacía en modo real;
```

---

# 15. Fallbacks permitidos por seguridad y coste

Si una API externa falla, el sistema puede usar fallback.

Ejemplos:

```text
voz premium falla → usar voz básica o solo texto;
traducción real bloqueada → usar fake en laboratorio;
API real no autorizada → detener o simular;
caché existe → usar caché;
```

El fallback no debe ocultar errores importantes. Debe registrarse que se usó fallback.

---

# 16. Checklist antes de ejecutar pruebas

Antes de ejecutar cualquier prueba:

```text
[ ] `.env.example` no contiene claves reales.
[ ] `.env` no está versionado.
[ ] `.gitignore` excluye `.env`.
[ ] `MODO_SIMULACION` está definido.
[ ] `PERMITIR_APIS_REALES` está definido.
[ ] Los límites de llamadas están definidos.
[ ] Los límites de caracteres están definidos.
[ ] Los timeouts están definidos.
[ ] Los reintentos máximos están definidos.
[ ] La caché está configurada.
[ ] No se usarán audios sensibles.
[ ] No se procesarán frases fuera del alcance permitido.
```

---

# 17. Checklist después de ejecutar pruebas

Después de ejecutar pruebas:

```text
[ ] No se expusieron claves.
[ ] No se guardaron audios familiares reales.
[ ] No se guardaron conversaciones privadas.
[ ] No se superaron límites de llamadas.
[ ] No se superaron límites de caracteres.
[ ] Se registraron errores de forma segura.
[ ] Se registró si se usó caché.
[ ] Se registró si se usó fallback.
[ ] Se limpiaron archivos temporales innecesarios.
```

---

# 18. Reglas para fases futuras

## 18.1. Frontend

El frontend nunca debe recibir API keys.

Todas las llamadas a proveedores externos deben pasar por backend.

## 18.2. WebSockets

Si en fases futuras se usan WebSockets:

```text
- limitar tamaño de mensajes;
- limitar duración de sesión;
- cerrar conexiones inactivas;
- validar tipo de archivo/audio;
- evitar guardar audio por defecto.
```

## 18.3. SQLite o persistencia futura

Si se agrega persistencia:

```text
- no guardar conversaciones completas por defecto;
- no bloquear el flujo principal;
- separar métricas técnicas de datos personales;
- permitir limpieza de historial si se implementa historial.
```

---

# 19. Relación con otros documentos

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

Para proveedores y fallbacks:

```text
06_proveedores_adaptadores_y_fallbacks.md
```

Para pruebas y criterios GO/NO-GO:

```text
07_tests_validacion_y_go_no_go.md
```

Para implementación por fases:

```text
08_plan_implementacion_desarrolladores.md
```

---

# 20. Criterio de calidad de este documento

Este documento se considera correcto si:

```text
[ ] Define protección de claves.
[ ] Define `.env` y `.env.example`.
[ ] Define modo simulación.
[ ] Define bloqueo de APIs reales por defecto.
[ ] Define límites de llamadas.
[ ] Define límites de caracteres.
[ ] Define timeouts y reintentos.
[ ] Define política de audios.
[ ] Define política de texto sensible.
[ ] Define política de logs.
[ ] Define caché local simple.
[ ] Define checklists pre y post prueba.
[ ] No repite arquitectura completa.
[ ] No repite plan de implementación completo.
```

---

# 21. Estado

```text
Estado: Borrador inicial aprobado para revisión.
```
