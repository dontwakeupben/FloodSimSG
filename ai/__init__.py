"""AI module for flood simulation."""
from .ai_advisor import AIAdvisor
from .ai_chatbot import FloodChatbot, ChatMessage
from .ai_chatbot_ui import ChatbotPanel, ChatButton, AlertHistoryView
from .proactive_alerts import (
    ProactiveAlertManager,
    ProactiveAlert,
    AlertPriority,
    AlertType,
    RainfallThresholdMonitor
)
from .audio_narrator import AudioNarrator, NullAudioNarrator, TTSBackend
from .risk_scoring import (
    RiskScorer,
    PersonalizedRiskScorer,
    RiskScore,
    RiskLevel,
    RiskFactors
)
from .ai_alert_generator import (
    AIAlertGenerator,
    GeneratedAlert,
    AlertSeverity,
)

__all__ = [
    # Advisor
    "AIAdvisor",
    # Chatbot
    "FloodChatbot",
    "ChatMessage",
    "ChatbotPanel",
    "ChatButton",
    "AlertHistoryView",
    # Proactive Alerts
    "ProactiveAlertManager",
    "ProactiveAlert",
    "AlertPriority",
    "AlertType",
    "RainfallThresholdMonitor",
    # Audio
    "AudioNarrator",
    "NullAudioNarrator",
    "TTSBackend",
    # Risk Scoring
    "RiskScorer",
    "PersonalizedRiskScorer",
    "RiskScore",
    "RiskLevel",
    "RiskFactors",
    # AI Alert Generator
    "AIAlertGenerator",
    "GeneratedAlert",
    "AlertSeverity",
]