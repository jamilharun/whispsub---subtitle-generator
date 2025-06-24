from pathlib import Path
from typing import List
from subtitle_checker import get_existing_subtitle_files

def list_folders(directory: Path) -> List[str]:
    """List all folders in a directory, sorted alphabetically."""
    folders = [f.name for f in directory.iterdir() if f.is_dir()]
    folders.sort()
    return folders

def list_mp3_files(folder_path: Path) -> List[str]:
    """List all MP3 files in a folder, sorted alphabetically."""
    mp3s = [f.name for f in folder_path.glob("*.mp3")]
    mp3s.sort()
    return mp3s

def list_mp3_files_with_subtitle_info(folder_path: Path) -> List[str]:
    """List MP3 files with subtitle status information."""
    mp3_files = []
    for mp3_file in folder_path.glob("*.mp3"):
        existing_formats = get_existing_subtitle_files(mp3_file)
        if existing_formats:
            formats_str = ",".join([f.upper() for f in existing_formats])
            display_name = f"{mp3_file.name} [{formats_str}]"
        else:
            display_name = mp3_file.name
        mp3_files.append(display_name)
    
    mp3_files.sort()
    return mp3_files

def extract_mp3_filename(display_name: str) -> str:
    """Extract the actual MP3 filename from the display name with subtitle info."""
    # Remove the subtitle info part (e.g., " [SRT,LRC]")
    if " [" in display_name:
        return display_name.split(" [")[0]
    return display_name