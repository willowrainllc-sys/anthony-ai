# --- EMPIRE PROVIDER INTERFACE: UNIVERSAL WORKER PROTOCOL v1.1 ---
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class VideoProvider(ABC):
    @abstractmethod
    async def generate_video(self, prompt: str, duration: int, bible: Dict[str, Any] = None) -> Optional[str]:
        """Returns path to generated video file."""
        pass

class ImageProvider(ABC):
    @abstractmethod
    async def generate_image(self, prompt: str, bible: Dict[str, Any] = None) -> Optional[str]:
        """Returns path to generated image file."""
        pass

class AudioProvider(ABC):
    @abstractmethod
    async def generate_speech(self, text: str, voice: str) -> Optional[str]:
        """Returns path to generated speech file."""
        pass

    @abstractmethod
    async def generate_music(self, mood: str, duration: int) -> Optional[str]:
        """Returns path to generated music file."""
        pass

class TranscriptionProvider(ABC):
    @abstractmethod
    async def transcribe_audio(self, audio_path: str) -> Dict[str, Any]:
        """Returns timestamped caption segments."""
        pass

class LLMProvider(ABC):
    @abstractmethod
    async def generate_text(self, prompt: str, system_msg: str = "", format: str = "text") -> Optional[str]:
        """Returns generated text or JSON."""
        pass

class VideoEditorProvider(ABC):
    @abstractmethod
    async def assemble_video(self, manifest: Dict[str, Any], output_path: str) -> bool:
        """Assembles clips, audio, and captions into a final master."""
        pass
