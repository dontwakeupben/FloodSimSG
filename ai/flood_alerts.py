"""Simple flood alert system for threshold-based TTS alerts."""
from typing import Optional, Callable


class FloodAlertManager:
    """Manages flood alerts based on rainfall thresholds.
    
    Simple hardcoded alerts that trigger when crossing:
    - 30mm: Light -> Heavy rain (warning)
    - 80mm: Heavy -> Severe rain (danger/critical)
    """
    
    # Location-specific alert messages
    ALERTS = {
        "ION Orchard": {
            30: {
                "rising": "ION Orchard: Heavy rain outside. You are safe on high ground.",
                "falling": "ION Orchard: Rain easing. Conditions improving."
            },
            80: {
                "rising": "URGENT at ION Orchard: Severe rain! Stay inside, avoid basement levels.",
                "falling": "ION Orchard: Rain decreasing but still heavy. Remain cautious."
            }
        },
        "Orchard Road": {
            30: {
                "rising": "Orchard Road warning: Heavy rain may cause flash floods. Move to higher ground.",
                "falling": "Orchard Road: Rain easing. Still watch for water pooling."
            },
            80: {
                "rising": "EMERGENCY on Orchard Road! Severe rain! Seek shelter immediately!",
                "falling": "Orchard Road: Rain decreasing from severe levels. Stay alert."
            }
        },
        "Tanglin Carpark": {
            30: {
                "rising": "Tanglin Carpark warning: Heavy rain! This area flooded in 2010 and 2011. Watch water levels.",
                "falling": "Tanglin Carpark: Rain easing. Check for water accumulation before leaving."
            },
            80: {
                "rising": "EMERGENCY at Tanglin Carpark! Severe rain! Evacuate NOW! Abandon vehicle if necessary!",
                "falling": "Tanglin Carpark: Severe rain decreasing but still dangerous. Evacuate if water rising."
            }
        }
    }
    
    def __init__(self, audio_narrator=None):
        """Initialize alert manager.
        
        Args:
            audio_narrator: Optional AudioNarrator for TTS
        """
        self.audio_narrator = audio_narrator
        self._last_rainfall = 0.0
        self._last_location = ""
        self._alerted_30 = False
        self._alerted_80 = False
        
    def update(self, rainfall: float, location: str) -> Optional[str]:
        """Update conditions and check for alerts.
        
        Args:
            rainfall: Current rainfall in mm
            location: Current location name
            
        Returns:
            Alert message if triggered, None otherwise
        """
        # Reset alerts on location change
        if location != self._last_location:
            self._last_rainfall = rainfall
            self._last_location = location
            self._alerted_30 = False
            self._alerted_80 = False
            return None
        
        # Check 80mm threshold first (more critical)
        if rainfall >= 80 and self._last_rainfall < 80:
            self._alerted_80 = True
            self._alerted_30 = True  # 80 implies 30
            alert = self._get_alert(location, 80, "rising")
            self._speak(alert)
            self._last_rainfall = rainfall
            return alert
        
        # Check falling from 80mm
        if rainfall < 80 and self._last_rainfall >= 80:
            self._alerted_80 = False
            alert = self._get_alert(location, 80, "falling")
            self._speak(alert)
            self._last_rainfall = rainfall
            return alert
        
        # Check 30mm threshold
        if rainfall >= 30 and self._last_rainfall < 30:
            self._alerted_30 = True
            alert = self._get_alert(location, 30, "rising")
            self._speak(alert)
            self._last_rainfall = rainfall
            return alert
        
        # Check falling from 30mm
        if rainfall < 30 and self._last_rainfall >= 30:
            self._alerted_30 = False
            self._alerted_80 = False
            alert = self._get_alert(location, 30, "falling")
            self._speak(alert)
            self._last_rainfall = rainfall
            return alert
        
        self._last_rainfall = rainfall
        return None
    
    def _get_alert(self, location: str, threshold: int, direction: str) -> str:
        """Get alert message for location and threshold.
        
        Args:
            location: Location name
            threshold: 30 or 80
            direction: 'rising' or 'falling'
            
        Returns:
            Alert message
        """
        location_alerts = self.ALERTS.get(location, {})
        threshold_alerts = location_alerts.get(threshold, {})
        message = threshold_alerts.get(direction, "Stay alert for flooding.")
        return message
    
    def _speak(self, message: str) -> None:
        """Speak alert via TTS if narrator available.
        
        Args:
            message: Message to speak
        """
        if self.audio_narrator:
            try:
                self.audio_narrator.speak(message, priority=1, alert_id="flood_alert")
            except Exception as e:
                print(f"[TTS Error] {e}")
