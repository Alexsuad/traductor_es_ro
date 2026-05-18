# File: traductor_rumano_lab/README.md
# ──────────────────────────────────────────────────────────────────────
# Propósito: Guía de uso, ejecución y descripción del laboratorio de simulación.
# Rol: Documentación viva del laboratorio Fase 1.
# ──────────────────────────────────────────────────────────────────────

# Traductor Familiar Español-Rumano — Laboratorio Fase 1

Este directorio contiene el espacio de pruebas controlado y aislado (**laboratorio**) diseñado para validar los contratos, flujos internos, la caché local simple y el registro de métricas del proyecto sin incurrir en costes externos ni usar APIs reales en esta etapa.

El laboratorio funciona estrictamente en **modo simulación** por defecto.

---

## 1. Estructura del laboratorio

La organización de archivos se apega estrictamente al mapa definido en la arquitectura técnica:

*   `src_lab/config/settings_lab.py`: Carga y validación robusta de variables mediante `pydantic-settings`.
*   `src_lab/ports/`: Interfaces abstractas para desacoplar los proveedores externos de la lógica interna.
*   `src_lab/providers_fake/`: Implementaciones simuladas de los proveedores externos.
*   `src_lab/cache/`: Persistencia en memoria y disco simple de traducciones de frases de prueba.
*   `src_lab/utils/`: Medición de latencia, normalización e informes deterministas.
*   `resultados/`: Registros de mediciones (`mediciones_fase_0.md`), errores (`errores_fase_0.md`) y caché JSON (`cache_frases.json`).
*   `audios_salida/`: Contenedor de archivos de audios simulados y temporales.

---

## 2. Ejecución con UV

Toda la ejecución y gestión de dependencias en este laboratorio se realiza de forma unificada utilizando la herramienta determinista **`uv`**.

### 2.1. Sincronización del entorno
Para asegurar que las dependencias estén correctamente instaladas en tu entorno virtual local, ejecuta:

```bash
uv sync
```

### 2.2. Verificar el Entorno
El script de verificación chequea de forma estricta que no existan dependencias prohibidas en el entorno y que las variables globales estén en su estado seguro de simulación:

```bash
uv run python scripts/verificar_entorno.py
```

### 2.3. Ejecutar Prueba Fake
Este script simula el flujo completo de traducción y generación de voz, aplicando caché, controlando límites y registrando los resultados en `resultados/mediciones_fase_0.md`:

```bash
uv run python scripts/prueba_fake_texto_traduccion_voz.py
```

### 2.4. Ejecutar la Suite de Tests
Para correr las pruebas unitarias y de integración locales:

```bash
uv run pytest
```

### 2.5. Lint y Formateo
Para validar la higiene y calidad del código fuente:

```bash
uv run ruff check .
```

---

## 3. Estado Seguro y Doble Confirmación

De acuerdo a las directrices de seguridad de `docs/04_seguridad_privacidad_y_costes.md`, las APIs externas están bloqueadas por defecto mediante:

```env
MODO_SIMULACION=true
PERMITIR_APIS_REALES=false
```

No se permite cambiar este comportamiento durante la Fase 1.
