"""
Database Connectors Module

This module provides connectors for Supabase and Pinecone databases.
It handles connection management, authentication, and basic database operations.
"""

import os
import logging
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class SupabaseConnector:
    """
    Connector for Supabase PostgreSQL database.
    
    This class handles:
    - Connection to Supabase
    - CRUD operations for structured data
    - Transaction management
    - Error handling and retry logic
    """
    
    def __init__(self, supabase_url: Optional[str] = None, supabase_key: Optional[str] = None):
        """
        Initialize Supabase connector.
        
        Args:
            supabase_url: Supabase project URL (optional, will use env var if not provided)
            supabase_key: Supabase API key (optional, will use env var if not provided)
        """
        self.supabase_url = supabase_url or os.getenv('SUPABASE_URL')
        self.supabase_key = supabase_key or os.getenv('SUPABASE_KEY')
        self.client = None
        
        if not self.supabase_url or not self.supabase_key:
            logger.warning("Supabase credentials not found in environment variables")
        else:
            self._initialize_client()
        
        logger.info(f"SupabaseConnector initialized with URL: {self.supabase_url}")

    def _initialize_client(self):
        """Initialize the Supabase client."""
        try:
            from supabase import create_client, Client
            
            self.client = create_client(self.supabase_url, self.supabase_key)
            logger.info("Supabase client initialized successfully")
            
        except ImportError:
            logger.error("supabase-py library not installed. Please install with: pip install supabase")
            self.client = None
        except Exception as e:
            logger.error(f"Error initializing Supabase client: {e}")
            self.client = None

    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Supabase.
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Supabase client not initialized'
                }
            
            # Test connection by querying a simple table
            # We'll try to get the schema information
            response = self.client.table('informe_general').select('*').limit(1).execute()
            
            return {
                'status': 'success',
                'message': 'Connection successful',
                'url': self.supabase_url,
                'has_client': bool(self.client)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}',
                'url': self.supabase_url
            }

    def insert_data(self, table_name: str, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
        """
        Insert data into a Supabase table.
        
        Args:
            table_name: Name of the table to insert into
            data: Data to insert (single record or list of records)
            
        Returns:
            Dictionary with insertion status and details
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Supabase client not initialized'
                }
            
            # Insert data
            response = self.client.table(table_name).insert(data).execute()
            
            # Check for errors in response
            if hasattr(response, 'error') and response.error:
                return {
                    'status': 'error',
                    'message': f'Insert failed: {response.error}',
                    'table': table_name
                }
            
            # Count inserted records
            inserted_count = len(response.data) if response.data else 0
            
            logger.info(f"Successfully inserted {inserted_count} records into {table_name}")
            
            return {
                'status': 'success',
                'message': f'Successfully inserted {inserted_count} records',
                'table': table_name,
                'inserted_count': inserted_count,
                'data': response.data
            }
            
        except Exception as e:
            logger.error(f"Error inserting data into {table_name}: {e}")
            return {
                'status': 'error',
                'message': f'Insert failed: {str(e)}',
                'table': table_name
            }

    def update_data(self, table_name: str, data: Dict[str, Any], conditions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update data in a Supabase table.
        
        Args:
            table_name: Name of the table to update
            data: Data to update
            conditions: Conditions for the update (WHERE clause)
            
        Returns:
            Dictionary with update status and details
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Supabase client not initialized'
                }
            
            # Build update query
            query = self.client.table(table_name).update(data)
            
            # Add conditions
            for key, value in conditions.items():
                query = query.eq(key, value)
            
            # Execute update
            response = query.execute()
            
            # Check for errors
            if hasattr(response, 'error') and response.error:
                return {
                    'status': 'error',
                    'message': f'Update failed: {response.error}',
                    'table': table_name
                }
            
            # Count updated records
            updated_count = len(response.data) if response.data else 0
            
            logger.info(f"Successfully updated {updated_count} records in {table_name}")
            
            return {
                'status': 'success',
                'message': f'Successfully updated {updated_count} records',
                'table': table_name,
                'updated_count': updated_count,
                'data': response.data
            }
            
        except Exception as e:
            logger.error(f"Error updating data in {table_name}: {e}")
            return {
                'status': 'error',
                'message': f'Update failed: {str(e)}',
                'table': table_name
            }

    def query_data(self, table_name: str, columns: Optional[List[str]] = None, 
                   conditions: Optional[Dict[str, Any]] = None, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Query data from a Supabase table.
        
        Args:
            table_name: Name of the table to query
            columns: Columns to select (None for all columns)
            conditions: Conditions for the query (WHERE clause)
            limit: Maximum number of records to return
            
        Returns:
            Dictionary with query results and details
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Supabase client not initialized'
                }
            
            # Build query
            if columns:
                query = self.client.table(table_name).select(','.join(columns))
            else:
                query = self.client.table(table_name).select('*')
            
            # Add conditions
            if conditions:
                for key, value in conditions.items():
                    query = query.eq(key, value)
            
            # Add limit
            if limit:
                query = query.limit(limit)
            
            # Execute query
            response = query.execute()
            
            # Check for errors
            if hasattr(response, 'error') and response.error:
                return {
                    'status': 'error',
                    'message': f'Query failed: {response.error}',
                    'table': table_name
                }
            
            # Get results
            results = response.data if response.data else []
            
            logger.info(f"Successfully queried {len(results)} records from {table_name}")
            
            return {
                'status': 'success',
                'message': f'Successfully queried {len(results)} records',
                'table': table_name,
                'record_count': len(results),
                'data': results
            }
            
        except Exception as e:
            logger.error(f"Error querying data from {table_name}: {e}")
            return {
                'status': 'error',
                'message': f'Query failed: {str(e)}',
                'table': table_name
            }

    def delete_data(self, table_name: str, conditions: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete data from a Supabase table.
        
        Args:
            table_name: Name of the table to delete from
            conditions: Conditions for the deletion (WHERE clause)
            
        Returns:
            Dictionary with deletion status and details
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Supabase client not initialized'
                }
            
            # Build delete query
            query = self.client.table(table_name).delete()
            
            # Add conditions
            for key, value in conditions.items():
                query = query.eq(key, value)
            
            # Execute delete
            response = query.execute()
            
            # Check for errors
            if hasattr(response, 'error') and response.error:
                return {
                    'status': 'error',
                    'message': f'Delete failed: {response.error}',
                    'table': table_name
                }
            
            # Count deleted records
            deleted_count = len(response.data) if response.data else 0
            
            logger.info(f"Successfully deleted {deleted_count} records from {table_name}")
            
            return {
                'status': 'success',
                'message': f'Successfully deleted {deleted_count} records',
                'table': table_name,
                'deleted_count': deleted_count
            }
            
        except Exception as e:
            logger.error(f"Error deleting data from {table_name}: {e}")
            return {
                'status': 'error',
                'message': f'Delete failed: {str(e)}',
                'table': table_name
            }

    def get_table_schema(self, table_name: str) -> Dict[str, Any]:
        """
        Get schema information for a table.
        
        Args:
            table_name: Name of the table
            
        Returns:
            Dictionary with schema information
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Supabase client not initialized'
                }
            
            # Query table schema (this is a simplified approach)
            # In a real implementation, you might want to query the information_schema
            response = self.client.table(table_name).select('*').limit(0).execute()
            
            return {
                'status': 'success',
                'message': 'Schema information retrieved',
                'table': table_name,
                'has_table': True
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Schema retrieval failed: {str(e)}',
                'table': table_name
            }

class PineconeConnector:
    """
    Connector for Pinecone vector database.
    
    This class handles:
    - Connection to Pinecone
    - Vector operations (upsert, query, delete)
    - Index management
    - Error handling and retry logic
    """
    
    def __init__(self, api_key: Optional[str] = None, environment: Optional[str] = None):
        """
        Initialize Pinecone connector.
        
        Args:
            api_key: Pinecone API key (optional, will use env var if not provided)
            environment: Pinecone environment (optional, will use env var if not provided)
        """
        self.api_key = api_key or os.getenv('PINECONE_API_KEY')
        self.environment = environment or os.getenv('PINECONE_ENVIRONMENT', 'gcp-starter')
        self.client = None
        
        if not self.api_key:
            logger.warning("PINECONE_API_KEY not found in environment variables")
        else:
            self._initialize_client()
        
        logger.info(f"PineconeConnector initialized with environment: {self.environment}")

    def _initialize_client(self):
        """Initialize the Pinecone client."""
        try:
            import pinecone
            
            # Initialize Pinecone
            pinecone.init(api_key=self.api_key, environment=self.environment)
            self.client = pinecone
            logger.info("Pinecone client initialized successfully")
            
        except ImportError:
            logger.error("pinecone-client library not installed. Please install with: pip install pinecone-client")
            self.client = None
        except Exception as e:
            logger.error(f"Error initializing Pinecone client: {e}")
            self.client = None

    def test_connection(self) -> Dict[str, Any]:
        """
        Test the connection to Pinecone.
        
        Returns:
            Dictionary with connection status and details
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Pinecone client not initialized'
                }
            
            # Test connection by listing indexes
            indexes = self.client.list_indexes()
            
            return {
                'status': 'success',
                'message': 'Connection successful',
                'environment': self.environment,
                'available_indexes': indexes,
                'index_count': len(indexes)
            }
            
        except Exception as e:
            return {
                'status': 'error',
                'message': f'Connection test failed: {str(e)}',
                'environment': self.environment
            }

    def get_index(self, index_name: str):
        """
        Get a Pinecone index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Pinecone index object or None if not found
        """
        try:
            if not self.client:
                logger.error("Pinecone client not initialized")
                return None
            
            # Check if index exists
            if index_name in self.client.list_indexes():
                return self.client.Index(index_name)
            else:
                logger.warning(f"Index '{index_name}' not found")
                return None
                
        except Exception as e:
            logger.error(f"Error getting index '{index_name}': {e}")
            return None

    def upsert_vectors(self, index_name: str, vectors: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Upsert vectors into a Pinecone index.
        
        Args:
            index_name: Name of the index
            vectors: List of vectors to upsert
            
        Returns:
            Dictionary with upsert status and details
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Pinecone client not initialized'
                }
            
            # Get index
            index = self.get_index(index_name)
            if not index:
                return {
                    'status': 'error',
                    'message': f'Index "{index_name}" not found',
                    'index': index_name
                }
            
            # Prepare vectors for upsert
            upsert_data = []
            for vector in vectors:
                if 'id' in vector and 'values' in vector:
                    upsert_data.append({
                        'id': vector['id'],
                        'values': vector['values'],
                        'metadata': vector.get('metadata', {})
                    })
            
            if not upsert_data:
                return {
                    'status': 'error',
                    'message': 'No valid vectors to upsert',
                    'index': index_name
                }
            
            # Upsert vectors
            index.upsert(vectors=upsert_data)
            
            logger.info(f"Successfully upserted {len(upsert_data)} vectors to {index_name}")
            
            return {
                'status': 'success',
                'message': f'Successfully upserted {len(upsert_data)} vectors',
                'index': index_name,
                'upserted_count': len(upsert_data)
            }
            
        except Exception as e:
            logger.error(f"Error upserting vectors to {index_name}: {e}")
            return {
                'status': 'error',
                'message': f'Upsert failed: {str(e)}',
                'index': index_name
            }

    def query_vectors(self, index_name: str, query_vector: List[float], 
                     top_k: int = 10, filter_dict: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Query vectors from a Pinecone index.
        
        Args:
            index_name: Name of the index
            query_vector: Query vector
            top_k: Number of results to return
            filter_dict: Filter conditions
            
        Returns:
            Dictionary with query results and details
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Pinecone client not initialized'
                }
            
            # Get index
            index = self.get_index(index_name)
            if not index:
                return {
                    'status': 'error',
                    'message': f'Index "{index_name}" not found',
                    'index': index_name
                }
            
            # Query vectors
            results = index.query(
                vector=query_vector,
                top_k=top_k,
                filter=filter_dict,
                include_metadata=True
            )
            
            # Extract matches
            matches = results.matches if hasattr(results, 'matches') else []
            
            logger.info(f"Successfully queried {len(matches)} vectors from {index_name}")
            
            return {
                'status': 'success',
                'message': f'Successfully queried {len(matches)} vectors',
                'index': index_name,
                'match_count': len(matches),
                'matches': matches
            }
            
        except Exception as e:
            logger.error(f"Error querying vectors from {index_name}: {e}")
            return {
                'status': 'error',
                'message': f'Query failed: {str(e)}',
                'index': index_name
            }

    def delete_vectors(self, index_name: str, vector_ids: List[str]) -> Dict[str, Any]:
        """
        Delete vectors from a Pinecone index.
        
        Args:
            index_name: Name of the index
            vector_ids: List of vector IDs to delete
            
        Returns:
            Dictionary with deletion status and details
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Pinecone client not initialized'
                }
            
            # Get index
            index = self.get_index(index_name)
            if not index:
                return {
                    'status': 'error',
                    'message': f'Index "{index_name}" not found',
                    'index': index_name
                }
            
            # Delete vectors
            index.delete(ids=vector_ids)
            
            logger.info(f"Successfully deleted {len(vector_ids)} vectors from {index_name}")
            
            return {
                'status': 'success',
                'message': f'Successfully deleted {len(vector_ids)} vectors',
                'index': index_name,
                'deleted_count': len(vector_ids)
            }
            
        except Exception as e:
            logger.error(f"Error deleting vectors from {index_name}: {e}")
            return {
                'status': 'error',
                'message': f'Delete failed: {str(e)}',
                'index': index_name
            }

    def get_index_stats(self, index_name: str) -> Dict[str, Any]:
        """
        Get statistics for a Pinecone index.
        
        Args:
            index_name: Name of the index
            
        Returns:
            Dictionary with index statistics
        """
        try:
            if not self.client:
                return {
                    'status': 'error',
                    'message': 'Pinecone client not initialized'
                }
            
            # Get index
            index = self.get_index(index_name)
            if not index:
                return {
                    'status': 'error',
                    'message': f'Index "{index_name}" not found',
                    'index': index_name
                }
            
            # Get index stats
            stats = index.describe_index_stats()
            
            return {
                'status': 'success',
                'message': 'Index statistics retrieved',
                'index': index_name,
                'stats': stats
            }
            
        except Exception as e:
            logger.error(f"Error getting stats for {index_name}: {e}")
            return {
                'status': 'error',
                'message': f'Stats retrieval failed: {str(e)}',
                'index': index_name
            }

    def list_indexes(self) -> List[str]:
        """
        List all available Pinecone indexes.
        
        Returns:
            List of index names
        """
        try:
            if not self.client:
                logger.error("Pinecone client not initialized")
                return []
            
            return self.client.list_indexes()
            
        except Exception as e:
            logger.error(f"Error listing indexes: {e}")
            return [] 