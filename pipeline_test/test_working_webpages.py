#!/usr/bin/env python3
"""
Test Pipeline with Working Webpages

This test uses webpages that we know work to verify
web scraping and data extraction capabilities.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config import get_config
from utils.web_tools import (
    search_web,
    scrape_webpage,
    extract_financial_data
)


def test_working_webpages():
    """Test with webpages that we know work."""
    print("\n🌐 Testing Working Webpages...")
    
    try:
        # Test with working URLs
        working_urls = [
            "https://www.hacienda.gov.py/",
            "https://www.google.com/",
            "https://www.wikipedia.org/"
        ]
        
        successful_scrapes = 0
        
        for url in working_urls:
            print(f"      Testing: {url}")
            result = scrape_webpage(url)
            
            if result.get("content"):
                print(f"         ✅ Scraped successfully")
                print(f"            Title: {result.get('title', 'No title')}")
                print(f"            Content length: {len(result.get('content', ''))} chars")
                successful_scrapes += 1
            else:
                print(f"         ❌ Failed to scrape: {result.get('metadata', {}).get('error', 'Unknown error')}")
        
        if successful_scrapes > 0:
            print(f"  ✅ Working webpages test: {successful_scrapes}/{len(working_urls)} successful")
            return True
        else:
            print("  ❌ Working webpages test failed")
            return False
        
    except Exception as e:
        print(f"  ❌ Working webpages test failed: {str(e)}")
        return False


def test_financial_data_extraction_working():
    """Test financial data extraction from working webpages."""
    print("\n💰 Testing Financial Data Extraction (Working Pages)...")
    
    try:
        # Test with Ministerio de Hacienda (we know it works)
        test_url = "https://www.hacienda.gov.py/"
        result = extract_financial_data(test_url)
        
        if result and "error" not in result:
            print("  ✅ Financial data extraction working")
            print(f"      URL: {result.get('url', 'No URL')}")
            print(f"      Extracted data length: {len(result.get('extracted_data', ''))} chars")
            print(f"      Raw content preview: {result.get('raw_content', '')[:100]}...")
            return True
        else:
            print(f"  ❌ Financial data extraction failed: {result.get('error', 'Unknown error')}")
            return False
        
    except Exception as e:
        print(f"  ❌ Financial data extraction failed: {str(e)}")
        return False


def test_paraguayan_search():
    """Test search for Paraguayan content."""
    print("\n🇵🇾 Testing Paraguayan Content Search...")
    
    try:
        # Test search for Paraguayan government content
        query = "site:gov.py paraguay economía"
        results = search_web(query, num_results=3)
        
        if results:
            print("  ✅ Paraguayan content search working")
            print(f"      Found {len(results)} results")
            for i, result in enumerate(results[:2]):
                print(f"      {i+1}. {result.get('title', 'No title')}")
                print(f"         URL: {result.get('url', 'No URL')}")
                print(f"         Snippet: {result.get('snippet', '')[:100]}...")
            return True
        else:
            print("  ❌ Paraguayan content search failed - no results")
            return False
        
    except Exception as e:
        print(f"  ❌ Paraguayan content search failed: {str(e)}")
        return False


def test_content_analysis():
    """Test content analysis with scraped data."""
    print("\n📊 Testing Content Analysis...")
    
    try:
        from langchain_google_genai import ChatGoogleGenerativeAI
        config = get_config()
        model_config = config.get_model_config()
        
        # Create LLM
        llm = ChatGoogleGenerativeAI(
            model=model_config["llm_model"],
            google_api_key=model_config["api_key"],
            temperature=model_config["temperature"],
            max_tokens=model_config["max_output_tokens"]
        )
        
        # Scrape a working webpage
        scraped = scrape_webpage("https://www.hacienda.gov.py/")
        
        if scraped.get("content"):
            # Analyze the content
            prompt = f"""
            Analiza este contenido web del Ministerio de Hacienda de Paraguay:
            
            Título: {scraped.get('title', '')}
            Contenido: {scraped.get('content', '')[:1000]}
            
            Identifica:
            1. ¿Es una página oficial del gobierno paraguayo?
            2. ¿Qué tipo de información contiene?
            3. ¿Hay datos financieros o económicos?
            
            Responde en formato JSON.
            """
            
            response = llm.invoke(prompt)
            
            print("  ✅ Content analysis working")
            print(f"      Analysis: {response.content[:200]}...")
            return True
        else:
            print("  ❌ Content analysis failed - no content to analyze")
            return False
        
    except Exception as e:
        print(f"  ❌ Content analysis failed: {str(e)}")
        return False


def main():
    """Run tests with working webpages."""
    print("🚀 Testing Pipeline with Working Webpages")
    print("=" * 60)
    print("📊 Testing web scraping with known working pages")
    print("🔒 No database writes - Context-efficient testing only")
    print("=" * 60)
    
    # Test each component
    results = []
    
    results.append(test_working_webpages())
    results.append(test_financial_data_extraction_working())
    results.append(test_paraguayan_search())
    results.append(test_content_analysis())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Working Webpage Test Results:")
    print("=" * 60)
    
    test_names = [
        "Working Webpages",
        "Financial Data Extraction (Working)", 
        "Paraguayan Content Search",
        "Content Analysis"
    ]
    
    passed = sum(results)
    total = len(results)
    
    for i, (name, result) in enumerate(zip(test_names, results)):
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status} - {name}")
    
    print(f"\n📈 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
    
    if passed == total:
        print("\n🎉 SUCCESS: Web scraping is working with real pages!")
        print("   Ready for full pipeline testing.")
    else:
        print(f"\n⚠️  {total-passed} test(s) failed. Check configuration.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 