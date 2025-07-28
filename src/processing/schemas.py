"""
Supabase Schema Definitions

This module contains the schema definitions for all Supabase tables used in the Inverbot pipeline.
These schemas are used by the processing module to structure extracted data correctly.
"""

from typing import Dict, Any, List
from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal

# Pydantic schema classes based on Supabase schemas
class InformeGeneralSchema(BaseModel):
    titulo_informe: str
    resumen_informe: str
    fecha_publicacion: datetime
    id_emisor: int
    id_tipo_informe: int
    url_fuente: str
    archivo_adjunto: str = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None

class ResumenInformeFinancieroSchema(BaseModel):
    id_informe: int
    fecha_corte_informe: datetime
    activos_totales: Decimal
    pasivos_totales: Decimal
    patrimonio_neto: Decimal
    ingresos_operacionales: Decimal = None
    gastos_operacionales: Decimal = None
    resultado_neto: Decimal = None
    moneda_informe: int
    calificacion_riesgo: str = None
    otras_metricas_jsonb: Dict[str, Any] = None
    fecha_creacion: datetime = None
    fecha_actualizacion: datetime = None

class MovimientoDiarioBolsaSchema(BaseModel):
    fecha_operacion: datetime
    cantidad_operacion: Decimal
    precio_operacion: Decimal
    monto_total: Decimal
    id_instrumento: int
    id_emisor: int
    id_moneda: int
    tipo_operacion: str
    volumen_negociado: Decimal = None
    fecha_creacion: datetime = None

class DatoMacroeconomicoSchema(BaseModel):
    indicador_nombre: str
    fecha_dato: datetime
    valor_numerico: Decimal = None
    valor_texto: str = None
    id_unidad_medida: int
    id_frecuencia: int
    id_moneda: int = None
    id_emisor: int = None
    fuente_dato: str
    url_fuente: str = None
    notas: str = None
    fecha_creacion: datetime = None

class LicitacionContratoSchema(BaseModel):
    titulo: str
    descripcion: str = None
    monto_adjudicado: Decimal
    fecha_adjudicacion: datetime
    fecha_inicio: datetime = None
    fecha_fin: datetime = None
    id_emisor_adjudicado: int
    id_moneda: int
    estado_licitacion: str = None
    url_fuente: str = None
    fecha_creacion: datetime = None

class EmisoresSchema(BaseModel):
    nombre_emisor: str
    tipo_emisor: str
    sector_economico: str
    pais_origen: str
    fecha_registro: datetime = None
    estado_activo: bool = True
    url_emisor: str = None
    fecha_creacion: datetime = None

# Schema definitions for Supabase tables
SUPABASE_SCHEMAS = {
    "Resumen_Informe_Financiero": {
        "description": "Financial report summaries with key metrics and data",
        "fields": {
            "id": "Primary key (auto-generated)",
            "id_informe": "Foreign key to Informe_General",
            "fecha_corte_informe": "Report cutoff date (YYYY-MM-DD)",
            "activos_totales": "Total assets (numeric)",
            "pasivos_totales": "Total liabilities (numeric)",
            "patrimonio_neto": "Net equity (numeric)",
            "ingresos_operacionales": "Operational income (numeric)",
            "gastos_operacionales": "Operational expenses (numeric)",
            "resultado_neto": "Net result (numeric)",
            "moneda_informe": "Currency ID (foreign key)",
            "calificacion_riesgo": "Risk rating (string)",
            "otras_metricas_jsonb": "Additional metrics in JSON format",
            "fecha_creacion": "Creation timestamp",
            "fecha_actualizacion": "Last update timestamp"
        },
        "required_fields": [
            "id_informe", "fecha_corte_informe", "activos_totales", 
            "pasivos_totales", "patrimonio_neto", "moneda_informe"
        ]
    },
    
    "Informe_General": {
        "description": "General report information and metadata",
        "fields": {
            "id": "Primary key (auto-generated)",
            "titulo_informe": "Report title (string)",
            "resumen_informe": "Report summary (text)",
            "fecha_publicacion": "Publication date (YYYY-MM-DD)",
            "id_emisor": "Issuer ID (foreign key)",
            "id_tipo_informe": "Report type ID (foreign key)",
            "id_frecuencia": "Frequency ID (foreign key)",
            "id_periodo": "Period ID (foreign key)",
            "url_fuente": "Source URL (string)",
            "archivo_adjunto": "Attached file path (string)",
            "fecha_creacion": "Creation timestamp",
            "fecha_actualizacion": "Last update timestamp"
        },
        "required_fields": [
            "titulo_informe", "fecha_publicacion", "id_emisor", 
            "id_tipo_informe", "url_fuente"
        ]
    },
    
    "Movimiento_Diario_Bolsa": {
        "description": "Daily stock market movements and transactions",
        "fields": {
            "id": "Primary key (auto-generated)",
            "fecha_operacion": "Operation date (YYYY-MM-DD)",
            "cantidad_operacion": "Operation quantity (numeric)",
            "precio_operacion": "Operation price (numeric)",
            "monto_total": "Total amount (numeric)",
            "id_instrumento": "Instrument ID (foreign key)",
            "id_emisor": "Issuer ID (foreign key)",
            "id_moneda": "Currency ID (foreign key)",
            "tipo_operacion": "Operation type (string)",
            "volumen_negociado": "Traded volume (numeric)",
            "fecha_creacion": "Creation timestamp"
        },
        "required_fields": [
            "fecha_operacion", "cantidad_operacion", "precio_operacion",
            "id_instrumento", "id_emisor", "id_moneda"
        ]
    },
    
    "Dato_Macroeconomico": {
        "description": "Macroeconomic indicators and statistics",
        "fields": {
            "id": "Primary key (auto-generated)",
            "indicador_nombre": "Indicator name (string)",
            "fecha_dato": "Data date (YYYY-MM-DD)",
            "valor_numerico": "Numeric value (numeric)",
            "valor_texto": "Text value (string)",
            "id_unidad_medida": "Unit of measure ID (foreign key)",
            "id_frecuencia": "Frequency ID (foreign key)",
            "id_moneda": "Currency ID (foreign key)",
            "id_emisor": "Issuer ID (foreign key)",
            "fuente_dato": "Data source (string)",
            "url_fuente": "Source URL (string)",
            "notas": "Additional notes (text)",
            "fecha_creacion": "Creation timestamp"
        },
        "required_fields": [
            "indicador_nombre", "fecha_dato", "id_unidad_medida", 
            "id_frecuencia", "fuente_dato"
        ]
    },
    
    "Licitacion_Contrato": {
        "description": "Public tenders and contracts information",
        "fields": {
            "id": "Primary key (auto-generated)",
            "titulo": "Title (string)",
            "descripcion": "Description (text)",
            "monto_adjudicado": "Awarded amount (numeric)",
            "fecha_adjudicacion": "Award date (YYYY-MM-DD)",
            "fecha_inicio": "Start date (YYYY-MM-DD)",
            "fecha_fin": "End date (YYYY-MM-DD)",
            "id_emisor_adjudicado": "Awarded issuer ID (foreign key)",
            "id_moneda": "Currency ID (foreign key)",
            "estado_licitacion": "Tender status (string)",
            "url_fuente": "Source URL (string)",
            "fecha_creacion": "Creation timestamp"
        },
        "required_fields": [
            "titulo", "monto_adjudicado", "fecha_adjudicacion", 
            "id_emisor_adjudicado", "id_moneda"
        ]
    },
    
    "Emisores": {
        "description": "Issuers and entities information",
        "fields": {
            "id": "Primary key (auto-generated)",
            "nombre_emisor": "Issuer name (string)",
            "tipo_emisor": "Issuer type (string)",
            "sector_economico": "Economic sector (string)",
            "pais_origen": "Country of origin (string)",
            "fecha_registro": "Registration date (YYYY-MM-DD)",
            "estado_activo": "Active status (boolean)",
            "url_emisor": "Issuer URL (string)",
            "fecha_creacion": "Creation timestamp"
        },
        "required_fields": [
            "nombre_emisor", "tipo_emisor", "sector_economico", "pais_origen"
        ]
    }
}

def get_schema_info(table_name: str) -> Dict[str, Any]:
    """
    Get schema information for a specific table.
    
    Args:
        table_name: Name of the table
        
    Returns:
        Dictionary containing schema information
    """
    return SUPABASE_SCHEMAS.get(table_name, {})

def get_required_fields(table_name: str) -> List[str]:
    """
    Get required fields for a specific table.
    
    Args:
        table_name: Name of the table
        
    Returns:
        List of required field names
    """
    schema = get_schema_info(table_name)
    return schema.get("required_fields", [])

def get_all_fields(table_name: str) -> Dict[str, str]:
    """
    Get all fields for a specific table.
    
    Args:
        table_name: Name of the table
        
    Returns:
        Dictionary mapping field names to descriptions
    """
    schema = get_schema_info(table_name)
    return schema.get("fields", {})

def validate_schema_exists(table_name: str) -> bool:
    """
    Validate if a schema exists for the given table name.
    
    Args:
        table_name: Name of the table to validate
        
    Returns:
        True if schema exists, False otherwise
    """
    return table_name in SUPABASE_SCHEMAS

def get_schema_description(table_name: str) -> str:
    """
    Get the description for a specific table schema.
    
    Args:
        table_name: Name of the table
        
    Returns:
        Schema description
    """
    schema = get_schema_info(table_name)
    return schema.get("description", "No description available") 