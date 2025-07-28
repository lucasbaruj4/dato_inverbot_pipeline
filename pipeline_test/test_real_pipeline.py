#!/usr/bin/env python3
"""
Real Pipeline Test
Execute the complete CrewAI pipeline with real data extraction and processing
Save all outputs to files instead of database
"""

import os
import json
import sys
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

def setup_output_directories():
    """Create structured output directories."""
    
    base_dir = Path("outputs")
    base_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    directories = [
        "extraction/raw_data",
        "extraction/processed_data", 
        "processing/agent_outputs",
        "processing/structured_data",
        "vectorization/embeddings",
        "vectorization/chunks",
        "loading/simulation_results",
        "crew_logs",
        "summary"
    ]
    
    for dir_path in directories:
        (base_dir / dir_path).mkdir(parents=True, exist_ok=True)
    
    return base_dir

def run_real_extraction():
    """Execute real data extraction with CrewAI."""
    
    print("🔍 EXECUTING REAL EXTRACTION...")
    print("=" * 50)
    
    try:
        from extraction.data_sources import DATA_SOURCES
        from extraction.extraction_agent import ExtractionAgent
        from crewai import Crew, Task
        
        # Create extraction agent - no need to pass data_sources to constructor
        extraction_agent = ExtractionAgent()
        agent = extraction_agent.get_agent()
        
        print(f"✅ Extraction agent created: {agent.role}")
        
        # Create extraction task
        extraction_task = Task(
            description=f"""
            Extract data from the first 3 data sources for testing:
            
            Sources to extract:
            1. {DATA_SOURCES[0]['category']} - {DATA_SOURCES[0]['url']}
            2. {DATA_SOURCES[1]['category']} - {DATA_SOURCES[1]['url']}
            3. {DATA_SOURCES[4]['category']} - {DATA_SOURCES[4]['url']} (BCP data)
            
            For each source:
            - Access the URL and extract meaningful content
            - Clean and structure the data
            - Identify key financial/economic information
            - Return structured data ready for processing
            
            Focus on quality over quantity - extract the most relevant information.
            """,
            agent=agent,
            expected_output="Structured data extracted from 3 sources with financial/economic information"
        )
        
        # Create and run crew
        print("🤖 Creating extraction crew...")
        crew = Crew(
            agents=[agent],
            tasks=[extraction_task],
            verbose=True
        )
        
        print("🚀 STARTING REAL EXTRACTION...")
        result = crew.kickoff()
        
        # Save extraction results
        extraction_results = {
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "sources_processed": 3,
            "agent_output": str(result),
            "sources_details": [
                {"category": DATA_SOURCES[0]['category'], "url": DATA_SOURCES[0]['url']},
                {"category": DATA_SOURCES[1]['category'], "url": DATA_SOURCES[1]['url']},
                {"category": DATA_SOURCES[4]['category'], "url": DATA_SOURCES[4]['url']}
            ]
        }
        
        # Save to file
        output_file = Path("outputs/extraction/processed_data/real_extraction_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extraction_results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Extraction completed and saved to: {output_file}")
        return extraction_results
        
    except Exception as e:
        print(f"❌ Extraction failed: {str(e)}")
        return {"status": "failed", "error": str(e)}

def run_real_processing(extraction_data):
    """Execute real data processing with CrewAI."""
    
    print("\n⚙️ EXECUTING REAL PROCESSING...")
    print("=" * 50)
    
    try:
        from processing.processing_agent import StructuredProcessingAgent
        from crewai import Crew, Task
        
        # Create processing agent
        processing_agent = StructuredProcessingAgent()
        agent = processing_agent.get_agent()
        
        print(f"✅ Processing agent created: {agent.role}")
        
        # Create processing task
        processing_task = Task(
            description=f"""
            Process the extracted data and structure it according to our schemas:
            
            Raw Data to Process:
            {extraction_data.get('agent_output', 'No data available')}
            
            Your tasks:
            1. Analyze the extracted financial/economic data
            2. Identify data types (balances, indicators, news, etc.)
            3. Structure data according to appropriate schemas
            4. Validate data quality and completeness
            5. Create structured output ready for vectorization
            
            Focus on creating high-quality, well-structured data.
            """,
            agent=agent,
            expected_output="Structured and validated data organized by schema types"
        )
        
        # Create and run crew
        print("🤖 Creating processing crew...")
        crew = Crew(
            agents=[agent],
            tasks=[processing_task],
            verbose=True
        )
        
        print("🚀 STARTING REAL PROCESSING...")
        result = crew.kickoff()
        
        # Save processing results
        processing_results = {
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "agent_output": str(result),
            "input_data_summary": f"Processed {extraction_data.get('sources_processed', 0)} sources"
        }
        
        # Save to file
        output_file = Path("outputs/processing/structured_data/real_processing_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(processing_results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Processing completed and saved to: {output_file}")
        return processing_results
        
    except Exception as e:
        print(f"❌ Processing failed: {str(e)}")
        return {"status": "failed", "error": str(e)}

def run_real_vectorization(processing_data):
    """Execute real vectorization with CrewAI."""
    
    print("\n🔢 EXECUTING REAL VECTORIZATION...")
    print("=" * 50)
    
    try:
        from vectorization.vectorization_agent import VectorizationAgent
        from crewai import Crew, Task
        
        # Create vectorization agent
        vectorization_agent = VectorizationAgent()
        agent = vectorization_agent.get_agent()
        
        print(f"✅ Vectorization agent created: {agent.role}")
        
        # Create vectorization task
        vectorization_task = Task(
            description=f"""
            Create embeddings from the processed data:
            
            Processed Data:
            {processing_data.get('agent_output', 'No data available')}
            
            Your tasks:
            1. Break down the structured data into meaningful chunks
            2. Generate embeddings using Google's text-embedding-004 model
            3. Create vector representations optimized for search
            4. Organize chunks by data type and relevance
            5. Prepare vector data for storage (but don't store yet)
            
            Focus on creating high-quality embeddings for semantic search.
            """,
            agent=agent,
            expected_output="Vector embeddings and chunks ready for database storage"
        )
        
        # Create and run crew
        print("🤖 Creating vectorization crew...")
        crew = Crew(
            agents=[agent],
            tasks=[vectorization_task],
            verbose=True
        )
        
        print("🚀 STARTING REAL VECTORIZATION...")
        result = crew.kickoff()
        
        # Save vectorization results
        vectorization_results = {
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "agent_output": str(result),
            "embedding_model": "models/text-embedding-004",
            "chunks_info": "Created from processed financial data"
        }
        
        # Save to file
        output_file = Path("outputs/vectorization/embeddings/real_vectorization_results.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(vectorization_results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Vectorization completed and saved to: {output_file}")
        return vectorization_results
        
    except Exception as e:
        print(f"❌ Vectorization failed: {str(e)}")
        return {"status": "failed", "error": str(e)}

def run_real_loading(vectorization_data):
    """Execute real loading simulation (no actual DB writes)."""
    
    print("\n📥 EXECUTING REAL LOADING SIMULATION...")
    print("=" * 50)
    
    try:
        from loading.loading_agent import LoadingAgent
        from crewai import Crew, Task
        
        # Create loading agent
        loading_agent = LoadingAgent()
        agent = loading_agent.get_agent()
        
        print(f"✅ Loading agent created: {agent.role}")
        
        # Create loading task
        loading_task = Task(
            description=f"""
            Prepare data for database loading (SIMULATION MODE - NO ACTUAL WRITES):
            
            Vector Data to Load:
            {vectorization_data.get('agent_output', 'No data available')}
            
            Your tasks:
            1. Validate all data for database compatibility
            2. Prepare Supabase insert statements (structured data)
            3. Prepare Pinecone insert statements (vector data)
            4. Create loading summary and validation report
            5. SIMULATE the loading process (DO NOT execute actual inserts)
            
            Focus on preparing perfect data for eventual database insertion.
            """,
            agent=agent,
            expected_output="Database-ready data with loading instructions (simulation mode)"
        )
        
        # Create and run crew
        print("🤖 Creating loading crew...")
        crew = Crew(
            agents=[agent],
            tasks=[loading_task],
            verbose=True
        )
        
        print("🚀 STARTING REAL LOADING SIMULATION...")
        result = crew.kickoff()
        
        # Save loading results
        loading_results = {
            "timestamp": datetime.now().isoformat(),
            "status": "completed",
            "simulation_mode": True,
            "agent_output": str(result),
            "database_targets": ["Supabase", "Pinecone"],
            "note": "SIMULATION MODE - No actual database writes performed"
        }
        
        # Save to file
        output_file = Path("outputs/loading/simulation_results/real_loading_simulation.json")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(loading_results, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Loading simulation completed and saved to: {output_file}")
        return loading_results
        
    except Exception as e:
        print(f"❌ Loading failed: {str(e)}")
        return {"status": "failed", "error": str(e)}

def create_final_summary(extraction_results, processing_results, vectorization_results, loading_results):
    """Create comprehensive summary of real pipeline execution."""
    
    print("\n📋 CREATING FINAL SUMMARY...")
    print("=" * 50)
    
    # Check success status
    all_successful = all(
        result.get("status") == "completed" 
        for result in [extraction_results, processing_results, vectorization_results, loading_results]
    )
    
    summary = {
        "test_timestamp": datetime.now().isoformat(),
        "pipeline_type": "REAL EXECUTION",
        "pipeline_status": "SUCCESS" if all_successful else "FAILED",
        "simulation_mode": True,
        "stages_completed": {
            "extraction": extraction_results.get("status") == "completed",
            "processing": processing_results.get("status") == "completed",
            "vectorization": vectorization_results.get("status") == "completed",
            "loading": loading_results.get("status") == "completed"
        },
        "data_flow": {
            "sources_extracted": extraction_results.get("sources_processed", 0),
            "data_processed": "Yes" if processing_results.get("status") == "completed" else "No",
            "embeddings_created": "Yes" if vectorization_results.get("status") == "completed" else "No",
            "loading_prepared": "Yes" if loading_results.get("status") == "completed" else "No"
        },
        "output_files": {
            "extraction": "outputs/extraction/processed_data/real_extraction_results.json",
            "processing": "outputs/processing/structured_data/real_processing_results.json",
            "vectorization": "outputs/vectorization/embeddings/real_vectorization_results.json",
            "loading": "outputs/loading/simulation_results/real_loading_simulation.json"
        }
    }
    
    # Save summary
    summary_file = Path("outputs/summary/real_pipeline_summary.json")
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    
    # Create detailed report
    status_emoji = "✅" if all_successful else "❌"
    
    report = f"""# Real Pipeline Execution Report

## Execution Summary
- **Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **Type**: REAL CREWAI EXECUTION
- **Status**: {status_emoji} {summary['pipeline_status']}
- **Mode**: Simulation (No database writes)

## Pipeline Stages
- {'✅' if summary['stages_completed']['extraction'] else '❌'} **Extraction**: Real web scraping and data extraction
- {'✅' if summary['stages_completed']['processing'] else '❌'} **Processing**: Real LLM-powered data structuring  
- {'✅' if summary['stages_completed']['vectorization'] else '❌'} **Vectorization**: Real Google AI embeddings
- {'✅' if summary['stages_completed']['loading'] else '❌'} **Loading**: Real database preparation (simulated)

## Data Flow
- **Sources Extracted**: {summary['data_flow']['sources_extracted']} real sources
- **Data Processed**: {summary['data_flow']['data_processed']} with Google Gemini
- **Embeddings Created**: {summary['data_flow']['embeddings_created']} with Google text-embedding-004
- **Loading Prepared**: {summary['data_flow']['loading_prepared']} for Supabase + Pinecone

## Output Files
```
outputs/
├── extraction/processed_data/real_extraction_results.json
├── processing/structured_data/real_processing_results.json
├── vectorization/embeddings/real_vectorization_results.json
├── loading/simulation_results/real_loading_simulation.json
└── summary/real_pipeline_summary.json
```

## Next Steps
1. ✅ Review all agent outputs in outputs/ directory
2. ✅ Validate data quality and structure
3. 🔄 Enable real database writes when ready
4. 📈 Scale to all 13 data sources
"""
    
    report_file = Path("outputs/summary/real_pipeline_report.md")
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"✅ Summary saved to: {summary_file}")
    print(f"✅ Report saved to: {report_file}")

def run_real_pipeline():
    """Execute the complete real pipeline with CrewAI."""
    
    print("🚀 STARTING REAL PIPELINE EXECUTION")
    print("=" * 60)
    print("🔥 EXECUTING ACTUAL CREWAI AGENTS")
    print("📊 REAL DATA EXTRACTION AND PROCESSING")
    print("🛡️ OUTPUTS TO FILES (NO DATABASE WRITES)")
    print("=" * 60)
    
    try:
        # Setup
        output_dir = setup_output_directories()
        print(f"📁 Output directories created: {output_dir}")
        
        # Execute real pipeline
        extraction_results = run_real_extraction()
        processing_results = run_real_processing(extraction_results)
        vectorization_results = run_real_vectorization(processing_results)
        loading_results = run_real_loading(vectorization_results)
        
        # Create summary
        create_final_summary(extraction_results, processing_results, vectorization_results, loading_results)
        
        print("\n" + "=" * 60)
        print("🎯 REAL PIPELINE EXECUTION COMPLETED!")
        print("=" * 60)
        print("📁 All outputs saved in: outputs/")
        print("📋 Summary: outputs/summary/real_pipeline_summary.json")
        print("📄 Report: outputs/summary/real_pipeline_report.md")
        
        # Final status
        all_successful = all(
            result.get("status") == "completed" 
            for result in [extraction_results, processing_results, vectorization_results, loading_results]
        )
        
        if all_successful:
            print("\n🎉 SUCCESS: Real pipeline executed successfully!")
            print("📊 Check outputs/ for actual CrewAI agent work")
        else:
            print("\n⚠️ Some stages failed - check outputs/ for details")
        
        return all_successful
        
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_real_pipeline()
    
    if success:
        print("\n✅ Real pipeline test completed successfully!")
    else:
        print("\n❌ Real pipeline test failed!") 