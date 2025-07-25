"""
Pinecone Schema Definitions

This module contains the schema definitions for all Pinecone indexes used in the Inverbot pipeline.
These schemas are used by the vectorization module to prepare metadata for vector storage.
"""

from typing import Dict, Any, List

# Schema definitions for Pinecone indexes
PINECONE_SCHEMAS = {
    "documentos-informes-vector": {
        "description": "Vector index for financial reports and general documents",
        "dimension": 384,  # sentence-transformers/all-MiniLM-L6-v2 dimension
        "metadata_fields": {
            "id_informe": "Foreign key to Informe_General table (integer)",
            "fecha_publicacion": "Publication date (YYYY-MM-DD)",
            "titulo_informe": "Report title (string)",
            "id_emisor": "Issuer ID (integer)",
            "tipo_contenido": "Content type: 'financial_report', 'annual_report', 'general_document' (string)",
            "chunk_text": "The actual text chunk (string)",
            "chunk_id": "Sequential chunk identifier (integer)",
            "source_url": "Source URL of the document (string)",
            "archivo_adjunto": "Attached file path if applicable (string)"
        },
        "required_metadata": [
            "id_informe", "fecha_publicacion", "titulo_informe", 
            "tipo_contenido", "chunk_text", "chunk_id"
        ]
    },
    
    "noticia-relevante-vector": {
        "description": "Vector index for relevant news and market information",
        "dimension": 384,
        "metadata_fields": {
            "id_noticia": "News identifier (integer)",
            "fecha_publicacion": "Publication date (YYYY-MM-DD)",
            "titulo_noticia": "News title (string)",
            "fuente_noticia": "News source (string)",
            "categoria": "News category: 'market', 'economic', 'financial', 'political' (string)",
            "chunk_text": "The actual text chunk (string)",
            "chunk_id": "Sequential chunk identifier (integer)",
            "url_fuente": "Source URL (string)",
            "relevancia": "Relevance score (float)"
        },
        "required_metadata": [
            "id_noticia", "fecha_publicacion", "titulo_noticia", 
            "fuente_noticia", "categoria", "chunk_text", "chunk_id"
        ]
    },
    
    "dato-macroeconomico-vector": {
        "description": "Vector index for macroeconomic indicators and statistics",
        "dimension": 384,
        "metadata_fields": {
            "id_dato": "Data point identifier (integer)",
            "indicador_nombre": "Indicator name (string)",
            "fecha_dato": "Data date (YYYY-MM-DD)",
            "valor_numerico": "Numeric value (float)",
            "unidad_medida": "Unit of measure (string)",
            "fuente_dato": "Data source (string)",
            "chunk_text": "The actual text chunk (string)",
            "chunk_id": "Sequential chunk identifier (integer)",
            "url_fuente": "Source URL (string)",
            "frecuencia": "Data frequency: 'daily', 'monthly', 'quarterly', 'annual' (string)"
        },
        "required_metadata": [
            "id_dato", "indicador_nombre", "fecha_dato", 
            "fuente_dato", "chunk_text", "chunk_id"
        ]
    },
    
    "licitacion-contrato-vector": {
        "description": "Vector index for public tenders and contracts",
        "dimension": 384,
        "metadata_fields": {
            "id_licitacion": "Tender identifier (integer)",
            "titulo": "Tender title (string)",
            "fecha_adjudicacion": "Award date (YYYY-MM-DD)",
            "monto_adjudicado": "Awarded amount (float)",
            "moneda": "Currency (string)",
            "estado_licitacion": "Tender status (string)",
            "chunk_text": "The actual text chunk (string)",
            "chunk_id": "Sequential chunk identifier (integer)",
            "url_fuente": "Source URL (string)",
            "entidad_contratante": "Contracting entity (string)"
        },
        "required_metadata": [
            "id_licitacion", "titulo", "fecha_adjudicacion", 
            "estado_licitacion", "chunk_text", "chunk_id"
        ]
    }
}

def get_pinecone_schema_info(index_name: str) -> Dict[str, Any]:
    """
    Get schema information for a specific Pinecone index.
    
    Args:
        index_name: Name of the index
        
    Returns:
        Dictionary containing schema information
    """
    return PINECONE_SCHEMAS.get(index_name, {})

def get_required_metadata(index_name: str) -> List[str]:
    """
    Get required metadata fields for a specific index.
    
    Args:
        index_name: Name of the index
        
    Returns:
        List of required metadata field names
    """
    schema = get_pinecone_schema_info(index_name)
    return schema.get("required_metadata", [])

def get_all_metadata_fields(index_name: str) -> Dict[str, str]:
    """
    Get all metadata fields for a specific index.
    
    Args:
        index_name: Name of the index
        
    Returns:
        Dictionary mapping field names to descriptions
    """
    schema = get_pinecone_schema_info(index_name)
    return schema.get("metadata_fields", {})

def validate_index_exists(index_name: str) -> bool:
    """
    Validate if a schema exists for the given index name.
    
    Args:
        index_name: Name of the index to validate
        
    Returns:
        True if schema exists, False otherwise
    """
    return index_name in PINECONE_SCHEMAS

def get_index_dimension(index_name: str) -> int:
    """
    Get the vector dimension for a specific index.
    
    Args:
        index_name: Name of the index
        
    Returns:
        Vector dimension (default 384 for sentence-transformers/all-MiniLM-L6-v2)
    """
    schema = get_pinecone_schema_info(index_name)
    return schema.get("dimension", 384)

def get_index_description(index_name: str) -> str:
    """
    Get the description for a specific index schema.
    
    Args:
        index_name: Name of the index
        
    Returns:
        Index description
    """
    schema = get_pinecone_schema_info(index_name)
    return schema.get("description", "No description available")

def get_available_indexes() -> List[str]:
    """
    Get list of available Pinecone index names.
    
    Returns:
        List of available index names
    """
    return list(PINECONE_SCHEMAS.keys())

def validate_metadata_completeness(metadata: Dict[str, Any], index_name: str) -> Dict[str, Any]:
    """
    Validate that metadata contains all required fields for an index.
    
    Args:
        metadata: Metadata dictionary to validate
        index_name: Name of the index to validate against
        
    Returns:
        Validation result with status and missing fields
    """
    required_fields = get_required_metadata(index_name)
    missing_fields = []
    
    for field in required_fields:
        if field not in metadata or metadata[field] is None:
            missing_fields.append(field)
    
    return {
        "is_valid": len(missing_fields) == 0,
        "missing_fields": missing_fields,
        "total_required": len(required_fields),
        "provided_fields": len(metadata)
    } 