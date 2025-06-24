#!/usr/bin/env python3
"""
WhispSub - Generate subtitles from MP3 files using Whisper
Refactored version with modular components and batch processing
"""

from pathlib import Path
from prerequisites import check_prerequisites
from user_selection import select_music_file
from audio_processor import generate_subtitles
from batch_processor import batch_process_folder

def main():
    """Main application entry point."""
    # Check prerequisites
    if not check_prerequisites():
        return
    
    # Get user selection
    selection = select_music_file()
    if not selection:
        print("Operation cancelled.")
        return
    
    target_path, subtitle_format, processing_mode = selection
    
    if processing_mode == 'single':
        # Single file processing
        print(f"\n🎯 Processing single file: {target_path.name}")
        success = generate_subtitles(target_path, subtitle_format)
        
        if success:
            print("\n🎉 Subtitle generation completed successfully!")
        else:
            print("\n❌ Subtitle generation failed.")
    
    elif processing_mode == 'batch':
        # Batch processing
        print(f"\n🎯 Starting batch processing of folder: {target_path}")
        results = batch_process_folder(target_path, subtitle_format)
        
        if results['processed'] > 0:
            print("\n🎉 Batch processing completed!")
        else:
            print("\n⚠️  No files were processed.")

if __name__ == "__main__":
    main()