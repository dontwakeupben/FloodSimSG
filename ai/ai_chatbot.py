from __future__ import annotations

"""AI Chatbot service for flood education Q&A using Azure OpenAI and LangChain.

This module provides:
- RAG (Retrieval Augmented Generation) using ChromaDB
- Conversation memory with LangChain
- Context-aware responses based on current rainfall
- Async handling for non-blocking game loop
"""
import os
import asyncio
import random
import threading
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# LangChain imports
try:
    from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
    try:
        from langchain_chroma import Chroma
    except ImportError:
        from langchain_community.vectorstores import Chroma
    from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
    from langchain_core.documents import Document
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough, RunnableLambda
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"Warning: LangChain packages not installed. AI chatbot will use fallback responses. Error: {e}")
    # Define dummy types for type hints when imports fail
    Document = Any


@dataclass
class ChatMessage:
    """A single chat message."""
    role: str  # "user" or "assistant"
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    is_new: bool = True  # Flag for notification system


class FloodChatbot:
    """AI chatbot for flood education with RAG and conversation memory.
    
    Uses Azure OpenAI with LangChain for:
    - Retrieval Augmented Generation from Singapore flood documents
    - Conversation memory to maintain context
    - Dynamic system prompts with rainfall context
    """
    
    # System prompt template with rainfall context variable
    SYSTEM_PROMPT_TEMPLATE = """You are a knowledgeable flood safety advisor for Singapore. 
Your role is to educate users about flood safety, Singapore's flood management systems, 
and historical flood incidents.

CURRENT GAME CONTEXT:
- Current Rainfall: {rainfall_mm}mm
- Current Location: {location}
- Rainfall Severity: {severity}

SEVERITY LEVELS:
- 0-30mm: Light rain - Normal conditions
- 30-80mm: Heavy rain - Monitor conditions
- 80mm+: Severe rain - Flood risk elevated

Use the current rainfall and location context to provide relevant, timely advice.
For example, if rainfall is high and user is in a flood-prone area, emphasize evacuation routes.

INSTRUCTIONS:
1. Answer questions about flood safety, Singapore PUB guidelines, and historical floods
2. Use retrieved documents to provide accurate, factual information
3. Keep responses concise (2-4 sentences) for game UI readability
4. If you don't know something, say so honestly
5. Always consider the current rainfall level in your advice

CONVERSATION HISTORY:
{chat_history}

RETRIEVED CONTEXT:
{context}

USER QUESTION: {question}

Provide a helpful, accurate response based on the retrieved documents and current rainfall context."""

    FALLBACK_RESPONSES = [
        "I'm currently unavailable. Please try asking about flood safety again in a moment.",
        "Connection issue detected. Basic flood safety: Move to higher ground when water rises.",
        "AI service temporarily offline. Remember: Never walk through flowing flood water.",
        "Unable to retrieve information. For flood emergencies, contact PUB at 1800-CALL-PUB.",
    ]
    
    def __init__(self, 
                 rainfall_context: float = 0.0,
                 location_context: str = "Singapore",
                 persist_directory: str = "./chroma_db"):
        """Initialize the flood chatbot.
        
        Args:
            rainfall_context: Current rainfall in mm (updated dynamically)
            location_context: Current location name (updated dynamically)
            persist_directory: Directory for ChromaDB persistence
        """
        self.rainfall = rainfall_context
        self.location = location_context
        self.persist_directory = persist_directory
        
        # Message history for display
        self.messages: List[ChatMessage] = []
        self.max_messages = 50
        
        # Conversation history for RAG context (simple list-based memory)
        self.conversation_history: List[str] = []
        self.max_history = 6  # Keep last 3 exchanges
        
        # Async handling
        self._processing = False
        self.response_callback: Optional[Callable[[str], None]] = None
        
        # Initialize components
        self._llm: Optional[Any] = None
        self._vectorstore: Optional[Any] = None
        self._rag_chain: Optional[Any] = None
        self._retriever: Optional[Any] = None
        
        if LANGCHAIN_AVAILABLE:
            self._initialize_components()
        else:
            print("FloodChatbot initialized in fallback mode (LangChain unavailable)")
        
    def _initialize_components(self) -> None:
        """Initialize LangChain components."""
        try:
            # Check for required environment variables
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            
            if not azure_endpoint or not api_key:
                print("Warning: Azure OpenAI credentials not found. Chatbot will use fallback responses.")
                return
            
            # Initialize Azure OpenAI LLM
            self._llm = AzureChatOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=api_key,
                api_version="2024-02-15-preview",
                deployment_name="gpt-5-nano"
            )
            
            # Initialize embeddings for RAG
            self._embeddings = AzureOpenAIEmbeddings(
                azure_endpoint=azure_endpoint,
                api_key=api_key,
                api_version="2024-02-15-preview",
                deployment="text-embedding-ada-002",
            )
            
            # Initialize or load ChromaDB vector store
            os.makedirs(self.persist_directory, exist_ok=True)
            
            try:
                self._vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self._embeddings
                )
                self._retriever = self._vectorstore.as_retriever(search_kwargs={"k": 3})
            except Exception as e:
                print(f"Note: Creating new vector store: {e}")
                self._vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self._embeddings
                )
                self._retriever = self._vectorstore.as_retriever(search_kwargs={"k": 3})
            
            # Build the RAG chain using modern LCEL pattern
            self._build_rag_chain()
            
            print("FloodChatbot initialized successfully with Azure OpenAI")
            
        except Exception as e:
            print(f"Warning: Failed to initialize AI components: {e}")
            import traceback
            traceback.print_exc()
            self._llm = None
            self._vectorstore = None
            self._rag_chain = None
            self._retriever = None
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Format documents for RAG context."""
        return "\n\n".join(d.page_content for d in docs)
    
    def _get_chat_history(self) -> str:
        """Get formatted conversation history."""
        return "\n".join(self.conversation_history) if self.conversation_history else "No previous conversation."
    
    def _build_rag_chain(self) -> None:
        """Build the RAG chain using modern LCEL pattern."""
        if self._llm is None or self._retriever is None:
            return
        
        # Create the prompt template
        prompt = PromptTemplate.from_template(self.SYSTEM_PROMPT_TEMPLATE)
        
        # Build the RAG chain
        self._rag_chain = (
            {
                "context": self._retriever | self._format_docs,
                "question": RunnablePassthrough(),
                "chat_history": lambda _: self._get_chat_history(),
                "rainfall_mm": lambda _: self.rainfall,
                "location": lambda _: self.location,
                "severity": lambda _: self._get_severity()
            }
            | prompt
            | self._llm
            | StrOutputParser()
        )
    
    def update_context(self, rainfall: float, location: str) -> None:
        """Update the rainfall and location context.
        
        Args:
            rainfall: Current rainfall in mm
            location: Current location name
        """
        self.rainfall = rainfall
        self.location = location
    
    def _get_severity(self) -> str:
        """Get severity level based on current rainfall."""
        if self.rainfall < 30:
            return "Light rain - Normal conditions"
        elif self.rainfall < 80:
            return "Heavy rain - Monitor conditions"
        else:
            return "Severe rain - Flood risk elevated"
    
    async def _generate_response_async(self, question: str) -> str:
        """Generate AI response asynchronously.
        
        Args:
            question: User's question
            
        Returns:
            AI-generated response
        """
        if self._rag_chain is None:
            return random.choice(self.FALLBACK_RESPONSES)
        
        try:
            # Run the chain in executor to avoid blocking
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self._rag_chain.invoke(question)
            )
            
            return response
            
        except Exception as e:
            print(f"Error generating response: {e}")
            import traceback
            traceback.print_exc()
            return random.choice(self.FALLBACK_RESPONSES)
    
    def ask(self, question: str, callback: Optional[Callable[[str], None]] = None) -> None:
        """Ask the chatbot a question (non-blocking).
        
        Args:
            question: User's question
            callback: Function to call with the response when ready
        """
        # Add user message to history
        self.messages.append(ChatMessage(
            role="user",
            content=question,
            timestamp=datetime.now()
        ))
        
        # Update conversation history for RAG context
        self.conversation_history.append(f"User: {question}")
        
        # Store callback
        self.response_callback = callback
        
        # Start thread for non-blocking execution
        self._processing = True
        thread = threading.Thread(
            target=self._generate_response_threaded,
            args=(question, callback),
            daemon=True
        )
        thread.start()
    
    def _generate_response_threaded(self, question: str, callback: Optional[Callable[[str], None]]) -> None:
        """Generate response in a background thread.
        
        Args:
            question: User's question
            callback: Function to call with the response
        """
        try:
            if self._rag_chain is None:
                response = random.choice(self.FALLBACK_RESPONSES)
            else:
                # Direct synchronous call to RAG chain
                response = self._rag_chain.invoke(question)
        except Exception as e:
            print(f"Error generating response: {e}")
            import traceback
            traceback.print_exc()
            response = random.choice(self.FALLBACK_RESPONSES)
        
        # Add to message history
        self._add_assistant_message(response)
        
        # Call callback if provided
        if callback:
            callback(response)
        
        self._processing = False
    
    def _add_assistant_message(self, content: str) -> None:
        """Add assistant message to history.
        
        Args:
            content: Message content
        """
        self.messages.append(ChatMessage(
            role="assistant",
            content=content,
            timestamp=datetime.now(),
            is_new=True
        ))
        
        # Update conversation history for RAG context
        self.conversation_history.append(f"Assistant: {content}")
        
        # Trim history if needed
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]
        
        # Trim message history if needed
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def mark_messages_read(self) -> None:
        """Mark all messages as read (clear notification flags)."""
        for msg in self.messages:
            msg.is_new = False
    
    def has_new_messages(self) -> bool:
        """Check if there are unread messages.
        
        Returns:
            True if new messages exist
        """
        return any(msg.is_new for msg in self.messages)
    
    def is_processing(self) -> bool:
        """Check if a response is being generated.
        
        Returns:
            True if processing, False otherwise
        """
        return self._processing
    
    def get_messages(self, limit: int = 20) -> List[ChatMessage]:
        """Get recent messages.
        
        Args:
            limit: Maximum number of messages to return
            
        Returns:
            List of chat messages
        """
        return self.messages[-limit:]
    
    def clear_history(self) -> None:
        """Clear conversation history."""
        self.messages.clear()
        self.conversation_history.clear()
    
    def add_documents(self, documents: List[Any]) -> None:
        """Add documents to the RAG vector store.
        
        Args:
            documents: List of LangChain Document objects
        """
        if self._vectorstore is not None:
            try:
                self._vectorstore.add_documents(documents)
                print(f"Added {len(documents)} documents to vector store")
            except Exception as e:
                print(f"Error adding documents: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("Warning: Vector store not initialized, cannot add documents")
    
    def is_available(self) -> bool:
        """Check if AI service is available.
        
        Returns:
            True if initialized and ready
        """
        return self._rag_chain is not None
    
    def get_retriever(self):
        """Get the retriever for document search.
        
        Returns:
            The retriever object or None
        """
        return self._retriever
