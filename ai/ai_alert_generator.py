from __future__ import annotations

"""AI Alert Generator for flood safety alerts using Azure OpenAI and LangChain.

This module provides:
- AI-generated contextual alerts when rainfall thresholds are breached
- RAG (Retrieval Augmented Generation) using ChromaDB for location-specific alerts
- Async generation for non-blocking operation
- TTS-optimized output (concise, speech-friendly)
"""
import os
import asyncio
import random
import threading
import time
from typing import List, Dict, Optional, Callable, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum

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
    from langchain_core.prompts import PromptTemplate
    from langchain_core.documents import Document
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    LANGCHAIN_AVAILABLE = False
    print(f"Warning: LangChain packages not installed. AI alert generator will use fallback responses. Error: {e}")
    Document = Any


class AlertSeverity(Enum):
    """Severity levels for alerts."""
    LOW = "low"           # Informational
    MEDIUM = "medium"     # Caution
    HIGH = "high"         # Warning
    CRITICAL = "critical" # Emergency


class AlertType(Enum):
    """Types of alerts that can be generated."""
    THRESHOLD_CROSSING = "threshold_crossing"  # Crossing 30mm/80mm boundaries
    ESCALATION = "escalation"                   # Rising within a bucket (50mm)
    SEVERE_WEATHER = "severe_weather"          # Extreme conditions (80mm+)
    LOCATION_CHANGE = "location_change"         # New zone entered


@dataclass
class GeneratedAlert:
    """A generated alert with both display and audio text."""
    message: str  # Full message for display
    audio_text: str  # Shortened version for TTS
    severity: AlertSeverity
    alert_type: AlertType
    location: str
    rainfall: float
    generated_at: datetime = field(default_factory=datetime.now)
    source_documents: List[str] = field(default_factory=list)


class AIAlertGenerator:
    """AI-powered alert generator for flood safety alerts.
    
    Uses Azure OpenAI with LangChain for:
    - Retrieval Augmented Generation from Singapore flood documents
    - Context-aware alerts based on rainfall and location
    - Concise, TTS-optimized output
    
    Example:
        generator = AIAlertGenerator()
        
        # Generate an alert
        alert = generator.generate_alert(
            alert_type=AlertType.THRESHOLD_CROSSING,
            location="Tanglin Carpark",
            rainfall=45.0,
            from_bucket="normal",
            to_bucket="warning"
        )
        
        # Use alert text
        print(alert.message)  # Display text
        narrator.speak(alert.audio_text)  # TTS text
    """
    
    # System prompt template for alert generation
    SYSTEM_PROMPT_TEMPLATE = """You are an emergency alert system for Singapore flood safety.
Your role is to generate urgent, actionable alerts when rainfall thresholds are breached.

CURRENT SITUATION:
- Location: {location}
- Current Rainfall: {rainfall}mm
- Alert Type: {alert_type}
- Severity Level: {severity}
- Previous State: {from_state}
- Current State: {to_state}

ALERT TYPE DEFINITIONS:
- threshold_crossing: User just crossed from one rainfall bucket to another (30mm or 80mm boundary)
- escalation: Rainfall is rising within the warning bucket (crossed 50mm internally)
- severe_weather: Extreme conditions in danger bucket (80mm+)
- location_change: User entered a new zone

SEVERITY LEVELS:
- low: Informational, no immediate danger
- medium: Caution, monitor conditions
- high: Warning, take action
- critical: Emergency, immediate danger

HISTORICAL CONTEXT FOR {location}:
{context}

INSTRUCTIONS:
1. Generate a BRIEF alert (MAXIMUM 140 characters for display, 100 for audio)
2. Use the retrieved historical documents to make alerts location-specific
3. Reference past flood incidents if applicable (e.g., "Tanglin flooded in 2010/2011")
4. Be urgent but clear - this is for emergency situations
5. Include ONE specific actionable recommendation
6. Use Singapore PUB guidelines where relevant
7. For critical alerts: Use commanding tone, clear evacuation instructions

OUTPUT FORMAT:
Provide your response in this exact format:
DISPLAY: [alert text for on-screen display, max 140 chars]
AUDIO: [shorter version for text-to-speech, max 100 chars, natural speech]

The AUDIO version should be shorter and optimized for speech (no abbreviations, natural phrasing)."""
    
    # Fallback messages when AI is unavailable
    FALLBACK_ALERTS = {
        AlertType.THRESHOLD_CROSSING: {
            "normal_to_warning": [
                "Heavy rain alert! Monitor conditions closely.",
                "Rain intensifying. Stay alert for flooding.",
                "Warning: Rainfall entering heavy range.",
            ],
            "warning_to_danger": [
                "EMERGENCY: Severe rain! Seek higher ground now!",
                "DANGER: Critical rainfall! Evacuate if in low areas!",
                "URGENT: Extreme rain! Move to safety immediately!",
            ],
            "danger_to_warning": [
                "Rain decreasing but still heavy. Remain cautious.",
                "Conditions improving but stay alert.",
            ],
            "warning_to_normal": [
                "Rain easing to normal levels.",
                "Conditions returning to normal. Stay dry!",
            ],
        },
        AlertType.ESCALATION: {
            "warning": [
                "Caution: Rain increasing. Be ready to move.",
                "Rain intensifying in warning zone. Watch for floods.",
            ],
        },
        AlertType.SEVERE_WEATHER: {
            "danger": [
                "CRITICAL: Severe weather! Evacuate now!",
                "EMERGENCY: Dangerous flooding conditions! Move to high ground!",
            ],
        },
        AlertType.LOCATION_CHANGE: {
            "ION Orchard": {
                "normal": "Welcome to ION Orchard. You are at 18 meters elevation, safe from flooding.",
                "warning": "ION Orchard: Heavy rain outside, but you are safe here on high ground.",
                "danger": "ION Orchard: Severe rain. You are safe, but avoid going outside.",
            },
            "Orchard Road": {
                "normal": "Welcome to Orchard Road. Watch for water pooling during rain.",
                "warning": "Orchard Road: Heavy rain may cause flash floods. Stay alert.",
                "danger": "URGENT: Severe rain on Orchard Road! Seek shelter immediately!",
            },
            "Tanglin Carpark": {
                "normal": "Welcome to Tanglin Carpark. Warning: This basement flooded in 2010 and 2011.",
                "warning": "Tanglin Carpark: Heavy rain! Be ready to evacuate. Watch water levels.",
                "danger": "EMERGENCY at Tanglin Carpark! Severe rain! Evacuate NOW!",
            },
        },
    }
    
    def __init__(
        self,
        persist_directory: str = "./chroma_db",
        use_ai: bool = True
    ):
        """Initialize the AI alert generator.
        
        Args:
            persist_directory: Directory for ChromaDB persistence
            use_ai: Whether to use AI generation or fallback messages
        """
        self.persist_directory = persist_directory
        self.use_ai = use_ai and LANGCHAIN_AVAILABLE
        
        # Async handling
        self._processing = False
        self._alert_callback: Optional[Callable[[GeneratedAlert], None]] = None
        
        # Initialize components
        self._llm: Optional[Any] = None
        self._vectorstore: Optional[Any] = None
        self._retriever: Optional[Any] = None
        self._alert_chain: Optional[Any] = None
        
        if self.use_ai:
            self._initialize_components()
        else:
            print("AIAlertGenerator initialized in fallback mode")
    
    def _initialize_components(self) -> None:
        """Initialize LangChain components."""
        try:
            # Check for required environment variables
            azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
            api_key = os.getenv("AZURE_OPENAI_API_KEY")
            
            if not azure_endpoint or not api_key:
                print("Warning: Azure OpenAI credentials not found. Alert generator will use fallback responses.")
                self.use_ai = False
                return
            
            # Initialize Azure OpenAI LLM
            self._llm = AzureChatOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=api_key,
                api_version="2024-02-15-preview",
                deployment_name="gpt-5-nano",
                max_tokens=100,   # Keep alerts concise
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
                self._retriever = self._vectorstore.as_retriever(search_kwargs={"k": 2})
            except Exception as e:
                print(f"Note: Creating new vector store: {e}")
                self._vectorstore = Chroma(
                    persist_directory=self.persist_directory,
                    embedding_function=self._embeddings
                )
                self._retriever = self._vectorstore.as_retriever(search_kwargs={"k": 2})
            
            # Build the alert generation chain
            self._build_alert_chain()
            
            print("AIAlertGenerator initialized successfully with Azure OpenAI")
            
        except Exception as e:
            print(f"Warning: Failed to initialize AI components: {e}")
            import traceback
            traceback.print_exc()
            self.use_ai = False
            self._llm = None
            self._vectorstore = None
            self._retriever = None
            self._alert_chain = None
    
    def _format_docs(self, docs: List[Document]) -> str:
        """Format documents for RAG context."""
        return "\n\n".join(d.page_content[:300] for d in docs)
    
    def _build_alert_chain(self) -> None:
        """Build the alert generation chain."""
        if self._llm is None or self._retriever is None:
            return
        
        # Create the prompt template
        prompt = PromptTemplate.from_template(self.SYSTEM_PROMPT_TEMPLATE)
        
        # Build the chain
        self._alert_chain = (
            {
                "context": lambda x: self._get_context(x.get("location", "")),
                "location": lambda x: x.get("location", "Unknown"),
                "rainfall": lambda x: x.get("rainfall", 0.0),
                "alert_type": lambda x: x.get("alert_type", "unknown"),
                "severity": lambda x: x.get("severity", "low"),
                "from_state": lambda x: x.get("from_state", "unknown"),
                "to_state": lambda x: x.get("to_state", "unknown"),
            }
            | prompt
            | self._llm
            | StrOutputParser()
        )
    
    def _get_context(self, location: str) -> str:
        """Retrieve relevant context for a location."""
        if not self._retriever:
            return "No historical data available."
        
        try:
            query = f"{location} Singapore flood history incidents risks"
            docs = self._retriever.invoke(query)
            return self._format_docs(docs)
        except Exception as e:
            print(f"Warning: Could not retrieve context: {e}")
            return "Historical data retrieval failed."
    
    def _parse_response(self, response: str) -> tuple[str, str]:
        """Parse the AI response into display and audio text.
        
        Args:
            response: Raw response from AI
            
        Returns:
            Tuple of (display_text, audio_text)
        """
        display_text = ""
        audio_text = ""
        
        lines = response.strip().split('\n')
        for line in lines:
            line = line.strip()
            if line.upper().startswith("DISPLAY:"):
                display_text = line[8:].strip()
            elif line.upper().startswith("AUDIO:"):
                audio_text = line[6:].strip()
        
        # If parsing failed, use the whole response for display
        if not display_text:
            display_text = response.strip()[:140]
        
        # If no audio text, generate from display text
        if not audio_text:
            audio_text = self._generate_audio_version(display_text)
        
        return display_text, audio_text
    
    def _generate_audio_version(self, text: str) -> str:
        """Generate a shorter audio-friendly version of alert text.
        
        Args:
            text: Full alert text
            
        Returns:
            Shortened version for TTS
        """
        # Remove common UI elements
        text = text.replace("⚠️ ", "").replace("🚨 ", "").replace("🔴 ", "").replace("ℹ️ ", "")
        
        # Truncate if too long
        if len(text) > 100:
            # Try to break at sentence
            truncated = text[:100]
            last_period = truncated.rfind('.')
            if last_period > 70:
                truncated = truncated[:last_period + 1]
            text = truncated
        
        return text
    
    def _get_fallback_alert(
        self,
        alert_type: AlertType,
        location: str,
        rainfall: float,
        from_state: str,
        to_state: str,
        severity: AlertSeverity
    ) -> GeneratedAlert:
        """Get a fallback alert when AI is unavailable.
        
        Args:
            alert_type: Type of alert
            location: Location name
            rainfall: Current rainfall in mm
            from_state: Previous state
            to_state: Current state
            severity: Alert severity
            
        Returns:
            GeneratedAlert with fallback message
        """
        message = ""
        audio_text = ""
        
        # Determine bucket from rainfall
        bucket = "normal" if rainfall < 30 else "warning" if rainfall < 80 else "danger"
        
        if alert_type == AlertType.LOCATION_CHANGE:
            # Location-specific messages
            location_msgs = self.FALLBACK_ALERTS[AlertType.LOCATION_CHANGE].get(location, {
                "normal": f"Welcome to {location}. Conditions are normal.",
                "warning": f"Welcome to {location}. Heavy rain detected.",
                "danger": f"Welcome to {location}. Severe rain! Seek shelter!",
            })
            message = location_msgs.get(bucket, location_msgs["normal"])
        
        elif alert_type == AlertType.THRESHOLD_CROSSING:
            # Crossing messages
            crossing_key = f"{from_state}_to_{to_state}"
            crossing_msgs = self.FALLBACK_ALERTS[AlertType.THRESHOLD_CROSSING].get(crossing_key, [])
            if crossing_msgs:
                message = random.choice(crossing_msgs)
            else:
                # Generic crossing message
                if to_state == "danger":
                    message = f"CRITICAL: Entering severe rain zone at {location}! Evacuate!"
                elif to_state == "warning":
                    message = f"Warning: Heavy rain at {location}. Monitor conditions."
                else:
                    message = f"Conditions improving at {location}."
        
        elif alert_type == AlertType.ESCALATION:
            escalation_msgs = self.FALLBACK_ALERTS[AlertType.ESCALATION].get(bucket, [])
            message = random.choice(escalation_msgs) if escalation_msgs else "Caution: Rain intensifying. Stay alert."
        
        elif alert_type == AlertType.SEVERE_WEATHER:
            severe_msgs = self.FALLBACK_ALERTS[AlertType.SEVERE_WEATHER].get(bucket, [])
            message = random.choice(severe_msgs) if severe_msgs else "CRITICAL: Severe weather! Seek shelter immediately!"
        
        # Generate audio text
        audio_text = self._generate_audio_version(message)
        
        return GeneratedAlert(
            message=message,
            audio_text=audio_text,
            severity=severity,
            alert_type=alert_type,
            location=location,
            rainfall=rainfall,
            source_documents=[]
        )
    
    def generate_alert(
        self,
        alert_type: AlertType,
        location: str,
        rainfall: float,
        from_state: str = "",
        to_state: str = "",
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        callback: Optional[Callable[[GeneratedAlert], None]] = None
    ) -> Optional[GeneratedAlert]:
        """Generate an alert synchronously.
        
        Args:
            alert_type: Type of alert to generate
            location: Current location
            rainfall: Current rainfall in mm
            from_state: Previous state (for threshold crossings)
            to_state: Current state (for threshold crossings)
            severity: Alert severity level
            callback: Optional callback for async notification
            
        Returns:
            GeneratedAlert or None if generation failed
        """
        # If AI not available, return fallback immediately
        if not self.use_ai or self._alert_chain is None:
            alert = self._get_fallback_alert(
                alert_type, location, rainfall, from_state, to_state, severity
            )
            if callback:
                callback(alert)
            return alert
        
        try:
            # Prepare input for chain
            chain_input = {
                "location": location,
                "rainfall": rainfall,
                "alert_type": alert_type.value,
                "severity": severity.value,
                "from_state": from_state if from_state else "unknown",
                "to_state": to_state if to_state else "unknown",
            }
            
            # Run the chain
            response = self._alert_chain.invoke(chain_input)
            
            # Parse response
            display_text, audio_text = self._parse_response(response)
            
            # Get source documents
            source_docs = []
            if self._retriever:
                try:
                    docs = self._retriever.invoke(f"{location} flood")
                    source_docs = [d.page_content[:150] for d in docs[:2]]
                except Exception:
                    pass
            
            alert = GeneratedAlert(
                message=display_text,
                audio_text=audio_text,
                severity=severity,
                alert_type=alert_type,
                location=location,
                rainfall=rainfall,
                source_documents=source_docs
            )
            
            if callback:
                callback(alert)
            
            return alert
            
        except Exception as e:
            print(f"Error generating AI alert: {e}")
            import traceback
            traceback.print_exc()
            
            # Fall back to hardcoded messages
            alert = self._get_fallback_alert(
                alert_type, location, rainfall, from_state, to_state, severity
            )
            if callback:
                callback(alert)
            return alert
    
    def generate_alert_async(
        self,
        alert_type: AlertType,
        location: str,
        rainfall: float,
        from_state: str = "",
        to_state: str = "",
        severity: AlertSeverity = AlertSeverity.MEDIUM,
        callback: Optional[Callable[[GeneratedAlert], None]] = None
    ) -> None:
        """Generate an alert asynchronously in a background thread.
        
        Args:
            alert_type: Type of alert to generate
            location: Current location
            rainfall: Current rainfall in mm
            from_state: Previous state
            to_state: Current state
            severity: Alert severity level
            callback: Function to call with the generated alert
        """
        def generate_in_thread():
            alert = self.generate_alert(
                alert_type=alert_type,
                location=location,
                rainfall=rainfall,
                from_state=from_state,
                to_state=to_state,
                severity=severity
            )
            if callback and alert:
                callback(alert)
        
        thread = threading.Thread(target=generate_in_thread, daemon=True)
        thread.start()
    
    def is_available(self) -> bool:
        """Check if AI generation is available.
        
        Returns:
            True if initialized and ready
        """
        return self.use_ai and self._alert_chain is not None
    
    def get_stats(self) -> Dict[str, Any]:
        """Get generator statistics.
        
        Returns:
            Dict with status info
        """
        return {
            "ai_available": self.is_available(),
            "using_fallback": not self.use_ai,
            "backend": "Azure OpenAI" if self.use_ai else "Fallback",
        }
