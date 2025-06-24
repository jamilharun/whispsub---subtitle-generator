import subprocess
from config import WHISPER_CLI, WHISPER_MODEL

def check_prerequisites() -> bool:
    """Check if all required tools and files are available."""
    # Check whisper-cli
    if not WHISPER_CLI.exists():
        print(f"Error: whisper-cli not found at {WHISPER_CLI}")
        return False
    
    # Check whisper model
    if not WHISPER_MODEL.exists():
        print(f"Error: model not found at {WHISPER_MODEL}")
        return False
    
    # Check ffmpeg
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
    except FileNotFoundError:
        print("Error: ffmpeg is not installed or not in PATH")
        return False
    
    return True