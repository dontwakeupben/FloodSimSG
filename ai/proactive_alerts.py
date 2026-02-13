"""Proactive Alert System for Flood Chatbot.

Monitors rainfall thresholds and automatically generates contextual AI alerts
when conditions change. Integrates with the existing FloodChatbot RAG system.
"""
from dataclasses import dataclass, field
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime, timedelta
from enum import Enum
import threading
import time

# Import AI alert generator
try:
    from .ai_alert_generator import AIAlertGenerator, GeneratedAlert, AlertSeverity, AlertType as GenAlertType
    AI_GENERATOR_AVAILABLE = True
except ImportError:
    AI_GENERATOR_AVAILABLE = False
    GeneratedAlert = None
    AlertSeverity = None
    GenAlertType = None


class AlertPriority(Enum):
    """Priority levels for proactive alerts."""
    LOW = "low"           # Informational
    MEDIUM = "medium"     # Caution
    HIGH = "high"         # Warning
    CRITICAL = "critical" # Emergency


class AlertType(Enum):
    """Types of proactive alerts."""
    THRESHOLD_CROSSING = "threshold_crossing"  # 30mm/80mm boundaries
    ESCALATION = "escalation"                   # Rising within a bucket
    LOCATION_CHANGE = "location_change"         # New zone entered
    SEVERE_WEATHER = "severe_weather"          # Extreme conditions
    HISTORICAL_CONTEXT = "historical_context"  # Reference to past floods


@dataclass
class ProactiveAlert:
    """A proactive alert message from the AI."""
    id: str
    message: str
    priority: AlertPriority
    alert_type: AlertType
    location: str
    rainfall: float
    created_at: datetime = field(default_factory=datetime.now)
    spoken: bool = False
    read: bool = False
    audio_text: Optional[str] = None  # Shorter version for TTS
    source_documents: List[str] = field(default_factory=list)
    
    def to_chat_message(self) -> str:
        """Convert to format for chatbot message history."""
        prefix = {
            AlertPriority.LOW: "ℹ️",
            AlertPriority.MEDIUM: "⚠️",
            AlertPriority.HIGH: "🚨",
            AlertPriority.CRITICAL: "🔴 EMERGENCY"
        }.get(self.priority, "ℹ️")
        
        return f"{prefix} **Alert**: {self.message}"
    
    def get_audio_text(self) -> str:
        """Get text optimized for text-to-speech."""
        if self.audio_text:
            return self.audio_text
        # Generate shorter version for speech
        return self.message[:150] if len(self.message) > 150 else self.message


class RainfallThresholdMonitor:
    """Monitors rainfall and detects threshold crossings.
    
    Tracks rainfall values and triggers alerts when crossing:
    - 30mm: Light → Heavy rain (warning threshold)
    - 50mm: Moderate → High risk within warning bucket
    - 80mm: Heavy → Severe rain (danger threshold)
    """
    
    THRESHOLDS = [30.0, 50.0, 80.0]
    
    def __init__(self):
        """Initialize the monitor."""
        self._last_rainfall: Optional[float] = None
        self._last_bucket: Optional[str] = None
        self._bucket_history: List[tuple] = []  # (timestamp, bucket, rainfall)
        
    def get_bucket(self, rainfall: float) -> str:
        """Get rainfall bucket for a value.
        
        Args:
            rainfall: Current rainfall in mm
            
        Returns:
            Bucket name: "normal", "warning", "danger"
        """
        if rainfall < 30:
            return "normal"
        elif rainfall < 80:
            return "warning"
        else:
            return "danger"
    
    def check_crossing(self, rainfall: float) -> Optional[Dict[str, Any]]:
        """Check if rainfall crossed any thresholds.
        
        Args:
            rainfall: Current rainfall in mm
            
        Returns:
            Dict with crossing info if threshold crossed, else None
        """
        if self._last_rainfall is None:
            self._last_rainfall = rainfall
            self._last_bucket = self.get_bucket(rainfall)
            return None
        
        current_bucket = self.get_bucket(rainfall)
        
        # Check for bucket change (major crossing)
        if current_bucket != self._last_bucket:
            crossed_threshold = None
            direction = "rising" if rainfall > self._last_rainfall else "falling"
            
            # Determine which threshold was crossed
            if direction == "rising":
                if current_bucket == "warning":
                    crossed_threshold = 30.0
                elif current_bucket == "danger":
                    crossed_threshold = 80.0
            else:  # falling
                if current_bucket == "warning":
                    crossed_threshold = 80.0
                elif current_bucket == "normal":
                    crossed_threshold = 30.0
            
            result = {
                "type": "bucket_change",
                "from_bucket": self._last_bucket,
                "to_bucket": current_bucket,
                "from_rainfall": self._last_rainfall,
                "to_rainfall": rainfall,
                "direction": direction,
                "threshold_crossed": crossed_threshold
            }
            
            self._last_rainfall = rainfall
            self._last_bucket = current_bucket
            self._bucket_history.append((datetime.now(), current_bucket, rainfall))
            
            return result
        
        # Check for internal threshold crossing within warning bucket
        if current_bucket == "warning":
            prev_below_50 = self._last_rainfall < 50
            curr_above_50 = rainfall >= 50
            
            if prev_below_50 and curr_above_50:
                result = {
                    "type": "internal_escalation",
                    "bucket": "warning",
                    "from_rainfall": self._last_rainfall,
                    "to_rainfall": rainfall,
                    "threshold_crossed": 50.0,
                    "direction": "rising"
                }
                self._last_rainfall = rainfall
                return result
        
        self._last_rainfall = rainfall
        return None
    
    def get_trend(self, window_seconds: int = 300) -> str:
        """Get rainfall trend over recent window.
        
        Args:
            window_seconds: Time window to analyze
            
        Returns:
            Trend description: "rising", "falling", "stable"
        """
        cutoff = datetime.now() - timedelta(seconds=window_seconds)
        recent = [(t, b, r) for t, b, r in self._bucket_history if t > cutoff]
        
        if len(recent) < 2:
            return "stable"
        
        first_rainfall = recent[0][2]
        last_rainfall = recent[-1][2]
        
        delta = last_rainfall - first_rainfall
        
        if delta > 10:
            return "rising"
        elif delta < -10:
            return "falling"
        return "stable"


class ProactiveAlertManager:
    """Manages proactive AI alerts for the flood chatbot.
    
    Monitors game conditions and automatically generates contextual alerts
    using the existing FloodChatbot RAG infrastructure.
    
    Example:
        manager = ProactiveAlertManager(chatbot)
        manager.start_monitoring()
        
        # In game loop
        manager.update_conditions(rainfall=45.0, location="Tanglin Carpark")
        
        # Check for new alerts
        if manager.has_new_alerts():
            alert = manager.get_next_alert()
            display_alert(alert)
            speak_alert(alert)
    """
    
    # Alert generation prompts for each type
    ALERT_PROMPTS = {
        AlertType.THRESHOLD_CROSSING: """Generate a brief flood safety alert (1-2 sentences) for someone at {location}.
Rainfall has just crossed from {from_bucket} to {to_bucket} conditions ({rainfall}mm).

Use the retrieved historical context to make the alert specific and actionable.
If this location has flooded before (like Tanglin 2010/2011), reference it.

Alert should be urgent but helpful.""",
        
        AlertType.ESCALATION: """Generate a brief caution alert for {location}.
Rainfall is escalating within the {bucket} range (now {rainfall}mm).

Reference relevant historical floods or specific risks for this location.
Give one actionable recommendation.""",
        
        AlertType.SEVERE_WEATHER: """Generate an urgent emergency alert for {location}.
Severe rainfall detected: {rainfall}mm. This is dangerous flood weather.

Use historical context to emphasize immediate danger if applicable.
Give clear evacuation instructions or safety actions.""",
        
        AlertType.LOCATION_CHANGE: """Welcome the user to {location} with relevant flood safety context.
Current rainfall: {rainfall}mm ({bucket} conditions).

Briefly mention any historical flood incidents here and current risk level.
Keep it conversational but informative.""",
    }
    
    def __init__(
        self,
        chatbot,  # FloodChatbot instance
        cooldown_seconds: int = 60,
        min_alert_interval: int = 30,
        use_ai_alerts: bool = True
    ):
        """Initialize the alert manager.
        
        Args:
            chatbot: FloodChatbot instance for RAG queries
            cooldown_seconds: Minimum time between same-type alerts
            min_alert_interval: Minimum time between any alerts
            use_ai_alerts: Whether to use AI-generated alerts (True) or fallback messages (False)
        """
        self.chatbot = chatbot
        self.cooldown_seconds = cooldown_seconds
        self.min_alert_interval = min_alert_interval
        self.use_ai_alerts = use_ai_alerts
        
        self._monitor = RainfallThresholdMonitor()
        self._alerts: List[ProactiveAlert] = []
        self._alert_history: List[ProactiveAlert] = []
        self._last_alert_time: Optional[datetime] = None
        self._cooldowns: Dict[AlertType, datetime] = {}
        
        self._current_rainfall: float = 0.0
        self._current_location: str = ""
        self._last_location: str = ""
        
        self._running = False
        self._monitor_thread: Optional[threading.Thread] = None
        self._alert_callbacks: List[Callable[[ProactiveAlert], None]] = []
        
        self._lock = threading.Lock()
        
        # Initialize AI alert generator
        self._alert_generator: Optional[AIAlertGenerator] = None
        if AI_GENERATOR_AVAILABLE and use_ai_alerts:
            try:
                self._alert_generator = AIAlertGenerator(use_ai=True)
                print("ProactiveAlertManager: AI alert generator initialized")
            except Exception as e:
                print(f"ProactiveAlertManager: Failed to initialize AI generator: {e}")
                self._alert_generator = None
        
    def add_alert_callback(self, callback: Callable[[ProactiveAlert], None]) -> None:
        """Add a callback to be called when new alerts are generated.
        
        Args:
            callback: Function(alert) to call
        """
        self._alert_callbacks.append(callback)
    
    def update_conditions(self, rainfall: float, location: str) -> Optional[ProactiveAlert]:
        """Update conditions and check for alerts.
        
        Args:
            rainfall: Current rainfall in mm
            location: Current location name
            
        Returns:
            ProactiveAlert if one was triggered, else None
        """
        with self._lock:
            self._current_rainfall = rainfall
            
            # Check for location change
            if location != self._current_location:
                self._last_location = self._current_location
                self._current_location = location
                self._monitor = RainfallThresholdMonitor()  # Reset monitor for new location
                
                # Generate location change alert
                if self._can_alert(AlertType.LOCATION_CHANGE):
                    return self._generate_alert(AlertType.LOCATION_CHANGE)
            
            # Check for threshold crossings
            crossing = self._monitor.check_crossing(rainfall)
            if crossing:
                if crossing["type"] == "bucket_change":
                    if crossing["to_bucket"] == "danger":
                        alert_type = AlertType.SEVERE_WEATHER
                    else:
                        alert_type = AlertType.THRESHOLD_CROSSING
                else:  # internal_escalation
                    alert_type = AlertType.ESCALATION
                
                if self._can_alert(alert_type):
                    return self._generate_alert(alert_type, crossing)
            
            return None
    
    def _can_alert(self, alert_type: AlertType) -> bool:
        """Check if alert type is off cooldown.
        
        Args:
            alert_type: Type of alert to check
            
        Returns:
            True if alert can be generated
        """
        now = datetime.now()
        
        # Check global interval
        if self._last_alert_time:
            time_since_last = (now - self._last_alert_time).total_seconds()
            if time_since_last < self.min_alert_interval:
                return False
        
        # Check type-specific cooldown
        if alert_type in self._cooldowns:
            time_since_type = (now - self._cooldowns[alert_type]).total_seconds()
            if time_since_type < self.cooldown_seconds:
                return False
        
        return True
    
    def _generate_alert(
        self,
        alert_type: AlertType,
        crossing_data: Optional[Dict] = None
    ) -> ProactiveAlert:
        """Generate an AI alert using RAG.
        
        Args:
            alert_type: Type of alert to generate
            crossing_data: Optional threshold crossing info
            
        Returns:
            Generated ProactiveAlert
        """
        # Use AI generator if available
        if self._alert_generator and self._alert_generator.is_available():
            return self._generate_ai_alert(alert_type, crossing_data)
        
        # Fall back to legacy generation
        return self._generate_legacy_alert(alert_type, crossing_data)
    
    def _generate_ai_alert(
        self,
        alert_type: AlertType,
        crossing_data: Optional[Dict] = None
    ) -> ProactiveAlert:
        """Generate alert using AIAlertGenerator.
        
        Args:
            alert_type: Type of alert to generate
            crossing_data: Optional threshold crossing info
            
        Returns:
            Generated ProactiveAlert
        """
        bucket = self._monitor.get_bucket(self._current_rainfall)
        
        # Map AlertType to GenAlertType
        type_map = {
            AlertType.THRESHOLD_CROSSING: GenAlertType.THRESHOLD_CROSSING,
            AlertType.ESCALATION: GenAlertType.ESCALATION,
            AlertType.SEVERE_WEATHER: GenAlertType.SEVERE_WEATHER,
            AlertType.LOCATION_CHANGE: GenAlertType.LOCATION_CHANGE,
        }
        gen_alert_type = type_map.get(alert_type, GenAlertType.THRESHOLD_CROSSING)
        
        # Map to AlertSeverity
        severity_map = {
            "normal": AlertSeverity.LOW,
            "warning": AlertSeverity.MEDIUM,
            "danger": AlertSeverity.CRITICAL if bucket == "danger" else AlertSeverity.HIGH,
        }
        severity = severity_map.get(bucket, AlertSeverity.MEDIUM)
        
        # Adjust severity based on alert type
        if alert_type == AlertType.SEVERE_WEATHER:
            severity = AlertSeverity.CRITICAL
        elif alert_type == AlertType.THRESHOLD_CROSSING and bucket == "danger":
            severity = AlertSeverity.CRITICAL
        elif alert_type == AlertType.ESCALATION:
            severity = AlertSeverity.MEDIUM
        
        # Get state transitions
        from_state = crossing_data.get("from_bucket", "") if crossing_data else ""
        to_state = crossing_data.get("to_bucket", "") if crossing_data else bucket
        
        # Generate AI alert
        generated = self._alert_generator.generate_alert(
            alert_type=gen_alert_type,
            location=self._current_location,
            rainfall=self._current_rainfall,
            from_state=from_state,
            to_state=to_state,
            severity=severity
        )
        
        # Map AlertSeverity back to AlertPriority
        priority_map = {
            AlertSeverity.LOW: AlertPriority.LOW,
            AlertSeverity.MEDIUM: AlertPriority.MEDIUM,
            AlertSeverity.HIGH: AlertPriority.HIGH,
            AlertSeverity.CRITICAL: AlertPriority.CRITICAL,
        }
        priority = priority_map.get(severity, AlertPriority.MEDIUM)
        
        # Create ProactiveAlert from GeneratedAlert
        alert = ProactiveAlert(
            id=f"{alert_type.value}_{int(time.time())}",
            message=generated.message,
            priority=priority,
            alert_type=alert_type,
            location=self._current_location,
            rainfall=self._current_rainfall,
            audio_text=generated.audio_text,
            source_documents=generated.source_documents
        )
        
        # Store and update cooldowns
        with self._lock:
            self._alerts.append(alert)
            self._alert_history.append(alert)
            self._last_alert_time = datetime.now()
            self._cooldowns[alert_type] = datetime.now()
        
        # Notify callbacks
        for callback in self._alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"Alert callback error: {e}")
        
        # Also add to chatbot message history (safely)
        try:
            if self.chatbot and hasattr(self.chatbot, '_add_assistant_message'):
                self.chatbot._add_assistant_message(alert.to_chat_message())
        except Exception as e:
            print(f"Warning: Could not add alert to chatbot history: {e}")
        
        return alert
    
    def _generate_legacy_alert(
        self,
        alert_type: AlertType,
        crossing_data: Optional[Dict] = None
    ) -> ProactiveAlert:
        """Generate alert using legacy fallback method.
        
        Args:
            alert_type: Type of alert to generate
            crossing_data: Optional threshold crossing info
            
        Returns:
            Generated ProactiveAlert
        """
        # Build prompt
        bucket = self._monitor.get_bucket(self._current_rainfall)
        prompt_template = self.ALERT_PROMPTS.get(alert_type, self.ALERT_PROMPTS[AlertType.THRESHOLD_CROSSING])
        
        prompt = prompt_template.format(
            location=self._current_location,
            rainfall=self._current_rainfall,
            bucket=bucket,
            from_bucket=crossing_data.get("from_bucket", "") if crossing_data else "",
            to_bucket=crossing_data.get("to_bucket", "") if crossing_data else ""
        )
        
        # Query RAG for context
        retrieved_docs = []
        if self.chatbot.is_available() and hasattr(self.chatbot, '_retriever') and self.chatbot._retriever:
            try:
                docs = self.chatbot._retriever.invoke(f"{self._current_location} flood history risks")
                retrieved_docs = [d.page_content[:200] for d in docs[:2]]
            except Exception as e:
                print(f"Warning: Could not retrieve context for alert: {e}")
        
        # Generate message using fallback
        message = self._generate_message_with_context(prompt, retrieved_docs)
        
        # Determine priority
        priority = self._get_priority(alert_type, bucket)
        
        # Create shorter audio version
        audio_text = self._generate_audio_text(message, priority)
        
        # Create alert
        alert = ProactiveAlert(
            id=f"{alert_type.value}_{int(time.time())}",
            message=message,
            priority=priority,
            alert_type=alert_type,
            location=self._current_location,
            rainfall=self._current_rainfall,
            audio_text=audio_text,
            source_documents=retrieved_docs
        )
        
        # Store and update cooldowns
        with self._lock:
            self._alerts.append(alert)
            self._alert_history.append(alert)
            self._last_alert_time = datetime.now()
            self._cooldowns[alert_type] = datetime.now()
        
        # Notify callbacks
        for callback in self._alert_callbacks:
            try:
                callback(alert)
            except Exception as e:
                print(f"Alert callback error: {e}")
        
        # Also add to chatbot message history (safely)
        try:
            if self.chatbot and hasattr(self.chatbot, '_add_assistant_message'):
                self.chatbot._add_assistant_message(alert.to_chat_message())
        except Exception as e:
            print(f"Warning: Could not add alert to chatbot history: {e}")
        
        return alert
    
    def _generate_message_with_context(self, prompt: str, docs: List[str]) -> str:
        """Generate alert message using AI or fallback.
        
        For now, using hardcoded fallback messages to ensure reliability.
        AI generation can be enabled later.
        
        Args:
            prompt: Generation prompt (unused for now)
            docs: Retrieved context documents (unused for now)
            
        Returns:
            Generated message
        """
        # Using hardcoded messages for now - reliable and instant
        return self._get_fallback_message()
        
        # TODO: Enable AI generation once basic alerts are working
        # if not self.chatbot.is_available():
        #     return self._get_fallback_message()
        # try:
        #     context = "\n".join(docs) if docs else "No specific historical data retrieved."
        #     full_prompt = f"Context from Singapore flood documents:\n{context}\n\n{prompt}\n\nKeep under 140 chars."
        #     response = self.chatbot._llm.invoke(full_prompt)
        #     return response.content.strip()
        # except Exception as e:
        #     return self._get_fallback_message()
    
    def _generate_audio_text(self, message: str, priority: AlertPriority) -> str:
        """Generate shorter version for text-to-speech.
        
        Args:
            message: Full message
            priority: Alert priority
            
        Returns:
            Shortened audio-friendly text
        """
        # Priority-based prefixes
        prefixes = {
            AlertPriority.CRITICAL: "Emergency alert! ",
            AlertPriority.HIGH: "Warning! ",
            AlertPriority.MEDIUM: "Caution: ",
            AlertPriority.LOW: ""
        }
        
        prefix = prefixes.get(priority, "")
        
        # Truncate if too long for speech
        max_len = 120
        if len(message) > max_len:
            # Try to break at sentence
            truncated = message[:max_len]
            last_period = truncated.rfind('.')
            if last_period > max_len * 0.7:
                truncated = truncated[:last_period + 1]
            message = truncated
        
        return prefix + message
    
    def _get_priority(self, alert_type: AlertType, bucket: str) -> AlertPriority:
        """Determine alert priority.
        
        Args:
            alert_type: Type of alert
            bucket: Current rainfall bucket
            
        Returns:
            AlertPriority
        """
        if bucket == "danger":
            return AlertPriority.CRITICAL
        elif alert_type == AlertType.THRESHOLD_CROSSING and bucket == "warning":
            return AlertPriority.HIGH
        elif alert_type == AlertType.ESCALATION:
            return AlertPriority.MEDIUM
        elif alert_type == AlertType.SEVERE_WEATHER:
            return AlertPriority.CRITICAL
        return AlertPriority.LOW
    
    def _get_fallback_message(self) -> str:
        """Get fallback alert message based on location and conditions."""
        bucket = self._monitor.get_bucket(self._current_rainfall)
        location = self._current_location
        
        # Location-specific messages
        messages = {
            "ION Orchard": {
                "normal": f"Welcome to ION Orchard. You are at 18 meters elevation, safe from flooding.",
                "warning": f"ION Orchard: Heavy rain detected. Street level may have water, but you are safe here.",
                "danger": f"ION Orchard: Severe rain. Stay in the mall. Avoid basement levels."
            },
            "Orchard Road": {
                "normal": f"Welcome to Orchard Road. Watch for water pooling during rain.",
                "warning": f"Orchard Road warning: Heavy rain may cause flash floods. Move to higher ground if needed.",
                "danger": f"URGENT: Severe rain on Orchard Road! Seek shelter immediately. Avoid drains and canals."
            },
            "Tanglin Carpark": {
                "normal": f"Welcome to Tanglin Carpark. Warning: This basement flooded in 2010 and 2011.",
                "warning": f"Tanglin Carpark warning: Heavy rain! Be ready to evacuate. Watch for rising water.",
                "danger": f"EMERGENCY at Tanglin Carpark! Severe rain! Evacuate NOW! Abandon vehicle if necessary!"
            }
        }
        
        location_messages = messages.get(location, {
            "normal": f"At {location}: Conditions are normal.",
            "warning": f"Warning at {location}: Heavy rain detected. Monitor conditions.",
            "danger": f"DANGER at {location}: Severe rainfall! Seek higher ground immediately."
        })
        
        return location_messages.get(bucket, f"Stay alert at {location}.")
    
    def get_pending_alerts(self) -> List[ProactiveAlert]:
        """Get all pending (unread) alerts.
        
        Returns:
            List of pending alerts
        """
        with self._lock:
            return [a for a in self._alerts if not a.read]
    
    def get_next_alert(self) -> Optional[ProactiveAlert]:
        """Get and mark as read the next pending alert.
        
        Returns:
            Next alert or None
        """
        with self._lock:
            for alert in self._alerts:
                if not alert.read:
                    alert.read = True
                    return alert
            return None
    
    def has_new_alerts(self) -> bool:
        """Check if there are unread alerts.
        
        Returns:
            True if unread alerts exist
        """
        return any(not a.read for a in self._alerts)
    
    def mark_alert_spoken(self, alert_id: str) -> None:
        """Mark an alert as having been spoken.
        
        Args:
            alert_id: ID of the alert
        """
        with self._lock:
            for alert in self._alerts:
                if alert.id == alert_id:
                    alert.spoken = True
                    break
    
    def get_alert_history(self, limit: int = 10) -> List[ProactiveAlert]:
        """Get recent alert history.
        
        Args:
            limit: Maximum alerts to return
            
        Returns:
            List of historical alerts
        """
        with self._lock:
            return self._alert_history[-limit:]
    
    def clear_alerts(self) -> None:
        """Clear all pending alerts."""
        with self._lock:
            self._alerts.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get alert statistics.
        
        Returns:
            Dict with alert counts, history size, etc.
        """
        with self._lock:
            ai_available = False
            if self._alert_generator is not None:
                try:
                    ai_available = self._alert_generator.is_available()
                except Exception:
                    ai_available = False
            
            stats = {
                "pending_alerts": len([a for a in self._alerts if not a.read]),
                "total_alerts": len(self._alert_history),
                "current_rainfall": self._current_rainfall,
                "current_location": self._current_location,
                "current_bucket": self._monitor.get_bucket(self._current_rainfall),
                "ai_generator_available": ai_available,
                "using_ai_alerts": self.use_ai_alerts and (self._alert_generator is not None),
            }
            return stats
    
    def is_ai_available(self) -> bool:
        """Check if AI alert generation is available.
        
        Returns:
            True if AI generator is ready
        """
        return self._alert_generator is not None and self._alert_generator.is_available()