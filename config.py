from pathlib import Path

# Configuration constants
HOME = Path.home()
MUSIC_DIR = HOME / "Music"
WHISPER_CLI = HOME / "Workspace/whisper.cpp/build/bin/whisper-cli"
WHISPER_MODEL = HOME / "Workspace/whisper.cpp/models/ggml-medium.bin"