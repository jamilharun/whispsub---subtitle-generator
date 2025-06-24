import questionary
from pathlib import Path
from typing import List, Dict, Tuple
from file_utils import list_mp3_files
from subtitle_checker import check_existing_subtitles, get_existing_subtitle_files
from audio_processor import generate_subtitles

class BatchProcessor:
    def __init__(self, folder_path: Path, subtitle_format: str):
        self.folder_path = folder_path
        self.subtitle_format = subtitle_format
        self.mp3_files = list_mp3_files(folder_path)
        self.results = {'processed': 0, 'skipped': 0, 'failed': 0, 'total': 0}
    
    def analyze_folder(self) -> Dict[str, List[str]]:
        """Analyze all MP3 files in the folder and categorize them."""
        analysis = {
            'needs_processing': [],      # Files that need the requested format
            'already_has_format': [],    # Files that already have the requested format
            'has_other_formats': [],     # Files that have other subtitle formats
            'no_subtitles': []          # Files with no subtitles at all
        }
        
        for mp3_file in self.mp3_files:
            mp3_path = self.folder_path / mp3_file
            existing = check_existing_subtitles(mp3_path)
            existing_formats = get_existing_subtitle_files(mp3_path)
            
            if existing[self.subtitle_format]:
                analysis['already_has_format'].append(mp3_file)
            elif existing_formats:
                analysis['has_other_formats'].append(mp3_file)
                analysis['needs_processing'].append(mp3_file)
            else:
                analysis['no_subtitles'].append(mp3_file)
                analysis['needs_processing'].append(mp3_file)
        
        return analysis
    
    def display_analysis(self, analysis: Dict[str, List[str]]):
        """Display the folder analysis to the user."""
        total_files = len(self.mp3_files)
        needs_processing = len(analysis['needs_processing'])
        already_has = len(analysis['already_has_format'])
        
        print(f"\n📊 Folder Analysis:")
        print(f"   Total MP3 files: {total_files}")
        print(f"   Need {self.subtitle_format.upper()} processing: {needs_processing}")
        print(f"   Already have {self.subtitle_format.upper()}: {already_has}")
        
        if analysis['no_subtitles']:
            print(f"   No subtitles: {len(analysis['no_subtitles'])}")
        
        if analysis['has_other_formats']:
            print(f"   Have other formats: {len(analysis['has_other_formats'])}")
        
        # Show some examples
        if analysis['already_has_format']:
            print(f"\n   Files with existing {self.subtitle_format.upper()}:")
            for file in analysis['already_has_format'][:3]:
                print(f"   • {file}")
            if len(analysis['already_has_format']) > 3:
                print(f"   • ... and {len(analysis['already_has_format']) - 3} more")
    
    def get_processing_strategy(self, analysis: Dict[str, List[str]]) -> str:
        """Get user's strategy for handling existing files."""
        if not analysis['already_has_format']:
            # No conflicts, can proceed directly
            return 'proceed'
        
        print(f"\n⚠️  Found {len(analysis['already_has_format'])} files that already have {self.subtitle_format.upper()} subtitles.")
        
        strategy = questionary.select(
            "How do you want to handle files that already have the requested format?",
            choices=[
                "Skip files that already have the format",
                "Overwrite all existing files",
                "Ask for each file individually",
                "Cancel batch operation"
            ]
        ).ask()
        
        if not strategy:
            return 'cancel'
        elif "Skip" in strategy:
            return 'skip_existing'
        elif "Overwrite" in strategy:
            return 'overwrite_all'
        elif "Ask" in strategy:
            return 'ask_each'
        else:
            return 'cancel'
    
    def process_all_files(self) -> Dict[str, int]:
        """Process all MP3 files in the folder according to user preferences."""
        analysis = self.analyze_folder()
        
        if not self.mp3_files:
            print("No MP3 files found in the folder.")
            return self.results
        
        self.display_analysis(analysis)
        
        if not analysis['needs_processing'] and not analysis['already_has_format']:
            print("No files to process!")
            return self.results
        
        strategy = self.get_processing_strategy(analysis)
        
        if strategy == 'cancel':
            print("❌ Batch operation cancelled.")
            return self.results
        
        # Determine which files to process
        files_to_process = []
        
        if strategy == 'skip_existing':
            files_to_process = analysis['needs_processing']
            self.results['skipped'] = len(analysis['already_has_format'])
        elif strategy == 'overwrite_all':
            files_to_process = self.mp3_files
        elif strategy == 'ask_each':
            files_to_process = self.mp3_files
        elif strategy == 'proceed':
            files_to_process = analysis['needs_processing']
        
        self.results['total'] = len(files_to_process)
        
        if not files_to_process:
            print("No files selected for processing.")
            return self.results
        
        # Confirm before starting
        if strategy != 'ask_each':
            confirm = questionary.confirm(
                f"Process {len(files_to_process)} files? This may take a while."
            ).ask()
            
            if not confirm:
                print("❌ Operation cancelled.")
                return self.results
        
        # Process files
        print(f"\n🚀 Starting batch processing of {len(files_to_process)} files...\n")
        
        for i, mp3_file in enumerate(files_to_process, 1):
            mp3_path = self.folder_path / mp3_file
            
            print(f"[{i}/{len(files_to_process)}] Processing: {mp3_file}")
            
            # Handle individual file strategy
            if strategy == 'ask_each':
                existing = check_existing_subtitles(mp3_path)
                if existing[self.subtitle_format]:
                    proceed = questionary.confirm(
                        f"File already has {self.subtitle_format.upper()}. Overwrite?"
                    ).ask()
                    if not proceed:
                        print("   ⏭️  Skipped")
                        self.results['skipped'] += 1
                        continue
            
            # Process the file
            success = generate_subtitles(mp3_path, self.subtitle_format)
            
            if success:
                self.results['processed'] += 1
                print(f"   ✅ Completed ({self.results['processed']}/{len(files_to_process)})")
            else:
                self.results['failed'] += 1
                print(f"   ❌ Failed")
            
            print()  # Empty line for readability
        
        return self.results
    
    def display_summary(self):
        """Display the final processing summary."""
        print("="*50)
        print("📋 BATCH PROCESSING SUMMARY")
        print("="*50)
        print(f"Total files processed: {self.results['processed']}")
        print(f"Files skipped: {self.results['skipped']}")
        print(f"Files failed: {self.results['failed']}")
        print(f"Success rate: {(self.results['processed']/(self.results['processed']+self.results['failed'])*100):.1f}%" if (self.results['processed']+self.results['failed']) > 0 else "N/A")
        print("="*50)

def batch_process_folder(folder_path: Path, subtitle_format: str):
    """Main function to batch process all MP3 files in a folder."""
    processor = BatchProcessor(folder_path, subtitle_format)
    results = processor.process_all_files()
    processor.display_summary()
    return results