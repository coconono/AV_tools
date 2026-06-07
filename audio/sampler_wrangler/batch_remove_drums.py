#!/usr/bin/env python3
"""
Batch Drum Removal Tool
Removes drums from multiple audio files in a directory.
"""

import os
import sys
from pathlib import Path
from remove_drums import remove_drums


def batch_remove_drums(directory, model="htdemucs", extensions=None, keep_temp=False):
    """
    Batch remove drums from all audio files in a directory.
    
    Args:
        directory (str): Path to directory containing audio files
        model (str): Demucs model to use (default: htdemucs)
        extensions (list): List of file extensions to process (default: common audio formats)
        keep_temp (bool): Keep temporary separated files (default: False)
    
    Returns:
        tuple: (successful_count, failed_count)
    """
    if extensions is None:
        extensions = ['.m4a', '.mp3', '.wav', '.flac', '.ogg', '.opus']
    
    # Validate directory exists
    if not os.path.isdir(directory):
        print(f"Error: Directory '{directory}' does not exist.")
        return (0, 0)
    
    # Find all audio files
    audio_files = []
    for ext in extensions:
        audio_files.extend(Path(directory).glob(f"*{ext}"))
    
    if not audio_files:
        print(f"No audio files found in '{directory}'")
        print(f"Looking for extensions: {', '.join(extensions)}")
        return (0, 0)
    
    print(f"Found {len(audio_files)} audio file(s) to process")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for i, input_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}] Processing: {input_file.name}")
        print("-" * 60)
        
        output_file = input_file.parent / f"{input_file.stem}_no_drums{input_file.suffix}"
        
        # Skip if output already exists
        if output_file.exists():
            print(f"Skipping - output already exists: {output_file.name}")
            continue
        
        if remove_drums(str(input_file), str(output_file), model, keep_temp):
            successful += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Processing complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(audio_files)}")
    
    return (successful, failed)


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python batch_remove_drums.py <directory> [options]")
        print("\nExamples:")
        print("  python batch_remove_drums.py /path/to/audio/files")
        print("  python batch_remove_drums.py /path/to/audio/files --model htdemucs_ft")
        print("\nOptions:")
        print("  --model MODEL  Specify Demucs model (htdemucs, htdemucs_ft, mdx_extra)")
        print("  --keep-temp    Keep temporary separated files")
        print("\nSupported formats: m4a, mp3, wav, flac, ogg, opus")
        sys.exit(1)
    
    directory = sys.argv[1]
    model = "htdemucs"
    keep_temp = False
    
    # Parse arguments
    for i in range(2, len(sys.argv)):
        arg = sys.argv[i]
        if arg == '--keep-temp':
            keep_temp = True
        elif arg == '--model' and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
    
    successful, failed = batch_remove_drums(directory, model, keep_temp=keep_temp)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
