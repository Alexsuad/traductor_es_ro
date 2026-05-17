# ADR-002 — Modo simulación por defecto

## Estado

Aprobado.

## Contexto

Durante el desarrollo inicial y las fases de laboratorio, el uso prematuro de APIs reales puede generar costes innecesarios, exposición accidental de secretos y dependencia de la conectividad externa para pruebas de lógica básica.

## Decisión

*   El proyecto iniciará siempre con `MODO_SIMULACION=true` en la configuración.
*   Se establece la variable `PERMITIR_APIS_REALES=false` por defecto.
*   La Fase 1 de implementación utilizará exclusivamente adaptadores "fake" que simulen el comportamiento de los proveedores.
*   Para habilitar llamadas a APIs reales, se requerirá una doble confirmación manual en el entorno:
    1.  `MODO_SIMULACION=false`
    2.  `PERMITIR_APIS_REALES=true`

## Consecuencias positivas

*   Cero gasto accidental durante el desarrollo y testing.
*   Pruebas más rápidas y deterministas sin latencia de red.
*   Seguridad incrementada al no enviar datos a proveedores externos sin intención explícita.

## Consecuencias negativas o trade-offs

*   Las pruebas en modo simulación no detectan problemas de red o cambios inesperados en las APIs de los proveedores reales.

## Alternativas consideradas

*   Uso de créditos gratuitos de APIs (descartado por la necesidad de configuración manual recurrente y riesgos de agotamiento).

## Documentos relacionados

*   docs/03_plan_laboratorio_fase_0.md
*   docs/04_seguridad_privacidad_y_costes.md
*   docs/08_plan_implementacion_desarrolladores.md
