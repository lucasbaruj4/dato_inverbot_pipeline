"""
Data Sources Configuration

This module contains the predefined data sources for the Inverbot pipeline.
These sources are used by the extraction module to gather financial and economic data.
"""

from typing import List, Dict, Any

# Main data sources for the Inverbot pipeline
DATA_SOURCES = [
    {
        "category": "Balances de Empresas",
        "url": "https://www.bolsadevalores.com.py/listado-de-emisores/",
        "content_type": ["EXCEL", "PDF", "TEXT"],
        "description": "Página de listado de emisores de la BVA, contiene un listado de emisores, cuando se selecciona un emisor en específico, se pueden encontrar balances, prospectos, análisis de riesgo y hechos relevantes del emisor en cuestión."
    },
    {
        "category": "Movimientos Diarios",
        "url": "https://www.bolsadevalores.com.py/informes-diarios/",
        "content_type": ["JSON"],
        "description": "Informes diarios de la BVA con movimientos del mercado."
    },
    {
        "category": "Volumen Mensual",
        "url": "https://www.bolsadevalores.com.py/informes-mensuales/",
        "content_type": ["TEXT", "PDF", "JSON"],
        "description": "Informes mensuales de la BVA, incluyendo PDFs y datos estructurados."
    },
    {
        "category": "Resumen Anual",
        "url": "https://www.bolsadevalores.com.py/informes-anuales/",
        "content_type": ["TEXT", "PDF"],
        "description": "Informes anuales de la BVA en formato PDF."
    },
    {
        "category": "Contexto Macroeconómico",
        "url": "https://www.bcp.gov.py/",
        "content_type": ["TEXT", "PDF", "EXCEL", "PPT"],
        "description": "Sitio web del Banco Central del Paraguay (BCP) para datos macroeconómicos."
    },
    {
        "category": "Estadísticas Sociales",
        "url": "https://www.ine.gov.py/vt/publicacion.php/",
        "content_type": ["PDF", "EXCEL", "PPT", "TEXT"],
        "description": "Portal del Instituto Nacional de Estadística (INE) para publicaciones y datos sociales."
    },
    {
        "category": "Contratos Públicos",
        "url": "https://www.contrataciones.gov.py/",
        "content_type": ["TEXT"],
        "description": "Portal de la Dirección Nacional de Contrataciones Públicas (DNCP) para datos de licitaciones y contratos."
    },
    {
        "category": "Datos de Inversión",
        "url": "https://www.dnit.gov.py/web/portal-institucional/invertir-en-py",
        "content_type": ["TEXT", "PNG", "PDF"],
        "description": "Sección del portal del DNIT con información para invertir en Paraguay."
    },
    {
        "category": "Informes Financieros (DNIT)",
        "url": "https://www.dnit.gov.py/web/portal-institucional/informes-financieros",
        "content_type": ["TEXT", "PDF"],
        "description": "Sección del portal del DNIT con informes financieros."
    }
]

# Test data sources for development and testing
TEST_DATA_SOURCES = [
    {
        "category": "Test Page",
        "url": "https://www.africau.edu/images/default/sample.pdf",
        "content_type": ["PDF"],
        "description": "Página de prueba con un enlace a un PDF simple."
    },
    {
        "category": "Test Page with Text",
        "url": "https://www.w3schools.com/html/html_paragraphs.asp",
        "content_type": ["TEXT"],
        "description": "Página de prueba con contenido de texto simple."
    }
]

def get_data_sources(source_type: str = "main") -> List[Dict[str, Any]]:
    """
    Get data sources based on the specified type.
    
    Args:
        source_type: Type of sources to return ("main" or "test")
        
    Returns:
        List of data source dictionaries
    """
    if source_type.lower() == "test":
        return TEST_DATA_SOURCES
    else:
        return DATA_SOURCES

def get_sources_by_category(category: str, source_type: str = "main") -> List[Dict[str, Any]]:
    """
    Get data sources filtered by category.
    
    Args:
        category: Category to filter by
        source_type: Type of sources to search ("main" or "test")
        
    Returns:
        List of data source dictionaries matching the category
    """
    sources = get_data_sources(source_type)
    return [source for source in sources if source["category"] == category]

def get_sources_by_content_type(content_type: str, source_type: str = "main") -> List[Dict[str, Any]]:
    """
    Get data sources filtered by content type.
    
    Args:
        content_type: Content type to filter by (e.g., "JSON", "PDF")
        source_type: Type of sources to search ("main" or "test")
        
    Returns:
        List of data source dictionaries matching the content type
    """
    sources = get_data_sources(source_type)
    return [source for source in sources if content_type in source["content_type"]] 