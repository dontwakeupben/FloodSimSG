"""Game entities: Platform, Water, RainEffect, and ArrowTransition."""
import pygame
import math
import random
from typing import List, Tuple, Optional, Dict

# Game dimensions (must match main.py)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Platform(pygame.Rect):
    """A platform that the player can stand on.
    
    Invisible collision box aligned with visual elements in background images.
    Can optionally show debug visualization if alpha > 0 in color.
    """
    
    def __init__(self, x: int, y: int, w: int, h: int, name: str, 
                 color_with_alpha: Tuple[int, int, int, int]):
        """Initialize a platform.
        
        Args:
            x, y: Top-left position in pixels
            w, h: Width and height in pixels
            name: Identifier for this platform (e.g., "steps", "car_roof")
            color_with_alpha: RGBA tuple for debug visualization (0 alpha = invisible)
        """
        super().__init__(x, y, w, h)
        self.name = name
        self.color = color_with_alpha
        self.visible = color_with_alpha[3] > 0  # Show if alpha > 0
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw platform for debug purposes if visible.
        
        Args:
            screen: The pygame surface to draw on
        """
        if self.visible:
            # Create surface with alpha
            surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            surf.fill(self.color)
            screen.blit(surf, (self.x, self.y))


class ArrowTransition:
    """A clickable pixelated arrow for transitioning between levels.
    
    Drawn programmatically to create a pixelated game UI element.
    Can point left or right and has hover/click animations.
    """
    
    # Color palette for pixelated arrow (red arrow with yellow outline)
    COLORS = {
        'base': (200, 60, 60),        # Main red
        'light': (255, 100, 100),     # Highlight
        'dark': (150, 30, 30),        # Shadow
        'border': (255, 220, 0),      # Yellow outline
        'hover_base': (230, 80, 80),  # Brighter when hovered
        'hover_light': (255, 140, 140),
    }
    
    def __init__(self, x: int, y: int, direction: str = "right", 
                 target_level: str = "", spawn_x: int = 100, spawn_y: int = 300,
                 tooltip: str = ""):
        """Initialize a clickable arrow transition.
        
        Args:
            x, y: Center position of the arrow
            direction: "left" or "right"
            target_level: Name of level to transition to
            spawn_x, spawn_y: Spawn position in target level
            tooltip: Text to show on hover
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.target_level = target_level
        self.spawn_point = (spawn_x, spawn_y)
        self.tooltip = tooltip
        
        # Arrow dimensions
        self.width = 64
        self.height = 48
        
        # Clickable area (slightly larger than visual)
        self.rect = pygame.Rect(
            x - self.width // 2 - 10,
            y - self.height // 2 - 10,
            self.width + 20,
            self.height + 20
        )
        
        # Animation state
        self.hovered = False
        self.clicked = False
        self.pulse_time = 0.0
        self.click_anim = 0.0
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process mouse events for arrow interaction.
        
        Args:
            event: Pygame event
            
        Returns:
            True if arrow was clicked
        """
        if event.type == pygame.MOUSEMOTION:
            self.hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                self.click_anim = 1.0
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
            
        return False
        
    def update(self, dt: float) -> None:
        """Update arrow animation state.
        
        Args:
            dt: Delta time in seconds
        """
        self.pulse_time += dt * 2
        if self.click_anim > 0:
            self.click_anim = max(0, self.click_anim - dt * 5)
            
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the pixelated arrow.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Calculate pulsing offset for idle animation
        pulse = math.sin(self.pulse_time) * 3 if self.hovered else math.sin(self.pulse_time) * 1.5
        click_offset = self.click_anim * 4
        
        # Base position with animations
        base_x = self.x + pulse - click_offset if self.direction == "right" else self.x - pulse + click_offset
        base_y = self.y
        
        # Choose colors based on state
        if self.hovered:
            base_color = self.COLORS['hover_base']
            light_color = self.COLORS['hover_light']
        else:
            base_color = self.COLORS['base']
            light_color = self.COLORS['light']
        dark_color = self.COLORS['dark']
        border_color = self.COLORS['border']
        
        # Pixel size for pixelated look
        pixel = 4
        
        # Draw pixelated arrow based on direction
        if self.direction == "right":
            self._draw_arrow_right(screen, base_x, base_y, pixel, 
                                   base_color, light_color, dark_color, border_color)
        else:
            self._draw_arrow_left(screen, base_x, base_y, pixel,
                                  base_color, light_color, dark_color, border_color)
        
        # Draw tooltip if hovered
        if self.hovered and self.tooltip:
            self._draw_tooltip(screen)
            
    def _draw_arrow_right(self, screen, x, y, pixel, base, light, dark, border):
        """Draw a right-pointing pixelated arrow with yellow border."""
        # Arrow shape (1 = pixel, 0 = empty)
        # 10x6 grid scaled by pixel size (extended body)
        pattern = [
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
            [1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        ]
        
        start_x = x - (len(pattern[0]) * pixel) // 2
        start_y = y - (len(pattern) * pixel) // 2
        
        # Draw yellow border (offset by 1 pixel in each direction)
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for row_idx, row in enumerate(pattern):
                for col_idx, cell in enumerate(row):
                    if cell:
                        px = start_x + col_idx * pixel + offset[0] * pixel
                        py = start_y + row_idx * pixel + offset[1] * pixel
                        pygame.draw.rect(screen, border, (px, py, pixel, pixel))
        
        # Draw main arrow pixels
        for row_idx, row in enumerate(pattern):
            for col_idx, cell in enumerate(row):
                if cell:
                    px = start_x + col_idx * pixel
                    py = start_y + row_idx * pixel
                    
                    # Choose color based on position for 3D effect
                    if col_idx < 3:
                        color = light  # Highlight on left
                    elif col_idx > 6:
                        color = dark   # Shadow on right
                    else:
                        color = base   # Base in middle
                    
                    pygame.draw.rect(screen, color, (px, py, pixel, pixel))
    
    def _draw_arrow_left(self, screen, x, y, pixel, base, light, dark, border):
        """Draw a left-pointing pixelated arrow with yellow border."""
        # Mirror of right arrow
        pattern = [
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
        ]
        
        start_x = x - (len(pattern[0]) * pixel) // 2
        start_y = y - (len(pattern) * pixel) // 2
        
        # Draw yellow border
        for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            for row_idx, row in enumerate(pattern):
                for col_idx, cell in enumerate(row):
                    if cell:
                        px = start_x + col_idx * pixel + offset[0] * pixel
                        py = start_y + row_idx * pixel + offset[1] * pixel
                        pygame.draw.rect(screen, border, (px, py, pixel, pixel))
        
        # Draw main arrow pixels
        for row_idx, row in enumerate(pattern):
            for col_idx, cell in enumerate(row):
                if cell:
                    px = start_x + col_idx * pixel
                    py = start_y + row_idx * pixel
                    
                    # Choose color - reversed for left arrow
                    if col_idx > 6:
                        color = light  # Highlight on right
                    elif col_idx < 3:
                        color = dark   # Shadow on left
                    else:
                        color = base   # Base in middle
                    
                    pygame.draw.rect(screen, color, (px, py, pixel, pixel))
    
    def _draw_tooltip(self, screen):
        """Draw tooltip text near the arrow."""
        font = pygame.font.Font(None, 24)
        text_surf = font.render(self.tooltip, True, (255, 255, 255))
        
        # Get screen dimensions
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        # Position tooltip above the arrow
        text_x = self.x - text_surf.get_width() // 2
        text_y = self.y - self.height // 2 - 30
        
        # Clamp to screen bounds with padding
        padding = 5
        text_x = max(padding, min(text_x, screen_width - text_surf.get_width() - padding))
        text_y = max(padding, text_y)
        
        # Draw dark background for readability
        bg_rect = text_surf.get_rect()
        bg_rect.inflate_ip(10, 6)
        bg_rect.x = text_x - 5
        bg_rect.y = text_y - 3
        pygame.draw.rect(screen, (0, 0, 0), bg_rect, border_radius=4)
        
        # Draw text
        screen.blit(text_surf, (text_x, text_y))


class ClickableObject:
    """An invisible clickable area in the scene that shows info on click.
    
    Used for interactive scenery objects like vehicles, buildings, signs, etc.
    Shows a yellow highlight/outline when hovered to indicate interactivity.
    """
    
    # Highlight color - semi-transparent yellow
    HIGHLIGHT_COLOR = (255, 220, 0, 120)
    OUTLINE_COLOR = (255, 240, 100, 200)
    HOVER_CURSOR = pygame.SYSTEM_CURSOR_HAND
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 title: str, description: str,
                 highlight_color: Optional[Tuple[int, int, int, int]] = None):
        """Initialize a clickable object.
        
        Args:
            x, y: Top-left position of the hitbox
            width, height: Size of the clickable area
            title: Display name of the object (shown in popup)
            description: Detailed info about the object
            highlight_color: Optional custom highlight color (RGBA)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.description = description
        self.highlight_color = highlight_color or self.HIGHLIGHT_COLOR
        
        # State
        self.hovered = False
        self.clicked = False
        self.pulse_time = 0.0
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process mouse events for this object.
        
        Args:
            event: Pygame event
            
        Returns:
            True if object was clicked
        """
        if event.type == pygame.MOUSEMOTION:
            was_hovered = self.hovered
            self.hovered = self.rect.collidepoint(event.pos)
            
            # Change cursor on hover
            if self.hovered != was_hovered:
                if self.hovered:
                    pygame.mouse.set_cursor(self.HOVER_CURSOR)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
            
        return False
        
    def update(self, dt: float) -> None:
        """Update hover animation.
        
        Args:
            dt: Delta time in seconds
        """
        self.pulse_time += dt * 3
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw hover highlight if mouse is over this object.
        
        Args:
            screen: The pygame surface to draw on
        """
        if self.hovered:
            # Create pulsing alpha effect
            pulse = (math.sin(self.pulse_time) + 1) / 2  # 0 to 1
            alpha = int(self.highlight_color[3] * (0.6 + 0.4 * pulse))
            
            # Create highlight surface
            highlight_surf = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
            color_with_alpha = (*self.highlight_color[:3], alpha)
            highlight_surf.fill(color_with_alpha)
            screen.blit(highlight_surf, self.rect.topleft)
            
            # Draw outline
            outline_color = (*self.OUTLINE_COLOR[:3],
                           int(self.OUTLINE_COLOR[3] * (0.7 + 0.3 * pulse)))
            pygame.draw.rect(screen, outline_color, self.rect, 3)
            
    def reset_cursor(self) -> None:
        """Reset cursor to default. Call when leaving level."""
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)


class Water:
    """Flood water that rises from the bottom of the screen.
    
    Visual indicator of flooding - rises higher as rainfall increases.
    """
    
    # Water color palette
    COLOR_SURFACE = (100, 150, 200, 180)  # Light blue with alpha
    COLOR_DEEP = (50, 80, 120, 200)       # Darker blue
    COLOR_FOAM = (200, 220, 240, 150)     # Foam/whitecaps
    
    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """Initialize water.
        
        Args:
            screen_width: Screen width for water bounds
            screen_height: Screen height for water bounds
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.height = 0  # Current water height in pixels
        self.target_height = 0
        self.wave_offset = 0.0
        self.wave_speed = 2.0
        self.foam_particles = []
        
    def update(self, rainfall_mm: float, flood_threshold: float, dt: float) -> None:
        """Update water height based on rainfall.
        
        Args:
            rainfall_mm: Current rainfall in mm
            flood_threshold: Rainfall threshold before flooding starts
            dt: Delta time in seconds
        """
        # Calculate target height (water rises above threshold)
        if rainfall_mm <= flood_threshold:
            self.target_height = 0
        else:
            # Each mm above threshold adds water height
            excess = rainfall_mm - flood_threshold
            self.target_height = excess * 3  # 3 pixels per mm
            
        # Clamp max height (don't fill entire screen)
        max_height = self.screen_height * 0.7  # Max 70% of screen
        self.target_height = min(self.target_height, max_height)
        
        # Smooth transition to target height
        diff = self.target_height - self.height
        self.height += diff * 5 * dt  # Smooth lerp
        
        # Update wave animation
        self.wave_offset += self.wave_speed * dt
        
        # Update foam particles
        self._update_foam(dt)
        
    def _update_foam(self, dt: float) -> None:
        """Update foam particles on water surface."""
        # Add new foam particles randomly
        if self.height > 20 and random.random() < 0.3:
            self.foam_particles.append({
                'x': random.randint(0, self.screen_width),
                'y': self.screen_height - self.height,
                'size': random.randint(2, 6),
                'life': 1.0,
                'drift': random.uniform(-10, 10)
            })
        
        # Update existing particles
        new_particles = []
        for p in self.foam_particles:
            p['life'] -= dt * 0.5
            p['x'] += p['drift'] * dt
            p['y'] = self.screen_height - self.height + math.sin(self.wave_offset + p['x'] * 0.01) * 3
            
            if p['life'] > 0:
                new_particles.append(p)
        
        self.foam_particles = new_particles
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the water with wave effect.
        
        Args:
            screen: The pygame surface to draw on
        """
        if self.height <= 0:
            return
            
        water_top = self.screen_height - int(self.height)
        
        # Create water surface with alpha
        water_surf = pygame.Surface((self.screen_width, int(self.height)), pygame.SRCALPHA)
        
        # Draw gradient from deep to surface
        for y in range(int(self.height)):
            # Calculate alpha and color based on depth
            depth_ratio = y / self.height if self.height > 0 else 0
            alpha = int(150 + depth_ratio * 50)
            
            # Mix colors
            r = int(self.COLOR_SURFACE[0] * (1 - depth_ratio) + self.COLOR_DEEP[0] * depth_ratio)
            g = int(self.COLOR_SURFACE[1] * (1 - depth_ratio) + self.COLOR_DEEP[1] * depth_ratio)
            b = int(self.COLOR_SURFACE[2] * (1 - depth_ratio) + self.COLOR_DEEP[2] * depth_ratio)
            
            pygame.draw.line(water_surf, (r, g, b, alpha), (0, y), (self.screen_width, y))
        
        screen.blit(water_surf, (0, water_top))
        
        # Draw wave line at surface
        points = []
        for x in range(0, self.screen_width + 10, 10):
            wave_y = water_top + math.sin(self.wave_offset + x * 0.02) * 3
            points.append((x, wave_y))
        
        if len(points) >= 2:
            pygame.draw.lines(screen, self.COLOR_SURFACE[:3], False, points, 3)
        
        # Draw foam particles
        for p in self.foam_particles:
            alpha = int(150 * p['life'])
            size = int(p['size'] * p['life'])
            if size > 0:
                foam_surf = pygame.Surface((size, size), pygame.SRCALPHA)
                foam_surf.fill((*self.COLOR_FOAM[:3], alpha))
                screen.blit(foam_surf, (int(p['x'] - size/2), int(p['y'] - size/2)))


class RainEffect:
    """Pixelated rain animation that scales intensity with rainfall value."""
    
    # Rain color palette (light blue to white)
    RAIN_COLOR_LIGHT = (200, 220, 255)
    RAIN_COLOR_MED = (150, 180, 220)
    RAIN_COLOR_HEAVY = (120, 150, 200)
    
    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """Initialize rain effect.
        
        Args:
            screen_width: Screen width for rain bounds
            screen_height: Screen height for rain bounds
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.drops = []
        self.pixel_size = 2  # Pixelated look - align to grid
        self.time = 0.0
        
    def _calculate_intensity(self, rainfall: float) -> dict:
        """Calculate rain intensity parameters based on rainfall value.
        
        Args:
            rainfall: Current rainfall in mm (0-150)
            
        Returns:
            Dictionary with drop_count, speed_mult, length_mult, opacity
        """
        if rainfall <= 0:
            return {
                'drop_count': 0,
                'speed_mult': 0,
                'length_mult': 0,
                'opacity': 0
            }
        
        # Normalize rainfall (0-1 range, with 150mm being max)
        normalized = min(rainfall / 150.0, 1.0)
        
        # Drop count: 0 at 0mm, scales to 200 at 150mm
        drop_count = int(20 + normalized * 180)
        
        # Speed multiplier: 1.0 at low, up to 2.5 at max
        speed_mult = 1.0 + normalized * 1.5
        
        # Length multiplier: short drops at low, long streaks at high
        length_mult = 1.0 + normalized * 3.0
        
        # Opacity: 80 at low, up to 200 at max
        opacity = int(80 + normalized * 120)
        
        return {
            'drop_count': drop_count,
            'speed_mult': speed_mult,
            'length_mult': length_mult,
            'opacity': opacity
        }
    
    def _create_drop(self, intensity: dict) -> dict:
        """Create a new rain drop with random properties.
        
        Args:
            intensity: Intensity parameters from _calculate_intensity
            
        Returns:
            Dictionary representing a rain drop
        """
        # Snap to pixel grid for pixelated look
        x = random.randint(0, self.screen_width)
        x = (x // self.pixel_size) * self.pixel_size
        
        y = random.randint(-100, 0)  # Start above screen
        y = (y // self.pixel_size) * self.pixel_size
        
        # Base speed varies by drop (some fall faster than others)
        base_speed = random.uniform(8, 15)
        speed = base_speed * intensity['speed_mult']
        
        # Drop length scales with intensity
        base_length = random.randint(2, 4)
        length = int(base_length * intensity['length_mult'])
        length = (length // self.pixel_size) * self.pixel_size  # Pixel align
        
        # Add some horizontal wind drift for variety
        drift = random.uniform(-0.5, 0.5)
        
        return {
            'x': x,
            'y': y,
            'speed': speed,
            'length': length,
            'drift': drift
        }
    
    def update(self, rainfall: float, dt: float) -> None:
        """Update rain animation state.
        
        Args:
            rainfall: Current rainfall in mm (0-150)
            dt: Delta time in seconds
        """
        self.time += dt
        
        intensity = self._calculate_intensity(rainfall)
        
        # If no rain, clear drops
        if intensity['drop_count'] == 0:
            self.drops = []
            return
        
        # Update existing drops
        new_drops = []
        for drop in self.drops:
            # Move drop down
            drop['y'] += drop['speed']
            drop['x'] += drop['drift'] * dt * 60  # Scale drift by framerate
            
            # Keep drops within bounds (wrap horizontal, remove if below screen)
            if drop['x'] < 0:
                drop['x'] = self.screen_width
            elif drop['x'] > self.screen_width:
                drop['x'] = 0
            
            # Keep drops that are still on screen
            if drop['y'] < self.screen_height + drop['length']:
                new_drops.append(drop)
        
        self.drops = new_drops
        
        # Add new drops to maintain target count
        drops_needed = intensity['drop_count'] - len(self.drops)
        for _ in range(max(0, drops_needed)):
            self.drops.append(self._create_drop(intensity))
    
    def draw(self, screen: pygame.Surface, rainfall: float) -> None:
        """Draw rain effect with pixelated style.
        
        Args:
            screen: The pygame surface to draw on
            rainfall: Current rainfall in mm (0-150)
        """
        if rainfall <= 0 or not self.drops:
            return
        
        intensity = self._calculate_intensity(rainfall)
        opacity = intensity['opacity']
        
        # Choose color based on intensity
        if intensity['drop_count'] < 60:
            color = self.RAIN_COLOR_LIGHT
        elif intensity['drop_count'] < 140:
            color = self.RAIN_COLOR_MED
        else:
            color = self.RAIN_COLOR_HEAVY
        
        # Draw each drop as pixelated rectangle
        for drop in self.drops:
            # Snap to pixel grid
            x = (int(drop['x']) // self.pixel_size) * self.pixel_size
            y = (int(drop['y']) // self.pixel_size) * self.pixel_size
            
            # Draw drop as vertical line of pixels
            for i in range(0, drop['length'], self.pixel_size):
                # Fade top and bottom of drop
                if i == 0 or i == drop['length'] - self.pixel_size:
                    alpha = int(opacity * 0.5)
                else:
                    alpha = opacity
                
                # Create small surface for alpha
                drop_pixel = pygame.Surface((self.pixel_size, self.pixel_size), pygame.SRCALPHA)
                drop_pixel.fill((*color, alpha))
                screen.blit(drop_pixel, (x, y + i))


class WaterRiseEffect:
    """Pixelated water rise effect for basement carpark flooding.
    
    Shows water rising from the bottom of the screen when rainfall exceeds
    severe levels (100mm+), simulating a basement flood scenario.
    """
    
    # Water color palette for pixelated look
    COLOR_DARK = (30, 60, 100)      # Deep water (bottom)
    COLOR_MID = (60, 100, 150)      # Mid water
    COLOR_LIGHT = (90, 140, 190)    # Surface water
    COLOR_FOAM = (180, 200, 220)    # Foam/ripples
    
    # Activation threshold (severe rainfall level)
    ACTIVATION_THRESHOLD = 100  # mm
    
    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """Initialize water rise effect.
        
        Args:
            screen_width: Screen width for water bounds
            screen_height: Screen height for water bounds
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.pixel_size = 4  # Larger pixels for retro look
        self.water_height = 0  # Current water height in pixels
        self.target_height = 0
        self.wave_time = 0.0
        self.ripples = []  # Surface ripple particles
        self.bubbles = []  # Underwater bubbles
        
    def _calculate_water_height(self, rainfall: float) -> float:
        """Calculate target water height based on rainfall.
        
        Water only appears after 100mm (severe level).
        Height increases gradually from 100mm to 150mm.
        
        Args:
            rainfall: Current rainfall in mm (0-150)
            
        Returns:
            Target water height in pixels
        """
        if rainfall <= self.ACTIVATION_THRESHOLD:
            return 0
        
        # Calculate excess above threshold
        excess = rainfall - self.ACTIVATION_THRESHOLD
        max_excess = 150 - self.ACTIVATION_THRESHOLD  # 50mm range
        
        # Normalize (0-1) and scale to max height
        ratio = min(excess / max_excess, 1.0)
        
        # Max height: 40% of screen (realistic basement flooding, not extreme)
        max_height = self.screen_height * 0.40
        
        return ratio * max_height
    
    def update(self, rainfall: float, dt: float) -> None:
        """Update water rise animation.
        
        Args:
            rainfall: Current rainfall in mm (0-150)
            dt: Delta time in seconds
        """
        self.wave_time += dt * 2
        
        # Calculate target height
        self.target_height = self._calculate_water_height(rainfall)
        
        # Smooth transition to target
        diff = self.target_height - self.water_height
        self.water_height += diff * 3 * dt  # Smooth lerp
        
        # Update ripples on surface
        self._update_ripples(dt)
        
        # Update bubbles underwater
        self._update_bubbles(dt)
        
    def _update_ripples(self, dt: float) -> None:
        """Update surface ripple particles."""
        # Add new ripples randomly when water is visible
        if self.water_height > 10 and random.random() < 0.2:
            self.ripples.append({
                'x': random.randint(0, self.screen_width),
                'y': self.screen_height - self.water_height,
                'width': random.randint(8, 20),
                'life': 1.0,
                'max_life': random.uniform(0.8, 1.5)
            })
        
        # Update existing ripples
        new_ripples = []
        water_surface_y = self.screen_height - self.water_height
        
        for r in self.ripples:
            r['life'] -= dt
            # Ripple floats slightly
            r['x'] += random.uniform(-5, 5) * dt
            r['y'] = water_surface_y + math.sin(self.wave_time + r['x'] * 0.05) * 2
            
            if r['life'] > 0:
                new_ripples.append(r)
        
        self.ripples = new_ripples
    
    def _update_bubbles(self, dt: float) -> None:
        """Update underwater bubble particles."""
        # Add bubbles when water is deep enough
        if self.water_height > 30 and random.random() < 0.1:
            self.bubbles.append({
                'x': random.randint(0, self.screen_width),
                'y': self.screen_height - random.randint(0, int(self.water_height * 0.8)),
                'size': random.randint(2, 5),
                'speed': random.uniform(10, 25),
                'life': 1.0
            })
        
        # Update bubbles
        new_bubbles = []
        water_surface_y = self.screen_height - self.water_height
        
        for b in self.bubbles:
            # Bubbles rise
            b['y'] -= b['speed'] * dt
            b['x'] += math.sin(self.wave_time * 2 + b['y'] * 0.05) * 0.5
            b['life'] -= dt * 0.3
            
            # Keep bubbles that are below surface and alive
            if b['y'] > water_surface_y and b['life'] > 0:
                new_bubbles.append(b)
        
        self.bubbles = new_bubbles
    
    def draw(self, screen: pygame.Surface, rainfall: float) -> None:
        """Draw pixelated water rise effect.
        
        Args:
            screen: The pygame surface to draw on
            rainfall: Current rainfall in mm (0-150)
        """
        if self.water_height <= 0:
            return
        
        water_top = int(self.screen_height - self.water_height)
        water_height_int = int(self.water_height)
        
        # Draw pixelated water column with gradient
        for y in range(water_top, self.screen_height, self.pixel_size):
            # Calculate depth ratio for color
            depth = (y - water_top) / self.water_height if self.water_height > 0 else 0
            
            # Choose color based on depth
            if depth < 0.3:
                color = self.COLOR_LIGHT
            elif depth < 0.7:
                color = self.COLOR_MID
            else:
                color = self.COLOR_DARK
            
            # Draw horizontal pixel strip
            for x in range(0, self.screen_width, self.pixel_size):
                # Add wave offset to surface
                wave_y = 0
                if y < water_top + self.pixel_size * 2:
                    wave_y = int(math.sin(self.wave_time + x * 0.02) * self.pixel_size)
                
                # Snap to grid
                draw_y = y + wave_y
                draw_y = (draw_y // self.pixel_size) * self.pixel_size
                
                # Draw pixel
                pygame.draw.rect(screen, color, (x, draw_y, self.pixel_size, self.pixel_size))
        
        # Draw ripples on surface
        for r in self.ripples:
            alpha = int(200 * (r['life'] / r['max_life']))
            ripple_surf = pygame.Surface((r['width'], self.pixel_size), pygame.SRCALPHA)
            ripple_surf.fill((*self.COLOR_FOAM, alpha))
            screen.blit(ripple_surf, (int(r['x'] - r['width']/2), int(r['y'])))
        
        # Draw bubbles
        for b in self.bubbles:
            alpha = int(150 * b['life'])
            bubble_surf = pygame.Surface((b['size'], b['size']), pygame.SRCALPHA)
            bubble_surf.fill((*self.COLOR_FOAM, alpha))
            screen.blit(bubble_surf, (int(b['x']), int(b['y'])))
