import subprocess
import tempfile
from pathlib import Path
from config import WHISPER_CLI, WHISPER_MODEL
from subtitle_checker import handle_existing_subtitles

def convert_mp3_to_wav(mp3_path: Path, wav_path: Path) -> bool:
    """Convert MP3 file to WAV format suitable for whisper."""
    print("\n🎙️ Converting MP3 to WAV...")
    
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",
        "-i", str(mp3_path),
        "-ar", "16000",
        "-ac", "1",
        "-hide_banner",
        "-loglevel", "error",  # Show errors but not info
        str(wav_path)
    ]
    
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error converting MP3 to WAV: {e}")
        return False

def generate_subtitles(mp3_path: Path, subtitle_format: str) -> bool:
    """Generate subtitles from MP3 file using whisper."""
    
    # Check for existing subtitles and get user preference
    action = handle_existing_subtitles(mp3_path, subtitle_format)
    
    if action == 'skip':
        print(f"⏭️  Skipping {mp3_path.name}")
        return True  # Return True as it's not an error, just a skip
    elif action == 'cancel':
        print("❌ Operation cancelled by user")
        return False
    elif action not in ['proceed', 'overwrite']:
        print(f"❌ Unknown action: {action}")
        return False
    
    # If we get here, proceed with generation (either new file or overwrite)
    if action == 'overwrite':
        print(f"🔄 Overwriting existing {subtitle_format.upper()} file...")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        wav_path = Path(tmpdir) / "converted.wav"
        
        # Convert MP3 to WAV
        if not convert_mp3_to_wav(mp3_path, wav_path):
            return False
        
        # Determine output path
        output_path = mp3_path.parent / f"{mp3_path.stem}.{subtitle_format}"
        
        print(f"📢 Running whisper-cli on {wav_path.name}...\n")
        
        cmd = [
            str(WHISPER_CLI),
            "-m", str(WHISPER_MODEL),
            "-f", str(wav_path),
            f"--output-{subtitle_format}",
            "-of", str(output_path.with_suffix(''))  # Output to same directory as MP3
        ]
        
        try:
            subprocess.run(cmd, check=True)
            print(f"✅ {subtitle_format.upper()} file generated at {output_path}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Error running whisper-cli: {e}")
            return False