from pathlib import Path
from typing import Dict, List
import questionary

def check_existing_subtitles(mp3_path: Path) -> Dict[str, bool]:
    """
    Check if subtitle files already exist for the given MP3 file.
    Returns dict with format as key and existence as boolean value.
    """
    base_name = mp3_path.stem
    parent_dir = mp3_path.parent
    
    existing = {
        'srt': (parent_dir / f"{base_name}.srt").exists(),
        'lrc': (parent_dir / f"{base_name}.lrc").exists()
    }
    
    return existing

def get_existing_subtitle_files(mp3_path: Path) -> List[str]:
    """Get list of existing subtitle formats for the MP3 file."""
    existing = check_existing_subtitles(mp3_path)
    return [fmt for fmt, exists in existing.items() if exists]

def handle_existing_subtitles(mp3_path: Path, requested_format: str) -> str:
    """
    Handle the case where subtitle files already exist.
    Returns the action to take: 'overwrite', 'skip', or 'cancel'
    """
    existing = check_existing_subtitles(mp3_path)
    existing_formats = get_existing_subtitle_files(mp3_path)
    
    if not existing_formats:
        # No existing subtitles, proceed normally
        return 'proceed'
    
    if existing[requested_format]:
        # The requested format already exists
        print(f"\n⚠️  A {requested_format.upper()} file already exists for this MP3:")
        print(f"   {mp3_path.parent / f'{mp3_path.stem}.{requested_format}'}")
        
        action = questionary.select(
            "What would you like to do?",
            choices=[
                "Overwrite the existing file",
                "Skip this file",
                "Cancel operation"
            ]
        ).ask()
        
        if not action:
            return 'cancel'
        elif "Overwrite" in action:
            return 'overwrite'
        elif "Skip" in action:
            return 'skip'
        else:
            return 'cancel'
    else:
        # Different format exists, but not the requested one
        existing_list = ", ".join([f.upper() for f in existing_formats])
        print(f"\n📄 This MP3 already has subtitle files: {existing_list}")
        print(f"   You're requesting: {requested_format.upper()}")
        
        action = questionary.select(
            "Do you want to generate the additional subtitle format?",
            choices=[
                "Yes, generate the new format",
                "No, skip this file",
                "Cancel operation"
            ]
        ).ask()
        
        if not action:
            return 'cancel'
        elif "Yes" in action:
            return 'proceed'
        elif "skip" in action:
            return 'skip'
        else:
            return 'cancel'

def display_subtitle_status(mp3_path: Path):
    """Display the current subtitle status for an MP3 file."""
    existing_formats = get_existing_subtitle_files(mp3_path)
    
    if existing_formats:
        formats_str = ", ".join([f.upper() for f in existing_formats])
        print(f"📄 Existing subtitles: {formats_str}")
    else:
        print("📄 No existing subtitle files")