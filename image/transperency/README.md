# Image Transparency Tool

A powerful Python tool for processing image transparency, including adding, removing, and modifying alpha channels.

## Features

- **Add Transparency**: Convert images to RGBA and adjust opacity
- **Remove Transparency**: Flatten images with customizable background colors
- **Color to Alpha**: Make specific colors transparent with tolerance control
- **Extract Alpha Channel**: Save alpha channel as separate grayscale image
- **Batch Processing**: Process entire directories with recursive support
- **Progress Tracking**: Visual progress bars for batch operations
- **Error Handling**: Graceful error handling with detailed summaries

## Installation

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Operations

**Add transparency with opacity:**
```bash
python transparency.py add input.jpg --opacity 80 --output output.png
```

**Remove transparency with custom background:**
```bash
python transparency.py remove input.png --background "#FF0000" --output output.jpg
```

**Make white pixels transparent:**
```bash
python transparency.py color-to-alpha input.png --color white --tolerance 10
```

**Extract alpha channel:**
```bash
python transparency.py extract-alpha input.png --output alpha.png
```

### Batch Processing

**Process entire directory:**
```bash
python transparency.py add ./images/ --opacity 75 --output-dir ./processed/
```

**Recursive directory processing:**
```bash
python transparency.py color-to-alpha ./images/ --color white --recursive --output-dir ./output/
```

## Command-Line Options

```
positional arguments:
  {add,remove,color-to-alpha,extract-alpha}
                        Operation to perform
  input                 Input file or directory path

optional arguments:
  -h, --help            Show help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file path (for single file processing)
  --output-dir OUTPUT_DIR
                        Output directory (for batch processing)
  --opacity OPACITY     Opacity level (0-100%, default: 100)
  --background BACKGROUND
                        Background color for transparency removal (default: white)
  --color COLOR         Color to make transparent (default: white)
  --tolerance TOLERANCE
                        Color matching tolerance (0-255, default: 10)
  --suffix SUFFIX       Suffix for output filenames (default: _transparent)
  -r, --recursive       Process directories recursively
  -v, --verbose         Enable verbose logging
```

## Supported Formats

- PNG
- JPEG
- WEBP
- GIF
- BMP
- TIFF

## Examples

### Remove white background from logo:
```bash
python transparency.py color-to-alpha logo.jpg --color white --tolerance 15 --output logo_transparent.png
```

### Batch process with 50% opacity:
```bash
python transparency.py add ./screenshots/ --opacity 50 --recursive --output-dir ./watermarked/
```

### Flatten transparent PNGs to JPEGs:
```bash
python transparency.py remove ./images/ --background white --output-dir ./flattened/
```

## Notes

- Output format is automatically determined by operation (PNG for transparency, JPEG for flattened)
- Original files are never overwritten unless explicitly specified
- Progress bars show real-time processing status for batch operations
- Summary reports display total files processed and any errors encountered

## License

MIT License
