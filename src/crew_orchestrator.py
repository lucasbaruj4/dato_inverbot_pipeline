"""
Crew Orchestrator Module

This module defines the CrewAI crew for orchestrating the complete pipeline.
It creates and manages the crew that coordinates all agents (extraction, processing, vectorization, loading).
"""

from crewai import Crew, Process, Task
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from .extraction.extraction_agent import ExtractionAgent
from .processing.processing_agent import StructuredProcessingAgent
from .vectorization.vectorization_agent import VectorizationAgent
from .loading.loading_agent import LoadingAgent

logger = logging.getLogger(__name__)

class CrewOrchestrator:
    """
    CrewAI orchestrator for the Inverbot Data Pipeline.
    
    This class manages the creation and execution of the complete pipeline crew,
    coordinating all agents (extraction, processing, vectorization, loading) in a
    sequential process.
    """
    
    def __init__(self, simulation_mode: bool = False):
        """
        Initialize the crew orchestrator.
        
        Args:
            simulation_mode: If True, all loading operations will be simulated
        """
        self.simulation_mode = simulation_mode
        self.crew = None
        self.agents = {}
        self.tasks = []
        
        # Initialize all agents
        self._initialize_agents()
        
        # Create tasks
        self._create_tasks()
        
        # Create crew
        self._create_crew()
        
        logger.info(f"CrewOrchestrator initialized (simulation_mode: {simulation_mode})")
    
    def _initialize_agents(self):
        """Initialize all pipeline agents."""
        try:
            logger.info("Initializing pipeline agents...")
            
            self.agents['extraction'] = ExtractionAgent()
            self.agents['processing'] = StructuredProcessingAgent()
            self.agents['vectorization'] = VectorizationAgent()
            self.agents['loading'] = LoadingAgent()
            
            logger.info("✅ All agents initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Error initializing agents: {e}")
            raise
    
    def _create_tasks(self):
        """Create the pipeline tasks."""
        try:
            logger.info("Creating pipeline tasks...")
            
            # Task 1: Extract data from sources
            extract_task = Task(
                description=(
                    "Extract raw content from the provided data sources. "
                    "Handle different content types (JSON, TEXT, PDF, EXCEL, PNG) "
                    "and return structured data with source information."
                ),
                expected_output=(
                    "A list of dictionaries, each containing: "
                    "'source_category', 'source_url', 'content_type', 'raw_content'"
                ),
                agent=self.agents['extraction'].get_agent(),
                context="This is the first step in the pipeline. Extract raw data from various sources."
            )
            
            # Task 2: Process extracted data into structured format
            process_task = Task(
                description=(
                    "Process the extracted raw data into structured format according to Supabase schemas. "
                    "Identify the type of data and apply appropriate processing logic. "
                    "Handle financial reports, daily movements, macroeconomic data, and public contracts."
                ),
                expected_output=(
                    "Structured data conforming to Supabase schemas: "
                    "Resumen_Informe_Financiero, Movimiento_Diario_Bolsa, Dato_Macroeconomico, etc."
                ),
                agent=self.agents['processing'].get_agent(),
                context="This step transforms raw extracted data into structured database records."
            )
            
            # Task 3: Create vector embeddings
            vectorize_task = Task(
                description=(
                    "Create vector embeddings from the processed content. "
                    "Chunk text appropriately and generate embeddings for vector database storage. "
                    "Prepare metadata for Pinecone insertion."
                ),
                expected_output=(
                    "Vector data with embeddings and metadata ready for Pinecone: "
                    "list of dictionaries with 'id', 'values', 'metadata'"
                ),
                agent=self.agents['vectorization'].get_agent(),
                context="This step prepares data for vector database storage and semantic search."
            )
            
            # Task 4: Load data into databases
            load_task = Task(
                description=(
                    f"Load the structured and vector data into the appropriate databases. "
                    f"Insert structured data into Supabase tables and vector data into Pinecone indexes. "
                    f"{'SIMULATION MODE: No actual database writes will occur.' if self.simulation_mode else ''}"
                ),
                expected_output=(
                    "Loading report with status, counts, and any errors encountered. "
                    "Include statistics for both structured and vector data loading."
                ),
                agent=self.agents['loading'].get_agent(),
                context="This is the final step that persists data to the databases."
            )
            
            self.tasks = [extract_task, process_task, vectorize_task, load_task]
            logger.info(f"✅ Created {len(self.tasks)} pipeline tasks")
            
        except Exception as e:
            logger.error(f"❌ Error creating tasks: {e}")
            raise
    
    def _create_crew(self):
        """Create the CrewAI crew."""
        try:
            logger.info("Creating CrewAI crew...")
            
            # Get all agents
            crew_agents = [
                self.agents['extraction'].get_agent(),
                self.agents['processing'].get_agent(),
                self.agents['vectorization'].get_agent(),
                self.agents['loading'].get_agent()
            ]
            
            # Create crew with sequential process
            self.crew = Crew(
                agents=crew_agents,
                tasks=self.tasks,
                process=Process.sequential,
                verbose=True,
                memory=True  # Enable memory for context between tasks
            )
            
            logger.info("✅ CrewAI crew created successfully")
            
        except Exception as e:
            logger.error(f"❌ Error creating crew: {e}")
            raise
    
    def execute_pipeline(self, data_sources: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Execute the complete pipeline with the provided data sources.
        
        Args:
            data_sources: List of data source dictionaries with 'category', 'url', 'content_type'
            
        Returns:
            Dictionary containing pipeline execution results
        """
        try:
            logger.info(f"🚀 Starting pipeline execution with {len(data_sources)} data sources")
            logger.info(f"Simulation mode: {self.simulation_mode}")
            
            # Execute the crew
            result = self.crew.kickoff(inputs={'sources_list': data_sources})
            
            # Prepare execution report
            execution_report = {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'data_sources_count': len(data_sources),
                'simulation_mode': self.simulation_mode,
                'result': result,
                'execution_summary': {
                    'agents_used': list(self.agents.keys()),
                    'tasks_executed': len(self.tasks),
                    'process_type': 'sequential'
                }
            }
            
            logger.info("✅ Pipeline execution completed successfully")
            return execution_report
            
        except Exception as e:
            logger.error(f"❌ Pipeline execution failed: {e}")
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e),
                'data_sources_count': len(data_sources),
                'simulation_mode': self.simulation_mode
            }
    
    def get_crew_info(self) -> Dict[str, Any]:
        """Get information about the configured crew."""
        return {
            'agents': {
                name: {
                    'role': agent.get_agent().role,
                    'goal': agent.get_agent().goal
                } for name, agent in self.agents.items()
            },
            'tasks': [
                {
                    'description': task.description[:100] + "..." if len(task.description) > 100 else task.description,
                    'expected_output': task.expected_output[:100] + "..." if len(task.expected_output) > 100 else task.expected_output
                } for task in self.tasks
            ],
            'process_type': 'sequential',
            'simulation_mode': self.simulation_mode,
            'crew_created': self.crew is not None
        }
    
    def test_crew_setup(self) -> Dict[str, Any]:
        """Test that the crew is properly configured."""
        try:
            logger.info("Testing crew setup...")
            
            # Check if all agents are initialized
            agent_status = {}
            for name, agent in self.agents.items():
                try:
                    crew_agent = agent.get_agent()
                    agent_status[name] = {
                        'status': 'success',
                        'role': crew_agent.role,
                        'tools_count': len(crew_agent.tools) if hasattr(crew_agent, 'tools') else 0
                    }
                except Exception as e:
                    agent_status[name] = {
                        'status': 'error',
                        'error': str(e)
                    }
            
            # Check if crew is created
            crew_status = {
                'created': self.crew is not None,
                'agents_count': len(self.agents),
                'tasks_count': len(self.tasks)
            }
            
            # Overall status
            all_agents_ok = all(status['status'] == 'success' for status in agent_status.values())
            overall_status = 'success' if all_agents_ok and crew_status['created'] else 'error'
            
            return {
                'status': overall_status,
                'timestamp': datetime.now().isoformat(),
                'agents': agent_status,
                'crew': crew_status,
                'simulation_mode': self.simulation_mode
            }
            
        except Exception as e:
            logger.error(f"❌ Crew setup test failed: {e}")
            return {
                'status': 'error',
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }

def create_pipeline_crew(simulation_mode: bool = False) -> CrewOrchestrator:
    """
    Factory function to create a pipeline crew orchestrator.
    
    Args:
        simulation_mode: If True, all loading operations will be simulated
        
    Returns:
        Configured CrewOrchestrator instance
    """
    return CrewOrchestrator(simulation_mode=simulation_mode)

def execute_pipeline_with_sources(data_sources: List[Dict[str, Any]], simulation_mode: bool = False) -> Dict[str, Any]:
    """
    Convenience function to execute the pipeline with data sources.
    
    Args:
        data_sources: List of data source dictionaries
        simulation_mode: If True, all loading operations will be simulated
        
    Returns:
        Pipeline execution results
    """
    orchestrator = create_pipeline_crew(simulation_mode=simulation_mode)
    return orchestrator.execute_pipeline(data_sources) 