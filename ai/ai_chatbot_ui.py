"""Pygame UI components for the AI chatbot interface."""
import pygame
import math
from typing import List, Callable, Optional
from datetime import datetime

from .ai_chatbot import FloodChatbot, ChatMessage


class ChatButton:
    """Floating chat button to open the chat panel."""
    
    # Color palette matching game UI theme
    COLORS = {
        'base': (80, 130, 200),
        'hover': (100, 160, 230),
        'highlight': (120, 180, 255),
        'shadow': (50, 90, 160),
        'border': (40, 80, 140),
        'notification': (220, 80, 80),  # Red for new messages
        'processing': (80, 200, 120),   # Green for processing
    }
    
    def __init__(self, x: int, y: int, size: int = 48):
        """Initialize chat button.
        
        Args:
            x, y: Position of button center
            size: Size of the square button
        """
        self.x = x
        self.y = y
        self.size = size
        self.rect = pygame.Rect(x - size//2, y - size//2, size, size)
        
        self.hovered = False
        self.clicked = False
        self.callback: Optional[Callable[[], None]] = None
        
        # Notification and processing states
        self.show_notification = False
        self.is_processing = False
        
        # Animation
        self.pulse_time = 0.0
        self.bounce_offset = 0.0
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        
    def set_callback(self, callback: Callable[[], None]) -> None:
        """Set the callback function when button is clicked."""
        self.callback = callback
        
    def set_notification(self, show: bool) -> None:
        """Show or hide notification indicator.
        
        Args:
            show: True to show red notification dot
        """
        self.show_notification = show
        
    def set_processing(self, processing: bool) -> None:
        """Set processing state for animation.
        
        Args:
            processing: True when AI is generating response
        """
        self.is_processing = processing
        
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
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.clicked = True
                if self.callback:
                    self.callback()
                return True
                
        elif event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
            
        return False
        
    def update(self, dt: float) -> None:
        """Update button animations.
        
        Args:
            dt: Delta time in seconds
        """
        self.pulse_time += dt * 3
        
        # Bounce animation when processing or notification
        if self.is_processing or self.show_notification:
            self.bounce_offset = math.sin(self.pulse_time * 2) * 3
        else:
            self.bounce_offset = 0
            
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the chat button.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Calculate animated position
        draw_y = self.y + self.bounce_offset
        
        # Button rect with bounce offset
        draw_rect = pygame.Rect(
            self.x - self.size // 2,
            draw_y - self.size // 2,
            self.size,
            self.size
        )
        
        # Choose colors based on state
        if self.hovered:
            base_color = self.COLORS['hover']
        else:
            base_color = self.COLORS['base']
            
        # Draw button background with 3D effect
        pygame.draw.rect(screen, base_color, draw_rect)
        
        # Top highlight
        pygame.draw.rect(screen, self.COLORS['highlight'], 
                        (draw_rect.x, draw_rect.y, draw_rect.width, 4))
        # Left highlight
        pygame.draw.rect(screen, self.COLORS['highlight'], 
                        (draw_rect.x, draw_rect.y, 4, draw_rect.height))
        # Bottom shadow
        pygame.draw.rect(screen, self.COLORS['shadow'], 
                        (draw_rect.x, draw_rect.bottom - 4, draw_rect.width, 4))
        # Right shadow
        pygame.draw.rect(screen, self.COLORS['shadow'], 
                        (draw_rect.right - 4, draw_rect.y, 4, draw_rect.height))
        
        # Border
        pygame.draw.rect(screen, self.COLORS['border'], draw_rect, 2)
        
        # Draw chat icon (pixelated speech bubble)
        self._draw_chat_icon(screen, self.x, int(draw_y))
        
        # Draw notification dot
        if self.show_notification:
            dot_rect = pygame.Rect(draw_rect.right - 14, draw_rect.y + 4, 10, 10)
            pygame.draw.ellipse(screen, self.COLORS['notification'], dot_rect)
            pygame.draw.ellipse(screen, (255, 255, 255), dot_rect, 1)
            
        # Draw processing indicator (pulsing ring)
        if self.is_processing:
            pulse = (math.sin(self.pulse_time) + 1) / 2  # 0 to 1
            ring_radius = int(self.size // 2 + 4 + pulse * 4)
            ring_color = (
                int(self.COLORS['processing'][0]),
                int(self.COLORS['processing'][1]),
                int(self.COLORS['processing'][2])
            )
            pygame.draw.circle(screen, ring_color, (self.x, int(draw_y)), ring_radius, 2)
            
        # Draw tooltip on hover
        if self.hovered:
            self._draw_tooltip(screen)
            
    def _draw_chat_icon(self, screen: pygame.Surface, cx: int, cy: int) -> None:
        """Draw a pixelated chat bubble icon."""
        # Main bubble body (rounded rect approximation)
        bubble_color = (255, 255, 255)
        
        # Bubble dimensions
        bw, bh = 28, 20
        bx = cx - bw // 2
        by = cy - bh // 2 - 2
        
        # Main bubble rectangle
        pygame.draw.rect(screen, bubble_color, (bx + 4, by, bw - 8, bh))
        pygame.draw.rect(screen, bubble_color, (bx, by + 4, bw, bh - 8))
        
        # Rounded corners
        pygame.draw.rect(screen, bubble_color, (bx + 2, by + 2, 4, 4))
        pygame.draw.rect(screen, bubble_color, (bx + bw - 6, by + 2, 4, 4))
        pygame.draw.rect(screen, bubble_color, (bx + 2, by + bh - 6, 4, 4))
        pygame.draw.rect(screen, bubble_color, (bx + bw - 6, by + bh - 6, 4, 4))
        
        # Speech tail
        pygame.draw.rect(screen, bubble_color, (bx + 6, by + bh - 2, 8, 6))
        pygame.draw.rect(screen, bubble_color, (bx + 4, by + bh, 4, 4))
        
        # Lines inside bubble (text representation)
        line_color = self.COLORS['base']
        pygame.draw.rect(screen, line_color, (bx + 6, by + 5, 16, 2))
        pygame.draw.rect(screen, line_color, (bx + 6, by + 9, 12, 2))
        pygame.draw.rect(screen, line_color, (bx + 6, by + 13, 14, 2))
        
    def _draw_tooltip(self, screen: pygame.Surface) -> None:
        """Draw hover tooltip."""
        tooltip_text = "Ask AI about floods"
        tooltip_surf = self.font.render(tooltip_text, True, (50, 50, 50))
        
        # Tooltip background
        padding = 8
        tooltip_rect = pygame.Rect(
            self.rect.x - tooltip_surf.get_width() - padding * 2 - 10,
            self.rect.centery - tooltip_surf.get_height() // 2 - padding,
            tooltip_surf.get_width() + padding * 2,
            tooltip_surf.get_height() + padding * 2
        )
        
        # Draw tooltip background
        pygame.draw.rect(screen, (250, 250, 250), tooltip_rect)
        pygame.draw.rect(screen, (200, 200, 200), tooltip_rect, 1)
        
        # Draw text
        screen.blit(tooltip_surf, (tooltip_rect.x + padding, tooltip_rect.y + padding))


class ChatbotPanel:
    """Chat panel UI for the AI chatbot."""
    
    # Colors matching game theme
    COLORS = {
        'bg': (245, 245, 250),
        'border': (120, 120, 130),
        'header_bg': (80, 130, 200),
        'header_text': (255, 255, 255),
        'user_msg': (220, 235, 255),
        'ai_msg': (240, 240, 240),
        'input_bg': (255, 255, 255),
        'input_border': (180, 180, 190),
        'text': (50, 50, 60),
        'timestamp': (150, 150, 160),
        'scroll_bg': (220, 220, 220),
        'scroll_thumb': (160, 160, 170),
    }
    
    def __init__(self, chatbot: FloodChatbot, 
                 x: int = 380, y: int = 50, 
                 width: int = 400, height: int = 500):
        """Initialize chatbot panel.
        
        Args:
            chatbot: The flood chatbot instance
            x, y: Position of panel
            width, height: Panel dimensions
        """
        self.chatbot = chatbot
        self.rect = pygame.Rect(x, y, width, height)
        self.visible = False
        
        # Header
        self.header_height = 36
        
        # Message area
        self.message_margin = 10
        self.message_area = pygame.Rect(
            x + self.message_margin,
            y + self.header_height + 5,
            width - self.message_margin * 2 - 12,  # Space for scrollbar
            height - self.header_height - 60  # Space for input
        )
        
        # Input area
        self.input_height = 40
        self.input_rect = pygame.Rect(
            x + self.message_margin,
            y + height - self.input_height - 10,
            width - self.message_margin * 2 - 60,  # Space for send button
            self.input_height
        )
        
        # Send button
        self.send_btn_rect = pygame.Rect(
            self.input_rect.right + 5,
            self.input_rect.y,
            50,
            self.input_height
        )
        
        # Close button
        self.close_btn_size = 24
        self.close_btn_rect = pygame.Rect(
            x + width - self.close_btn_size - 8,
            y + (self.header_height - self.close_btn_size) // 2,
            self.close_btn_size,
            self.close_btn_size
        )
        
        # Input state
        self.input_text = ""
        self.input_active = False
        self.cursor_visible = True
        self.cursor_timer = 0.0
        
        # Scroll state
        self.scroll_offset = 0
        self.max_scroll = 0
        self.scroll_dragging = False
        
        # Fonts
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        self.font_header = pygame.font.Font(None, 28)
        
    def toggle(self) -> None:
        """Toggle panel visibility."""
        self.visible = not self.visible
        if self.visible:
            # Mark messages as read when opening
            self.chatbot.mark_messages_read()
            self.input_active = True
        else:
            self.input_active = False
            
    def show(self) -> None:
        """Show the chat panel."""
        self.visible = True
        self.chatbot.mark_messages_read()
        self.input_active = True
        
    def hide(self) -> None:
        """Hide the chat panel."""
        self.visible = False
        self.input_active = False
        
    def has_unread(self) -> bool:
        """Check if there are unread messages."""
        return self.chatbot.has_new_messages()
        
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Process events for the panel.
        
        Args:
            event: Pygame event
            
        Returns:
            True if event was handled
        """
        if not self.visible:
            return False
            
        mouse_pos = pygame.mouse.get_pos()
        
        # Close button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.close_btn_rect.collidepoint(event.pos):
                self.hide()
                return True
                
            # Send button
            if self.send_btn_rect.collidepoint(event.pos):
                self._submit_message()
                return True
                
            # Input field
            if self.input_rect.collidepoint(event.pos):
                self.input_active = True
            else:
                self.input_active = False
        
        # Scroll wheel support for message area
        if event.type == pygame.MOUSEWHEEL:
            if self.message_area.collidepoint(mouse_pos):
                self.scroll_offset -= event.y * 30  # Scroll 30 pixels per wheel tick
                # Clamp scroll offset
                messages = self.chatbot.get_messages()
                content_height = self._get_content_height(messages)
                max_scroll = max(0, content_height - self.message_area.height)
                self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
                return True
                
        # Keyboard input (only when input is active)
        if event.type == pygame.KEYDOWN and self.input_active:
            if event.key == pygame.K_RETURN:
                self._submit_message()
                return True
            elif event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
                return True
            elif event.key == pygame.K_ESCAPE:
                self.hide()
                return True
            elif event.unicode.isprintable():
                if len(self.input_text) < 150:
                    self.input_text += event.unicode
                return True
                
        return self.rect.collidepoint(mouse_pos)
        
    def _submit_message(self) -> None:
        """Submit current input to chatbot."""
        if self.input_text.strip() and not self.chatbot.is_processing():
            question = self.input_text.strip()
            self.input_text = ""
            # Scroll to bottom immediately after user message, then again after response
            self._scroll_to_bottom()
            self.chatbot.ask(question, lambda _: self._scroll_to_bottom())
            
    def _scroll_to_bottom(self) -> None:
        """Scroll to show latest message."""
        messages = self.chatbot.get_messages()
        # Calculate total content height
        total_height = self._get_content_height(messages)
        # Set scroll to show bottom of content
        self.scroll_offset = max(0, total_height - self.message_area.height + 10)
        
    def update(self, dt: float) -> None:
        """Update panel state.
        
        Args:
            dt: Delta time in seconds
        """
        if not self.visible:
            return
            
        # Cursor blink
        self.cursor_timer += dt
        if self.cursor_timer > 0.5:
            self.cursor_timer = 0
            self.cursor_visible = not self.cursor_visible
            
    def draw(self, screen: pygame.Surface) -> None:
        """Draw the chat panel.
        
        Args:
            screen: Pygame surface to draw on
        """
        if not self.visible:
            return
            
        # Draw panel background
        pygame.draw.rect(screen, self.COLORS['bg'], self.rect)
        
        # Draw border with 3D effect
        # Shadow
        pygame.draw.rect(screen, (180, 180, 190), 
                        (self.rect.x + 2, self.rect.bottom - 3, self.rect.width, 3))
        pygame.draw.rect(screen, (180, 180, 190), 
                        (self.rect.right - 3, self.rect.y + 2, 3, self.rect.height - 3))
        # Highlight
        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.rect.x, self.rect.y, self.rect.width, 2))
        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.rect.x, self.rect.y, 2, self.rect.height))
        # Main border
        pygame.draw.rect(screen, self.COLORS['border'], self.rect, 2)
        
        # Draw header
        self._draw_header(screen)
        
        # Draw messages
        self._draw_messages(screen)
        
        # Draw input area
        self._draw_input(screen)
        
    def _draw_header(self, screen: pygame.Surface) -> None:
        """Draw panel header."""
        header_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.header_height)
        pygame.draw.rect(screen, self.COLORS['header_bg'], header_rect)
        
        # Header text
        title = self.font_header.render("Flood Safety AI", True, self.COLORS['header_text'])
        screen.blit(title, (self.rect.x + 12, self.rect.y + 8))
        
        # Close button
        if self.close_btn_rect.collidepoint(pygame.mouse.get_pos()):
            close_color = (255, 150, 150)
        else:
            close_color = self.COLORS['header_text']
            
        # X shape
        cx, cy = self.close_btn_rect.center
        pygame.draw.line(screen, close_color, (cx - 6, cy - 6), (cx + 6, cy + 6), 2)
        pygame.draw.line(screen, close_color, (cx - 6, cy + 6), (cx + 6, cy - 6), 2)
        
    def _get_content_height(self, messages: list) -> int:
        """Calculate the actual total height of all messages."""
        total = 0
        for msg in messages:
            lines = self._wrap_text(msg.content, self.message_area.width - 60)
            msg_height = len(lines) * 18 + 28  # text height + padding for label
            total += msg_height + 8  # + spacing between messages
        return total
    
    def _draw_messages(self, screen: pygame.Surface) -> None:
        """Draw message history."""
        # Message area background
        pygame.draw.rect(screen, (255, 255, 255), self.message_area)
        pygame.draw.rect(screen, self.COLORS['input_border'], self.message_area, 1)
        
        # Clip to message area
        clip_rect = screen.get_clip()
        screen.set_clip(self.message_area)
        
        messages = self.chatbot.get_messages(limit=50)
        y_offset = self.message_area.y + 5 - self.scroll_offset
        
        for msg in messages:
            # Calculate message height
            lines = self._wrap_text(msg.content, self.message_area.width - 60)
            msg_height = len(lines) * 18 + 28  # text height + padding for label
            
            # Skip if completely off-screen
            if y_offset + msg_height < self.message_area.y or y_offset > self.message_area.bottom:
                y_offset += msg_height + 8
                continue
            
            # Message bubble
            is_user = msg.role == "user"
            bubble_color = self.COLORS['user_msg'] if is_user else self.COLORS['ai_msg']
            bubble_x = self.message_area.x + 5 if is_user else self.message_area.x + 35
            bubble_width = self.message_area.width - 45
            
            bubble_rect = pygame.Rect(bubble_x, y_offset, bubble_width, msg_height)
            pygame.draw.rect(screen, bubble_color, bubble_rect)
            pygame.draw.rect(screen, self.COLORS['input_border'], bubble_rect, 1)
            
            # Role label
            label = "You" if is_user else "AI"
            label_surf = self.font_small.render(label, True, self.COLORS['timestamp'])
            screen.blit(label_surf, (bubble_x + 5, y_offset + 3))
            
            # Message text
            text_y = y_offset + 18
            for line in lines:
                line_surf = self.font.render(line, True, self.COLORS['text'])
                screen.blit(line_surf, (bubble_x + 5, text_y))
                text_y += 18
            
            y_offset += msg_height + 8
        
        # Restore clip
        screen.set_clip(clip_rect)
        
        # Draw scrollbar if needed
        total_height = self._get_content_height(messages)
        if total_height > self.message_area.height:
            self._draw_scrollbar(screen, total_height)
            
    def _draw_scrollbar(self, screen: pygame.Surface, content_height: int) -> None:
        """Draw scrollbar."""
        scrollbar_x = self.message_area.right + 2
        scrollbar_width = 8
        scrollbar_rect = pygame.Rect(scrollbar_x, self.message_area.y, scrollbar_width, self.message_area.height)
        
        # Background
        pygame.draw.rect(screen, self.COLORS['scroll_bg'], scrollbar_rect)
        
        # Thumb
        thumb_height = max(30, self.message_area.height * self.message_area.height // content_height)
        thumb_y = self.message_area.y + (self.scroll_offset * self.message_area.height // content_height)
        thumb_rect = pygame.Rect(scrollbar_x, thumb_y, scrollbar_width, thumb_height)
        pygame.draw.rect(screen, self.COLORS['scroll_thumb'], thumb_rect)
        
    def _draw_input(self, screen: pygame.Surface) -> None:
        """Draw input field and send button."""
        # Input background
        input_color = self.COLORS['input_bg'] if self.input_active else (250, 250, 250)
        pygame.draw.rect(screen, input_color, self.input_rect)
        pygame.draw.rect(screen, self.COLORS['input_border'], self.input_rect, 2)
        
        # Input text
        text_surf = self.font.render(self.input_text, True, self.COLORS['text'])
        text_x = self.input_rect.x + 8
        text_y = self.input_rect.centery - text_surf.get_height() // 2
        
        # Clip text if too long
        if text_surf.get_width() > self.input_rect.width - 20:
            clip_width = self.input_rect.width - 20
            text_surf = text_surf.subsurface((text_surf.get_width() - clip_width, 0, clip_width, text_surf.get_height()))
        screen.blit(text_surf, (text_x, text_y))
        
        # Cursor
        if self.input_active and self.cursor_visible:
            cursor_x = text_x + text_surf.get_width() + 2
            pygame.draw.line(screen, self.COLORS['text'], 
                           (cursor_x, self.input_rect.y + 8), 
                           (cursor_x, self.input_rect.bottom - 8), 2)
        
        # Send button
        btn_color = self.COLORS['header_bg'] if self.send_btn_rect.collidepoint(pygame.mouse.get_pos()) else (100, 150, 220)
        if not self.input_text.strip() or self.chatbot.is_processing():
            btn_color = (180, 180, 190)  # Disabled
            
        pygame.draw.rect(screen, btn_color, self.send_btn_rect)
        pygame.draw.rect(screen, self.COLORS['border'], self.send_btn_rect, 1)
        
        # Send icon (arrow)
        cx, cy = self.send_btn_rect.center
        arrow_color = (255, 255, 255) if self.input_text.strip() and not self.chatbot.is_processing() else (200, 200, 200)
        pygame.draw.polygon(screen, arrow_color, [
            (cx - 4, cy - 6),
            (cx + 6, cy),
            (cx - 4, cy + 6)
        ])
        
        # Processing indicator
        if self.chatbot.is_processing():
            loading = self.font_small.render("...", True, self.COLORS['text'])
            screen.blit(loading, (self.input_rect.x, self.input_rect.bottom + 2))
            
    def _wrap_text(self, text: str, max_width: int) -> List[str]:
        """Wrap text to fit within max_width.
        
        Args:
            text: Text to wrap
            max_width: Maximum pixel width
            
        Returns:
            List of wrapped lines
        """
        words = text.split(' ')
        lines = []
        current_line = []
        
        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = self.font.render(test_line, True, self.COLORS['text'])
            if test_surf.get_width() <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
            
        return lines if lines else [""]
