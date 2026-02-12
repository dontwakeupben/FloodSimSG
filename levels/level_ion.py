"""ION Orchard Mall level - High ground, safe zone."""
import pygame
from .level_base import BaseLevel
from core import ArrowTransition, ClickableObject


class IonLevel(BaseLevel):
    """ION Orchard entrance level.
    
    Visual: ION Orchard mall facade with distinctive architecture, glass panels, entrance steps
    
    Navigation: Click the right arrow to go to Orchard Road
    
    Flood behavior: Water rises from bottom but rarely reaches platforms
    due to high threshold (80mm).
    """
    
    def __init__(self):
        """Initialize ION Mall level."""
        super().__init__()
        self.name = "ION Orchard"
        self.flood_threshold = 80  # High threshold - safe zone
        
    def load(self) -> None:
        """Load assets and create arrows for ION level."""
        # Load background image
        self.load_background("assets/ion-mall.png")
        
        # Create clickable arrow for transitioning to Orchard Road
        # Position at right side of screen, middle height
        self.arrows = [
            ArrowTransition(
                x=750,  # Right side
                y=300,  # Middle of screen
                direction="right",
                target_level="orchard",
                spawn_x=50,
                spawn_y=480,
                tooltip="Go to Orchard Road"
            )
        ]
        
        # Create clickable objects for interactive scenery
        self.clickable_objects = [
            # Placeholder: Mall entrance sign
            ClickableObject(
                x=237,          # Left position
                y=352,          # Top position
                width=260,      # Width
                height=135,     # Height
                title="ION Orchard Entrance",
                description="The iconic ION Orchard mall entrance. "
                           "This area is on high ground and rarely floods "
                           "even during heavy rainfall."
            ),
        
        ]
