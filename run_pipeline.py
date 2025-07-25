#!/usr/bin/env python3
"""
Inverbot Data Pipeline - Main Execution Script

This script provides the main entry point for running the complete data pipeline.
It uses the CrewOrchestrator to execute the full pipeline with real data sources.
"""

import sys
import argparse
from pathlib import Path
from typing import List, Dict, Any
import logging

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.crew_orchestrator import create_pipeline_crew, execute_pipeline_with_sources
from src.extraction.data_sources import get_data_sources
from src.utils.logging import get_logger

logger = get_logger(__name__)

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Inverbot Data Pipeline - Main Execution Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run pipeline with all data sources
  python run_pipeline.py

  # Run pipeline in simulation mode (no database writes)
  python run_pipeline.py --simulation

  # Run pipeline with specific data sources
  python run_pipeline.py --sources financial macroeconomic

  # Run pipeline with verbose logging
  python run_pipeline.py --verbose

  # Run pipeline with custom data sources file
  python run_pipeline.py --data-sources custom_sources.json
        """
    )
    
    parser.add_argument(
        '--simulation',
        action='store_true',
        help='Run in simulation mode (no database writes)'
    )
    
    parser.add_argument(
        '--sources',
        nargs='+',
        choices=['financial', 'macroeconomic', 'contracts', 'news', 'movements'],
        help='Specific data source categories to process'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--data-sources',
        type=str,
        help='Path to custom data sources JSON file'
    )
    
    parser.add_argument(
        '--test-mode',
        action='store_true',
        help='Run with test data sources only'
    )
    
    return parser.parse_args()

def get_pipeline_data_sources(args) -> List[Dict[str, Any]]:
    """Get data sources based on command line arguments."""
    if args.data_sources:
        # Load custom data sources from file
        import json
        try:
            with open(args.data_sources, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load custom data sources: {e}")
            sys.exit(1)
    
    elif args.test_mode:
        # Use test data sources
        return get_data_sources("test")
    
    elif args.sources:
        # Filter main data sources by category
        all_sources = get_data_sources("main")
        filtered_sources = []
        
        for source in all_sources:
            category = source.get('category', '').lower()
            if any(source_type in category for source_type in args.sources):
                filtered_sources.append(source)
        
        logger.info(f"Filtered to {len(filtered_sources)} sources from categories: {args.sources}")
        return filtered_sources
    
    else:
        # Use all main data sources
        return get_data_sources("main")

def main():
    """Main pipeline execution function."""
    # Parse arguments
    args = parse_arguments()
    
    # Set up logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)
    
    logger.info("🚀 Starting Inverbot Data Pipeline")
    logger.info("=" * 50)
    
    # Log execution parameters
    logger.info(f"Simulation mode: {args.simulation}")
    logger.info(f"Test mode: {args.test_mode}")
    if args.sources:
        logger.info(f"Source categories: {args.sources}")
    if args.data_sources:
        logger.info(f"Custom data sources: {args.data_sources}")
    
    try:
        # Get data sources
        data_sources = get_pipeline_data_sources(args)
        logger.info(f"📊 Processing {len(data_sources)} data sources")
        
        if not data_sources:
            logger.error("No data sources found. Exiting.")
            sys.exit(1)
        
        # Log data sources for transparency
        for i, source in enumerate(data_sources[:5]):  # Show first 5
            logger.info(f"  {i+1}. {source.get('category', 'Unknown')} - {source.get('url', 'No URL')}")
        if len(data_sources) > 5:
            logger.info(f"  ... and {len(data_sources) - 5} more sources")
        
        # Execute pipeline
        logger.info("🔄 Executing pipeline...")
        result = execute_pipeline_with_sources(
            data_sources=data_sources,
            simulation_mode=args.simulation
        )
        
        # Process results
        if result['status'] == 'success':
            logger.info("✅ Pipeline execution completed successfully!")
            
            # Log execution summary
            execution_summary = result.get('execution_summary', {})
            logger.info(f"📈 Execution Summary:")
            logger.info(f"  - Agents used: {execution_summary.get('agents_used', [])}")
            logger.info(f"  - Tasks executed: {execution_summary.get('tasks_executed', 0)}")
            logger.info(f"  - Process type: {execution_summary.get('process_type', 'unknown')}")
            
            # Log simulation mode if active
            if args.simulation:
                logger.info("🛡️ SIMULATION MODE: No actual database writes occurred")
                logger.info("   To run with real database writes, remove --simulation flag")
            
            return 0
            
        else:
            logger.error(f"❌ Pipeline execution failed: {result.get('error', 'Unknown error')}")
            return 1
            
    except KeyboardInterrupt:
        logger.info("⏹️ Pipeline execution interrupted by user")
        return 1
        
    except Exception as e:
        logger.error(f"❌ Unexpected error during pipeline execution: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code) 