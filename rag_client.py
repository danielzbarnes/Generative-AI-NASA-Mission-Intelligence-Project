# needed for issues with Chroma
import os
import sys
import pysqlite3
sys.modules["sqlite3"] = pysqlite3
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from dotenv import load_dotenv

import chromadb
from chromadb.config import Settings
from typing import Dict, List, Optional
from pathlib import Path

load_dotenv()

def discover_chroma_backends() -> Dict[str, Dict[str, str]]:
    """Discover available ChromaDB backends in the project directory"""
    backends = {}
    current_dir = Path(".")
    
        # Look for ChromaDB directories
    # TODO: Create list of directories that match specific criteria (directory type and name pattern)
    client_dirs = [d for d in current_dir.iterdir() if d.is_dir() and "chroma" in d.name.lower()]
    
    # TODO: Loop through each discovered directory
    for chroma_dir in client_dirs:
        
        # TODO: Wrap connection attempt in try-except block for error handling
        try:
                    
            # TODO: Initialize database client with directory path and configuration settings
            client = chromadb.PersistentClient(path=str(chroma_dir), settings=Settings(anonymized_telemetry=False))
            
            # TODO: Retrieve list of available collections from the database
            collections = client.list_collections()
            
            # TODO: Loop through each collection found
            for collection in collections:
                
                # TODO: Create unique identifier key combining directory and collection names
                backend_key = f"{chroma_dir.name}_{collection.name}"
                # TODO: Build information dictionary containing:
                    # TODO: Store directory path as string
                    # TODO: Store collection name
                    # TODO: Create user-friendly display name
                    # TODO: Get document count with fallback for unsupported operations
                # TODO: Add collection information to backends dictionary
                backends[backend_key] = {
                    "directory": str(chroma_dir),
                    "collection_name": collection.name,
                    "display_name": f"{chroma_dir.name} - {collection.name} Collection",
                    "document_count": collection.count() if hasattr(collection, "count") else "N/A"
                }    
                
        
        # TODO: Handle connection or access errors gracefully
            # TODO: Create fallback entry for inaccessible directories
            # TODO: Include error information in display name with truncation
            # TODO: Set appropriate fallback values for missing information
        except Exception as e:
            error_message = str(e)
            truncated_error = (error_message[:50] + "...") if len(error_message) > 50 else error_message
            backends[chroma_dir.name] = {
                "directory": str(chroma_dir),
                "collection": None,
                "display_name": f"{chroma_dir.name} (Error: {truncated_error})",
                "document_count": None
            }

    # TODO: Return complete backends dictionary with all discovered collections
    return backends

def initialize_rag_system(chroma_dir: str, collection_name: str):
    """Initialize the RAG system with specified backend (cached for performance)"""

    # TODO: Create a chomadb persistentclient
    # TODO: Return the collection with the collection_name
    client = chromadb.PersistentClient(path=chroma_dir, settings=Settings(anonymized_telemetry=False))
    
    try:
    
        open_embedding_fuction = OpenAIEmbeddingFunction(api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small")
        
        collection = client.get_collection(name=collection_name, embedding_function=open_embedding_fuction)
        return collection, True, None
    
    except Exception as e:
        print(f"Error initializing RAG system: {e}")
        return None, False, str(e)

def retrieve_documents(collection, query: str, n_results: int = 3, 
                      mission_filter: Optional[str] = None) -> Optional[Dict]:
    """Retrieve relevant documents from ChromaDB with optional filtering"""

    # TODO: Initialize filter variable to None (represents no filtering)
    filter_dict = None

    # TODO: Check if filter parameter exists and is not set to "all" or equivalent
    # TODO: If filter conditions are met, create filter dictionary with appropriate field-value pairs
    if mission_filter and mission_filter != "all":
        filter_dict = {"mission": mission_filter}

    # TODO: Execute database query with the following parameters:
        # TODO: Pass search query in the required format
        # TODO: Set maximum number of results to return
        # TODO: Apply conditional filter (None for no filtering, dictionary for specific filtering)
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=filter_dict
    )

    # TODO: Return query results to caller
    return results

def format_context(documents: List[str], metadatas: List[Dict]) -> str:
    """Format retrieved documents into context"""
    if not documents:
        return ""
    
    # TODO: Initialize list with header text for context section
    header = "Relevant Mission Information:\n"
    context_parts = [header]

    combined = []
    for doc, meta in zip(documents, metadatas):
        score = meta.get("score", 0) or meta.get("distance", 0) or 0
        combined.append((doc, meta, score))

    combined.sort(key=lambda x: x[2], reverse=True)
    
    seen = set()
    unique_combined = []
    for doc, meta, score in combined:
        identifier = (meta.get("mission", "Unknown Mission"),  meta.get("category", meta.get("category", "Unknown Category")))
        if identifier not in seen:
            seen.add(identifier)
            unique_combined.append((doc, meta, score))

    # TODO: Loop through paired documents and their metadata using enumeration
    for idx, (doc, meta, score) in enumerate(zip(documents, metadatas, [m.get("score", 0) or m.get("distance", 0) for m in metadatas])):
        
        # TODO: Extract mission information from metadata with fallback value
        mission_info = meta.get("mission", "Unknown Mission")
        
        # TODO: Clean up mission name formatting (replace underscores, capitalize)
        mission_info = mission_info.replace("_", " ").title()
        
        # TODO: Extract source information from metadata with fallback value  
        source_info = meta.get("source", "Unknown Source")
        
        # TODO: Extract category information from metadata with fallback value
        category_info = meta.get("document_category", meta.get("category", "Unknown Category"))
        
        # TODO: Clean up category name formatting (replace underscores, capitalize)
        category_info = category_info.replace("_", " ").title()
        
        # TODO: Create formatted source header with index number and extracted information
        # TODO: Add source header to context parts list
        source_info = meta.get("source", "Unknown Source")
        
        source_header =(
            f"Source {idx + 1}: {mission_info} - {category_info} "
            f"(Source: {source_info}, Score: {score})\n"
        )

        context_parts.append(source_header)
        
        # TODO: Check document length and truncate if necessary
        # TODO: Add truncated or full document content to context parts list
        if len(doc) > 500:
            context_parts.append(doc[:500] + "...\n")
        else:
            context_parts.append(doc + "\n")

    # TODO: Join all context parts with newlines and return formatted string
    return "\n".join(context_parts)