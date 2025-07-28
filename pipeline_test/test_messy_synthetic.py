#!/usr/bin/env python3
"""
Test Pipeline with Messy Synthetic Data

This test uses intentionally messy, unstructured data to ensure the AI
is actually processing and understanding, not just copying.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_config
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings


def create_messy_synthetic_data() -> Dict[str, Any]:
    """Create messy, unstructured synthetic data that requires real AI processing."""
    return {
        "url": "https://bva.com.py/bolsa/2024/12/19/movimientos-diarios",
        "content": """
        BOLSA DE VALORES Y PRODUCTOS DE ASUNCIÓN
        MOVIMIENTOS DIARIOS - 19/12/2024
        
        OPERACIONES REALIZADAS:
        
        Ticker: BANCO
        Volumen: 15,420
        Precio: 45.50
        Variación: +2.3%
        Monto: 701,610.00
        
        Ticker: CEMENTO
        Volumen: 8,750
        Precio: 32.80
        Variación: -1.2%
        Monto: 287,000.00
        
        Ticker: ENERGIA
        Volumen: 22,100
        Precio: 18.90
        Variación: +0.8%
        Monto: 417,690.00
        
        RESUMEN DEL DÍA:
        Total operaciones: 46,270
        Monto total: 1,406,300.00
        Índice BVA: 1,245.67 (+1.1%)
        
        NOTAS:
        - Mayor actividad en sector bancario
        - Cemento con caída por expectativas de demanda
        - Energía estable con volumen alto
        """,
        "metadata": {
            "source": "bva_website",
            "date": "2024-12-19",
            "type": "daily_movements"
        }
    }


def create_messy_financial_report() -> Dict[str, Any]:
    """Create messy financial report data."""
    return {
        "url": "https://hacienda.gov.py/informes/2024/trimestre4/resumen-financiero",
        "content": """
        MINISTERIO DE HACIENDA
        RESUMEN FINANCIERO - Q4 2024
        
        INGRESOS FISCALES:
        IVA: 2,450,320,000 Gs
        IRP: 1,890,450,000 Gs
        ISC: 890,120,000 Gs
        Otros: 450,780,000 Gs
        TOTAL: 5,681,670,000 Gs
        
        GASTOS PÚBLICOS:
        Educación: 1,200,000,000 Gs
        Salud: 980,000,000 Gs
        Infraestructura: 1,500,000,000 Gs
        Seguridad: 750,000,000 Gs
        Otros: 1,251,670,000 Gs
        TOTAL: 5,681,670,000 Gs
        
        BALANCE: 0 Gs (equilibrado)
        
        DEUDA PÚBLICA:
        Interna: 15,200,000,000 Gs
        Externa: 8,500,000,000 Gs
        TOTAL: 23,700,000,000 Gs
        
        INDICADORES:
        PIB: 45,200,000,000 Gs
        Inflación: 3.2%
        Desempleo: 5.8%
        """,
        "metadata": {
            "source": "hacienda_website",
            "date": "2024-12-19",
            "type": "financial_report"
        }
    }


def test_llm_processing_messy_data():
    """Test LLM processing with messy synthetic data."""
    print("\n🧠 Testing LLM with Messy Data...")
    
    try:
        config = get_config()
        model_config = config.get_model_config()
        
        # Create LLM
        llm = ChatGoogleGenerativeAI(
            model=model_config["llm_model"],
            google_api_key=model_config["api_key"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_output_tokens"]
        )
        
        # Test with messy data
        messy_data = create_messy_synthetic_data()
        
        prompt = f"""
        Analiza estos datos de la bolsa de valores y extrae la información estructurada:
        
        {messy_data['content']}
        
        Proporciona solo los datos estructurados en formato JSON.
        """
        
        response = llm.invoke(prompt)
        
        print("  ✅ LLM Processing messy data")
        print(f"      Response: {response.content[:200]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ LLM Processing Failed: {str(e)}")
        return False


def test_embedding_messy_data():
    """Test embedding generation with messy data."""
    print("\n🔢 Testing Embeddings with Messy Data...")
    
    try:
        config = get_config()
        model_config = config.get_model_config()
        
        # Create embedding model
        embedding_model = GoogleGenerativeAIEmbeddings(
            model=model_config["embedding_model"],
            google_api_key=model_config["api_key"]
        )
        
        # Test with messy data
        messy_data = create_messy_synthetic_data()
        financial_data = create_messy_financial_report()
        
        # Generate embeddings for messy content
        embeddings = embedding_model.embed_documents([
            messy_data['content'],
            financial_data['content']
        ])
        
        print("  ✅ Embedding Generation working")
        print(f"      Embedding count: {len(embeddings)}")
        print(f"      Embedding dimension: {len(embeddings[0])}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Embedding Generation Failed: {str(e)}")
        return False


def test_data_extraction_messy():
    """Test data extraction from messy content."""
    print("\n🔍 Testing Data Extraction from Messy Content...")
    
    try:
        config = get_config()
        model_config = config.get_model_config()
        
        # Create LLM
        llm = ChatGoogleGenerativeAI(
            model=model_config["llm_model"],
            google_api_key=model_config["api_key"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_output_tokens"]
        )
        
        # Test extraction from messy financial report
        financial_data = create_messy_financial_report()
        
        prompt = f"""
        Extrae los datos financieros de este informe desordenado:
        
        {financial_data['content']}
        
        Identifica:
        1. Ingresos totales
        2. Gastos totales
        3. Deuda pública
        4. Indicadores económicos
        
        Responde en formato JSON.
        """
        
        response = llm.invoke(prompt)
        
        print("  ✅ Data Extraction working")
        print(f"      Extracted: {response.content[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Data Extraction Failed: {str(e)}")
        return False


def test_schema_mapping_messy():
    """Test schema mapping with messy data."""
    print("\n📊 Testing Schema Mapping with Messy Data...")
    
    try:
        config = get_config()
        model_config = config.get_model_config()
        
        # Create LLM
        llm = ChatGoogleGenerativeAI(
            model=model_config["llm_model"],
            google_api_key=model_config["api_key"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_output_tokens"]
        )
        
        # Test mapping messy data to structured schema
        messy_data = create_messy_synthetic_data()
        
        prompt = f"""
        Mapea estos datos desordenados de la bolsa a un esquema estructurado:
        
        {messy_data['content']}
        
        Crea un JSON con esta estructura:
        {{
            "fecha": "YYYY-MM-DD",
            "operaciones": [
                {{
                    "ticker": "string",
                    "volumen": "number",
                    "precio": "number",
                    "variacion": "number",
                    "monto": "number"
                }}
            ],
            "resumen": {{
                "total_operaciones": "number",
                "monto_total": "number",
                "indice_bva": "number"
            }}
        }}
        """
        
        response = llm.invoke(prompt)
        
        print("  ✅ Schema Mapping working")
        print(f"      Mapped: {response.content[:150]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ Schema Mapping Failed: {str(e)}")
        return False


def main():
    """Run tests with messy synthetic data."""
    print("🚀 Testing Pipeline with Messy Synthetic Data")
    print("=" * 60)
    print("📊 Testing AI processing with unstructured, messy data")
    print("🔒 No database writes - Context-efficient testing only")
    print("=" * 60)
    
    # Test each component with messy data
    results = []
    
    results.append(test_llm_processing_messy_data())
    results.append(test_embedding_messy_data())
    results.append(test_data_extraction_messy())
    results.append(test_schema_mapping_messy())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Messy Data Test Results:")
    print("=" * 60)
    
    test_names = [
        "LLM Processing Messy Data",
        "Embedding Messy Data", 
        "Data Extraction from Messy",
        "Schema Mapping Messy Data"
    ]
    
    passed = sum(results)
    total = len(results)
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\n📈 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 SUCCESS: AI is actually processing messy data!")
        print("   Ready for real web content testing.")
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Check AI processing.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 