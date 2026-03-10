"""Property domain enumerations — closed value sets for F-0003."""

from __future__ import annotations

from enum import Enum


class PropertyType(str, Enum):
    VIVIENDA = "VIVIENDA"
    APARTAMENTO = "APARTAMENTO"
    PLAZA_APARCAMIENTO = "PLAZA_APARCAMIENTO"
    ESTUDIO = "ESTUDIO"
    LOCAL_COMERCIAL = "LOCAL_COMERCIAL"
    OFICINA = "OFICINA"
    TRASTERO = "TRASTERO"
    OTRO = "OTRO"


class AcquisitionType(str, Enum):
    ONEROSA = "ONEROSA"
    LUCRATIVA = "LUCRATIVA"
    AMBAS = "AMBAS"


class FiscalNature(str, Enum):
    URBANA = "URBANA"
    RUSTICA = "RUSTICA"


class FiscalSituation(str, Enum):
    CON_REFERENCIA_CATASTRAL = "CON_REFERENCIA_CATASTRAL"
    PAIS_VASCO = "PAIS_VASCO"
    NAVARRA = "NAVARRA"
    SIN_REFERENCIA_CATASTRAL = "SIN_REFERENCIA_CATASTRAL"
