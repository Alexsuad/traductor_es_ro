# File: docs/09_modelo_operativo_chats_y_equipos.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Definir el modelo operativo de equipos y chats del proyecto.
# Rol: Guía de gobernanza y flujo de instrucciones para Antigravity/Codex.
# ──────────────────────────────────────────────────────────────────────

# 09 — Modelo Operativo de Chats y Equipos

## 1. Propósito del modelo operativo

Este documento define la estructura de trabajo, responsabilidades y flujo de comunicación entre los diferentes equipos (chats) humanos y la herramienta de desarrollo agéntico (Antigravity/Codex).

> [!IMPORTANT]
> **Este documento NO define agentes internos ni la arquitectura agéntica de Antigravity/Codex, según la herramienta usada.**
> Define equipos y chats humanos-operativos dentro del ecosistema del proyecto para asegurar un desarrollo ordenado y evitar contraórdenes.

---

## 2. Lista oficial de equipos y chats

El proyecto se organiza en los siguientes equipos especializados:

1.  **Arquitectura y Programación:** Responsable de la estructura global, patrones y decisiones de alto nivel.
2.  **Arnés de Desarrollo Agéntico:** Responsable de la orquestación agéntica, skills, workflows y gates de validación.
3.  **Backend:** Responsable de la lógica de negocio, integración de APIs, adaptadores y procesamiento de datos.
4.  **Frontend:** Responsable de la interfaz de usuario, experiencia de uso (UX técnica) e interacción cliente-servidor.
5.  **Testing:** Responsable de la creación de pruebas (unitarias, integración, E2E) y validación de requisitos.
6.  **Calidad y Seguridad:** Responsable de la auditoría de código, seguridad de secretos, gestión de costes y cumplimiento de estándares.
7.  **Experto de Usuario / Cliente:** Responsable de la auditoría funcional y validación de la experiencia real desde el punto de vista del usuario final.

---

## 3. Gobernanza de instrucciones a Antigravity/Codex

### 3.1. Equipos con capacidad de instrucción técnica
Los siguientes equipos pueden dar instrucciones directas a Antigravity o Codex, **siempre dentro de su dominio operativo**:

*   Arquitectura y Programación
*   Arnés de Desarrollo Agéntico
*   Backend
*   Frontend
*   Testing
*   Calidad y Seguridad

### 3.2. Excepción: Equipo Experto de Usuario / Cliente
El Equipo Experto de Usuario / Cliente **NO puede dar instrucciones directas a Antigravity ni Codex**. 

Su función es auditar desde el producto:
*   ¿La herramienta se entiende?
*   ¿La experiencia es cómoda?
*   ¿El flujo sirve para una conversación familiar real?
*   ¿Los mensajes son claros?
*   ¿El audio ayuda o estorba?

Si detecta un problema o necesidad de cambio, debe reportarlo al equipo correspondiente (ej. Frontend o Arquitectura) para que este lo convierta en una instrucción técnica.

---

## 4. Matriz de permisos y límites

| Equipo | Puede instruir a Antigravity/Codex | Puede auditar | Puede bloquear fase | Límite principal |
| :--- | :---: | :---: | :---: | :--- |
| **Arquitectura y Programación** | Sí | Sí | Sí | No decide agentes/skills del Arnés. |
| **Arnés de Desarrollo Agéntico** | Sí | Sí | Sí | No implementa Backend/Frontend directamente. |
| **Backend** | Sí | Sí (Backend) | Sí (Backend) | No toca UX/Frontend salvo contrato de API. |
| **Frontend** | Sí | Sí (Frontend) | Sí (UX técnica) | No cambia lógica de Backend salvo contrato. |
| **Testing** | Sí | Sí | Sí | No reescribe producto sin aprobación del equipo dueño. |
| **Calidad y Seguridad** | Sí | Sí | Sí | No implementa funcionalidades de negocio. |
| **Experto de Usuario / Cliente** | **No** | Sí | Sí (Funcional) | Reporta al equipo operativo, no instruye a la IA. |

> [!NOTE]
> **Nota operativa (Testing):** El Equipo Testing puede instruir a Antigravity/Codex para crear, ajustar o ejecutar pruebas. Si durante una prueba detecta que debe cambiarse código funcional, debe reportarlo al equipo dueño del dominio afectado antes de ordenar una modificación directa.
>
> **Nota operativa (Calidad y Seguridad):** El Equipo Calidad y Seguridad puede solicitar correcciones relacionadas con secretos, costes, privacidad, dependencias, trazabilidad, cumplimiento documental o riesgos técnicos. No debe implementar nuevas funcionalidades de producto salvo que el cambio sea estrictamente correctivo y esté dentro de su dominio.

---

## 5. Regla de oro contra contraórdenes

> [!CAUTION]
> **Ningún equipo debe dar instrucciones técnicas fuera de su dominio operativo.**
> Si un hallazgo pertenece a otro dominio, debe reportarse al equipo responsable. No se permite la corrección directa por parte de un equipo ajeno al dominio afectado para evitar inconsistencias y deudas técnicas.

---

## 6. Relación con el Arnés de Desarrollo Agéntico

El **Equipo Arnés de Desarrollo Agéntico** es el único equipo autorizado para decidir la estructura agéntica interna de Antigravity/Codex, según la herramienta usada. Esto incluye:
*   Decidir si se crean archivos `AGENTS.md`, `GEMINI.md`, reglas, workflows o carpetas de skills con su correspondiente `SKILL.md`, según la herramienta usada.
*   Definir si la herramienta debe adoptar perfiles separados (Backend, Frontend, etc.) internamente.
*   Configurar los gates de validación automática.

---

## 7. Flujo de escalamiento de hallazgos (Experto de Usuario)

Para asegurar que las observaciones del Cliente/Usuario se implementen correctamente, se seguirá este flujo:

1.  **Hallazgo detectado:** El Experto de Usuario identifica una fricción o error funcional.
2.  **Clasificación del dominio:** Se identifica qué equipo es responsable (ej. es un error de texto -> Frontend; es un error de traducción -> Backend).
3.  **Envío al equipo responsable:** Se comunica el hallazgo con impacto y contexto.
4.  **Conversión en instrucción:** El equipo responsable valida el hallazgo y genera la instrucción técnica para Antigravity.
5.  **Ejecución:** Antigravity/Codex realiza el cambio.
6.  **Validación:** El equipo responsable y el Experto de Usuario verifican la solución.
7.  **Cierre:** Se cierra el hallazgo con evidencia técnica y funcional.

---

## 8. Formato mínimo para reportar hallazgos

Todo hallazgo enviado entre equipos debe incluir:

```text
ID del hallazgo:
Equipo que reporta:
Equipo responsable sugerido:
Documento o archivo relacionado:
Descripción del problema:
Impacto:
Severidad: baja / media / alta / crítica
Evidencia:
Recomendación:
¿Bloquea fase?: sí / no
```

Este formato evita reportes ambiguos y facilita que el equipo responsable convierta el hallazgo en una instrucción técnica clara para Antigravity/Codex.

## 8.1. Criterio mínimo de cierre de una instrucción

Una instrucción enviada a Antigravity/Codex no debe considerarse cerrada solo porque la herramienta diga que terminó. Debe cerrarse con evidencia mínima:

```text
ID de instrucción:
Equipo solicitante:
Equipo responsable:
Archivos modificados:
Comandos ejecutados:
Resultado de validación:
Evidencia generada:
Estado final:
Pendientes:
```

**Estados permitidos:**
*   `cerrado_con_evidencia`
*   `cerrado_parcial`
*   `bloqueado_por_conflicto`
*   `bloqueado_por_falta_de_datos`
*   `bloqueado_por_seguridad`
*   `pendiente_validacion`

**Regla:** No usar cierres ambiguos como "listo", "terminado", "funciona" o "hecho" sin evidencia.

---

## 9. Resolución de conflictos entre equipos

Si dos equipos emiten instrucciones contradictorias, se debe detener la ejecución del cambio hasta resolver el conflicto.

Orden recomendado de resolución:

1.  Identificar qué documentos oficiales se ven afectados.
2.  Determinar qué equipo es dueño del dominio principal.
3.  Consultar al Equipo Arquitectura y Programación si afecta arquitectura o estructura técnica.
4.  Consultar al Equipo Calidad y Seguridad si afecta seguridad, privacidad, costes o cumplimiento.
5.  Consultar al Equipo Arnés de Desarrollo Agéntico si afecta reglas, skills, workflows, gates o comportamiento interno de Antigravity/Codex.
6.  Registrar la decisión final antes de continuar.

**Regla:** Ninguna herramienta de desarrollo debe ejecutar cambios contradictorios sin una decisión de cierre.

---

## 10. Relación con ADR

Cuando una decisión entre equipos afecte arquitectura, fases, proveedores, seguridad, costes, privacidad, flujo de implementación o estructura agéntica, debe evaluarse si requiere un ADR (Architectural Decision Record).

Ejemplos de decisiones que pueden requerir ADR:
*   Cambiar el motor principal de traducción.
*   Modificar el alcance del MVP.
*   Cambiar el orden de fases.
*   Permitir APIs reales antes de lo previsto.
*   Cambiar la estructura del laboratorio.
*   Introducir un nuevo proveedor externo.
*   Modificar la estrategia de Antigravity/Codex.
*   Alterar reglas, gates o workflows principales.

**Regla:** Si una decisión puede ser discutida en el futuro o afecta a más de un equipo, debe registrarse como ADR o quedar referenciada en el ADR correspondiente. Los ADR no reemplazan este documento; registran decisiones concretas.
