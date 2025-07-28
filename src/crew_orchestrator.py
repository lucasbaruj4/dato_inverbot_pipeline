"""
Crew Orchestrator Module

This module defines the CrewAI crew for orchestrating the complete pipeline.
It creates and manages the crew that coordinates all agents (extraction, processing, vectorization, loading).
"""

from crewai import Crew, Process, Task
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from extraction.extraction_agent import ExtractionAgent
from processing.processing_agent import StructuredProcessingAgent
from vectorization.vectorization_agent import VectorizationAgent
from loading.loading_agent import LoadingAgent

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
        """Create the pipeline tasks with proper data flow and token optimization."""
        try:
            logger.info("Creating optimized pipeline tasks...")
            
            # Task 1: Extract data from sources
            extract_task = Task(
                description=(
                    "Extract raw content from data sources. "
                    "Handle JSON, TEXT, PDF, EXCEL, PNG formats. "
                    "Return structured data with source info."
                ),
                expected_output=(
                    "List of dicts with: source_category, source_url, content_type, raw_content"
                ),
                agent=self.agents['extraction'].get_agent(),
                context=["First step: extract raw data from sources."]
            )
            
            # Task 2: Process extracted data (depends on extract_task output)
            process_task = Task(
                description=(
                    "Process extracted data into structured format. "
                    "Map to Supabase schemas: financial reports, movements, macro data, contracts."
                ),
                expected_output=(
                    "Structured data for: Resumen_Informe_Financiero, Movimiento_Diario_Bolsa, Dato_Macroeconomico"
                ),
                agent=self.agents['processing'].get_agent(),
                context=["Transform raw data into structured database records."],
                output_json=True  # Ensure structured output
            )
            
            # Task 3: Create vector embeddings (depends on process_task output)
            vectorize_task = Task(
                description=(
                    "Create vector embeddings from processed content. "
                    "Chunk text and generate embeddings for Pinecone storage."
                ),
                expected_output=(
                    "Vector data: list of dicts with id, values, metadata"
                ),
                agent=self.agents['vectorization'].get_agent(),
                context=["Prepare data for vector database storage."],
                output_json=True
            )
            
            # Task 4: Load data into databases (depends on vectorize_task output)
            load_task = Task(
                description=(
                    f"Load structured and vector data into databases. "
                    f"Insert into Supabase tables and Pinecone indexes. "
                    f"{'SIMULATION: No actual writes.' if self.simulation_mode else ''}"
                ),
                expected_output=(
                    "Loading report: status, counts, errors for structured and vector data."
                ),
                agent=self.agents['loading'].get_agent(),
                context=["Final step: persist data to databases."],
                output_json=True
            )
            
            self.tasks = [extract_task, process_task, vectorize_task, load_task]
            logger.info(f"✅ Created {len(self.tasks)} optimized pipeline tasks")
            
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
            
            # Reset token usage for this execution
            from utils.logging import reset_token_usage, get_token_usage_summary
            reset_token_usage()
            
            # Execute the crew
            result = self.crew.kickoff(inputs={'sources_list': data_sources})
            
            # Get token usage summary
            token_summary = get_token_usage_summary()
            
            # Prepare execution report
            execution_report = {
                'status': 'success',
                'timestamp': datetime.now().isoformat(),
                'data_sources_count': len(data_sources),
                'simulation_mode': self.simulation_mode,
                'result': result,
                'token_usage': token_summary,
                'execution_summary': {
                    'agents_used': list(self.agents.keys()),
                    'tasks_executed': len(self.tasks),
                    'process_type': 'sequential',
                    'estimated_cost_usd': token_summary['estimated_cost_usd']
                }
            }
            
            logger.info(f"✅ Pipeline execution completed successfully")
            logger.info(f"💰 Estimated cost: ${token_summary['estimated_cost_usd']}")
            logger.info(f"📊 Total tokens: {token_summary['total_input_tokens']} input, {token_summary['total_output_tokens']} output")
            
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