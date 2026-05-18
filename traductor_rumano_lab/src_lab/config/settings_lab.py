# File: src_lab/config/settings_lab.py
# ──────────────────────────────────────────────────────────────────────
# Propósito: Carga, validación e inyección robusta de variables de entorno del laboratorio.
# Rol: Fuente única de verdad de la configuración del sistema (Pydantic).
# ──────────────────────────────────────────────────────────────────────

import os
from functools import lru_cache
from typing import List, Optional
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class SettingsLab(BaseSettings):
    """Cargador robusto de variables y límites operativos para el laboratorio."""

    # --- CONTROL GLOBAL DE SEGURIDAD ---
    modo_simulacion: bool = Field(alias="MODO_SIMULACION", default=True)
    permitir_apis_reales: bool = Field(alias="PERMITIR_APIS_REALES", default=False)

    # --- CONFIGURACIÓN DE IDIOMAS ---
    idiomas_habilitados_str: str = Field(alias="IDIOMAS_HABILITADOS", default="es,ro,en")
    idioma_principal_usuario: str = Field(alias="IDIOMA_PRINCIPAL_USUARIO", default="es")
    idioma_familia_principal: str = Field(alias="IDIOMA_FAMILIA_PRINCIPAL", default="ro")
    idioma_puente: str = Field(alias="IDIOMA_PUENTE", default="en")
    usar_idioma_puente: bool = Field(alias="USAR_IDIOMA_PUENTE", default=False)
    permitir_pruebas_con_ingles: bool = Field(alias="PERMITIR_PRUEBAS_CON_INGLES", default=True)

    # --- CONFIGURACIÓN DE MOTORES ---
    modo_motor: str = Field(alias="MODO_MOTOR", default="AUTO")
    permitir_translate_realtime: bool = Field(alias="PERMITIR_TRANSLATE_REALTIME", default=False)
    permitir_whisper_realtime: bool = Field(alias="PERMITIR_WHISPER_REALTIME", default=False)
    permitir_pipeline_modular: bool = Field(alias="PERMITIR_PIPELINE_MODULAR", default=True)
    permitir_modo_combinado: bool = Field(alias="PERMITIR_MODO_COMBINADO", default=False)

    # --- LÍMITES DE USO ---
    max_llamadas_por_ejecucion: int = Field(alias="MAX_LLAMADAS_POR_EJECUCION", default=10)
    max_caracteres_por_frase: int = Field(alias="MAX_CARACTERES_POR_FRASE", default=300)
    max_frases_por_prueba: int = Field(alias="MAX_FRASES_POR_PRUEBA", default=5)

    max_minutos_translate_dia: int = Field(alias="MAX_MINUTOS_TRANSLATE_DIA", default=10)
    max_minutos_whisper_dia: int = Field(alias="MAX_MINUTOS_WHISPER_DIA", default=10)
    max_minutos_modo_combinado_dia: int = Field(alias="MAX_MINUTOS_MODO_COMBINADO_DIA", default=5)
    max_llamadas_pipeline_dia: int = Field(alias="MAX_LLAMADAS_PIPELINE_DIA", default=50)

    # --- OPERACIÓN Y CACHÉ ---
    usar_cache: bool = Field(alias="USAR_CACHE", default=True)
    ruta_cache_frases: str = Field(alias="RUTA_CACHE_FRASES", default="resultados/cache_frases.json")
    ruta_resultados: str = Field(alias="RUTA_RESULTADOS", default="resultados")
    ruta_audios_salida: str = Field(alias="RUTA_AUDIOS_SALIDA", default="audios_salida")

    reintentos_maximos: int = Field(alias="REINTENTOS_MAXIMOS", default=2)
    timeout_traduccion_segundos: float = Field(alias="TIMEOUT_TRADUCCION_SEGUNDOS", default=3.0)
    timeout_voz_segundos: float = Field(alias="TIMEOUT_VOZ_SEGUNDOS", default=5.0)
    timeout_transcripcion_segundos: float = Field(alias="TIMEOUT_TRANSCRIPCION_SEGUNDOS", default=5.0)

    detener_si_supera_limite: bool = Field(alias="DETENER_SI_SUPERA_LIMITE", default=True)

    # --- CREDENCIALES DE PROVEEDORES ---
    deepl_api_key: Optional[str] = Field(alias="DEEPL_API_KEY", default=None)
    elevenlabs_api_key: Optional[str] = Field(alias="ELEVENLABS_API_KEY", default=None)
    openai_api_key: Optional[str] = Field(alias="OPENAI_API_KEY", default=None)
    google_application_credentials: Optional[str] = Field(alias="GOOGLE_APPLICATION_CREDENTIALS", default=None)

    # Configuración de Pydantic
    model_config = SettingsConfigDict(
        env_file=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True
    )

    @property
    def idiomas_habilitados(self) -> List[str]:
        """Retorna la lista de idiomas habilitados normalizada."""
        return [i.strip().lower() for i in self.idiomas_habilitados_str.split(",") if i.strip()]

    @field_validator("permitir_apis_reales")
    @classmethod
    def validar_seguridad_apis(cls, v: bool, info) -> bool:
        """Aplica la regla de doble confirmación obligatoria del ADR-002."""
        # Obtenemos modo_simulacion del diccionario de valores si está disponible
        modo_sim = info.data.get("modo_simulacion", True)
        if v and modo_sim:
            raise ValueError(
                "¡BLOQUEO DE SEGURIDAD ACTIVADO!: No se pueden permitir APIs reales "
                "mientras el modo simulación esté habilitado (MODO_SIMULACION=true)."
            )
        return v


@lru_cache()
def get_settings() -> SettingsLab:
    """Retorna una instancia única y cacheada de la configuración."""
    return SettingsLab()
