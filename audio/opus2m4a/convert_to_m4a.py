#!/usr/bin/env python3
"""
Audio to M4A Converter
Converts audio files to M4A format using ffmpeg.
"""

import subprocess
import sys
import os
from pathlib import Path


def convert_to_m4a(input_file, output_file=None, audio_bitrate="192k"):
    """
    Convert an audio file to M4A format.
    
    Args:
        input_file (str): Path to the input audio file
        output_file (str, optional): Path to the output M4A file. 
                                    If None, uses input filename with .m4a extension
        audio_bitrate (str): Audio bitrate for conversion (default: 192k)
    
    Returns:
        bool: True if conversion successful, False otherwise
    """
    # Validate input file exists
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return False
    
    # Generate output filename if not provided
    if output_file is None:
        input_path = Path(input_file)
        output_file = input_path.with_suffix('.m4a')
    
    print(f"Converting: {input_file}")
    print(f"Output: {output_file}")
    print(f"Bitrate: {audio_bitrate}")
    
    # Build ffmpeg command
    # -i: input file
    # -c:a aac: use AAC codec for audio
    # -b:a: audio bitrate
    # -vn: disable video recording
    # -y: overwrite output file without asking
    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-c:a', 'aac',
        '-b:a', audio_bitrate,
        '-vn',
        '-y',
        output_file
    ]
    
    try:
        # Run ffmpeg
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print(f"\n✓ Conversion successful!")
        print(f"  Output saved to: {output_file}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Conversion failed!")
        print(f"Error: {e.stderr}")
        return False
    except FileNotFoundError:
        print("\n✗ Error: ffmpeg not found!")
        print("Please install ffmpeg:")
        print("  macOS: brew install ffmpeg")
        print("  Linux: sudo apt-get install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/download.html")
        return False


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python convert_to_m4a.py <input_file> [output_file] [bitrate]")
        print("\nExamples:")
        print("  python convert_to_m4a.py audio.opus")
        print("  python convert_to_m4a.py audio.opus output.m4a")
        print("  python convert_to_m4a.py audio.opus output.m4a 256k")
        print("\nDefault bitrate: 192k")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    audio_bitrate = sys.argv[3] if len(sys.argv) > 3 else "192k"
    
    success = convert_to_m4a(input_file, output_file, audio_bitrate)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
