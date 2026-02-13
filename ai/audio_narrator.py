"""Voice/Audio Narration System for Flood Chatbot Alerts.

Provides text-to-speech capabilities for proactive alerts using ElevenLabs.
"""
import threading
import queue
import time
from dataclasses import dataclass, field
from typing import Optional, Callable, List, Dict, Any
from datetime import datetime
from enum import Enum
import os


class TTSBackend(Enum):
    """Available text-to-speech backends."""
    ELEVENLABS = "elevenlabs"  # Cloud, high quality, requires API key
    NONE = "none"              # No audio output


@dataclass(order=True)
class AudioQueueItem:
    """An item in the audio queue with priority."""
    priority: int  # Lower = higher priority (for heapq)
    timestamp: datetime = field(compare=False)
    text: str = field(compare=False)
    alert_id: str = field(compare=False)
    interrupt_current: bool = field(default=False, compare=False)


class AudioNarrator:
    """Text-to-speech narrator for flood alerts using ElevenLabs.
    
    Manages a priority queue for audio playback.
    
    Example:
        narrator = AudioNarrator()
        narrator.start()
        
        # Queue an alert
        narrator.speak("Warning: Heavy rain detected at Tanglin Carpark", priority=2)
        
        # Emergency alert (interrupts current playback)
        narrator.speak("EMERGENCY: Evacuate now!", priority=0, interrupt=True)
        
        narrator.stop()
    """
    
    # Priority levels (lower = more urgent)
    PRIORITY_CRITICAL = 0   # Emergency evacuation
    PRIORITY_HIGH = 1       # Warnings
    PRIORITY_MEDIUM = 2     # Cautions
    PRIORITY_LOW = 3        # Informational
    
    def __init__(
        self,
        elevenlabs_api_key: Optional[str] = None,
        voice_id: Optional[str] = None,
        volume: float = 0.9
    ):
        """Initialize the audio narrator.
        
        Args:
            elevenlabs_api_key: API key for ElevenLabs (optional, uses env var)
            voice_id: Voice ID for ElevenLabs (optional)
            volume: Volume level 0.0-1.0
        """
        self.elevenlabs_api_key = elevenlabs_api_key or os.getenv("ELEVENLABS_API_KEY")
        self.voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
        self.volume = max(0.0, min(1.0, volume))
        
        # Check if ElevenLabs is available
        self.backend = TTSBackend.NONE
        if self.elevenlabs_api_key:
            try:
                from elevenlabs.client import ElevenLabs
                self.backend = TTSBackend.ELEVENLABS
            except ImportError:
                print("AudioNarrator: ElevenLabs not installed, audio disabled")
        else:
            print("AudioNarrator: No ElevenLabs API key found, audio disabled")
        
        # TTS client
        self._elevenlabs_client: Optional[Any] = None
        
        # Audio queue and threading
        self._queue: queue.PriorityQueue = queue.PriorityQueue()
        self._playback_thread: Optional[threading.Thread] = None
        self._running = False
        self._current_playback: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        
        # Callbacks
        self.on_start: Optional[Callable[[str], None]] = None
        self.on_end: Optional[Callable[[str], None]] = None
        self.on_interrupt: Optional[Callable[[str], None]] = None
        
        # Statistics
        self._stats = {
            "queued": 0,
            "played": 0,
            "interrupted": 0,
            "errors": 0
        }
        self._stats_lock = threading.Lock()
        
        # Initialize backend
        self._initialize_backend()
    
    def _initialize_backend(self) -> None:
        """Initialize the ElevenLabs TTS backend."""
        if self.backend == TTSBackend.ELEVENLABS:
            self._init_elevenlabs()
    
    def _init_elevenlabs(self) -> bool:
        """Initialize ElevenLabs client.
        
        Returns:
            True if successful
        """
        if not self.elevenlabs_api_key:
            print("AudioNarrator: No ElevenLabs API key")
            self.backend = TTSBackend.NONE
            return False
        
        try:
            from elevenlabs.client import ElevenLabs
            import pygame
            
            # Initialize pygame mixer for audio playback
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            
            self._elevenlabs_client = ElevenLabs(api_key=self.elevenlabs_api_key)
            print("AudioNarrator: Initialized ElevenLabs")
            return True
            
        except Exception as e:
            print(f"AudioNarrator: Failed to initialize ElevenLabs: {e}")
            self.backend = TTSBackend.NONE
            return False
    
    def start(self) -> None:
        """Start the audio narration service."""
        if self._running:
            return
        
        if self.backend == TTSBackend.NONE:
            print("AudioNarrator: No TTS backend available, audio disabled")
            return
        
        self._running = True
        self._stop_event.clear()
        self._playback_thread = threading.Thread(target=self._playback_loop, daemon=True)
        self._playback_thread.start()
        print("AudioNarrator: Started")
    
    def stop(self) -> None:
        """Stop the audio narration service."""
        if not self._running:
            return
        
        self._running = False
        self._stop_event.set()
        
        # Clear queue
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
        
        if self._playback_thread:
            self._playback_thread.join(timeout=2.0)
        
        print("AudioNarrator: Stopped")
    
    def _playback_loop(self) -> None:
        """Main playback loop running in background thread."""
        while self._running and not self._stop_event.is_set():
            try:
                # Get next item with timeout to allow checking stop_event
                item = self._queue.get(timeout=0.5)
                self._play_item(item)
            except queue.Empty:
                continue
            except Exception as e:
                print(f"AudioNarrator: Playback loop error: {e}")
                with self._stats_lock:
                    self._stats["errors"] += 1
    
    def _play_item(self, item: AudioQueueItem) -> None:
        """Play a single audio item.
        
        Args:
            item: AudioQueueItem to play
        """
        if self.on_start:
            try:
                self.on_start(item.alert_id)
            except Exception as e:
                print(f"AudioNarrator: on_start callback error: {e}")
        
        try:
            if self.backend == TTSBackend.ELEVENLABS:
                self._play_elevenlabs(item.text)
            
            with self._stats_lock:
                self._stats["played"] += 1
                
        except Exception as e:
            print(f"AudioNarrator: Playback error: {e}")
            with self._stats_lock:
                self._stats["errors"] += 1
        
        if self.on_end:
            try:
                self.on_end(item.alert_id)
            except Exception as e:
                print(f"AudioNarrator: on_end callback error: {e}")
    
    def _play_elevenlabs(self, text: str) -> None:
        """Play text using ElevenLabs.
        
        Args:
            text: Text to speak
        """
        if not self._elevenlabs_client:
            return
        
        try:
            import io
            import pygame
            from elevenlabs import VoiceSettings
            
            # Use the text_to_speech.convert API with slower speed
            audio_iterator = self._elevenlabs_client.text_to_speech.convert(
                text=text,
                voice_id=self.voice_id,
                model_id="eleven_flash_v2_5",  # Fast model for real-time
                output_format="mp3_44100_128",
                voice_settings=VoiceSettings(
                    speed=0.85,  # Slower speech (0.5-2.0, 1.0 is normal)
                    stability=0.5,
                    similarity_boost=0.5
                )
            )
            
            # Collect all audio chunks into bytes
            audio_bytes = b"".join(chunk for chunk in audio_iterator)
            
            # Play using pygame
            sound = pygame.mixer.Sound(io.BytesIO(audio_bytes))
            sound.set_volume(self.volume)
            sound.play()
            
            # Wait for audio to finish (blocking for alerts)
            time.sleep(sound.get_length())
            
        except Exception as e:
            print(f"AudioNarrator: ElevenLabs error: {e}")
    
    def speak(
        self,
        text: str,
        priority: int = PRIORITY_MEDIUM,
        alert_id: str = "",
        interrupt: bool = False
    ) -> None:
        """Queue text for speech.
        
        Args:
            text: Text to speak
            priority: Priority level (0=critical, 3=low)
            alert_id: Optional ID for tracking
            interrupt: If True, interrupt current playback
        """
        if self.backend == TTSBackend.NONE:
            return
        
        # Skip empty text
        if not text or not text.strip():
            return
        
        item = AudioQueueItem(
            priority=priority,
            timestamp=datetime.now(),
            text=text.strip(),
            alert_id=alert_id,
            interrupt_current=interrupt
        )
        
        self._queue.put(item)
        
        with self._stats_lock:
            self._stats["queued"] += 1
        
        # Handle interrupt
        if interrupt and self._current_playback:
            if self.on_interrupt:
                try:
                    self.on_interrupt(alert_id)
                except Exception as e:
                    print(f"AudioNarrator: on_interrupt callback error: {e}")
    
    def speak_alert(self, alert) -> None:
        """Speak a proactive alert.
        
        Args:
            alert: ProactiveAlert object with audio_text
        """
        from .proactive_alerts import AlertPriority
        
        # Map alert priority to audio priority
        priority_map = {
            AlertPriority.CRITICAL: self.PRIORITY_CRITICAL,
            AlertPriority.HIGH: self.PRIORITY_HIGH,
            AlertPriority.MEDIUM: self.PRIORITY_MEDIUM,
            AlertPriority.LOW: self.PRIORITY_LOW
        }
        
        priority = priority_map.get(alert.priority, self.PRIORITY_MEDIUM)
        interrupt = alert.priority in [AlertPriority.CRITICAL, AlertPriority.HIGH]
        
        self.speak(
            text=alert.get_audio_text(),
            priority=priority,
            alert_id=alert.id,
            interrupt=interrupt
        )
    
    def is_playing(self) -> bool:
        """Check if audio is currently playing.
        
        Returns:
            True if playing
        """
        return self._current_playback is not None and self._current_playback.is_alive()
    
    def get_queue_size(self) -> int:
        """Get number of items in queue.
        
        Returns:
            Queue size
        """
        return self._queue.qsize()
    
    def clear_queue(self) -> None:
        """Clear all pending audio."""
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except queue.Empty:
                break
    
    def get_stats(self) -> Dict[str, Any]:
        """Get audio statistics.
        
        Returns:
            Dict with stats
        """
        with self._stats_lock:
            return dict(self._stats)
    
    def get_backend_info(self) -> Dict[str, Any]:
        """Get information about the current backend.
        
        Returns:
            Dict with backend info
        """
        return {
            "backend": self.backend.value,
            "available": self.backend != TTSBackend.NONE,
            "running": self._running,
            "queue_size": self.get_queue_size(),
            "is_playing": self.is_playing()
        }


class NullAudioNarrator(AudioNarrator):
    """Null object pattern for when audio is disabled."""
    
    def __init__(self):
        """Initialize null narrator."""
        super().__init__()
    
    def start(self) -> None:
        """No-op."""
        pass
    
    def stop(self) -> None:
        """No-op."""
        pass
    
    def speak(self, text: str, priority: int = 2, alert_id: str = "", interrupt: bool = False) -> None:
        """No-op."""
        pass
    
    def speak_alert(self, alert) -> None:
        """No-op."""
        pass
