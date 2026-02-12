"""AI Advisor providing contextual flood safety advice."""
from typing import Dict


class AIAdvisor:
    """Provides location-specific flood safety advice based on current level."""
    
    # Advice messages for each zone (based on rainfall)
    ADVICE: Dict[str, Dict[str, str]] = {
        "ION Orchard": {
            "normal": "Safe high ground. 18m elevation. MRT accessible via underground.",
            "warning": "ION Orchard - Heavy rain detected. Monitor conditions at street exits.",
            "danger": "Severe rain at ION. Check basement levels. Use overhead walkways if available."
        },
        "Orchard Road": {
            "normal": "Street level. Watch for pooling at curbs during light rain.",
            "warning": "Flash flood prone area. Heavy rain may cause accumulation. Move to higher ground.",
            "danger": "URGENT: Severe rain! Seek higher ground immediately. Avoid underground crossings!"
        },
        "Tanglin Carpark": {
            "normal": "DANGER ZONE: Historical flood site 2010/2011. Monitor weather conditions.",
            "warning": "Heavy rain at Tanglin! Be prepared to evacuate. Watch for rising water.",
            "danger": "EMERGENCY: Severe rain! Abandon vehicle and evacuate NOW via exits!"
        }
    }
    
    def __init__(self):
        """Initialize the AI advisor."""
        self.current_level = ""
        self.rainfall = 0
        
    def update(self, level_name: str, rainfall: float) -> None:
        """Update advisor state with current conditions.
        
        Args:
            level_name: Current zone name
            rainfall: Current rainfall in mm
        """
        self.current_level = level_name
        self.rainfall = rainfall
        
    def get_advice(self) -> str:
        """Get appropriate advice for current conditions.
        
        Returns:
            Contextual safety message based on level and rainfall conditions
        """
        if self.current_level not in self.ADVICE:
            return "Unknown location. Stay alert for flooding."
            
        level_advice = self.ADVICE[self.current_level]
        
        # Determine severity based on rainfall
        if self.rainfall < 30:
            return level_advice["normal"]
        elif self.rainfall < 80:
            return level_advice["warning"]
        else:
            return level_advice["danger"]
            
    def get_level_warning(self) -> str:
        """Get persistent warning text for the current level.
        
        Returns:
            Warning label to display in UI (e.g., "Tanglin Carpark - 2010 Flood Site")
        """
        warnings = {
            "ION Orchard": "ION Orchard - 18m Above Sea Level",
            "Orchard Road": "Orchard Road - Flash Flood Zone",
            "Tanglin Carpark": "TANGLIN CARPARK - 2010/2011 Flood Site!"
        }
        return warnings.get(self.current_level, "")
