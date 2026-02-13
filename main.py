"""Flood Simulation Prototype - First-person click-based game.

A first-person exploration game demonstrating flood behavior across three zones:
- ION Orchard (High Ground) - Safe zone, 80mm threshold
- Orchard Road (Street Level) - Moderate risk, 50mm threshold  
- Tanglin Carpark (Basement) - Extreme danger, 30mm threshold

Controls:
- Mouse: Click arrows to navigate between areas
- Mouse: Adjust rainfall slider (top-left)
- Key C: Toggle AI chatbot
- Mouse: Click chat button (bottom-right)
"""
import pygame
import sys
import os

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

# Ensure we're in the correct directory for imports and assets
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from levels import BaseLevel, IonLevel, OrchardLevel, CarparkLevel
from core import RainEffect, WaterRiseEffect
from ai import (
    AIAdvisor, FloodChatbot, ChatbotPanel, ChatButton,
    ProactiveAlertManager, AudioNarrator
)
from ai.flood_alerts import FloodAlertManager
from ui import UIPanel, FadeTransition, CollapsibleRainfallPanel, BackButton, InfoPopup, MapMenu

# Game constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 720  # Increased to fit full image + menu
FPS = 60
GAME_AREA_HEIGHT = 600  # Full image height
UI_HEIGHT = 120  # Bottom portion for UI (below image)


class Game:
    """Main game class managing levels and game loop."""
    
    def __init__(self):
        """Initialize pygame and game state."""
        pygame.init()
        pygame.display.set_caption("Singapore Flood Simulation")
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state: "map_menu" or "level"
        self.game_state = "map_menu"
        
        # Load font for zone title
        self.title_font = pygame.font.Font(None, 64)
        self.title_shadow_font = pygame.font.Font(None, 64)
        
        # Global rainfall (shared across all levels)
        self.rainfall = 0.0
        
        # Initialize rain effect
        self.rain = RainEffect(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Initialize water rise effect for carpark flooding
        self.water_rise = WaterRiseEffect(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Initialize AI advisor
        self.ai_advisor = AIAdvisor()
        
        # Initialize AI chatbot with context
        self.ai_chatbot = FloodChatbot(
            rainfall_context=0.0,
            location_context="Singapore"
        )
        
        # Initialize back button (top-left, leftmost)
        self.back_button = BackButton(20, 20, 44)
        self.back_button.set_callback(self._return_to_map)
        
        # Initialize collapsible rainfall panel (to the right of back button)
        self.rainfall_panel = CollapsibleRainfallPanel(72, 20)
        
        # Initialize UI panel (bottom for advice)
        self.ui_panel = UIPanel(0, GAME_AREA_HEIGHT, SCREEN_WIDTH, UI_HEIGHT)
        
        # Initialize info popup for clickable objects
        self.info_popup = InfoPopup(SCREEN_WIDTH, GAME_AREA_HEIGHT)
        
        # Initialize fade transition
        self.fade = FadeTransition(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Initialize map menu
        self.map_menu = MapMenu(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.map_menu.set_callback(self._on_zone_selected)
        
        # Initialize audio narrator FIRST (needed by other components)
        self.audio_narrator = AudioNarrator()
        self.audio_narrator.start()
        
        # Initialize chatbot panel with TTS support
        self.chatbot_panel = ChatbotPanel(self.ai_chatbot, audio_narrator=self.audio_narrator)
        
        # Initialize chat button (bottom right, above UI panel)
        self.chat_button = ChatButton(SCREEN_WIDTH - 68, SCREEN_HEIGHT - 168, size=48)
        self.chat_button.set_callback(lambda: self.chatbot_panel.toggle())
        
        # Initialize proactive alert manager
        self.alert_manager = ProactiveAlertManager(
            chatbot=self.ai_chatbot,
            cooldown_seconds=60,
            min_alert_interval=30,
            use_ai_alerts=True  # Use fallback messages for stability
        )
        
        # Initialize simple flood alert manager
        self.flood_alerts = FloodAlertManager(self.audio_narrator)
        
        # Connect alerts to audio (legacy)
        self.alert_manager.add_alert_callback(self._on_proactive_alert)
        
        # Load all levels
        self.levels = {}
        self._load_levels()
        
        # Start with no level selected
        self.current_level_name = None
        self.current_level = None
        
        # Debug mode
        self.debug_mode = False
        
    def _load_levels(self) -> None:
        """Load and initialize all game levels."""
        # ION Mall - High ground, safe
        ion = IonLevel()
        ion.load()
        self.levels["ion"] = ion
        
        # Orchard Road - Street level
        orchard = OrchardLevel()
        orchard.load()
        self.levels["orchard"] = orchard
        
        # Tanglin Carpark - Basement, dangerous
        carpark = CarparkLevel()
        carpark.load()
        self.levels["carpark"] = carpark
        
    def _on_zone_selected(self, level_id: str) -> None:
        """Handle zone selection from map menu.
        
        Args:
            level_id: The level to start
        """
        def do_switch():
            self.game_state = "level"
            self.current_level_name = level_id
            self.current_level = self.levels[level_id]
            self.fade.start_fade_in()
            
        self.fade.start_fade_out(do_switch)
        
    def _return_to_map(self) -> None:
        """Return to the map menu from a level."""
        def do_return():
            # Reset cursor before leaving level
            if self.current_level:
                self.current_level.reset_clickable_cursors()
            self.game_state = "map_menu"
            self.current_level = None
            self.current_level_name = None
            self.fade.start_fade_in()
            
        self.fade.start_fade_out(do_return)
        
    def _on_proactive_alert(self, alert) -> None:
        """Handle proactive alerts from the alert manager.
        
        Args:
            alert: ProactiveAlert that was triggered
        """
        # Speak the alert
        self.audio_narrator.speak_alert(alert)
        
        # Flash chat button for high priority alerts
        if alert.priority.value in ["high", "critical"]:
            self.chat_button.set_notification(True)
        
        print(f"[ALERT] {alert.priority.value.upper()}: {alert.message}")
        
    def _switch_level(self, target_name: str, spawn_x: int, spawn_y: int) -> None:
        """Switch to a different level with fade transition.
        
        Args:
            target_name: Name of level to switch to
            spawn_x, spawn_y: Unused (kept for compatibility)
        """
        def do_switch():
            # Reset cursor before switching
            if self.current_level:
                self.current_level.reset_clickable_cursors()
            self.current_level_name = target_name
            self.current_level = self.levels[target_name]
            self.fade.start_fade_in()
            
        self.fade.start_fade_out(do_switch)
        
    def handle_events(self) -> None:
        """Process input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Close chat panel if open, else return to map/quit
                    if self.chatbot_panel.visible:
                        self.chatbot_panel.hide()
                    elif self.game_state == "level":
                        self.game_state = "map_menu"
                        self.current_level = None
                        self.current_level_name = None
                    else:
                        self.running = False
                elif event.key == pygame.K_F1:
                    self.debug_mode = not self.debug_mode
                elif event.key == pygame.K_t:
                    # Test audio narrator
                    print("Testing audio narrator...")
                    self.audio_narrator.speak(
                        "This is a test of the flood simulation audio system.",
                        priority=1,
                        alert_id="test"
                    )
            
            # Handle chatbot panel events (highest priority when visible)
            # Handle chatbot panel events only in level mode
            if self.game_state == "level":
                if self.chatbot_panel.visible:
                    if self.chatbot_panel.handle_event(event):
                        continue
                
                # Handle chat button click
                if self.chat_button.handle_event(event):
                    continue
            
            # Handle events based on game state
            if self.game_state == "map_menu":
                self.map_menu.handle_event(event)
            else:
                # In level mode
                # Pass events to info popup first (it captures clicks to dismiss)
                if self.info_popup.handle_event(event):
                    continue
                
                # Pass events to back button
                if self.back_button.handle_event(event):
                    continue
                
                # Pass events to rainfall panel
                if self.rainfall_panel.handle_event(event):
                    self.rainfall = self.rainfall_panel.get_rainfall()
                    continue
                
                # Handle clickable object clicks
                if self.current_level:
                    obj_info = self.current_level.handle_clickable_events(event)
                    if obj_info:
                        title, description = obj_info
                        # Show popup near mouse position
                        mouse_pos = pygame.mouse.get_pos()
                        self.info_popup.show(title, description, mouse_pos[0], mouse_pos[1])
                        continue
                
                # Handle arrow clicks for level transitions
                if self.current_level:
                    transition = self.current_level.handle_event(event)
                    if transition:
                        target_level, spawn_x, spawn_y = transition
                        self._switch_level(target_level, spawn_x, spawn_y)
                
    def update(self, dt: float) -> None:
        """Update game state.
        
        Args:
            dt: Delta time in seconds
        """
        # Update fade transition
        if self.fade.update():
            return  # Don't update game during fade
        
        if self.game_state == "map_menu":
            # Update map menu animations
            self.map_menu.update(dt)
        else:
            # In level mode
            # Update AI advisor (no water height)
            self.ai_advisor.update(self.current_level.name, self.rainfall)
            
            # Update AI chatbot context
            if self.current_level:
                self.ai_chatbot.update_context(
                    rainfall=self.rainfall,
                    location=self.current_level.name
                )
            
            # Simple hardcoded flood alerts (stable)
            alert_msg = self.flood_alerts.update(
                rainfall=self.rainfall,
                location=self.current_level.name
            )
            if alert_msg:
                print(f"[FLOOD ALERT] {alert_msg}")
            
            # Update rain effect (disabled for carpark when flooding)
            if self.current_level_name == "carpark":
                self.water_rise.update(self.rainfall, dt)
            else:
                self.rain.update(self.rainfall, dt)
            
            # Update panels
            self.rainfall_panel.update(self.rainfall)
            
            # Update current level (arrows and clickable objects animation)
            if self.current_level:
                self.current_level.update(dt)
                self.current_level.update_clickables(dt)
            
            # Update info popup
            self.info_popup.update(dt)
        
        # Update chatbot panel and button (only when in a level)
        if self.game_state == "level":
            self.chatbot_panel.update(dt)
            self.chat_button.update(dt)
            
            # Update chat button notification state
            if self.ai_chatbot.is_processing():
                self.chat_button.set_processing(True)
                self.chat_button.set_notification(False)
            elif not self.chatbot_panel.visible and self.ai_chatbot.has_new_messages():
                self.chat_button.set_processing(False)
                self.chat_button.set_notification(True)
            else:
                self.chat_button.set_processing(False)
                self.chat_button.set_notification(False)
        else:
            # Hide chat panel when in map menu
            if self.chatbot_panel.visible:
                self.chatbot_panel.hide()
        
    def draw(self) -> None:
        """Render the game frame."""
        if self.game_state == "map_menu":
            # Draw map menu
            self.map_menu.draw(self.screen)
        else:
            # In level mode
            # 1. Draw background image for current level
            self.current_level.draw_background(self.screen)
            
            # 2. Draw rain effect (or water rise for carpark flooding)
            if self.current_level_name == "carpark":
                self.water_rise.draw(self.screen, self.rainfall)
            else:
                self.rain.draw(self.screen, self.rainfall)
            
            # 3. Draw clickable object highlights (hover effects)
            self.current_level.draw_clickables(self.screen)
            
            # 4. Draw transition arrows
            self.current_level.draw_arrows(self.screen)
            
            # 5. Draw zone title at top center
            self._draw_zone_title(self.current_level.name)
            
            # 6. Draw back button (top-left)
            self.back_button.draw(self.screen)
            
            # 7. Draw collapsible rainfall panel
            self.rainfall_panel.draw(self.screen)
            
            # 8. Draw UI panel (bottom advice panel)
            advice = self.ai_advisor.get_advice()
            warning = self.ai_advisor.get_level_warning()
            self.ui_panel.draw(self.screen, self.current_level.name, warning, advice)
            
            # 9. Draw info popup (if visible)
            self.info_popup.draw(self.screen)
        
        # Draw chat button and panel only when in a level
        if self.game_state == "level":
            self.chat_button.draw(self.screen)
            if self.chatbot_panel.visible:
                self.chatbot_panel.draw(self.screen)
        
        # Draw fade overlay if active
        self.fade.draw(self.screen)
        
        # Debug info
        if self.debug_mode:
            font = pygame.font.Font(None, 24)
            debug_text = f"Rain: {self.rainfall:.0f}mm | State: {self.game_state}"
            if self.current_level_name:
                debug_text += f" | Level: {self.current_level_name}"
            debug_text += f" | AI: {'Ready' if self.ai_chatbot.is_available() else 'Fallback'}"
            surf = font.render(debug_text, True, (255, 255, 0))
            self.screen.blit(surf, (10, 10))
            
            # Draw FPS
            fps_text = f"FPS: {int(self.clock.get_fps())}"
            fps_surf = font.render(fps_text, True, (255, 255, 0))
            self.screen.blit(fps_surf, (10, 35))
            
            # Draw cursor position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            cursor_text = f"Cursor: ({mouse_x}, {mouse_y})"
            cursor_surf = font.render(cursor_text, True, (255, 255, 0))
            self.screen.blit(cursor_surf, (10, 60))
            
            # Draw audio/alert status
            audio_info = self.audio_narrator.get_backend_info()
            audio_text = f"Audio: {audio_info['backend']} | Queue: {audio_info['queue_size']}"
            audio_surf = font.render(audio_text, True, (255, 255, 0))
            self.screen.blit(audio_surf, (10, 85))
            
            alert_stats = self.alert_manager.get_stats()
            alert_text = f"Alerts: {alert_stats['pending_alerts']} pending, {alert_stats['total_alerts']} total"
            alert_surf = font.render(alert_text, True, (255, 255, 0))
            self.screen.blit(alert_surf, (10, 110))
        
        pygame.display.flip()
        
    def _draw_zone_title(self, zone_name: str) -> None:
        """Draw zone name as a title at the top center of screen.
        
        Args:
            zone_name: Current zone/level name to display
        """
        # Create title surface
        title_surf = self.title_font.render(zone_name, True, (255, 255, 255))
        shadow_surf = self.title_shadow_font.render(zone_name, True, (0, 0, 0))
        
        # Calculate position (centered at top)
        title_x = (SCREEN_WIDTH - title_surf.get_width()) // 2
        title_y = 15
        
        # Draw pixelated shadow effect
        for offset in [(3, 3), (2, 2), (1, 1)]:
            self.screen.blit(shadow_surf, (title_x + offset[0], title_y + offset[1]))
        
        # Draw black outline around text
        outline_color = (0, 0, 0)
        outline_offsets = [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, -2), (-2, 2), (2, 2)]
        for ox, oy in outline_offsets:
            outline_surf = self.title_font.render(zone_name, True, outline_color)
            self.screen.blit(outline_surf, (title_x + ox, title_y + oy))
        
        # Draw main title in bright white
        self.screen.blit(title_surf, (title_x, title_y))
        
        # Draw decorative pixel line underneath
        line_y = title_y + title_surf.get_height() + 8
        line_width = title_surf.get_width() + 40
        line_x = (SCREEN_WIDTH - line_width) // 2
        
        # Draw pixelated underline with gradient effect
        pygame.draw.rect(self.screen, (100, 150, 200), (line_x, line_y, line_width, 4))
        pygame.draw.rect(self.screen, (150, 200, 255), (line_x + 5, line_y, line_width - 10, 2))
        pygame.draw.rect(self.screen, (50, 100, 150), (line_x, line_y + 2, line_width, 2))
        
    def run(self) -> None:
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0  # Delta time in seconds
            
            self.handle_events()
            self.update(dt)
            self.draw()
        
        # Cleanup
        self.audio_narrator.stop()
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the flood simulation."""
    print("=" * 60)
    print("Singapore Flood Simulation - Orchard District")
    print("=" * 60)
    print("\nControls:")
    print("  Mouse: Click arrows to navigate")
    print("  Mouse: Adjust rainfall slider (top-left)")
    print("  Mouse: Click chat button (bottom-right) or press C")
    print("  Debug Mode: F1 (shows FPS, cursor position)")
    print("  Test Audio: T")
    print("  Quit: ESC")
    print("\nZones:")
    print("  ION Orchard - High ground (80mm threshold)")
    print("  Orchard Road - Street level (50mm threshold)")
    print("  Tanglin Carpark - Basement DANGER (30mm threshold)")
    print("=" * 60)
    
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
