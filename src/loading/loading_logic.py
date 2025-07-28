"""
Loading Logic Module

This module contains the core loading functionality for inserting processed data
into Supabase (structured data) and Pinecone (vector data) databases.
"""

import logging
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

from loading.database_connectors import SupabaseConnector, PineconeConnector

logger = logging.getLogger(__name__)

class LoadingLogic:
    """
    Core loading logic for database operations.
    
    This class provides methods to:
    - Load structured data into Supabase tables
    - Load vector data into Pinecone indexes
    - Handle transactions and error recovery
    - Validate data before loading
    - Coordinate loading operations between databases
    """
    
    def __init__(self, supabase_connector: Optional[SupabaseConnector] = None, 
                 pinecone_connector: Optional[PineconeConnector] = None):
        """
        Initialize the loading logic.
        
        Args:
            supabase_connector: Supabase connector instance (optional, will create if not provided)
            pinecone_connector: Pinecone connector instance (optional, will create if not provided)
        """
        self.supabase_connector = supabase_connector or SupabaseConnector()
        self.pinecone_connector = pinecone_connector or PineconeConnector()
        
        logger.info("LoadingLogic initialized with database connectors")

    def test_connections(self) -> Dict[str, Any]:
        """
        Test connections to both databases.
        
        Returns:
            Dictionary with connection status for both databases
        """
        logger.info("Testing database connections...")
        
        # Test Supabase connection
        supabase_result = self.supabase_connector.test_connection()
        
        # Test Pinecone connection
        pinecone_result = self.pinecone_connector.test_connection()
        
        return {
            'supabase': supabase_result,
            'pinecone': pinecone_result,
            'all_connected': (
                supabase_result.get('status') == 'success' and 
                pinecone_result.get('status') == 'success'
            )
        }

    def load_structured_data(self, table_name: str, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Load structured data into Supabase table.
        
        Args:
            table_name: Name of the target table
            data: Data to insert (single record or list of records)
            
        Returns:
            Dictionary with loading status and details
        """
        logger.info(f"Loading structured data into {table_name}")
        
        try:
            # Validate data
            validation_result = self._validate_structured_data(table_name, data)
            if not validation_result['is_valid']:
                return {
                    'status': 'error',
                    'message': f'Data validation failed: {validation_result["issues"]}',
                    'table': table_name
                }
            
            # Insert data into Supabase
            result = self.supabase_connector.insert_data(table_name, data)
            
            if result['status'] == 'success':
                logger.info(f"Successfully loaded {result['inserted_count']} records into {table_name}")
            else:
                logger.error(f"Failed to load data into {table_name}: {result['message']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error loading structured data into {table_name}: {e}")
            return {
                'status': 'error',
                'message': f'Loading failed: {str(e)}',
                'table': table_name
            }

    def load_vector_data(self, index_name: str, vectors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Load vector data into Pinecone index.
        
        Args:
            index_name: Name of the target index
            vectors: List of vectors to upsert
            
        Returns:
            Dictionary with loading status and details
        """
        logger.info(f"Loading vector data into {index_name}")
        
        try:
            # Validate vectors
            validation_result = self._validate_vector_data(vectors)
            if not validation_result['is_valid']:
                return {
                    'status': 'error',
                    'message': f'Vector validation failed: {validation_result["issues"]}',
                    'index': index_name
                }
            
            # Upsert vectors into Pinecone
            result = self.pinecone_connector.upsert_vectors(index_name, vectors)
            
            if result['status'] == 'success':
                logger.info(f"Successfully loaded {result['upserted_count']} vectors into {index_name}")
            else:
                logger.error(f"Failed to load vectors into {index_name}: {result['message']}")
            
            return result
            
        except Exception as e:
            logger.error(f"Error loading vector data into {index_name}: {e}")
            return {
                'status': 'error',
                'message': f'Loading failed: {str(e)}',
                'index': index_name
            }

    def load_financial_data(self, financial_data: Dict[str, Any], vectors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Load financial data into both Supabase and Pinecone.
        
        Args:
            financial_data: Structured financial data for Supabase
            vectors: Vector data for Pinecone (optional)
            
        Returns:
            Dictionary with loading results for both databases
        """
        logger.info("Loading financial data into databases")
        
        results = {
            'supabase': None,
            'pinecone': None,
            'overall_status': 'pending'
        }
        
        try:
            # Load structured data into Supabase
            if financial_data:
                supabase_result = self.load_structured_data('resumen_informe_financiero', financial_data)
                results['supabase'] = supabase_result
                
                if supabase_result['status'] == 'success':
                    logger.info("Financial data loaded into Supabase successfully")
                else:
                    logger.error(f"Failed to load financial data into Supabase: {supabase_result['message']}")
            
            # Load vector data into Pinecone
            if vectors:
                pinecone_result = self.load_vector_data('documentos-informes-vector', vectors)
                results['pinecone'] = pinecone_result
                
                if pinecone_result['status'] == 'success':
                    logger.info("Financial vectors loaded into Pinecone successfully")
                else:
                    logger.error(f"Failed to load financial vectors into Pinecone: {pinecone_result['message']}")
            
            # Determine overall status
            supabase_success = results['supabase'] and results['supabase']['status'] == 'success'
            pinecone_success = results['pinecone'] and results['pinecone']['status'] == 'success'
            
            if supabase_success and pinecone_success:
                results['overall_status'] = 'success'
            elif supabase_success or pinecone_success:
                results['overall_status'] = 'partial'
            else:
                results['overall_status'] = 'failed'
            
            return results
            
        except Exception as e:
            logger.error(f"Error loading financial data: {e}")
            results['overall_status'] = 'failed'
            return results

    def load_macroeconomic_data(self, macro_data: Dict[str, Any], vectors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Load macroeconomic data into both Supabase and Pinecone.
        
        Args:
            macro_data: Structured macroeconomic data for Supabase
            vectors: Vector data for Pinecone (optional)
            
        Returns:
            Dictionary with loading results for both databases
        """
        logger.info("Loading macroeconomic data into databases")
        
        results = {
            'supabase': None,
            'pinecone': None,
            'overall_status': 'pending'
        }
        
        try:
            # Load structured data into Supabase
            if macro_data:
                supabase_result = self.load_structured_data('dato_macroeconomico', macro_data)
                results['supabase'] = supabase_result
                
                if supabase_result['status'] == 'success':
                    logger.info("Macroeconomic data loaded into Supabase successfully")
                else:
                    logger.error(f"Failed to load macroeconomic data into Supabase: {supabase_result['message']}")
            
            # Load vector data into Pinecone
            if vectors:
                pinecone_result = self.load_vector_data('dato-macroeconomico-vector', vectors)
                results['pinecone'] = pinecone_result
                
                if pinecone_result['status'] == 'success':
                    logger.info("Macroeconomic vectors loaded into Pinecone successfully")
                else:
                    logger.error(f"Failed to load macroeconomic vectors into Pinecone: {pinecone_result['message']}")
            
            # Determine overall status
            supabase_success = results['supabase'] and results['supabase']['status'] == 'success'
            pinecone_success = results['pinecone'] and results['pinecone']['status'] == 'success'
            
            if supabase_success and pinecone_success:
                results['overall_status'] = 'success'
            elif supabase_success or pinecone_success:
                results['overall_status'] = 'partial'
            else:
                results['overall_status'] = 'failed'
            
            return results
            
        except Exception as e:
            logger.error(f"Error loading macroeconomic data: {e}")
            results['overall_status'] = 'failed'
            return results

    def load_public_contracts(self, contract_data: Dict[str, Any], vectors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Load public contract data into both Supabase and Pinecone.
        
        Args:
            contract_data: Structured contract data for Supabase
            vectors: Vector data for Pinecone (optional)
            
        Returns:
            Dictionary with loading results for both databases
        """
        logger.info("Loading public contract data into databases")
        
        results = {
            'supabase': None,
            'pinecone': None,
            'overall_status': 'pending'
        }
        
        try:
            # Load structured data into Supabase
            if contract_data:
                supabase_result = self.load_structured_data('licitacion_contrato', contract_data)
                results['supabase'] = supabase_result
                
                if supabase_result['status'] == 'success':
                    logger.info("Contract data loaded into Supabase successfully")
                else:
                    logger.error(f"Failed to load contract data into Supabase: {supabase_result['message']}")
            
            # Load vector data into Pinecone
            if vectors:
                pinecone_result = self.load_vector_data('licitacion-contrato-vector', vectors)
                results['pinecone'] = pinecone_result
                
                if pinecone_result['status'] == 'success':
                    logger.info("Contract vectors loaded into Pinecone successfully")
                else:
                    logger.error(f"Failed to load contract vectors into Pinecone: {pinecone_result['message']}")
            
            # Determine overall status
            supabase_success = results['supabase'] and results['supabase']['status'] == 'success'
            pinecone_success = results['pinecone'] and results['pinecone']['status'] == 'success'
            
            if supabase_success and pinecone_success:
                results['overall_status'] = 'success'
            elif supabase_success or pinecone_success:
                results['overall_status'] = 'partial'
            else:
                results['overall_status'] = 'failed'
            
            return results
            
        except Exception as e:
            logger.error(f"Error loading public contract data: {e}")
            results['overall_status'] = 'failed'
            return results

    def load_news_data(self, news_data: Dict[str, Any], vectors: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Load news data into both Supabase and Pinecone.
        
        Args:
            news_data: Structured news data for Supabase
            vectors: Vector data for Pinecone (optional)
            
        Returns:
            Dictionary with loading results for both databases
        """
        logger.info("Loading news data into databases")
        
        results = {
            'supabase': None,
            'pinecone': None,
            'overall_status': 'pending'
        }
        
        try:
            # Load structured data into Supabase
            if news_data:
                supabase_result = self.load_structured_data('noticia_relevante', news_data)
                results['supabase'] = supabase_result
                
                if supabase_result['status'] == 'success':
                    logger.info("News data loaded into Supabase successfully")
                else:
                    logger.error(f"Failed to load news data into Supabase: {supabase_result['message']}")
            
            # Load vector data into Pinecone
            if vectors:
                pinecone_result = self.load_vector_data('noticia-relevante-vector', vectors)
                results['pinecone'] = pinecone_result
                
                if pinecone_result['status'] == 'success':
                    logger.info("News vectors loaded into Pinecone successfully")
                else:
                    logger.error(f"Failed to load news vectors into Pinecone: {pinecone_result['message']}")
            
            # Determine overall status
            supabase_success = results['supabase'] and results['supabase']['status'] == 'success'
            pinecone_success = results['pinecone'] and results['pinecone']['status'] == 'success'
            
            if supabase_success and pinecone_success:
                results['overall_status'] = 'success'
            elif supabase_success or pinecone_success:
                results['overall_status'] = 'partial'
            else:
                results['overall_status'] = 'failed'
            
            return results
            
        except Exception as e:
            logger.error(f"Error loading news data: {e}")
            results['overall_status'] = 'failed'
            return results

    def load_data_by_type(self, data_type: str, structured_data: Optional[Dict[str, Any]] = None, 
                         vector_data: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Load data by type into appropriate databases.
        
        Args:
            data_type: Type of data ('financial', 'macroeconomic', 'contracts', 'news')
            structured_data: Structured data for Supabase
            vector_data: Vector data for Pinecone
            
        Returns:
            Dictionary with loading results
        """
        logger.info(f"Loading {data_type} data into databases")
        
        if data_type == 'financial':
            return self.load_financial_data(structured_data, vector_data)
        elif data_type == 'macroeconomic':
            return self.load_macroeconomic_data(structured_data, vector_data)
        elif data_type == 'contracts':
            return self.load_public_contracts(structured_data, vector_data)
        elif data_type == 'news':
            return self.load_news_data(structured_data, vector_data)
        else:
            logger.error(f"Unknown data type: {data_type}")
            return {
                'status': 'error',
                'message': f'Unknown data type: {data_type}',
                'overall_status': 'failed'
            }

    def _validate_structured_data(self, table_name: str, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Validate structured data before loading into Supabase.
        
        Args:
            table_name: Name of the target table
            data: Data to validate
            
        Returns:
            Validation result with status and issues
        """
        try:
            # Convert single record to list for consistent processing
            if isinstance(data, dict):
                data_list = [data]
            else:
                data_list = data
            
            if not data_list:
                return {
                    'is_valid': False,
                    'issues': ['No data provided']
                }
            
            issues = []
            
            # Basic validation for each record
            for i, record in enumerate(data_list):
                if not isinstance(record, dict):
                    issues.append(f"Record {i}: Not a dictionary")
                    continue
                
                # Check for required fields based on table
                required_fields = self._get_required_fields(table_name)
                for field in required_fields:
                    if field not in record or record[field] is None:
                        issues.append(f"Record {i}: Missing required field '{field}'")
            
            return {
                'is_valid': len(issues) == 0,
                'issues': issues
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'issues': [f'Validation error: {str(e)}']
            }

    def _validate_vector_data(self, vectors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Validate vector data before loading into Pinecone.
        
        Args:
            vectors: List of vectors to validate
            
        Returns:
            Validation result with status and issues
        """
        try:
            if not vectors:
                return {
                    'is_valid': False,
                    'issues': ['No vectors provided']
                }
            
            issues = []
            
            for i, vector in enumerate(vectors):
                # Check required fields
                if 'id' not in vector:
                    issues.append(f"Vector {i}: Missing 'id' field")
                
                if 'values' not in vector:
                    issues.append(f"Vector {i}: Missing 'values' field")
                elif not isinstance(vector['values'], list):
                    issues.append(f"Vector {i}: 'values' field is not a list")
                elif len(vector['values']) != 384:  # sentence-transformers/all-MiniLM-L6-v2 dimension
                    issues.append(f"Vector {i}: Incorrect embedding dimension {len(vector['values'])} (expected 384)")
                
                # Check metadata
                if 'metadata' not in vector:
                    issues.append(f"Vector {i}: Missing 'metadata' field")
                elif not isinstance(vector['metadata'], dict):
                    issues.append(f"Vector {i}: 'metadata' field is not a dictionary")
            
            return {
                'is_valid': len(issues) == 0,
                'issues': issues
            }
            
        except Exception as e:
            return {
                'is_valid': False,
                'issues': [f'Validation error: {str(e)}']
            }

    def _get_required_fields(self, table_name: str) -> List[str]:
        """
        Get required fields for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            List of required field names
        """
        # Define required fields for each table
        required_fields_map = {
            'resumen_informe_financiero': ['id_informe', 'fecha_corte_informe', 'activos_totales', 'pasivos_totales', 'patrimonio_neto'],
            'dato_macroeconomico': ['indicador_nombre', 'fecha_dato', 'valor_numerico', 'fuente_dato'],
            'licitacion_contrato': ['titulo', 'fecha_adjudicacion', 'estado_licitacion'],
            'noticia_relevante': ['titulo_noticia', 'fecha_publicacion', 'fuente_noticia', 'categoria'],
            'informe_general': ['titulo_informe', 'fecha_publicacion', 'id_emisor'],
            'movimiento_diario_bolsa': ['fecha_movimiento', 'id_emisor', 'precio_cierre'],
            'emisores': ['nombre_emisor', 'tipo_emisor']
        }
        
        return required_fields_map.get(table_name, [])

    def get_loading_statistics(self) -> Dict[str, Any]:
        """
        Get loading statistics and database status.
        
        Returns:
            Dictionary with loading statistics
        """
        try:
            # Test connections
            connection_status = self.test_connections()
            
            # Get Pinecone index statistics
            pinecone_stats = {}
            if connection_status['pinecone']['status'] == 'success':
                available_indexes = self.pinecone_connector.list_indexes()
                for index_name in available_indexes:
                    stats = self.pinecone_connector.get_index_stats(index_name)
                    if stats['status'] == 'success':
                        pinecone_stats[index_name] = stats['stats']
            
            return {
                'connections': connection_status,
                'pinecone_stats': pinecone_stats,
                'available_indexes': self.pinecone_connector.list_indexes() if connection_status['pinecone']['status'] == 'success' else []
            }
            
        except Exception as e:
            logger.error(f"Error getting loading statistics: {e}")
            return {
                'error': str(e)
            } 