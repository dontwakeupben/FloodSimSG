"""Abstract base class for all levels in the flood simulation."""
from abc import ABC, abstractmethod
import pygame
from typing import Optional, Tuple


class BaseLevel(ABC):
    """Abstract base class defining the interface for all game levels.
    
    Each level represents a different zone (ION Mall, Orchard Road, Tanglin Carpark)
    with unique flood characteristics. Now uses clickable arrows for transitions
    and clickable objects for interactive scenery.
    """
    
    def __init__(self):
        """Initialize base level properties."""
        self.name = ""
        self.arrows = []  # List of ArrowTransition objects
        self.clickable_objects = []  # List of ClickableObject instances
        self.flood_threshold = 50  # mm of rainfall before flooding starts
        self.background_image = None  # pygame.Surface loaded in child classes
        self.background_color = (100, 150, 200)  # Fallback color
        
    def load_background(self, image_path: str) -> None:
        """Load and scale a background image to fit the 800x600 window.
        
        Args:
            image_path: Relative path to the image file (e.g., "assets/ion-mall.png")
        """
        try:
            raw_image = pygame.image.load(image_path)
            # Scale to fit 800x600 window
            self.background_image = pygame.transform.scale(raw_image, (800, 600))
        except pygame.error as e:
            print(f"Warning: Could not load background {image_path}: {e}")
            self.background_image = None
            
    def draw_background(self, screen: pygame.Surface) -> None:
        """Draw the background image or fill with fallback color.
        
        Args:
            screen: The pygame surface to draw on
        """
        if self.background_image:
            screen.blit(self.background_image, (0, 0))
        else:
            screen.fill(self.background_color)
            
    def calculate_water_height(self, rainfall: float) -> float:
        """Calculate how high the water should be based on rainfall.
        
        Water rises when rainfall exceeds the level's flood_threshold.
        Each mm above threshold raises water by 4 pixels.
        
        Args:
            rainfall: Current rainfall in mm (0-150)
            
        Returns:
            Water height in pixels from bottom of screen (0-600)
        """
        if rainfall <= self.flood_threshold:
            return 0
        height = (rainfall - self.flood_threshold) * 4
        return min(height, 600)  # Cap at full screen height
        
    def handle_event(self, event: pygame.event.Event) -> tuple:
        """Handle events for all arrows in this level.
        
        Args:
            event: Pygame event
            
        Returns:
            Tuple of (target_level, spawn_x, spawn_y) if arrow clicked, else None
        """
        for arrow in self.arrows:
            if arrow.handle_event(event):
                return (arrow.target_level, arrow.spawn_point[0], arrow.spawn_point[1])
        return None
        
    def handle_clickable_events(self, event: pygame.event.Event) -> Optional[Tuple[str, str]]:
        """Handle events for all clickable objects in this level.
        
        Args:
            event: Pygame event
            
        Returns:
            Tuple of (title, description) if a clickable object was clicked, else None
        """
        for obj in self.clickable_objects:
            if obj.handle_event(event):
                return (obj.title, obj.description)
        return None
        
    def update(self, dt: float) -> None:
        """Update all arrows in this level.
        
        Args:
            dt: Delta time in seconds
        """
        for arrow in self.arrows:
            arrow.update(dt)
            
    def update_clickables(self, dt: float) -> None:
        """Update all clickable objects in this level.
        
        Args:
            dt: Delta time in seconds
        """
        for obj in self.clickable_objects:
            obj.update(dt)
            
    def draw_arrows(self, screen: pygame.Surface) -> None:
        """Draw all transition arrows for this level.
        
        Args:
            screen: The pygame surface to draw on
        """
        for arrow in self.arrows:
            arrow.draw(screen)
            
    def draw_clickables(self, screen: pygame.Surface) -> None:
        """Draw all clickable object highlights for this level.
        
        Args:
            screen: The pygame surface to draw on
        """
        for obj in self.clickable_objects:
            obj.draw(screen)
            
    def reset_clickable_cursors(self) -> None:
        """Reset all clickable object cursors. Call when leaving level."""
        for obj in self.clickable_objects:
            obj.reset_cursor()
        
    @abstractmethod
    def load(self) -> None:
        """Load level-specific assets and create arrows.
        
        Must be implemented by each level subclass to:
        1. Load the background image
        2. Create ArrowTransition objects for navigation
        """
        pass
