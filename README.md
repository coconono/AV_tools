# AV Tools

A collection of Python-based audio and visual processing utilities for common multimedia manipulation tasks.

## 📁 Project Structure

```
AV_tools/
├── audio/
│   └── opus2m4a/          # Audio conversion and manipulation tools
│       ├── convert_to_m4a.py
│       ├── extract_vocals.py
│       ├── remove_drums.py
│       └── batch_*.py     # Batch processing variants
│
└── image/
    └── transperency/      # Image transparency processing
        └── transparency.py
```

## 🎵 Audio Tools

Located in `audio/opus2m4a/`, these tools provide:

- **Audio Format Conversion**: Convert various audio formats to M4A
- **Vocal Extraction**: AI-powered vocal isolation from audio tracks
- **Drum Removal**: Remove drum tracks using deep learning models
- **Batch Processing**: Process multiple files at once

**Key Dependencies**: ffmpeg, demucs, torchaudio

📖 [Full Audio Tools Documentation](audio/opus2m4a/README.md)

## 🖼️ Image Tools

Located in `image/transperency/`, these tools provide:

- **Add/Remove Transparency**: Adjust image opacity and alpha channels
- **Color-to-Alpha**: Make specific colors transparent with tolerance control
- **Extract Alpha Channel**: Save alpha masks as separate images
- **Batch Processing**: Process entire directories recursively

**Key Dependencies**: Pillow (PIL)

📖 [Full Image Tools Documentation](image/transperency/README.md)

## 🚀 Quick Start

### Prerequisites

- **Python 3.6+**
- **ffmpeg** (for audio tools)
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Installation

1. Clone or download this repository

2. Navigate to the specific tool directory:
   ```bash
   cd audio/opus2m4a/    # For audio tools
   # or
   cd image/transperency/ # For image tools
   ```

3. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the desired script (see individual README files for usage)

## 📝 Usage Examples

### Audio Conversion
```bash
cd audio/opus2m4a
python convert_to_m4a.py input.opus output.m4a
```

### Vocal Extraction
```bash
cd audio/opus2m4a
python extract_vocals.py song.mp3 --output vocals.m4a
```

### Image Transparency
```bash
cd image/transperency
python transparency.py add image.jpg --opacity 80 --output transparent.png
```

## 🛠️ Development

Each tool is self-contained with its own:
- `README.md` - Detailed usage instructions
- `requirements.txt` - Python dependencies
- Batch processing variants (where applicable)

## 📄 License

This is a personal collection of utility scripts. Use at your own discretion.

## 🤝 Contributing

This is a personal toolset, but suggestions and improvements are welcome.

## ⚠️ Notes

- Audio processing tools require significant disk space for AI models (~200-300MB)
- First-time use of demucs will download pretrained models
- Some operations are CPU/GPU intensive and may take time for large files
