#!/usr/bin/env python3
"""
Test Pipeline with Real Webpages

This test uses real Paraguayan institution webpages to verify
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
    extract_financial_data,
    search_financial_institutions
)


def test_web_search():
    """Test web search functionality."""
    print("\n🔍 Testing Web Search...")
    
    try:
        # Test search for Paraguayan financial institutions
        query = "bolsa de valores paraguay movimientos diarios"
        results = search_web(query, num_results=3)
        
        if results:
            print("  ✅ Web search working")
            print(f"      Found {len(results)} results")
            for i, result in enumerate(results[:2]):
                print(f"      {i+1}. {result.get('title', 'No title')}")
                print(f"         URL: {result.get('url', 'No URL')}")
        else:
            print("  ❌ Web search failed - no results")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Web search failed: {str(e)}")
        return False


def test_webpage_scraping():
    """Test webpage scraping functionality."""
    print("\n📄 Testing Webpage Scraping...")
    
    try:
        # Test with a known Paraguayan institution URL
        test_urls = [
            "https://www.bvp.com.py/",
            "https://www.hacienda.gov.py/",
            "https://www.bcp.gov.py/"
        ]
        
        for url in test_urls:
            print(f"      Testing: {url}")
            result = scrape_webpage(url)
            
            if result.get("content"):
                print(f"      ✅ Scraped successfully")
                print(f"         Title: {result.get('title', 'No title')}")
                print(f"         Content length: {len(result.get('content', ''))} chars")
                return True
            else:
                print(f"      ❌ Failed to scrape: {result.get('metadata', {}).get('error', 'Unknown error')}")
        
        return False
        
    except Exception as e:
        print(f"  ❌ Webpage scraping failed: {str(e)}")
        return False


def test_financial_data_extraction():
    """Test financial data extraction from webpages."""
    print("\n💰 Testing Financial Data Extraction...")
    
    try:
        # Test with a financial institution
        test_url = "https://www.bvp.com.py/"
        result = extract_financial_data(test_url)
        
        if result and "error" not in result:
            print("  ✅ Financial data extraction working")
            print(f"      URL: {result.get('url', 'No URL')}")
            print(f"      Extracted data length: {len(result.get('extracted_data', ''))} chars")
            return True
        else:
            print(f"  ❌ Financial data extraction failed: {result.get('error', 'Unknown error')}")
            return False
        
    except Exception as e:
        print(f"  ❌ Financial data extraction failed: {str(e)}")
        return False


def test_financial_institution_search():
    """Test searching for financial institutions and extracting their data."""
    print("\n🏛️ Testing Financial Institution Search...")
    
    try:
        # Test search for Paraguayan financial institutions
        query = "bolsa valores paraguay"
        results = search_financial_institutions(query)
        
        if results:
            print("  ✅ Financial institution search working")
            print(f"      Found {len(results)} institutions with data")
            for i, result in enumerate(results[:2]):
                institution = result.get("search_result", {})
                print(f"      {i+1}. {institution.get('title', 'No title')}")
                print(f"         URL: {institution.get('url', 'No URL')}")
        else:
            print("  ❌ Financial institution search failed - no results")
            return False
            
        return True
        
    except Exception as e:
        print(f"  ❌ Financial institution search failed: {str(e)}")
        return False


def test_paraguayan_institutions():
    """Test with specific Paraguayan institutions."""
    print("\n🇵🇾 Testing Paraguayan Institutions...")
    
    try:
        institutions = [
            {
                "name": "Bolsa de Valores y Productos de Asunción",
                "url": "https://www.bvp.com.py/",
                "query": "movimientos diarios bolsa valores"
            },
            {
                "name": "Ministerio de Hacienda",
                "url": "https://www.hacienda.gov.py/",
                "query": "informes financieros trimestre"
            },
            {
                "name": "Banco Central del Paraguay",
                "url": "https://www.bcp.gov.py/",
                "query": "indicadores económicos paraguay"
            }
        ]
        
        successful_tests = 0
        
        for institution in institutions:
            print(f"      Testing: {institution['name']}")
            
            # Test scraping
            scraped = scrape_webpage(institution['url'])
            if scraped.get("content"):
                print(f"         ✅ Scraped successfully")
                successful_tests += 1
            else:
                print(f"         ❌ Scraping failed")
            
            # Test search
            search_results = search_web(institution['query'], num_results=2)
            if search_results:
                print(f"         ✅ Search working")
                successful_tests += 1
            else:
                print(f"         ❌ Search failed")
        
        if successful_tests > 0:
            print(f"  ✅ Paraguayan institutions test: {successful_tests}/6 successful")
            return True
        else:
            print("  ❌ Paraguayan institutions test failed")
            return False
        
    except Exception as e:
        print(f"  ❌ Paraguayan institutions test failed: {str(e)}")
        return False


def main():
    """Run tests with real webpages."""
    print("🚀 Testing Pipeline with Real Webpages")
    print("=" * 60)
    print("📊 Testing web scraping with Paraguayan institutions")
    print("🔒 No database writes - Context-efficient testing only")
    print("=" * 60)
    
    # Test configuration
    print("\n⚙️ Testing Configuration...")
    try:
        config = get_config()
        print("  ✅ Configuration loaded successfully")
        print(f"      Serper API: {'Configured' if config.serper_api_key else 'Missing'}")
        print(f"      Firecrawl API: {'Configured' if config.firecrawl_api_key else 'Missing'}")
    except Exception as e:
        print(f"  ❌ Configuration Failed: {str(e)}")
        return
    
    # Test each component
    results = []
    
    results.append(test_web_search())
    results.append(test_webpage_scraping())
    results.append(test_financial_data_extraction())
    results.append(test_financial_institution_search())
    results.append(test_paraguayan_institutions())
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Real Webpage Test Results:")
    print("=" * 60)
    
    test_names = [
        "Web Search",
        "Webpage Scraping", 
        "Financial Data Extraction",
        "Financial Institution Search",
        "Paraguayan Institutions"
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
        print(f"\n⚠️  {total-passed} test(s) failed. Check API keys and connectivity.")
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 