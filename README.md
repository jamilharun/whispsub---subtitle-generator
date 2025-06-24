````markdown
# WhispSub 🎵📝

**WhispSub** is a Python tool that automatically generates subtitle files (SRT/LRC) from MP3 audio files using whisper.cpp (OpenAI's Whisper implementation).

## ✨ Features

- Single file or batch processing
- SRT/LRC subtitle generation
- Smart duplicate detection
- Interactive file selection

## 🚀 Quick Setup

### 1. Clone this repository

```bash
git clone https://github.com/jamilharun/WhispSub.git
cd WhispSub
```
````

### 2. Set up Python environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Install whisper.cpp separately

WhispSub requires [whisper.cpp](https://github.com/ggerganov/whisper.cpp) to be installed separately:

```bash
git clone https://github.com/ggerganov/whisper.cpp.git
cd whisper.cpp
make

# Download a model (medium recommended)
./models/download-ggml-model.sh medium
```

### 4. Configure paths

Edit `config.py` to point to your installations:

```python
WHISPER_CLI = "/path/to/whisper.cpp/main"
WHISPER_MODEL = "/path/to/whisper.cpp/models/ggml-medium.bin"
MUSIC_DIR = "/path/to/your/music/folder"
```

### 5. Run WhispSub

```bash
python main.py
```

## 🔧 Dependencies

- Python 3.8+
- FFmpeg (`sudo apt install ffmpeg` / `brew install ffmpeg`)
- [whisper.cpp](https://github.com/ggerganov/whisper.cpp)

## 🤝 Contributing

PRs welcome! Please open an issue first to discuss changes.

## 📄 License

MIT

```

Key improvements:
1. **Clear separation** between WhispSub setup and whisper.cpp installation
2. **Direct link** to whisper.cpp repository
3. **Simplified flow** with numbered steps
4. **Removed redundant details** about models (users can check whisper.cpp's README)
5. **Better emphasis** on the virtual environment setup
6. **Cleaner configuration** instructions

The document now has better focus while maintaining all critical information. Users can clearly see:
1. How to set up the Python project
2. Where to get whisper.cpp
3. How to connect the two
```
