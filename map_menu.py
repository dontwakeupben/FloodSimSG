"""Interactive map menu for Singapore Flood Simulation.

Displays a pixel-art stylized Singapore-shaped map with clickable zones for each district.
Players can hover over areas to see names and click to enter levels.

Uses an 8x8 pixel grid for authentic retro pixel art aesthetic.
"""
import pygame
import math
from typing import List, Callable, Optional, Tuple
from entities import RainEffect


class PixelGrid:
    """8x8 pixel grid system for snapping positions and sizes."""
    
    GRID_SIZE = 8
    
    @classmethod
    def snap(cls, value: int) -> int:
        """Snap a value to the nearest grid position."""
        return (value // cls.GRID_SIZE) * cls.GRID_SIZE
    
    @classmethod
    def snap_rect(cls, rect: pygame.Rect) -> pygame.Rect:
        """Snap a rectangle to the pixel grid."""
        return pygame.Rect(
            cls.snap(rect.x),
            cls.snap(rect.y),
            cls.snap(rect.width) if rect.width >= cls.GRID_SIZE else cls.GRID_SIZE,
            cls.snap(rect.height) if rect.height >= cls.GRID_SIZE else cls.GRID_SIZE
        )


class PixelPalette:
    """Limited color palette for retro pixel art aesthetic."""
    
    # Land colors
    LAND_LIGHT = (140, 180, 110)
    LAND_MID = (110, 150, 80)
    LAND_DARK = (80, 120, 50)
    LAND_BORDER = (50, 80, 40)
    
    # Water colors
    WATER_LIGHT = (100, 150, 200)
    WATER_MID = (70, 110, 160)
    WATER_DARK = (50, 80, 120)
    
    # Zone state colors
    SAFE_BASE = (100, 160, 100)
    SAFE_HOVER = (130, 200, 130)
    MODERATE_BASE = (180, 160, 80)
    MODERATE_HOVER = (220, 200, 100)
    DANGER_BASE = (160, 100, 90)
    DANGER_HOVER = (200, 130, 120)
    
    # UI colors
    TEXT_WHITE = (248, 248, 248)
    TEXT_SHADOW = (40, 40, 50)
    PANEL_BG = (30, 35, 45)
    BORDER = (120, 130, 140)
    HIGHLIGHT = (255, 220, 120)


class PixelDraw:
    """Pixel-art drawing utilities."""
    
    @staticmethod
    def draw_pixel_border(screen: pygame.Surface, rect: pygame.Rect,
                         color: Tuple[int, int, int], thickness: int = 2) -> None:
        """Draw a chunky pixel-art style border."""
        # Draw outer border with 3D effect
        # Shadow (bottom-right)
        pygame.draw.rect(screen, (0, 0, 0, 100),
                        rect.move(4, 4), thickness)
        # Highlight (top-left)
        pygame.draw.rect(screen,
                        (min(255, color[0] + 60),
                         min(255, color[1] + 60),
                         min(255, color[2] + 60)),
                        rect, thickness)
        # Main border
        pygame.draw.rect(screen, color, rect, thickness)
    
    @staticmethod
    def draw_dithered_rect(screen: pygame.Surface, rect: pygame.Rect,
                          color1: Tuple[int, int, int],
                          color2: Tuple[int, int, int],
                          pattern: str = 'checker') -> None:
        """Draw a rectangle with dithered pattern for texture."""
        # Draw base color
        pygame.draw.rect(screen, color1, rect)
        
        # Add dither pattern
        if pattern == 'checker':
            for y in range(rect.top, rect.bottom, PixelGrid.GRID_SIZE):
                for x in range(rect.left, rect.right, PixelGrid.GRID_SIZE):
                    if ((x // PixelGrid.GRID_SIZE + y // PixelGrid.GRID_SIZE) % 2 == 0):
                        pixel_rect = pygame.Rect(x, y, PixelGrid.GRID_SIZE, PixelGrid.GRID_SIZE)
                        pixel_rect = pixel_rect.clip(rect)
                        if pixel_rect.width > 0 and pixel_rect.height > 0:
                            pygame.draw.rect(screen, color2, pixel_rect)
        elif pattern == 'diagonal':
            for y in range(rect.top, rect.bottom, PixelGrid.GRID_SIZE):
                for x in range(rect.left, rect.right, PixelGrid.GRID_SIZE):
                    if ((x - rect.left + y - rect.top) // PixelGrid.GRID_SIZE) % 2 == 0:
                        pixel_rect = pygame.Rect(x, y, PixelGrid.GRID_SIZE, PixelGrid.GRID_SIZE)
                        pixel_rect = pixel_rect.clip(rect)
                        if pixel_rect.width > 0 and pixel_rect.height > 0:
                            pygame.draw.rect(screen, color2, pixel_rect)
    
    @staticmethod
    def draw_pixel_text(screen: pygame.Surface, font: pygame.font.Font,
                       text: str, pos: Tuple[int, int],
                       color: Tuple[int, int, int] = PixelPalette.TEXT_WHITE,
                       shadow: bool = True) -> pygame.Rect:
        """Draw text with pixel-art shadow effect."""
        x, y = pos
        
        if shadow:
            # Draw shadow
            shadow_surf = font.render(text, False, PixelPalette.TEXT_SHADOW)
            screen.blit(shadow_surf, (x + 2, y + 2))
        
        # Draw main text (no anti-aliasing for pixel look)
        text_surf = font.render(text, False, color)
        screen.blit(text_surf, (x, y))
        
        return text_surf.get_rect(topleft=pos)


class Zone:
    """Interactive zone on the map representing a district/area."""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 name: str, level_id: str, description: str = "",
                 zone_type: str = "safe"):
        """Initialize a map zone.
        
        Args:
            x, y: Top-left position of the zone (will snap to pixel grid)
            width, height: Dimensions of the zone (will snap to pixel grid)
            name: Display name (e.g., "Orchard Road")
            level_id: Level identifier (e.g., "orchard")
            description: Optional tooltip description
            zone_type: "safe", "moderate", or "danger" for color scheme
        """
        # Snap to pixel grid
        self.rect = pygame.Rect(
            PixelGrid.snap(x),
            PixelGrid.snap(y),
            max(PixelGrid.GRID_SIZE * 4, PixelGrid.snap(width)),
            max(PixelGrid.GRID_SIZE * 3, PixelGrid.snap(height))
        )
        self.name = name
        self.level_id = level_id
        self.description = description or f"Explore {name}"
        self.zone_type = zone_type
        
        # Set colors based on zone type
        self._set_colors_by_type()
        
        self.text_color = PixelPalette.TEXT_WHITE
        self.is_hovered = False
        self.pulse_offset = 0.0
        self.dither_offset = 0
        
    def _set_colors_by_type(self) -> None:
        """Set color scheme based on zone type."""
        if self.zone_type == "safe":
            self.base_color = PixelPalette.SAFE_BASE
            self.hover_color = PixelPalette.SAFE_HOVER
            self.border_color = (60, 110, 60)
            self.dither_color = (80, 130, 80)
        elif self.zone_type == "moderate":
            self.base_color = PixelPalette.MODERATE_BASE
            self.hover_color = PixelPalette.MODERATE_HOVER
            self.border_color = (120, 100, 50)
            self.dither_color = (150, 130, 60)
        else:  # danger
            self.base_color = PixelPalette.DANGER_BASE
            self.hover_color = PixelPalette.DANGER_HOVER
            self.border_color = (110, 60, 50)
            self.dither_color = (130, 70, 60)
        
    def update(self, dt: float) -> None:
        """Update zone animation."""
        self.pulse_offset += dt * 3
        if self.pulse_offset > 6.28:  # 2 * pi
            self.pulse_offset = 0
            
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle mouse events for this zone.
        
        Args:
            event: Pygame event
            
        Returns:
            True if zone was clicked
        """
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                return True
        return False
        
    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the zone with pixel-art style.
        
        Args:
            screen: Surface to draw on
            font: Font for text rendering
        """
        # Determine color based on hover state
        color = self.hover_color if self.is_hovered else self.base_color
        
        # Add subtle pulse effect when hovered
        if self.is_hovered:
            pulse = abs(math.sin(self.pulse_offset)) * 20
            color = (
                min(255, int(color[0] + pulse)),
                min(255, int(color[1] + pulse)),
                min(255, int(color[2] + pulse))
            )
        
        # Draw zone with dithered pattern
        PixelDraw.draw_dithered_rect(screen, self.rect, color,
                                     self.dither_color, 'checker')
        
        # Draw pixel-art border with 3D effect
        border_thickness = PixelGrid.GRID_SIZE // 2
        
        # Outer shadow
        shadow_rect = self.rect.move(2, 2)
        pygame.draw.rect(screen, (20, 25, 30), shadow_rect, border_thickness)
        
        # Highlight (top-left)
        highlight_color = (
            min(255, color[0] + 50),
            min(255, color[1] + 50),
            min(255, color[2] + 50)
        )
        pygame.draw.rect(screen, highlight_color,
                        self.rect.inflate(-border_thickness, -border_thickness),
                        border_thickness)
        
        # Main border
        pygame.draw.rect(screen, self.border_color, self.rect, border_thickness)
        
        # Draw zone name with pixel-art shadow
        text_rect = font.render(self.name, False, self.text_color).get_rect(center=self.rect.center)
        PixelDraw.draw_pixel_text(screen, font, self.name,
                                 (text_rect.x, text_rect.y),
                                 self.text_color)


class Tooltip:
    """Tooltip that appears when hovering over zones."""
    
    def __init__(self):
        """Initialize tooltip."""
        self.text = ""
        self.visible = False
        self.position = (0, 0)
        self.padding = 8
        self.bg_color = (40, 40, 50, 230)
        self.border_color = (150, 150, 160)
        self.text_color = (255, 255, 255)
        
    def show(self, text: str, position: Tuple[int, int]) -> None:
        """Show tooltip with given text at position.
        
        Args:
            text: Tooltip text
            position: (x, y) screen position
        """
        self.text = text
        self.position = position
        self.visible = True
        
    def hide(self) -> None:
        """Hide the tooltip."""
        self.visible = False
        
    def draw(self, screen: pygame.Surface, font: pygame.font.Font) -> None:
        """Draw the tooltip if visible.
        
        Args:
            screen: Surface to draw on
            font: Font for text rendering
        """
        if not self.visible or not self.text:
            return
            
        # Render text
        text_surface = font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        
        # Calculate tooltip background
        bg_rect = pygame.Rect(
            self.position[0],
            self.position[1] - text_rect.height - self.padding * 2 - 5,
            text_rect.width + self.padding * 2,
            text_rect.height + self.padding * 2
        )
        
        # Keep tooltip on screen
        if bg_rect.left < 0:
            bg_rect.left = 5
        if bg_rect.right > screen.get_width():
            bg_rect.right = screen.get_width() - 5
        if bg_rect.top < 0:
            bg_rect.top = self.position[1] + 15
            
        # Draw background
        pygame.draw.rect(screen, self.bg_color[:3], bg_rect)
        pygame.draw.rect(screen, self.border_color, bg_rect, 2)
        
        # Draw text
        text_pos = (bg_rect.x + self.padding, bg_rect.y + self.padding)
        screen.blit(text_surface, text_pos)


class MapMenu:
    """Interactive pixel-art map menu showing Singapore with clickable zones."""
    
    def __init__(self, screen_width: int, screen_height: int):
        """Initialize the map menu.
        
        Args:
            screen_width: Screen width in pixels
            screen_height: Screen height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Pixel fonts - use smaller sizes for pixel look
        self.title_font = pygame.font.Font(None, 40)
        self.zone_font = pygame.font.Font(None, 24)
        self.tooltip_font = pygame.font.Font(None, 20)
        self.instruction_font = pygame.font.Font(None, 28)
        
        # Colors from pixel palette
        self.water_color = PixelPalette.WATER_MID
        self.land_color = PixelPalette.LAND_MID
        self.land_border_color = PixelPalette.LAND_BORDER
        self.title_color = PixelPalette.TEXT_WHITE
        
        # Scanline overlay for retro effect
        self.scanline_surface = None
        self._create_scanlines()
        
        # Initialize rain effect for background atmosphere
        self.rain = RainEffect(screen_width, screen_height)
        
        # Create zones
        self.zones: List[Zone] = []
        self._create_zones()
        
        # Tooltip
        self.tooltip = Tooltip()
        
        # Callback for zone selection
        self.on_zone_selected: Optional[Callable[[str], None]] = None
        
        # Singapore outline points (pixelated)
        self._create_pixelated_singapore_outline()
        
        # Load pixelated Singapore map image (replaces green polygon)
        self.background_image = None
        self._load_background_image()
        
    def _create_scanlines(self) -> None:
        """Create scanline overlay for retro CRT effect."""
        self.scanline_surface = pygame.Surface(
            (self.screen_width, self.screen_height), pygame.SRCALPHA
        )
        # Draw horizontal scanlines
        for y in range(0, self.screen_height, 4):
            pygame.draw.line(self.scanline_surface, (0, 0, 0, 30),
                           (0, y), (self.screen_width, y), 1)
        
    def _create_pixelated_singapore_outline(self) -> None:
        """Create a pixel-grid aligned Singapore landmass outline."""
        # Center the map
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Singapore-like shape snapped to pixel grid
        # Creating a more pixelated, blocky silhouette
        raw_points = [
            (0, -24),      # North (Top)
            (8, -16),      # Northeast
            (20, -8),      # East upper
            (24, 4),       # East lower
            (16, 16),      # Southeast
            (4, 24),       # South
            (-8, 20),      # Southwest
            (-16, 8),      # West lower
            (-24, 0),      # West middle
            (-20, -12),    # West upper
            (-12, -20),    # Northwest
        ]
        
        # Convert to pixel coordinates and snap to grid
        scale = PixelGrid.GRID_SIZE
        self.singapore_points = []
        for dx, dy in raw_points:
            px = center_x + dx * scale
            py = center_y + dy * scale
            self.singapore_points.append((PixelGrid.snap(px), PixelGrid.snap(py)))
        
        # Create inner highlight points
        self.inner_land_points = []
        for x, y in self.singapore_points:
            # Offset toward center
            inner_x = x + (center_x - x) // 8
            inner_y = y + (center_y - y) // 8
            self.inner_land_points.append((inner_x, inner_y))
    
    def _load_background_image(self) -> None:
        """Load the pixelated Singapore map image.
        
        Loads the image and centers it on screen.
        Falls back to None if image cannot be loaded.
        """
        try:
            import os
            # Try multiple possible paths
            possible_paths = [
                "assets/singapore-map.png",
                "flood_sim/assets/singapore-map.png",
                os.path.join(os.path.dirname(__file__), "assets", "singapore-map.png"),
            ]
            
            image_path = None
            for path in possible_paths:
                if os.path.exists(path):
                    image_path = path
                    break
            
            if image_path:
                raw_image = pygame.image.load(image_path).convert_alpha()
                # Scale to fit game area (800x600)
                self.background_image = pygame.transform.scale(raw_image,
                                                               (self.screen_width, self.screen_height))
                print(f"Loaded Singapore map: {image_path}")
            else:
                print("Singapore map image not found, using fallback polygon rendering")
                self.background_image = None
        except Exception as e:
            print(f"Warning: Could not load Singapore map image: {e}")
            self.background_image = None
    
    def _create_zones(self) -> None:
        """Create the clickable zones for each district (pixel-grid aligned)."""
        center_x = self.screen_width // 2
        center_y = self.screen_height // 2
        
        # Tanglin Carpark - Top left area (high risk - red)
        tanglin = Zone(
            x=center_x - 144,
            y=center_y - 60,
            width=112,
            height=80,
            name="Orchard",
            level_id="ion",
            description="Orchard Area",
            zone_type="safe"
        )
        self.zones.append(tanglin)
        
    
        
    def set_callback(self, callback: Callable[[str], None]) -> None:
        """Set the callback for zone selection.
        
        Args:
            callback: Function to call with level_id when zone is clicked
        """
        self.on_zone_selected = callback
        
    def update(self, dt: float) -> None:
        """Update map menu animations.
        
        Args:
            dt: Delta time in seconds
        """
        # Update rain with light background rainfall
        self.rain.update(rainfall=15.0, dt=dt)
        
        # Update zones
        for zone in self.zones:
            zone.update(dt)
            
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events.
        
        Args:
            event: Pygame event
            
        Returns:
            True if a zone was selected
        """
        # Handle zone events
        hovered_zone = None
        for zone in self.zones:
            if zone.handle_event(event):
                # Zone was clicked
                if self.on_zone_selected:
                    self.on_zone_selected(zone.level_id)
                return True
            if zone.is_hovered:
                hovered_zone = zone
                
        # Update tooltip
        if hovered_zone:
            mouse_pos = pygame.mouse.get_pos()
            self.tooltip.show(hovered_zone.description, mouse_pos)
        else:
            self.tooltip.hide()
            
        return False
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the pixel-art map menu.
        
        Args:
            screen: Surface to draw on
        """
        # Fill water background
        screen.fill(self.water_color)
        
        # Draw rain effect
        self.rain.draw(screen, rainfall=15.0)
        
        # Draw Singapore landmass - either image or fallback polygon
        if self.background_image:
            # Draw the pixelated Singapore map image (centered)
            screen.blit(self.background_image, (0, 0))
        else:
            # Fallback: Draw polygon if image not available
            if len(self.singapore_points) >= 3:
                # Draw main land shape
                pygame.draw.polygon(screen, self.land_color, self.singapore_points)
                
                # Add texture with inner highlight
                if hasattr(self, 'inner_land_points'):
                    pygame.draw.polygon(screen, PixelPalette.LAND_LIGHT,
                                      self.inner_land_points,
                                      PixelGrid.GRID_SIZE // 2)
                
                # Draw pixelated border
                border_thickness = PixelGrid.GRID_SIZE // 2
                pygame.draw.polygon(screen, self.land_border_color,
                                  self.singapore_points, border_thickness)
                
                # Add coastal dithering (checkerboard pattern at edges)
                for i, (x, y) in enumerate(self.singapore_points):
                    next_point = self.singapore_points[(i + 1) % len(self.singapore_points)]
                    # Draw small pixel blocks along edges for detail
                    mid_x = (x + next_point[0]) // 2
                    mid_y = (y + next_point[1]) // 2
                    pygame.draw.rect(screen, PixelPalette.LAND_DARK,
                                   (mid_x - 2, mid_y - 2, 4, 4))
        
        # Draw pixel-art roads between zones
        road_color = (140, 130, 100)
        road_border = (100, 90, 70)
        for i, zone1 in enumerate(self.zones):
            for zone2 in self.zones[i+1:]:
                # Draw road with border for 3D effect
                start = zone1.rect.center
                end = zone2.rect.center
                # Road border (shadow)
                pygame.draw.line(screen, road_border,
                               (start[0]+2, start[1]+2),
                               (end[0]+2, end[1]+2), 6)
                # Road surface
                pygame.draw.line(screen, road_color, start, end, 4)
                # Road highlight
                pygame.draw.line(screen, (180, 170, 140),
                               (start[0]-1, start[1]-1),
                               (end[0]-1, end[1]-1), 2)
                
                # Draw pixel junction markers
                mid_x = (start[0] + end[0]) // 2
                mid_y = (start[1] + end[1]) // 2
                # Snap to grid
                mid_x = PixelGrid.snap(mid_x)
                mid_y = PixelGrid.snap(mid_y)
                pygame.draw.rect(screen, road_border,
                               (mid_x - 4, mid_y - 4, 8, 8))
                pygame.draw.rect(screen, (200, 190, 160),
                               (mid_x - 2, mid_y - 2, 4, 4))
        
        # Draw zones
        for zone in self.zones:
            zone.draw(screen, self.zone_font)
        
        # Draw title with pixel-art shadow
        title_x = self.screen_width // 2
        title_y = 48
        PixelDraw.draw_pixel_text(screen, self.title_font,
                                 "SINGAPORE FLOOD SIM",
                                 (title_x - self.title_font.size("SINGAPORE FLOOD SIM")[0] // 2,
                                  title_y),
                                 PixelPalette.HIGHLIGHT)
        
        # Draw instruction text
        instruction_text = "CLICK AN AREA TO EXPLORE"
        inst_width = self.instruction_font.size(instruction_text)[0]
        PixelDraw.draw_pixel_text(screen, self.instruction_font, instruction_text,
                                 ((self.screen_width - inst_width) // 2,
                                  self.screen_height - 48),
                                 (200, 200, 200))
        
        # Draw pixel-art legend
        self._draw_pixel_legend(screen)
        
        # Draw tooltip last (on top)
        self.tooltip.draw(screen, self.tooltip_font)
        
        # Apply scanline overlay for retro effect
        if self.scanline_surface:
            screen.blit(self.scanline_surface, (0, 0))
        
    def _draw_pixel_legend(self, screen: pygame.Surface) -> None:
        """Draw pixel-art style risk level legend.
        
        Args:
            screen: Surface to draw on
        """
        legend_x = PixelGrid.snap(16)
        legend_y = PixelGrid.snap(self.screen_height - 120)
        legend_width = PixelGrid.snap(160)
        legend_height = PixelGrid.snap(88)
        
        # Legend background panel with pixel border
        legend_rect = pygame.Rect(legend_x, legend_y, legend_width, legend_height)
        
        # Panel shadow
        pygame.draw.rect(screen, (20, 25, 30),
                        legend_rect.move(4, 4))
        # Panel background
        pygame.draw.rect(screen, PixelPalette.PANEL_BG, legend_rect)
        # Panel border (pixel style)
        pygame.draw.rect(screen, PixelPalette.BORDER, legend_rect,
                        PixelGrid.GRID_SIZE // 2)
        # Panel highlight
        pygame.draw.rect(screen,
                        (min(255, PixelPalette.PANEL_BG[0] + 30),
                         min(255, PixelPalette.PANEL_BG[1] + 30),
                         min(255, PixelPalette.PANEL_BG[2] + 30)),
                        legend_rect.inflate(-4, -4), 2)
        
        # Legend items using pixel palette
        items = [
            ("SAFE", PixelPalette.SAFE_BASE),
            ("MODERATE", PixelPalette.MODERATE_BASE),
            ("HIGH RISK", PixelPalette.DANGER_BASE),
        ]
        
        for i, (label, color) in enumerate(items):
            y_pos = legend_y + 12 + i * 24
            # Icon background
            icon_rect = pygame.Rect(legend_x + 12, y_pos, 16, 16)
            pygame.draw.rect(screen, color, icon_rect)
            pygame.draw.rect(screen, (40, 40, 40), icon_rect, 1)
            # Dither pattern on icon
            PixelDraw.draw_dithered_rect(screen, icon_rect, color,
                                        (min(255, color[0] + 20),
                                         min(255, color[1] + 20),
                                         min(255, color[2] + 20)),
                                        'checker')
            # Label
            PixelDraw.draw_pixel_text(screen, self.tooltip_font, label,
                                     (legend_x + 36, y_pos - 2),
                                     (220, 220, 220), shadow=False)
