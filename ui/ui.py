"""UI components: Slider, panels, and interface elements."""
import pygame
from typing import Callable, Optional


class Slider:
    """Interactive slider for controlling rainfall (0-150mm)."""
    
    def __init__(self, x: int, y: int, width: int, height: int,
                 min_val: float = 0, max_val: float = 150):
        """Initialize slider.
        
        Args:
            x, y: Position on screen
            width, height: Dimensions
            min_val, max_val: Value range (default 0-150mm)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = min_val
        self.dragging = False
        self.handle_radius = height // 2 + 5
        self.disabled = False
        
    def set_disabled(self, disabled: bool) -> None:
        """Set whether the slider is disabled (greyed out, unmovable).
        
        Args:
            disabled: True to disable the slider, False to enable
        """
        self.disabled = disabled
        if disabled:
            self.dragging = False
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process mouse events for slider interaction.
        
        Args:
            event: Pygame event
            
        Returns:
            True if value changed
        """
        # Ignore all events if disabled
        if self.disabled:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._update_value(event.pos[0])
                return True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._update_value(event.pos[0])
            return True
        return False
        
    def _update_value(self, mouse_x: int) -> None:
        """Update slider value based on mouse position."""
        # Calculate position within slider track
        relative_x = max(0, min(mouse_x - self.rect.x, self.rect.width))
        ratio = relative_x / self.rect.width
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the slider with pixelated style.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Choose colors based on disabled state
        if self.disabled:
            track_bg = (160, 160, 160)  # Darker grey track
            track_border = (100, 100, 100)  # Grey border
            fill_color = (140, 140, 140)  # Grey fill
            fill_border = (100, 100, 100)  # Grey fill border
            handle_base = (120, 120, 120)  # Grey handle
            handle_highlight = (160, 160, 160)  # Light grey highlight
            handle_shadow = (80, 80, 80)  # Dark grey shadow
            handle_border = (60, 60, 60)  # Dark grey border
        else:
            track_bg = (180, 180, 180)
            track_border = (120, 120, 120)
            fill_color = (80, 130, 200)
            fill_border = (40, 90, 160)
            handle_base = (60, 110, 180)
            handle_highlight = (100, 150, 220)
            handle_shadow = (30, 70, 130)
            handle_border = (30, 60, 120)
        
        # Pixelated track background (no border_radius for sharp edges)
        pygame.draw.rect(screen, track_bg, self.rect)
        pygame.draw.rect(screen, track_border, self.rect, 2)
        
        # Draw filled portion (pixelated gradient effect)
        fill_width = int((self.value / self.max_val) * self.rect.width)
        fill_rect = pygame.Rect(self.rect.x, self.rect.y, fill_width, self.rect.height)
        
        # Create pixelated fill pattern
        for x in range(fill_rect.x, fill_rect.x + fill_width, 4):
            pygame.draw.rect(screen, fill_color, (x, fill_rect.y, 4, fill_rect.height))
        # Draw darker border on fill
        if fill_width > 0:
            pygame.draw.rect(screen, fill_border, fill_rect, 2)
        
        # Draw pixelated square handle instead of circle
        handle_x = self.rect.x + int((self.value / self.max_val) * self.rect.width)
        handle_y = self.rect.centery
        handle_size = self.handle_radius
        handle_rect = pygame.Rect(
            handle_x - handle_size,
            handle_y - handle_size,
            handle_size * 2,
            handle_size * 2
        )
        # Draw pixelated handle with 3D bevel effect
        pygame.draw.rect(screen, handle_base, handle_rect)  # Base
        pygame.draw.rect(screen, handle_highlight, (handle_rect.x, handle_rect.y, handle_rect.width, 3))  # Top highlight
        pygame.draw.rect(screen, handle_shadow, (handle_rect.x, handle_rect.bottom - 3, handle_rect.width, 3))  # Bottom shadow
        pygame.draw.rect(screen, handle_border, handle_rect, 2)  # Border
        
        # Draw small dots on handle for grip
        pygame.draw.rect(screen, (200, 200, 200), (handle_x - 2, handle_y - 4, 4, 2))
        pygame.draw.rect(screen, (200, 200, 200), (handle_x - 2, handle_y + 2, 4, 2))
        
    def get_value(self) -> float:
        """Get current slider value."""
        return self.value
        
    def set_value(self, value: float) -> None:
        """Set slider value (clamped to range)."""
        self.value = max(self.min_val, min(self.max_val, value))


class CollapsibleRainfallPanel:
    """Top-left collapsible panel for rainfall control."""
    
    def __init__(self, x: int = 20, y: int = 20):
        """Initialize collapsible rainfall panel.
        
        Args:
            x, y: Position of the toggle button (top-left corner)
        """
        self.toggle_size = 44
        self.toggle_rect = pygame.Rect(x, y, self.toggle_size, self.toggle_size)
        self.expanded = False
        
        # Panel dimensions (when expanded)
        self.panel_width = 220
        self.panel_height = 150  # Increased height for live indicator
        self.panel_rect = pygame.Rect(x, y + self.toggle_size + 8, self.panel_width, self.panel_height)
        
        # Create slider inside the panel (positioned below checkbox)
        slider_margin = 25
        slider_width = self.panel_width - slider_margin * 2
        slider_height = 16
        slider_x = self.panel_rect.x + slider_margin
        slider_y = self.panel_rect.y + 55  # Moved down to make room for checkbox
        self.rainfall_slider = Slider(slider_x, slider_y, slider_width, slider_height, 0, 150)
        
        # Fonts
        self.font = pygame.font.Font(None, 26)
        self.font_large = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 20)
        
        # Hover states
        self.toggle_hovered = False
        self.close_hovered = False
        
        # Close button rect (relative to panel)
        self.close_btn_size = 20
        self.close_btn_rect = pygame.Rect(
            self.panel_rect.right - self.close_btn_size - 10,
            self.panel_rect.y + 10,
            self.close_btn_size,
            self.close_btn_size
        )
        
        # Live data mode
        self.live_mode = False
        self.live_indicator_time = 0.0
        
        # Checkbox for live data toggle (positioned at bottom of panel)
        # Position will be calculated dynamically in _draw_live_checkbox
        self.checkbox_rect = pygame.Rect(
            self.panel_rect.x + 15,
            0,  # Will be set dynamically
            14,
            14
        )
        self.checkbox_checked = False
        self.checkbox_hovered = False
        self.live_checkbox_callback: Optional[Callable[[bool], None]] = None
        
        # Live data stats
        self.live_rainfall_value = 0.0
        self.live_station_info = ""
        self.live_last_updated = ""
        self.live_api_error = None
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process events for the panel.
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Update hover states
        self.toggle_hovered = self.toggle_rect.collidepoint(mouse_pos)
        self.close_hovered = self.close_btn_rect.collidepoint(mouse_pos) if self.expanded else False
        self.checkbox_hovered = self.checkbox_rect.collidepoint(mouse_pos) if self.expanded else False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check toggle button click
            if self.toggle_rect.collidepoint(event.pos):
                self.expanded = not self.expanded
                return True
            
            # Check close button click (only when expanded)
            if self.expanded and self.close_btn_rect.collidepoint(event.pos):
                self.expanded = False
                return True
            
            # Check checkbox click (only when expanded)
            if self.expanded and self.checkbox_rect.collidepoint(event.pos):
                self.checkbox_checked = not self.checkbox_checked
                self.live_mode = self.checkbox_checked
                # Update slider disabled state based on live mode
                self.rainfall_slider.set_disabled(self.live_mode)
                # Notify callback
                if self.live_checkbox_callback:
                    self.live_checkbox_callback(self.live_mode)
                return True
            
            # If expanded and clicking outside panel (but not on toggle), close
            if self.expanded and not self.panel_rect.collidepoint(event.pos):
                if not self.toggle_rect.collidepoint(event.pos):
                    self.expanded = False
                    return True
        
        # Pass events to slider when expanded
        if self.expanded:
            return self.rainfall_slider.handle_event(event)
        
        return False
        
    def update(self, rainfall: float) -> None:
        """Update panel with current rainfall value."""
        self.rainfall_slider.set_value(rainfall)
        
    def draw(self, screen: pygame.Surface, warning_level: str = "") -> None:
        """Draw the collapsible panel.
        
        Args:
            screen: The pygame surface to draw on
            warning_level: Current warning level for color indication
        """
        # Draw toggle button
        self._draw_toggle_button(screen)
        
        # Draw expanded panel if open
        if self.expanded:
            self._draw_expanded_panel(screen, warning_level)
            
    def _draw_toggle_button(self, screen: pygame.Surface) -> None:
        """Draw the circular toggle button with rain icon."""
        rect = self.toggle_rect
        
        # Button background with 3D effect
        if self.toggle_hovered:
            base_color = (100, 150, 220)
            highlight_color = (140, 190, 255)
            shadow_color = (60, 100, 170)
        else:
            base_color = (80, 130, 200)
            highlight_color = (120, 170, 240)
            shadow_color = (50, 90, 160)
        
        # Draw circular button using rect approximation (pixelated style)
        pygame.draw.rect(screen, base_color, rect)
        
        # 3D bevel effect
        pygame.draw.rect(screen, highlight_color, (rect.x, rect.y, rect.width, 3))
        pygame.draw.rect(screen, highlight_color, (rect.x, rect.y, 3, rect.height))
        pygame.draw.rect(screen, shadow_color, (rect.x, rect.bottom - 3, rect.width, 3))
        pygame.draw.rect(screen, shadow_color, (rect.right - 3, rect.y, 3, rect.height))
        
        # Border
        pygame.draw.rect(screen, (40, 80, 140), rect, 2)
        
        # Draw rain icon (pixelated cloud with rain)
        self._draw_rain_icon(screen, rect.centerx, rect.centery)
        
        # Draw indicator dot when collapsed but has rainfall
        if not self.expanded and self.rainfall_slider.get_value() > 0:
            dot_color = self._get_warning_color(self.rainfall_slider.get_value())
            pygame.draw.rect(screen, dot_color, (rect.right - 10, rect.y + 4, 6, 6))
        
    def _draw_rain_icon(self, screen: pygame.Surface, cx: int, cy: int) -> None:
        """Draw a pixelated rain cloud icon."""
        # Cloud body (rectangular blocks for pixelated look)
        cloud_color = (240, 240, 250)
        cloud_shadow = (180, 180, 200)
        
        # Main cloud body
        pygame.draw.rect(screen, cloud_color, (cx - 12, cy - 8, 24, 12))
        pygame.draw.rect(screen, cloud_color, (cx - 8, cy - 12, 16, 8))
        pygame.draw.rect(screen, cloud_shadow, (cx - 10, cy + 2, 20, 2))
        
        # Rain drops
        drop_color = (150, 200, 255)
        drops = [
            (cx - 6, cy + 6, 2, 4),
            (cx, cy + 8, 2, 4),
            (cx + 6, cy + 6, 2, 4),
        ]
        for drop in drops:
            pygame.draw.rect(screen, drop_color, drop)
        
    def _draw_expanded_panel(self, screen: pygame.Surface, warning_level: str) -> None:
        """Draw the expanded panel with slider and controls."""
        rect = self.panel_rect
        
        # Increase panel height for live stats when in live mode
        if self.live_mode:
            self.panel_height = 240  # Extra space for live stats with margin
        else:
            self.panel_height = 190  # Base height with checkbox at bottom
        self.panel_rect.height = self.panel_height
        
        # Panel background
        pygame.draw.rect(screen, (245, 245, 250), rect)
        
        # Panel border with 3D effect
        # Outer shadow
        pygame.draw.rect(screen, (180, 180, 190),
                        (rect.x + 2, rect.bottom - 3, rect.width, 3))
        pygame.draw.rect(screen, (180, 180, 190),
                        (rect.right - 3, rect.y + 2, 3, rect.height - 3))
        
        # Inner highlight
        pygame.draw.rect(screen, (255, 255, 255),
                        (rect.x, rect.y, rect.width, 2))
        pygame.draw.rect(screen, (255, 255, 255),
                        (rect.x, rect.y, 2, rect.height))
        
        # Dark border
        pygame.draw.rect(screen, (120, 120, 130), rect, 2)
        
        # Corner accents
        corner_size = 6
        accent_color = (80, 130, 200)
        # Top-left
        pygame.draw.rect(screen, accent_color,
                        (rect.x + 2, rect.y + 2, corner_size, 2))
        pygame.draw.rect(screen, accent_color,
                        (rect.x + 2, rect.y + 2, 2, corner_size))
        
        # Header background
        header_rect = pygame.Rect(rect.x + 4, rect.y + 4, rect.width - 8, 28)
        pygame.draw.rect(screen, (230, 235, 245), header_rect)
        
        # Draw "Rainfall" label
        label = self.font.render("Rainfall", True, (50, 50, 60))
        screen.blit(label, (rect.x + 12, rect.y + 10))
        
        # Draw close button
        self._draw_close_button(screen)
        
        # Draw slider
        self.rainfall_slider.draw(screen)
        
        # Draw value display (below slider)
        value = self.rainfall_slider.get_value()
        value_text = f"{value:.0f}mm"
        value_surf = self.font_large.render(value_text, True, (40, 80, 140))
        value_x = rect.centerx - value_surf.get_width() // 2
        screen.blit(value_surf, (value_x, rect.y + 100))
        
        # Draw warning indicator bar below value
        warning_color = self._get_warning_color(value)
        bar_rect = pygame.Rect(rect.x + 20, rect.y + 130, rect.width - 40, 8)
        pygame.draw.rect(screen, (200, 200, 210), bar_rect)
        
        # Fill bar based on value (0-150mm mapped to bar width)
        fill_width = int((value / 150.0) * (rect.width - 40))
        if fill_width > 0:
            fill_rect = pygame.Rect(rect.x + 20, rect.y + 130, fill_width, 8)
            pygame.draw.rect(screen, warning_color, fill_rect)
        
        pygame.draw.rect(screen, (150, 150, 160), bar_rect, 1)
        
        # Draw live data checkbox below warning bar
        self._draw_live_checkbox(screen)
        
        # Draw live data stats below checkbox (if in live mode)
        if self.live_mode:
            self._draw_live_stats(screen)
    
    def _draw_live_checkbox(self, screen: pygame.Surface) -> None:
        """Draw the live data checkbox with label."""
        # Calculate checkbox position below warning bar
        rect = self.panel_rect
        cb_x = rect.x + 15
        cb_y = rect.y + 145  # Just below warning bar
        
        # Update the stored rect for hit testing
        self.checkbox_rect.x = cb_x
        self.checkbox_rect.y = cb_y
        
        # Draw checkbox background (white with border)
        if self.checkbox_hovered:
            border_color = (80, 130, 200)
            bg_color = (230, 240, 255)
        else:
            border_color = (100, 100, 110)
            bg_color = (255, 255, 255)
        
        pygame.draw.rect(screen, bg_color, self.checkbox_rect)
        pygame.draw.rect(screen, border_color, self.checkbox_rect, 2)
        
        # Draw red square if checked
        if self.checkbox_checked:
            # Draw filled red square inside checkbox
            red_square_padding = 3
            red_square_rect = pygame.Rect(
                cb_x + red_square_padding,
                cb_y + red_square_padding,
                self.checkbox_rect.width - red_square_padding * 2,
                self.checkbox_rect.height - red_square_padding * 2
            )
            pygame.draw.rect(screen, (200, 50, 50), red_square_rect)
        
        # Draw label next to checkbox
        label_text = "Use Live Data"
        label_surf = self.font_small.render(label_text, True, (50, 50, 60))
        screen.blit(label_surf, (cb_x + 20, cb_y + 1))
    
    def _draw_live_stats(self, screen: pygame.Surface) -> None:
        """Draw live rainfall statistics in the panel."""
        rect = self.panel_rect
        stats_y = rect.y + 165  # Below checkbox
        
        # Draw live indicator with pulsing effect
        pulse_color = (80, 180, 80)
        pygame.draw.rect(screen, pulse_color, (rect.x + 15, stats_y, 8, 8))
        
        # "LIVE" label
        live_label = self.font_small.render("LIVE", True, (60, 140, 60))
        screen.blit(live_label, (rect.x + 28, stats_y))
        
        # Current rainfall value
        value_text = f"{self.live_rainfall_value:.1f}mm"
        value_surf = self.font.render(value_text, True, (40, 80, 140))
        screen.blit(value_surf, (rect.x + 70, stats_y - 2))
        
        # Station info (if available) - truncate if too long
        stats_y += 18
        if self.live_station_info:
            # Truncate station info to fit panel width
            max_width = self.panel_width - 30
            station_text = self.live_station_info
            station_surf = self.font_small.render(station_text, True, (100, 100, 110))
            # Truncate if too wide
            while station_surf.get_width() > max_width and len(station_text) > 3:
                station_text = station_text[:-4] + "..."
                station_surf = self.font_small.render(station_text, True, (100, 100, 110))
            screen.blit(station_surf, (rect.x + 15, stats_y))
        
        # Last updated time
        stats_y += 16
        if self.live_last_updated:
            updated_text = f"Updated: {self.live_last_updated}"
            updated_surf = self.font_small.render(updated_text, True, (120, 120, 130))
            screen.blit(updated_surf, (rect.x + 15, stats_y))
        
        # Error message (if any)
        if self.live_api_error:
            error_y = rect.y + rect.height - 18
            error_text = f"Error: {self.live_api_error}"
            error_surf = self.font_small.render(error_text, True, (180, 60, 60))
            screen.blit(error_surf, (rect.x + 15, error_y))
        
    def set_live_mode(self, enabled: bool) -> None:
        """Set whether the panel is in live data mode.
        
        Args:
            enabled: True for live data mode, False for manual slider
        """
        self.live_mode = enabled
        self.checkbox_checked = enabled
        self.rainfall_slider.set_disabled(enabled)
        
    def set_rainfall(self, value: float) -> None:
        """Set the rainfall value (for live data updates).
        
        Args:
            value: Rainfall value in mm
        """
        self.rainfall_slider.set_value(value)
        
    def set_live_stats(self, rainfall: float, station_info: str = "",
                       last_updated: str = "", error: Optional[str] = None) -> None:
        """Update live rainfall statistics display.
        
        Args:
            rainfall: Current live rainfall value in mm
            station_info: Information about data source/stations
            last_updated: Timestamp of last data update
            error: Error message if API fetch failed
        """
        self.live_rainfall_value = rainfall
        self.live_station_info = station_info
        self.live_last_updated = last_updated
        self.live_api_error = error
        
    def set_live_checkbox_callback(self, callback: Callable[[bool], None]) -> None:
        """Set callback function for when checkbox is toggled.
        
        Args:
            callback: Function called with True when live mode enabled, False when disabled
        """
        self.live_checkbox_callback = callback
        
    def is_live_mode(self) -> bool:
        """Check if panel is currently in live data mode.
        
        Returns:
            True if live mode is enabled
        """
        return self.live_mode
        
    def _draw_close_button(self, screen: pygame.Surface) -> None:
        """Draw the close (X) button."""
        rect = self.close_btn_rect
        
        # Button background
        if self.close_hovered:
            bg_color = (220, 100, 100)
            border_color = (180, 60, 60)
        else:
            bg_color = (200, 200, 210)
            border_color = (150, 150, 160)
        
        pygame.draw.rect(screen, bg_color, rect)
        pygame.draw.rect(screen, border_color, rect, 1)
        
        # Draw X
        x_color = (255, 255, 255) if self.close_hovered else (80, 80, 90)
        pygame.draw.line(screen, x_color,
                        (rect.x + 5, rect.y + 5),
                        (rect.right - 5, rect.bottom - 5), 2)
        pygame.draw.line(screen, x_color,
                        (rect.x + 5, rect.bottom - 5),
                        (rect.right - 5, rect.y + 5), 2)
        
    def _get_warning_color(self, value: float) -> tuple:
        """Get color based on rainfall value."""
        if value < 30:
            return (80, 180, 80)  # Green - safe
        elif value < 80:
            return (220, 180, 60)  # Yellow - caution
        else:
            return (220, 80, 80)   # Red - danger
        
    def get_rainfall(self) -> float:
        """Get current rainfall value from slider."""
        return self.rainfall_slider.get_value()


class BackButton:
    """Back button to return to map menu from a level."""
    
    def __init__(self, x: int = 20, y: int = 20, size: int = 44):
        """Initialize back button.
        
        Args:
            x, y: Position of the button (top-left corner)
            size: Size of the square button
        """
        self.rect = pygame.Rect(x, y, size, size)
        self.hovered = False
        self.callback: Optional[Callable[[], None]] = None
        
    def set_callback(self, callback: Callable[[], None]) -> None:
        """Set the callback function when button is clicked."""
        self.callback = callback
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process events for the button.
        
        Args:
            event: Pygame event
            
        Returns:
            True if button was clicked
        """
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.callback:
                    self.callback()
                return True
        
        return False
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the back button with arrow icon."""
        rect = self.rect
        
        # Button background with 3D effect
        if self.hovered:
            base_color = (120, 140, 180)
            highlight_color = (160, 180, 220)
            shadow_color = (80, 100, 140)
            border_color = (60, 80, 120)
        else:
            base_color = (100, 120, 160)
            highlight_color = (140, 160, 200)
            shadow_color = (60, 80, 120)
            border_color = (40, 60, 100)
        
        # Draw button background
        pygame.draw.rect(screen, base_color, rect)
        
        # 3D bevel effect - highlight (top-left)
        pygame.draw.rect(screen, highlight_color, (rect.x, rect.y, rect.width, 3))
        pygame.draw.rect(screen, highlight_color, (rect.x, rect.y, 3, rect.height))
        
        # 3D bevel effect - shadow (bottom-right)
        pygame.draw.rect(screen, shadow_color, (rect.x, rect.bottom - 3, rect.width, 3))
        pygame.draw.rect(screen, shadow_color, (rect.right - 3, rect.y, 3, rect.height))
        
        # Border
        pygame.draw.rect(screen, border_color, rect, 2)
        
        # Draw back arrow (pointing left) - shifted right to fit inside button
        arrow_color = (240, 240, 250)
        cx, cy = rect.centerx, rect.centery
        
        # Offset arrow to the right so it doesn't touch edges
        offset_x = 3
        arrow_offset_x=-2
        
        # Arrow shaft
        pygame.draw.rect(screen, arrow_color, (cx - 4 + offset_x, cy-1.1, 8, 4))
        
        # Arrow head (smaller, fully inside button)
        arrow_points = [
            (cx - 8 + arrow_offset_x, cy),      # tip
            (cx + arrow_offset_x, cy - 5),      # top
            (cx + arrow_offset_x, cy + 5),      # bottom
        ]
        pygame.draw.polygon(screen, arrow_color, arrow_points)


class UIPanel:
    """Bottom panel for displaying AI advice, zone info, and water level."""
    
    def __init__(self, x: int, y: int, width: int, height: int):
        """Initialize UI panel.
        
        Args:
            x, y: Position (typically bottom of screen)
            width, height: Dimensions
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Info text area (left side)
        self.info_rect = pygame.Rect(x + 20, y + 15, 280, height - 30)
        
        # Advice text area (right side)
        self.advice_rect = pygame.Rect(x + 320, y + 15, width - 340, height - 30)
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process events for UI elements.
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled
        """
        # This panel no longer has interactive elements
        return False
        
    def update(self, rainfall: float) -> None:
        """Update UI with current rainfall value (no-op for non-interactive panel)."""
        pass
        
    def draw(self, screen: pygame.Surface, level_name: str,
             level_warning: str, advice: str) -> None:
        """Draw the UI panel with pixelated style.
        
        Args:
            screen: The pygame surface to draw on
            level_name: Current zone name
            level_warning: Warning text for current level
            advice: AI advisor text
        """
        # Draw pixelated panel background with 3D bevel effect
        # Main background
        pygame.draw.rect(screen, (220, 220, 220), self.rect)
        
        # Pixelated border with shadows and highlights
        # Outer shadow
        pygame.draw.rect(screen, (150, 150, 150),
                        (self.rect.x + 2, self.rect.bottom - 4, self.rect.width, 4))
        pygame.draw.rect(screen, (150, 150, 150),
                        (self.rect.right - 4, self.rect.y + 2, 4, self.rect.height - 4))
        
        # Inner highlight (top and left)
        pygame.draw.rect(screen, (250, 250, 250),
                        (self.rect.x, self.rect.y, self.rect.width, 3))
        pygame.draw.rect(screen, (250, 250, 250),
                        (self.rect.x, self.rect.y, 3, self.rect.height))
        
        # Dark border
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 3)
        
        # Draw pixel art style corner accents
        corner_size = 8
        # Top-left corner
        pygame.draw.rect(screen, (80, 80, 80),
                        (self.rect.x + 3, self.rect.y + 3, corner_size, 3))
        pygame.draw.rect(screen, (80, 80, 80),
                        (self.rect.x + 3, self.rect.y + 3, 3, corner_size))
        # Top-right corner
        pygame.draw.rect(screen, (80, 80, 80),
                        (self.rect.right - corner_size - 3, self.rect.y + 3, corner_size, 3))
        pygame.draw.rect(screen, (80, 80, 80),
                        (self.rect.right - 6, self.rect.y + 3, 3, corner_size))
        # Bottom-left corner
        pygame.draw.rect(screen, (80, 80, 80),
                        (self.rect.x + 3, self.rect.bottom - 6, corner_size, 3))
        pygame.draw.rect(screen, (80, 80, 80),
                        (self.rect.x + 3, self.rect.bottom - corner_size - 3, 3, corner_size))
        # Bottom-right corner
        pygame.draw.rect(screen, (80, 80, 80),
                        (self.rect.right - corner_size - 3, self.rect.bottom - 6, corner_size, 3))
        pygame.draw.rect(screen, (80, 80, 80),
                        (self.rect.right - 6, self.rect.bottom - corner_size - 3, 3, corner_size))
        
        # Draw zone title with pixel shadow effect
        title_shadow = self.font_large.render(level_name, True, (120, 120, 120))
        screen.blit(title_shadow, (self.info_rect.x + 2, self.info_rect.y + 2))
        title = self.font_large.render(level_name, True, (40, 40, 40))
        screen.blit(title, (self.info_rect.x, self.info_rect.y))
        
        # Draw pixelated separator between sections
        pygame.draw.rect(screen, (180, 180, 180),
                        (self.advice_rect.x - 20, self.rect.y + 15, 3, self.rect.height - 30))
        
        # Draw level warning (if applicable)
        if level_warning:
            if "DANGER" in level_warning or "2010" in level_warning:
                warning_color = (180, 50, 50)
                # Draw pixelated warning box
                warning_box = pygame.Rect(self.advice_rect.x - 5, self.advice_rect.y,
                                         self.advice_rect.width + 10, 30)
                pygame.draw.rect(screen, (255, 200, 200), warning_box)
                pygame.draw.rect(screen, (180, 50, 50), warning_box, 2)
            else:
                warning_color = (50, 100, 50)
            warning_shadow = self.font.render(level_warning, True, (200, 200, 200))
            screen.blit(warning_shadow, (self.advice_rect.x + 1, self.advice_rect.y + 2))
            warning = self.font.render(level_warning, True, warning_color)
            screen.blit(warning, (self.advice_rect.x, self.advice_rect.y))
        
        # Draw AI advice text (wrapped to fit)
        advice_y_offset = 35 if level_warning else 5
        self._draw_wrapped_text(screen, advice, self.advice_rect.x, self.advice_rect.y + advice_y_offset,
                               self.advice_rect.width, (60, 60, 60))
        

        
    def _draw_wrapped_text(self, screen: pygame.Surface, text: str, x: int, y: int,
                          max_width: int, color: tuple) -> None:
        """Draw text that wraps to fit within max_width.
        
        Args:
            screen: Surface to draw on
            text: Text to draw
            x, y: Starting position
            max_width: Maximum width before wrapping
            color: Text color
        """
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = self.font.render(test_line, True, color)
            if test_surf.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
            
        # Draw lines
        line_height = 26
        for i, line in enumerate(lines[:4]):  # Max 4 lines
            surf = self.font.render(line, True, color)
            screen.blit(surf, (x, y + i * line_height))
            
    def get_rainfall(self) -> float:
        """Get current rainfall value (deprecated, use rainfall_panel instead)."""
        return 0.0


class FadeTransition:
    """Fade transition effect between levels."""
    
    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """Initialize fade transition."""
        self.overlay = pygame.Surface((screen_width, screen_height))
        self.overlay.fill((0, 0, 0))
        self.alpha = 0
        self.fading_out = False
        self.fading_in = False
        self.fade_speed = 15  # Alpha change per frame
        self.callback: Optional[Callable] = None
        
    def start_fade_out(self, callback: Callable) -> None:
        """Start fade out animation.
        
        Args:
            callback: Function to call when fade out completes
        """
        self.fading_out = True
        self.fading_in = False
        self.alpha = 0
        self.callback = callback
        
    def start_fade_in(self) -> None:
        """Start fade in animation after level change."""
        self.fading_out = False
        self.fading_in = True
        self.alpha = 255
        
    def update(self) -> bool:
        """Update fade animation.
        
        Returns:
            True if fade is still active
        """
        if self.fading_out:
            self.alpha += self.fade_speed
            if self.alpha >= 255:
                self.alpha = 255
                self.fading_out = False
                if self.callback:
                    self.callback()
                    self.callback = None
                return True
            return True
            
        elif self.fading_in:
            self.alpha -= self.fade_speed
            if self.alpha <= 0:
                self.alpha = 0
                self.fading_in = False
                return False
            return True
            
        return False
        
    def draw(self, screen: pygame.Surface) -> None:
        """Draw fade overlay if active."""
        if self.alpha > 0:
            self.overlay.set_alpha(int(self.alpha))
            screen.blit(self.overlay, (0, 0))


class InfoPopup:
    """Popup that appears when clicking interactive objects in the scene.
    
    Shows object title and description near the clicked location.
    Can be dismissed by clicking elsewhere or pressing Escape.
    """
    
    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """Initialize the info popup."""
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.visible = False
        self.title = ""
        self.description = ""
        self.target_x = 0
        self.target_y = 0
        
        # Popup dimensions
        self.width = 280
        self.min_height = 80
        self.padding = 15
        
        # Animation
        self.scale = 0.0
        self.target_scale = 1.0
        self.animation_speed = 10.0
        
        # Fonts
        self.title_font = pygame.font.Font(None, 28)
        self.body_font = pygame.font.Font(None, 22)
        
        # Colors
        self.bg_color = (40, 45, 55, 240)
        self.border_color = (255, 220, 100)
        self.title_color = (255, 220, 100)
        self.text_color = (220, 220, 220)
        
    def show(self, title: str, description: str, target_x: int, target_y: int) -> None:
        """Show the popup with object information.
        
        Args:
            title: Object name/title
            description: Object description text
            target_x, target_y: Position to show popup near (usually object center)
        """
        self.title = title
        self.description = description
        self.target_x = target_x
        self.target_y = target_y
        self.visible = True
        self.scale = 0.0
        
    def hide(self) -> None:
        """Hide the popup."""
        self.visible = False
        self.scale = 0.0
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle events for the popup.
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled (popup was visible and dismissed)
        """
        if not self.visible:
            return False
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Hide when clicking anywhere
            self.hide()
            return True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.hide()
                return True
                
        return False
        
    def update(self, dt: float) -> None:
        """Update popup animation.
        
        Args:
            dt: Delta time in seconds
        """
        if self.visible and self.scale < self.target_scale:
            self.scale = min(self.target_scale, self.scale + dt * self.animation_speed)
            
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the popup if visible.
        
        Args:
            screen: The pygame surface to draw on
        """
        if not self.visible or self.scale <= 0:
            return
            
        # Calculate popup rectangle
        # Position to the right of the object, or left if near screen edge
        popup_x = self.target_x + 20
        if popup_x + self.width > self.screen_width - 10:
            popup_x = self.target_x - self.width - 20
            
        # Calculate height based on text
        title_surf = self.title_font.render(self.title, True, self.title_color)
        
        # Wrap description text
        words = self.description.split(' ')
        lines = []
        current_line = []
        max_text_width = self.width - self.padding * 2
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = self.body_font.render(test_line, True, self.text_color)
            if test_surf.get_width() <= max_text_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
            
        line_height = 24
        text_height = len(lines) * line_height
        popup_height = max(self.min_height, self.padding * 3 + title_surf.get_height() + text_height)
        
        # Adjust Y to keep on screen
        popup_y = self.target_y - popup_height // 2
        popup_y = max(10, min(popup_y, self.screen_height - popup_height - 10))
        
        # Apply scale animation
        current_width = int(self.width * self.scale)
        current_height = int(popup_height * self.scale)
        center_x = popup_x + self.width // 2
        center_y = popup_y + popup_height // 2
        draw_x = center_x - current_width // 2
        draw_y = center_y - current_height // 2
        
        if current_width > 0 and current_height > 0:
            # Create popup surface with alpha
            popup_surf = pygame.Surface((current_width, current_height), pygame.SRCALPHA)
            
            # Draw background
            bg_with_alpha = (*self.bg_color[:3], int(self.bg_color[3] * self.scale))
            pygame.draw.rect(popup_surf, bg_with_alpha, (0, 0, current_width, current_height))
            pygame.draw.rect(popup_surf, self.border_color, (0, 0, current_width, current_height), 2)
            
            # Draw content only when fully scaled
            if self.scale > 0.8:
                # Title
                title_x = self.padding
                title_y = self.padding
                popup_surf.blit(title_surf, (title_x, title_y))
                
                # Description lines
                desc_y = title_y + title_surf.get_height() + 10
                for i, line in enumerate(lines):
                    line_surf = self.body_font.render(line, True, self.text_color)
                    popup_surf.blit(line_surf, (self.padding, desc_y + i * line_height))
                    
                # Draw hint text
                hint_surf = self.body_font.render("Click to close", True, (150, 150, 150))
                hint_x = current_width - hint_surf.get_width() - self.padding
                hint_y = current_height - hint_surf.get_height() - 8
                popup_surf.blit(hint_surf, (hint_x, hint_y))
            
            screen.blit(popup_surf, (draw_x, draw_y))
