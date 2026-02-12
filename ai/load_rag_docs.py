"""Script to load Singapore flood documents into ChromaDB vector store.

Usage:
    python load_rag_docs.py

This will load all .txt and .md files from the rag_documents/ directory
into the ChromaDB vector store for use by the AI chatbot.
"""
import os
import sys
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()


# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent


def load_documents_from_directory(directory: str = None) -> list:
    """Load all documents from the specified directory.
    
    Args:
        directory: Path to directory containing documents (default: script_dir/rag_documents)
        
    Returns:
        List of loaded documents
    """
    if directory is None:
        docs_path = SCRIPT_DIR / "rag_documents"
    else:
        docs_path = Path(directory)
    
    if not docs_path.exists():
        print(f"Creating directory: {docs_path}")
        docs_path.mkdir(parents=True, exist_ok=True)
        return []
    
    # Import here to avoid issues if langchain is not installed
    try:
        from langchain_community.document_loaders import TextLoader
    except ImportError:
        print("Error: langchain_community not installed.")
        print("Run: pip install langchain-community langchain-text-splitters")
        return []
    
    documents = []
    
    # Load .txt files
    for txt_file in docs_path.glob("*.txt"):
        try:
            loader = TextLoader(str(txt_file), encoding='utf-8')
            docs = loader.load()
            documents.extend(docs)
            print(f"Loaded: {txt_file.name}")
        except Exception as e:
            print(f"Error loading {txt_file}: {e}")
    
    # Load .md files
    for md_file in docs_path.glob("*.md"):
        try:
            loader = TextLoader(str(md_file), encoding='utf-8')
            docs = loader.load()
            documents.extend(docs)
            print(f"Loaded: {md_file.name}")
        except Exception as e:
            print(f"Error loading {md_file}: {e}")
    
    return documents


def split_documents(documents: list, chunk_size: int = 500, chunk_overlap: int = 50) -> list:
    """Split documents into chunks for better retrieval.
    
    Args:
        documents: List of documents to split
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks
        
    Returns:
        List of split document chunks
    """
    try:
        from langchain_text_splitters import RecursiveCharacterTextSplitter
    except ImportError:
        print("Error: langchain_text_splitters not installed.")
        return documents  # Return unsplit if splitter not available
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", "!", "?", " "]
    )
    
    return text_splitter.split_documents(documents)


def main():
    """Main entry point."""
    print("=" * 60)
    print("Singapore Flood RAG Document Loader")
    print("=" * 60)
    
    # Import chatbot here to check availability
    from ai_chatbot import FloodChatbot
    
    # Load raw documents
    print("\nLoading documents from rag_documents/...")
    raw_documents = load_documents_from_directory()
    
    if not raw_documents:
        print("\nNo documents found. Please add .txt or .md files to rag_documents/")
        print("\nExample documents you might add:")
        print("  - singapore_flood_history.txt")
        print("  - pub_guidelines.txt")
        print("  - emergency_procedures.md")
        print("  - tanglin_2010_flood.txt")
        return
    
    print(f"\nLoaded {len(raw_documents)} raw documents")
    
    # Split documents into chunks for better retrieval
    print("\nSplitting documents into chunks...")
    split_documents_list = split_documents(raw_documents)
    print(f"Created {len(split_documents_list)} document chunks")
    
    # Initialize chatbot and add documents
    print("\nInitializing ChromaDB vector store...")
    chatbot = FloodChatbot()
    
    if not chatbot.is_available():
        print("\nError: AI components not available. Check your Azure OpenAI credentials.")
        return
    
    print("\nAdding documents to vector store...")
    chatbot.add_documents(split_documents_list)
    
    print("\n" + "=" * 60)
    print("Documents loaded successfully!")
    print("=" * 60)
    print("\nYou can now use the AI chatbot in the game.")
    print("The chatbot will use these documents to answer questions.")


if __name__ == "__main__":
    main()
