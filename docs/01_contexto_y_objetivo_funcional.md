# 01 — Contexto y objetivo funcional

## Proyecto

**Traductor Familiar Español-Rumano**

## Propósito de este documento

Este documento define el problema que busca resolver el proyecto, el objetivo humano, el objetivo funcional, los usuarios principales, los casos de uso y el alcance inicial del MVP.

No describe la arquitectura técnica, proveedores, pruebas detalladas ni plan de implementación. Esos temas pertenecen a otros documentos del sistema documental.

---

# 1. Pregunta principal que responde este documento

```text
¿Qué problema resuelve el proyecto, para quién lo resuelve y qué debe lograr la primera versión?
```

---

# 2. Contexto del proyecto

El proyecto nace de una necesidad familiar concreta: facilitar la comunicación entre una persona hispanohablante y una familia rumana durante una estancia en Rumania.

El caso principal es ayudar a Alex a comunicarse mejor con el esposo de su hija y con la familia de él, quienes hablan rumano. Actualmente existe una barrera importante de idioma: Alex no comprende bien cuando le hablan en rumano y ellos tampoco comprenden bien cuando Alex habla en español.

El objetivo no es construir una plataforma comercial compleja ni un sistema genérico de traducción universal. El objetivo inicial es crear una herramienta práctica, sencilla y útil para conversaciones familiares reales.

---

# 3. Objetivo humano

El objetivo humano del proyecto es reducir la distancia comunicativa entre miembros de una familia que no comparten el mismo idioma.

La herramienta debe ayudar a que las conversaciones sean más cercanas, naturales y respetuosas.

Debe permitir expresar ideas como:

```text
Me alegra estar aquí con ustedes.
Gracias por recibirme.
Quiero poder comunicarme mejor con ustedes.
Para mí es importante acercarme más a la familia de mi hija.
```

El valor del proyecto no está solo en traducir palabras, sino en facilitar un puente familiar.

---

# 4. Objetivo funcional

Crear una herramienta familiar modular que permita traducir inicialmente entre:

```text
Español ↔ Rumano (Caso principal)
Español ↔ Inglés (Ruta candidata / Puente)
Rumano ↔ Inglés (Ruta candidata / Puente)
```

La arquitectura debe estar preparada para futuros idiomas, manteniendo el enfoque en la simplicidad familiar.

La primera versión debe permitir, como mínimo:

```text
1. Introducir o capturar una frase en español.
2. Obtener una traducción comprensible en rumano.
3. Introducir o capturar una frase en rumano.
4. Obtener una traducción comprensible en español.
5. Mostrar siempre el texto traducido.
6. Generar audio traducido cuando sea viable.
7. Funcionar con frases cortas y familiares.
8. Evitar que la herramienta sea más incómoda que útil.
```

---

# 5. Usuarios principales

## 5.1. Usuario principal

```text
Alex
```

Necesita comunicarse en español con personas que hablan rumano.

Sus necesidades principales son:

```text
- Entender frases familiares en rumano.
- Responder en español y que el sistema ayude a traducir al rumano.
- Preparar frases afectuosas y respetuosas.
- Usar la herramienta en situaciones familiares reales.
- Evitar herramientas lentas o difíciles de manejar.
```

## 5.2. Usuarios secundarios

```text
Familia rumana
```

Necesitan recibir frases en rumano y, eventualmente, expresar frases en rumano para que Alex las entienda en español.

Sus necesidades principales son:

```text
- Escuchar o leer traducciones claras.
- No sentirse obligados a usar una herramienta complicada.
- Poder hablar de forma natural y pausada.
- Entender que la herramienta busca facilitar la comunicación familiar.
```

---

# 6. Problema principal

El problema principal no es únicamente técnico. Es una combinación de:

```text
barrera de idioma
latencia de herramientas existentes
necesidad de tono familiar
uso en situaciones reales
riesgo de incomodidad social
```

Una herramienta lenta o difícil de usar puede romper el ritmo de la conversación. Por eso el proyecto debe priorizar:

```text
rapidez
simplicidad
claridad
bajo coste
privacidad
uso móvil
```

---

# 7. Casos de uso iniciales

## 7.1. Saludo familiar

Alex quiere decir una frase breve y afectuosa en español para que la familia la reciba en rumano.

Ejemplo:

```text
Estoy muy feliz de estar aquí con ustedes.
```

Resultado esperado:

```text
Traducción clara al rumano, preferiblemente con texto visible y audio reproducible.
```

---

## 7.2. Pedir que hablen más despacio

Alex necesita pedir ayuda para seguir la conversación.

Ejemplo:

```text
¿Pueden hablar un poco más despacio, por favor?
```

Resultado esperado:

```text
Traducción natural y respetuosa al rumano.
```

---

## 7.3. Explicar el uso del traductor

Alex necesita explicar que usará una herramienta para entender mejor.

Ejemplo:

```text
Voy a usar el traductor para entenderlos mejor y poder hablar más con ustedes.
```

Resultado esperado:

```text
Traducción clara que no suene fría ni distante.
```

---

## 7.4. Entender una frase rumana sencilla

Un familiar dice una frase breve en rumano.

Ejemplo:

```text
Ne bucurăm că ești aici cu noi.
```

Resultado esperado:

```text
Traducción al español comprensible: Nos alegra que estés aquí con nosotros.
```

---

## 7.5. Conversación en la mesa

Durante una comida, Alex necesita entender o decir frases sencillas.

Ejemplos:

```text
La comida está muy rica, muchas gracias por recibirme.
¿Quieres tomar café?
No te preocupes, podemos repetir.
```

Resultado esperado:

```text
Traducciones breves, claras y rápidas.
```

---

# 8. Alcance del MVP

El MVP debe ser deliberadamente pequeño.

## 8.1. Incluido en el MVP

```text
- Traducción español → rumano.
- Traducción rumano → español.
- Uso con frases cortas.
- Texto traducido visible.
- Audio traducido cuando sea viable.
- Flujo tipo push-to-talk o entrada controlada.
- Modo texto primero y audio después.
- Control básico de errores.
- Control de coste y uso.
- Protección de claves de API.
- No guardar conversaciones familiares por defecto.
```

## 8.2. No incluido en el MVP

```text
- Traducción continua siempre encendida.
- App nativa para App Store o Google Play.
- Multiusuario avanzado.
- Login complejo.
- Dashboard administrativo.
- Historial completo de conversaciones.
- Guardado automático de audios familiares.
- Transcripción de reuniones largas.
- Traducción de documentos oficiales.
- Uso médico, legal o financiero crítico.
- Funciones empresariales.
```

---

# 9. Idiomas del MVP

El sistema se diseña como un traductor familiar modular configurable.

### 9.1. Caso humano principal
*   **Español ↔ Rumano** (Prioridad absoluta para la familia).

### 9.2. Rutas candidatas de prueba
*   **Español ↔ Inglés**
*   **Rumano ↔ Inglés**

El inglés se incluye como ruta de prueba, posible idioma puente y opción de comparación tecnológica. Ninguna ruta es definitiva hasta validar calidad, latencia y coste.

### 9.3. Futuros idiomas
La arquitectura modular permitirá añadir nuevos idiomas sin rediseñar el núcleo del sistema.

---

# 10. Requisitos funcionales iniciales

## RF-01 — Traducir español a rumano

El sistema debe permitir traducir una frase en español a rumano.

## RF-02 — Traducir rumano a español

El sistema debe permitir traducir una frase en rumano a español.

## RF-03 — Mostrar texto traducido

El sistema debe mostrar siempre el resultado escrito de la traducción.

## RF-04 — Generar audio cuando sea viable

El sistema debe generar audio del texto traducido cuando el proveedor de voz esté disponible y el coste/latencia sean aceptables.

## RF-05 — Mantener frases cortas como unidad principal

El sistema debe estar optimizado inicialmente para frases breves, no para discursos largos.

## RF-06 — Permitir modo degradado

Si falla la generación de audio, el sistema debe seguir mostrando texto traducido.

## RF-07 — Evitar detección automática innecesaria

La dirección de traducción debe ser explícita:

```text
Español → Rumano
Rumano → Español
```

Esto reduce errores y evita depender de autodetección de idioma en la primera versión.

---

# 11. Requisitos no funcionales iniciales

## RNF-01 — Simplicidad

La herramienta debe ser fácil de usar en una situación familiar real.

## RNF-02 — Baja fricción

La interacción debe requerir el menor número posible de pasos.

## RNF-03 — Latencia aceptable

La herramienta debe priorizar mostrar el texto traducido rápidamente. El audio puede llegar después si tarda más.

## RNF-04 — Privacidad

No se deben guardar conversaciones familiares completas por defecto.

## RNF-05 — Coste controlado

Las pruebas y el uso inicial deben tener límites estrictos para evitar gastos inesperados.

## RNF-06 — Robustez básica

Si falla una API externa, el sistema debe usar fallback o mostrar un error claro.

## RNF-07 — Uso móvil

El diseño debe considerar que el uso principal puede ocurrir desde un teléfono móvil.

---

# 12. Criterios de éxito funcional

El MVP se considera útil si permite completar esta frase:

```text
Alex puede mantener una conversación familiar lenta pero usable en español ↔ rumano, con texto traducido claro y audio opcional suficientemente entendible.
```

No se exige conversación simultánea perfecta.

Sí se exige que la herramienta sea más útil que incómoda.

---

# 13. Criterios de fracaso funcional

El MVP no se considera útil si ocurre lo siguiente:

```text
- La traducción cambia el sentido de frases familiares importantes.
- La herramienta tarda tanto que rompe la conversación.
- La voz generada no se entiende.
- La interfaz resulta incómoda en una conversación real.
- El coste no puede controlarse.
- La herramienta exige guardar conversaciones familiares completas.
```

---

# 14. Principios de diseño funcional

## 14.1. Frases cortas primero

El sistema se diseñará para frases breves, no para discursos largos.

## 14.2. Texto primero

La traducción escrita debe aparecer antes de esperar el audio.

## 14.3. Audio como ayuda, no como bloqueo

El audio es útil, pero no debe impedir que el usuario vea la traducción.

## 14.4. Modo familiar

Las traducciones deben priorizar claridad, respeto y naturalidad.

## 14.5. Sin automatismo excesivo

En la primera versión, el usuario define la dirección:

```text
Español → Rumano
Rumano → Español
```

## 14.6. Privacidad por defecto

No se guardan conversaciones reales salvo decisión explícita en fases futuras.

---

# 15. Fuera de alcance explícito

Queda fuera de este documento y del MVP inicial:

```text
- Arquitectura técnica detallada.
- Selección final de proveedores.
- Implementación del laboratorio.
- Tests detallados.
- Despliegue.
- App nativa.
- Traducción profesional certificada.
- Uso médico, legal o financiero.
```

Para esos temas, consultar los documentos correspondientes.

---

# 16. Referencias internas

Para arquitectura técnica, consultar:

```text
02_arquitectura_tecnica.md
```

Para laboratorio de validación, consultar:

```text
03_plan_laboratorio_fase_0.md
```

Para seguridad, privacidad y costes, consultar:

```text
04_seguridad_privacidad_y_costes.md
```

Para frontend y experiencia de usuario, consultar:

```text
05_frontend_y_experiencia_usuario.md
```

Para proveedores y fallbacks, consultar:

```text
06_proveedores_adaptadores_y_fallbacks.md
```

Para pruebas y decisión GO/NO-GO, consultar:

```text
07_tests_validacion_y_go_no_go.md
```

Para implementación por fases, consultar:

```text
08_plan_implementacion_desarrolladores.md
```

---

# 17. Criterio de calidad de este documento

Este documento se considera correcto si:

```text
[ ] Define claramente el problema.
[ ] Define el objetivo humano.
[ ] Define el objetivo funcional.
[ ] Define usuarios principales y secundarios.
[ ] Define casos de uso iniciales.
[ ] Define alcance del MVP.
[ ] Define lo que queda fuera del MVP.
[ ] No repite arquitectura técnica detallada.
[ ] No repite proveedores en profundidad.
[ ] Referencia correctamente los documentos técnicos.
```

---

# 18. Estado

```text
Estado: Aprobado documentalmente para cierre de planeación.
```
