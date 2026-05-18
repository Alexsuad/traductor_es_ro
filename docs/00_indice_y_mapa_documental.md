# File: docs/00_indice_y_mapa_documental.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Organizar el índice maestro de toda la documentación del proyecto y el mapa de lectura.
# Rol: Índice y Mapa Documental Principal (docs/00)
# ──────────────────────────────────────────────────────────────────────

# 00 — Índice y mapa documental


## Proyecto

**Traductor Familiar Español-Rumano**

## Propósito de este documento

Este documento organiza la documentación técnica del proyecto y define cómo debe consultarse durante el desarrollo.

Su función no es explicar toda la arquitectura ni repetir el contenido de los demás documentos. Su función es servir como **mapa maestro** para que el equipo de desarrollo sepa:

* qué documento consultar,
* para qué sirve cada archivo,
* qué información pertenece a cada documento,
* en qué orden debe leerse la documentación,
* qué reglas deben seguirse para evitar duplicidad, contradicciones y desorden documental.

---

# 1. Principio rector documental

La documentación del proyecto se organizará bajo una regla principal:

```text
Un documento, una responsabilidad.
```

Cada documento debe contener solo la información necesaria para cumplir su propósito.

No se debe copiar el mismo contenido completo en varios archivos. Cuando un documento necesite apoyarse en otro, debe hacer una referencia interna clara.

Ejemplo correcto:

```text
Para detalles sobre control de costes, ver:
04_seguridad_privacidad_y_costes.md
```

Ejemplo incorrecto:

```text
Copiar toda la sección de costes dentro de arquitectura, pruebas y plan de implementación.
```

---

# 2. Estructura documental oficial

La documentación principal del proyecto se ubicará dentro de la carpeta:

```text
docs/
```

Estructura propuesta:

```text
docs/
├── 00_indice_y_mapa_documental.md
├── 01_contexto_y_objetivo_funcional.md
├── 02_arquitectura_tecnica.md
├── 03_plan_laboratorio_fase_0.md
├── 04_seguridad_privacidad_y_costes.md
├── 05_frontend_y_experiencia_usuario.md
├── 06_proveedores_adaptadores_y_fallbacks.md
├── 07_tests_validacion_y_go_no_go.md
├── 08_plan_implementacion_desarrolladores.md
└── 09_modelo_operativo_chats_y_equipos.md
```

Si el proyecto requiere registrar decisiones arquitectónicas específicas, se usará una carpeta adicional:

```text
docs/adr/
├── adr_001_pipeline_modular_y_motor_hibrido.md
├── adr_002_modo_simulacion_por_defecto.md
├── adr_003_hexagonal_solo_para_proveedores.md
├── adr_004_texto_primero_audio_despues.md
├── adr_005_frontend_fastapi_jinja_htmx.md
├── adr_006_idiomas_configurables_e_ingles_candidato.md
├── adr_007_no_elegir_proveedor_principal_sin_pruebas.md
├── adr_008_modelo_operativo_chats_y_equipos.md
└── adr_009_control_de_turnos_y_simultaneidad_experimental.md
```

Los ADR son documentos breves de decisión. No reemplazan la documentación principal.

---

# 3. Descripción de cada documento

## 3.1. `00_indice_y_mapa_documental.md`

### Pregunta que responde

```text
¿Dónde está cada cosa dentro de la documentación?
```

### Incluye

* Mapa documental.
* Propósito de cada documento.
* Orden de lectura recomendado.
* Reglas para evitar duplicidad.
* Relación entre documentos.
* Roles que consultan cada archivo.

### No incluye

* Arquitectura técnica detallada.
* Plan de implementación completo.
* Tests detallados.
* Seguridad detallada.
* Proveedores específicos en profundidad.

### Rol principal que lo consulta

* Arquitecto de software.
* Líder técnico.
* Equipo de desarrollo antes de iniciar trabajo.
* IA/agente que necesite entender la estructura documental.

---

## 3.2. `01_contexto_y_objetivo_funcional.md`

### Pregunta que responde

```text
¿Qué problema resuelve el proyecto y para quién?
```

### Incluye

* Contexto humano del proyecto.
* Objetivo funcional.
* Usuarios principales.
* Casos de uso familiares.
* Alcance del MVP modular.
* Lo que queda fuera del MVP.
* Idiomas soportados: Caso principal ES ↔ RO con arquitectura modular para EN y futuros.

### No incluye

* Stack tecnológico.
* Arquitectura de carpetas.
* Detalles de proveedores.
* Tests técnicos.
* Reglas de seguridad detalladas.

### Referencias internas

* Para arquitectura técnica, ver `02_arquitectura_tecnica.md`.
* Para validación técnica inicial, ver `03_plan_laboratorio_fase_0.md`.
* Para criterios GO/NO-GO, ver `07_tests_validacion_y_go_no_go.md`.

### Rol principal que lo consulta

* Product owner.
* Arquitecto.
* Desarrolladores nuevos en el proyecto.
* Diseñador UX.

---

## 3.3. `02_arquitectura_tecnica.md`

### Pregunta que responde

```text
¿Cómo estará diseñado técnicamente el sistema?
```

### Incluye

* Arquitectura general del sistema (Modular y Escalable).
* Motor Híbrido (`MODO_MOTOR=AUTO`): Realtime vs Pipeline.
* Pipeline principal: transcripción → traducción → voz.
* Decisión de no depender exclusivamente de un modelo speech-to-speech directo.
* Arquitectura hexagonal limitada a proveedores externos.
* Puertos y adaptadores permitidos.
* Reglas antizombi para llamadas externas.
* Estrategia de texto primero y audio después.
* Catálogo de idiomas y rutas candidatas (ES, RO, EN).
* Decisiones técnicas principales.

### No incluye

* Frases de prueba.
* Plantillas de medición.
* Costes detallados.
* Diseño visual de interfaz.
* Plan paso a paso de implementación.

### Referencias internas

* Para proveedores concretos y fallbacks, ver `06_proveedores_adaptadores_y_fallbacks.md`.
* Para seguridad y costes, ver `04_seguridad_privacidad_y_costes.md`.
* Para implementación por fases, ver `08_plan_implementacion_desarrolladores.md`.

### Rol principal que lo consulta

* Arquitecto de software.
* Backend developer.
* Revisor técnico.
* IA/agente de desarrollo.

---

## 3.4. `03_plan_laboratorio_fase_0.md`

### Pregunta que responde

```text
¿Cómo validamos técnicamente el proyecto antes de construir la app real?
```

### Incluye

* Objetivo de Fase 0.
* Laboratorio `traductor_rumano_lab`.
* Modo simulación.
* Fake adapters.
* Pruebas sin coste.
* Pruebas reales mínimas.
* Estructura del laboratorio.
* Dependencias permitidas en la primera fase.
* Dependencias no permitidas todavía.
* Criterios para pasar de laboratorio a app real.

### No incluye

* Arquitectura completa de producción.
* Frontend web final.
* WebSockets avanzados.
* SQLite como persistencia definitiva.
* Despliegue.

### Referencias internas

* Para control de costes, ver `04_seguridad_privacidad_y_costes.md`.
* Para criterios GO/NO-GO, ver `07_tests_validacion_y_go_no_go.md`.
* Para fases de implementación posteriores, ver `08_plan_implementacion_desarrolladores.md`.

### Rol principal que lo consulta

* Desarrollador backend.
* QA.
* Arquitecto.
* IA/agente encargado de crear el laboratorio.

---

## 3.5. `04_seguridad_privacidad_y_costes.md`

### Pregunta que responde

```text
¿Cómo evitamos fugas de datos, exposición de claves y gasto innecesario?
```

### Incluye

* Gestión de `.env` y `.env.example`.
* Protección de API keys.
* Variables de control económico.
* `MODO_SIMULACION=true` por defecto.
* `PERMITIR_APIS_REALES=false` por defecto.
* Límites de llamadas.
* Límites de caracteres.
* Timeouts.
* Reintentos máximos.
* Política de audios.
* Política de logs.
* Política de conservación de datos.
* Caché local simple.
* Reglas para evitar gasto accidental.

### No incluye

* Diseño de interfaz.
* Comparación extensa de proveedores.
* Plan completo de implementación.
* Arquitectura completa del backend.

### Referencias internas

* Para laboratorio de pruebas, ver `03_plan_laboratorio_fase_0.md`.
* Para proveedores y fallbacks, ver `06_proveedores_adaptadores_y_fallbacks.md`.
* Para pruebas y validaciones, ver `07_tests_validacion_y_go_no_go.md`.

### Rol principal que lo consulta

* Backend developer.
* DevOps.
* QA.
* Arquitecto.
* Responsable de control de costes.

---

## 3.6. `05_frontend_y_experiencia_usuario.md`

### Pregunta que responde

```text
¿Cómo será la interacción del usuario con la herramienta?
```

### Incluye

* Dos niveles de vista: Pantalla Familiar (Simple) vs Configuración Técnica.
* Decisión de usar FastAPI + Jinja2 + HTMX para MVP web.
* JavaScript limitado a micrófono/audio.
* Uso de MediaRecorder API.
* Interfaz móvil simple.
* Acciones: Hablo yo / Me hablan ellos.
* Texto visible antes del audio.
* Estados de carga.
* Mensajes de error comprensibles.
* Uso push-to-talk.
* Decisiones UX para reducir fricción familiar.

### No incluye

* Proveedores externos en detalle.
* Costes de APIs.
* Tests técnicos completos.
* Persistencia.
* Despliegue.

### Referencias internas

* Para arquitectura general, ver `02_arquitectura_tecnica.md`.
* Para criterios de validación UX, ver `07_tests_validacion_y_go_no_go.md`.
* Para implementación por fases, ver `08_plan_implementacion_desarrolladores.md`.

### Rol principal que lo consulta

* Frontend developer.
* Diseñador UX.
* Arquitecto.
* QA funcional.

---

## 3.7. `06_proveedores_adaptadores_y_fallbacks.md`

### Pregunta que responde

```text
¿Qué proveedor se usa para cada función y cómo se reemplaza si falla?
```

### Incluye

* Proveedores de transcripción.
* Proveedores de traducción.
* Proveedores de voz.
* Adaptadores fake.
* Fallbacks.
* Timeouts por tipo de proveedor.
* Reintentos permitidos.
* Cuándo usar DeepL.
* Cuándo usar Google Cloud Translation.
* Cuándo usar OpenAI texto.
* Cuándo usar ElevenLabs.
* Cuándo usar gTTS.
* Criterios para cambiar de proveedor.

### No incluye

* Objetivo humano del proyecto.
* UX visual.
* Plan de fases completo.
* Plantillas de medición completas.

### Referencias internas

* Para arquitectura de puertos y adaptadores, ver `02_arquitectura_tecnica.md`.
* Para control de costes, ver `04_seguridad_privacidad_y_costes.md`.
* Para validación de proveedores, ver `07_tests_validacion_y_go_no_go.md`.

### Rol principal que lo consulta

* Backend developer.
* Arquitecto.
* QA técnico.
* Responsable de integración con APIs.

---

## 3.8. `07_tests_validacion_y_go_no_go.md`

### Pregunta que responde

```text
¿Cómo sabemos si el proyecto puede avanzar?
```

### Incluye

* Pruebas manuales.
* Pruebas fake.
* Pruebas reales mínimas.
* Métricas de latencia.
* Métricas de traducción.
* Métricas de voz.
* Métricas de transcripción.
* Matriz GO / GO parcial / NO-GO.
* Condiciones críticas de fallo.
* Plantillas de medición.
* Criterios de cierre por fase.

### No incluye

* Arquitectura completa.
* UX detallada.
* Comparación extensa de frameworks.
* Proveedores en profundidad.

### Referencias internas

* Para laboratorio, ver `03_plan_laboratorio_fase_0.md`.
* Para proveedores, ver `06_proveedores_adaptadores_y_fallbacks.md`.
* Para seguridad y costes, ver `04_seguridad_privacidad_y_costes.md`.

### Rol principal que lo consulta

* QA.
* Arquitecto.
* Backend developer.
* Equipo encargado de decidir avance de fase.

---

## 3.9. `08_plan_implementacion_desarrolladores.md`

### Pregunta que responde

```text
¿Qué debe hacer el equipo de desarrollo, en qué orden y con qué límites?
```

### Incluye

* Fase 1: laboratorio con simulación.
* Fase 2: pruebas reales controladas.
* Fase 3: traducción real.
* Fase 4: voz real.
* Fase 5: transcripción.
* Fase 6: MVP web.
* Fase 7: seguridad y endurecimiento.
* Fase 8: pruebas reales de uso.
* Comandos con `uv`.
* Archivos permitidos por fase.
* Dependencias permitidas por fase.
* Criterios de cierre por fase.
* Qué no debe hacerse antes de tiempo.

### No incluye

* Explicación larga del problema humano.
* Comparación extensa de proveedores.
* Detalles completos de privacidad.
* Plantillas extensas de pruebas.

### Referencias internas

* Para objetivo funcional, ver `01_contexto_y_objetivo_funcional.md`.
* Para arquitectura, ver `02_arquitectura_tecnica.md`.
* Para laboratorio, ver `03_plan_laboratorio_fase_0.md`.
* Para seguridad, ver `04_seguridad_privacidad_y_costes.md`.
* Para validación, ver `07_tests_validacion_y_go_no_go.md`.

### Rol principal que lo consulta

* Equipo de desarrollo.
* Líder técnico.
* IA/agente de implementación.
* Revisor de entregables.

---

## 3.10. `09_modelo_operativo_chats_y_equipos.md`

### Pregunta que responde

```text
¿Cómo se coordinan los equipos/chats del proyecto y quién puede dar instrucciones a Antigravity/Codex?
```

### Incluye

* Lista oficial de equipos.
* Permisos de instrucción a Antigravity/Codex.
* Límites por equipo.
* Flujo de escalamiento de hallazgos.
* Formato mínimo de reporte.
* Resolución de conflictos entre equipos.
* Criterios de cierre de instrucciones con evidencia.
* Relación con ADR.

### No incluye

* Arquitectura técnica del traductor.
* Arquitectura interna de agentes.
* Código.
* Skills detalladas.
* Workflows completos.
* Gates técnicos específicos.

### Referencias internas

* Para arquitectura técnica, ver `02_arquitectura_tecnica.md`.
* Para implementación por fases, ver `08_plan_implementacion_desarrolladores.md`.
* Para seguridad y costes, ver `04_seguridad_privacidad_y_costes.md`.

### Rol principal que lo consulta

* Todos los equipos operativos.
* Arquitectura y Programación.
* Arnés de Desarrollo Agéntico.
* Testing.
* Calidad y Seguridad.

---

# 4. Orden recomendado de lectura

## 4.1. Para todo el equipo

```text
1. 00_indice_y_mapa_documental.md
2. 01_contexto_y_objetivo_funcional.md
3. 02_arquitectura_tecnica.md
4. 03_plan_laboratorio_fase_0.md
5. 08_plan_implementacion_desarrolladores.md
6. 09_modelo_operativo_chats_y_equipos.md
```

## 4.2. Para backend developers

```text
1. 02_arquitectura_tecnica.md
2. 03_plan_laboratorio_fase_0.md
3. 04_seguridad_privacidad_y_costes.md
4. 06_proveedores_adaptadores_y_fallbacks.md
5. 07_tests_validacion_y_go_no_go.md
6. 08_plan_implementacion_desarrolladores.md
7. 09_modelo_operativo_chats_y_equipos.md
```

## 4.3. Para frontend / UX

```text
1. 01_contexto_y_objetivo_funcional.md
2. 05_frontend_y_experiencia_usuario.md
3. 07_tests_validacion_y_go_no_go.md
4. 08_plan_implementacion_desarrolladores.md
5. 09_modelo_operativo_chats_y_equipos.md
```

## 4.4. Para QA

```text
1. 01_contexto_y_objetivo_funcional.md
2. 03_plan_laboratorio_fase_0.md
3. 04_seguridad_privacidad_y_costes.md
4. 07_tests_validacion_y_go_no_go.md
5. 09_modelo_operativo_chats_y_equipos.md
```

## 4.5. Para DevOps o responsable de entorno

```text
1. 04_seguridad_privacidad_y_costes.md
2. 08_plan_implementacion_desarrolladores.md
3. 02_arquitectura_tecnica.md
4. 09_modelo_operativo_chats_y_equipos.md
```

## 4.6. Para una IA/agente de desarrollo

```text
1. 00_indice_y_mapa_documental.md
2. 01_contexto_y_objetivo_funcional.md
3. 02_arquitectura_tecnica.md
4. 03_plan_laboratorio_fase_0.md
5. 04_seguridad_privacidad_y_costes.md
6. 06_proveedores_adaptadores_y_fallbacks.md
7. 07_tests_validacion_y_go_no_go.md
8. 08_plan_implementacion_desarrolladores.md
9. 09_modelo_operativo_chats_y_equipos.md
```

---

# 5. Reglas para evitar duplicidad documental

## 5.1. No duplicar contenido completo

No se debe copiar una sección completa de un documento a otro.

Si un tema ya está desarrollado en otro documento, se debe referenciar.

Ejemplo:

```text
Para límites de coste y variables de control, ver:
04_seguridad_privacidad_y_costes.md
```

## 5.2. Repetición permitida solo como resumen mínimo

Se permite repetir una idea solo cuando sea necesario para entender el documento de forma independiente.

La repetición debe ser breve.

Ejemplo permitido:

```text
El sistema usará un pipeline modular: transcripción → traducción → voz.
Para detalles técnicos, ver 02_arquitectura_tecnica.md.
```

## 5.3. Un cambio técnico debe actualizar un solo documento principal

Cada tema tiene un documento dueño.

| Tema                           | Documento dueño                             |
| ------------------------------ | ------------------------------------------- |
| Objetivo funcional             | `01_contexto_y_objetivo_funcional.md`       |
| Arquitectura técnica           | `02_arquitectura_tecnica.md`                |
| Laboratorio Fase 0             | `03_plan_laboratorio_fase_0.md`             |
| Seguridad, privacidad y costes | `04_seguridad_privacidad_y_costes.md`       |
| Frontend y UX                  | `05_frontend_y_experiencia_usuario.md`      |
| Proveedores y fallbacks        | `06_proveedores_adaptadores_y_fallbacks.md` |
| Tests y GO/NO-GO               | `07_tests_validacion_y_go_no_go.md`         |
| Implementación por fases       | `08_plan_implementacion_desarrolladores.md` |
| Modelo operativo y equipos    | `09_modelo_operativo_chats_y_equipos.md`    |

## 5.4. Los documentos no deben contradecirse

Si una decisión cambia, se debe actualizar:

1. El documento dueño del tema.
2. Cualquier referencia breve que haya quedado desactualizada.
3. El ADR correspondiente, si existe.

---

# 6. Relación entre documentos

```text
01_contexto_y_objetivo_funcional.md
        ↓
02_arquitectura_tecnica.md
        ↓
03_plan_laboratorio_fase_0.md
        ↓
07_tests_validacion_y_go_no_go.md
        ↓
08_plan_implementacion_desarrolladores.md
        ↓
09_modelo_operativo_chats_y_equipos.md
```

Documentos transversales:

```text
04_seguridad_privacidad_y_costes.md
06_proveedores_adaptadores_y_fallbacks.md
05_frontend_y_experiencia_usuario.md
```

Los documentos transversales no reemplazan el flujo principal. Lo complementan.

---

# 7. Reglas para ADR

Los ADR deben usarse cuando exista una decisión importante que pueda ser discutida en el futuro.

Ejemplos:

```text
¿Por qué pipeline modular y no speech-to-speech directo?
¿Por qué HTMX y no Flet en el MVP?
¿Por qué modo simulación por defecto?
¿Por qué limitar arquitectura hexagonal a proveedores?
```

Cada ADR debe ser breve y tener esta estructura:

```text
# ADR-XXX — Título

## Estado
Aceptado / Propuesto / Reemplazado

## Contexto

## Decisión

## Consecuencias

## Documentos relacionados
```

---

# 8. Estado documental inicial

El documento base actual del proyecto contiene una planeación extensa hasta Fase 0.9 y punto 21.

Ese documento debe tratarse como **fuente inicial de extracción**, no como documento final operativo.

A partir de ahora, la documentación oficial debe organizarse en los archivos definidos en este mapa.

---

# 9. Criterio de calidad documental

Cada documento nuevo debe cumplir:

```text
[ ] Tiene un propósito único.
[ ] Indica qué pregunta responde.
[ ] Indica qué incluye.
[ ] Indica qué no incluye.
[ ] Evita repetir contenido de otros documentos.
[ ] Tiene referencias internas.
[ ] Usa nombres consistentes.
[ ] Puede consultarse de forma independiente.
[ ] No contradice otros documentos.
[ ] Sirve a un rol claro del equipo.
```

---

# 10. Criterio de cierre de este documento

Este documento se considera completo cuando:

```text
[ ] Existe la lista oficial de documentos.
[ ] Cada documento tiene propósito definido.
[ ] Cada documento tiene alcance definido.
[ ] Existe orden de lectura.
[ ] Existen reglas contra duplicidad.
[ ] Existe mapa de relación entre documentos.
[ ] Existe regla para ADR.
```

---

# 11. Estado del mapa documental

El mapa documental del proyecto se encuentra completamente al día y consolidado:

```text
- Documentos activos: Del 00 al 09 (cobertura total de arquitectura, seguridad, pruebas y gobernanza).
- Architectural Decision Records: Del ADR-001 al ADR-009 registrados y aprobados.
- Estado general: Cierre de planeación documental finalizado con éxito.
```
