#!/usr/bin/env python3
"""
Batch Audio to M4A Converter
Converts multiple audio files in a directory to M4A format.
"""

import os
import sys
from pathlib import Path
from convert_to_m4a import convert_to_m4a


def batch_convert(directory, audio_bitrate="192k", extensions=None):
    """
    Batch convert all audio files in a directory to M4A format.
    
    Args:
        directory (str): Path to directory containing audio files
        audio_bitrate (str): Audio bitrate for conversion (default: 192k)
        extensions (list): List of file extensions to convert (default: common audio formats)
    
    Returns:
        tuple: (successful_count, failed_count)
    """
    if extensions is None:
        extensions = ['.opus', '.mp3', '.wav', '.flac', '.ogg', '.aac', '.wma', '.m4a']
    
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
    
    print(f"Found {len(audio_files)} audio file(s) to convert")
    print("=" * 60)
    
    successful = 0
    failed = 0
    
    for i, input_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}]")
        
        # Skip if already m4a
        if input_file.suffix.lower() == '.m4a':
            print(f"Skipping {input_file.name} (already M4A)")
            continue
        
        output_file = input_file.with_suffix('.m4a')
        
        if convert_to_m4a(str(input_file), str(output_file), audio_bitrate):
            successful += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Conversion complete!")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total: {len(audio_files)}")
    
    return (successful, failed)


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python batch_convert.py <directory> [bitrate]")
        print("\nExamples:")
        print("  python batch_convert.py /path/to/audio/files")
        print("  python batch_convert.py /path/to/audio/files 256k")
        print("\nDefault bitrate: 192k")
        print("\nSupported formats: opus, mp3, wav, flac, ogg, aac, wma")
        sys.exit(1)
    
    directory = sys.argv[1]
    audio_bitrate = sys.argv[2] if len(sys.argv) > 2 else "192k"
    
    successful, failed = batch_convert(directory, audio_bitrate)
    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
