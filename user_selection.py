import questionary
from pathlib import Path
from typing import Optional, Tuple
from config import MUSIC_DIR
from file_utils import list_folders, list_mp3_files_with_subtitle_info, extract_mp3_filename
from subtitle_checker import display_subtitle_status

import questionary
from pathlib import Path
from typing import Optional, Tuple, Union
from config import MUSIC_DIR
from file_utils import list_folders, list_mp3_files_with_subtitle_info, extract_mp3_filename
from subtitle_checker import display_subtitle_status

def select_processing_mode() -> str:
    """Choose between single file or batch processing."""
    mode = questionary.select(
        "Choose processing mode:",
        choices=[
            "Process single MP3 file",
            "Process all MP3 files in folder (batch mode)"
        ]
    ).ask()
    
    if not mode:
        return 'cancel'
    elif "single" in mode:
        return 'single'
    else:
        return 'batch'

def select_music_file() -> Optional[Tuple[Path, str, str]]:
    """
    Interactive selection of music file(s) and subtitle format.
    Returns tuple of (mp3_path_or_folder, subtitle_format, processing_mode) or None if cancelled.
    """
    # Step 0: Choose processing mode
    processing_mode = select_processing_mode()
    if processing_mode == 'cancel':
        return None
    
    # Step 1: Choose Top-Level Folder
    folders = list_folders(MUSIC_DIR)
    if not folders:
        print("No folders found in ~/Music.")
        return None

    selected_folder = questionary.select(
        "Choose a folder in ~/Music:",
        choices=folders
    ).ask()
    
    if not selected_folder:
        return None
    
    folder_path = MUSIC_DIR / selected_folder

    # Step 2: Choose Subfolder (if available)
    subfolders = list_folders(folder_path)
    if subfolders:
        selected_subfolder = questionary.select(
            f"Choose a subfolder in {selected_folder}:",
            choices=subfolders
        ).ask()
        
        if not selected_subfolder:
            return None
            
        subfolder_path = folder_path / selected_subfolder
    else:
        subfolder_path = folder_path

    # Step 3: Handle single file vs batch mode
    if processing_mode == 'single':
        # Single file selection
        mp3_files_with_info = list_mp3_files_with_subtitle_info(subfolder_path)
        if not mp3_files_with_info:
            print("No MP3 files in that folder.")
            return None

        selected_mp3_display = questionary.select(
            "Choose an MP3 file (existing subtitles shown in brackets):",
            choices=mp3_files_with_info
        ).ask()
        
        if not selected_mp3_display:
            return None

        # Extract the actual filename from the display name
        selected_mp3 = extract_mp3_filename(selected_mp3_display)
        mp3_path = subfolder_path / selected_mp3
        
        # Display current subtitle status
        print(f"\n🎵 Selected: {mp3_path.name}")
        display_subtitle_status(mp3_path)
        
        target_path = mp3_path
    else:
        # Batch mode - use the folder path
        from file_utils import list_mp3_files
        mp3_count = len(list_mp3_files(subfolder_path))
        if mp3_count == 0:
            print("No MP3 files in that folder.")
            return None
        
        print(f"\n📁 Selected folder: {subfolder_path}")
        print(f"🎵 Found {mp3_count} MP3 files for batch processing")
        
        target_path = subfolder_path

    # Step 4: Choose Subtitle Format
    subtitle_format = questionary.select(
        "Choose subtitle format to generate:",
        choices=["srt", "lrc"]
    ).ask()
    
    if not subtitle_format:
        return None

    return target_path, subtitle_format, processing_mode