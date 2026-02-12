"""Tanglin Carpark level - Basement, extreme danger zone."""
import pygame
from .level_base import BaseLevel
from core import ArrowTransition, ClickableObject


class CarparkLevel(BaseLevel):
    """Tanglin Mall basement carpark level.
    
    Visual: Basement carpark interior with parked cars, concrete pillars, blue floor markings
    
    Navigation: Left arrow to go back to Orchard Road
    
    Flood behavior:
    - Threshold 30mm (floods immediately)
    - Water rises fast from floor drains
    - Visual: Water covers blue floor, submerges tires first, then car bodies
    """
    
    def __init__(self):
        """Initialize Tanglin Carpark level."""
        super().__init__()
        self.name = "Tanglin Carpark"
        self.flood_threshold = 30  # Floods immediately - dangerous!
        
    def load(self) -> None:
        """Load assets and create arrows for Carpark level."""
        # Load background image
        self.load_background("assets/tanglin-carpark.png")
    
        
        # Create clickable objects for interactive scenery
        self.clickable_objects = [
            # Placeholder: Flooded vehicle
            ClickableObject(
                x=399,          # Left position
                y=204,          # Top position
                width=120,      # Width
                height=120,      # Height
                title="Submerged Car",
                description="A car partially submerged in flood water. "
                           "Basement carparks can flood rapidly during heavy rain. "
                           "Vehicles should be moved to higher ground when flood warnings are issued."
            ),
            # Placeholder: Drainage grate
            ClickableObject(
                x=500,          # Left position
                y=450,          # Top position
                width=60,       # Width
                height=40,      # Height
                title="Floor Drain",
                description="A floor drainage system. "
                           "During floods, water can back up through drains. "
                           "Adjust these coordinates to match your carpark asset."
            ),
        ]
                # Create clickable arrow to go back to Orchard Road
        self.arrows = [
            ArrowTransition(
                x=50,   # Left side
                y=300,  # Middle of screen
                direction="left",
                target_level="orchard",
                spawn_x=750,
                spawn_y=480,
                tooltip="Back to Orchard Road"
            )
        ]
