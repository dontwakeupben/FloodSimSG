"""Orchard Road level - Street level, flash flood zone."""
import pygame
from .level_base import BaseLevel
from core import ArrowTransition, ClickableObject


class OrchardLevel(BaseLevel):
    """Orchard Road street level.
    
    Visual: Street scene with hanging decorations, vehicles, road markings, buildings
    
    Navigation: 
    - Left arrow: Back to ION Orchard
    - Right arrow: Down to Tanglin Carpark
    
    Flood behavior: Water covers road surface at 50mm threshold
    """
    
    def __init__(self):
        """Initialize Orchard Road level."""
        super().__init__()
        self.name = "Orchard Road"
        self.flood_threshold = 50  # Street level floods at moderate rainfall
        
    def load(self) -> None:
        """Load assets and create arrows for Orchard Road level."""
        # Load background image
        self.load_background("assets/orchard-road.png")
        
        # Create clickable arrows for both directions
        self.arrows = [
            # Left arrow - back to ION Orchard
            ArrowTransition(
                x=50,   # Left side
                y=300,  # Middle of screen
                direction="left",
                target_level="ion",
                spawn_x=750,
                spawn_y=430,
                tooltip="Back to ION Orchard"
            ),
            # Right arrow - to Tanglin Carpark
            ArrowTransition(
                x=750,  # Right side
                y=300,  # Middle of screen
                direction="right",
                target_level="carpark",
                spawn_x=50,
                spawn_y=515,
                tooltip="Go to Tanglin Carpark"
            )
        ]
        
        # Create clickable objects for interactive scenery
        self.clickable_objects = [
            # Green double-decker bus on the left side
            ClickableObject(
                x=170,          # Left position of bus
                y=360,          # Top position of bus
                width=130,      # Bus width
                height=190,     # Bus height
                title="Public Bus",
                description="A double-decker bus caught in the flash flood. "
                           "Vehicles can stall in as little as 300mm of standing water. "
                           "Never attempt to drive through flooded roads."
            ),
            ClickableObject(
                x=383,          # Left position of bus
                y=476,          # Top position of bus
                width=70,      # Bus width
                height=80,     # Bus height
                title="Car",
                description="A car can be unsafe during floods or extreme rainfall due to slippery roads or high water levels. "
                           "Vehicles can stall in as little as 300mm of standing water."
                           "Never attempt to drive through flooded roads."
            ),
            
            
        ]
