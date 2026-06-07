#!/usr/bin/env python3
"""
Drum Removal Tool
Removes drums from audio files using Demucs (audio source separation).
"""

import subprocess
import sys
import os
from pathlib import Path
import shutil


def check_dependencies():
    """Check if required dependencies are installed."""
    # Check for demucs
    try:
        result = subprocess.run(
            ['demucs', '--help'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return True
    except FileNotFoundError:
        return False


def install_demucs():
    """Provide installation instructions for Demucs."""
    print("\n✗ Demucs not found!")
    print("\nTo install Demucs, run:")
    print("  pip3 install demucs")
    print("\nOr with conda:")
    print("  conda install -c conda-forge demucs")
    print("\nNote: Demucs works best with a GPU, but also works on CPU (slower)")


def remove_drums(input_file, output_file=None, model="htdemucs", keep_temp=False):
    """
    Remove drums from an audio file using Demucs.
    
    Args:
        input_file (str): Path to the input audio file (m4a, mp3, wav, etc.)
        output_file (str, optional): Path to the output file.
                                    If None, uses input filename with '_no_drums' suffix
        model (str): Demucs model to use (default: htdemucs)
                    Options: htdemucs, htdemucs_ft, mdx_extra
        keep_temp (bool): Keep temporary separated files (default: False)
    
    Returns:
        bool: True if successful, False otherwise
    """
    # Validate input file exists
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        return False
    
    # Check dependencies
    if not check_dependencies():
        install_demucs()
        return False
    
    input_path = Path(input_file)
    
    # Generate output filename if not provided
    if output_file is None:
        output_file = input_path.parent / f"{input_path.stem}_no_drums{input_path.suffix}"
    
    output_path = Path(output_file)
    
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")
    print(f"Model: {model}")
    print("\nProcessing... This may take a while depending on file length and hardware.")
    
    # Create temporary directory for separation
    temp_dir = input_path.parent / "demucs_temp"
    
    try:
        # Run Demucs to separate audio into stems
        # Demucs separates into: vocals, drums, bass, other
        cmd = [
            'demucs',
            '--two-stems=drums',  # Only separate drums from everything else
            '-n', model,
            '-o', str(temp_dir),
            str(input_file)
        ]
        
        print(f"\nRunning Demucs...")
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        # Find the no_drums output file
        # Demucs outputs to: temp_dir/model_name/filename/no_drums.wav
        separated_dir = temp_dir / model / input_path.stem
        no_drums_file = separated_dir / "no_drums.wav"
        
        if not no_drums_file.exists():
            print(f"Error: Expected output file not found at {no_drums_file}")
            return False
        
        # Convert to desired output format if not WAV
        if output_path.suffix.lower() != '.wav':
            print(f"\nConverting to {output_path.suffix}...")
            convert_cmd = [
                'ffmpeg',
                '-i', str(no_drums_file),
                '-c:a', 'aac',
                '-b:a', '256k',
                '-y',
                str(output_path)
            ]
            
            subprocess.run(
                convert_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
        else:
            # Just copy the WAV file
            shutil.copy2(no_drums_file, output_path)
        
        print(f"\n✓ Drums removed successfully!")
        print(f"  Output saved to: {output_path}")
        
        # Clean up temporary files
        if not keep_temp:
            print("\nCleaning up temporary files...")
            shutil.rmtree(temp_dir)
        else:
            print(f"\nTemporary files kept in: {separated_dir}")
            print(f"  - no_drums.wav (music without drums)")
            print(f"  - drums.wav (isolated drums)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Processing failed!")
        print(f"Error: {e.stderr}")
        return False
    except FileNotFoundError as e:
        print(f"\n✗ Error: Required tool not found!")
        print(f"Make sure both demucs and ffmpeg are installed.")
        return False
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        return False
    finally:
        # Clean up on error
        if not keep_temp and temp_dir.exists():
            try:
                shutil.rmtree(temp_dir)
            except:
                pass


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python remove_drums.py <input_file> [output_file] [options]")
        print("\nExamples:")
        print("  python remove_drums.py audio.m4a")
        print("  python remove_drums.py audio.m4a no_drums.m4a")
        print("  python remove_drums.py audio.m4a --keep-temp")
        print("\nOptions:")
        print("  --keep-temp    Keep temporary separated files")
        print("  --model MODEL  Specify Demucs model (htdemucs, htdemucs_ft, mdx_extra)")
        print("\nModels:")
        print("  htdemucs      - Default, good balance of quality and speed")
        print("  htdemucs_ft   - Fine-tuned version, slightly better quality")
        print("  mdx_extra     - Highest quality, slower")
        print("\nNote: First run will download the model (~200-300MB)")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = None
    keep_temp = False
    model = "htdemucs"
    
    # Parse arguments
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == '--keep-temp':
            keep_temp = True
        elif arg == '--model' and i + 1 < len(sys.argv):
            model = sys.argv[i + 1]
            i += 1
        elif output_file is None and not arg.startswith('--'):
            output_file = arg
        i += 1
    
    success = remove_drums(input_file, output_file, model, keep_temp)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
