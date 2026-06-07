# AV Tools

I made the robots make a bunch of tools so I don't have to pay sucker AI companies. More to come as I need them. I'm sharing them with you. Please be kind.

A lot of these are silly command stuff I could probably bind in a shell alias or something but I like using python

## 📁 Project Structure

```sh
AV_tools/
├── audio/
│   └── sample_wrangler/          # Audio conversion and manipulation tools
│       ├── convert_to_m4a.py
│       ├── extract_vocals.py
│       ├── remove_drums.py
│       └── batch_*.py     # Batch processing variants
│
├── image/
│   └── transperency/      # Image transparency processing
│       └── transparency.py
│
└── streaming/
    └── get_latest_live/   # YouTube live stream checker
        ├── get_latest_live.py
        └── get_latest_live.sh
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

## 🎬 Streaming Tools

Located in `streaming/get_latest_live/`, these tools provide:

- **YouTube Live Stream Checker**: Check any YouTube channel for upcoming scheduled live streams
- **Multiple Output Formats**: Get results in formatted text or JSON
- **Flexible Configuration**: Use environment variables or config files for API keys
- **Automated Setup**: Shell script handles virtual environment and dependencies

**Key Dependencies**: google-api-python-client, python-dotenv, pyyaml

📖 [Full Streaming Tools Documentation](streaming/get_latest_live/README.md)

## 🚀 Quick Start

### Prerequisites

- **Python 3.6+** (Python 3.7+ for streaming tools)
- **ffmpeg** (for audio tools)
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`
  - Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- **YouTube Data API v3 Key** (for streaming tools)
  - Get one from [Google Cloud Console](https://console.cloud.google.com/apis/credentials)

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

### YouTube Live Stream Check

```bash
cd streaming/get_latest_live
./get_latest_live.sh  # Automated setup and execution
# or
python get_latest_live.py --format json
```

## 🛠️ Development

Each tool is self-contained with its own:

- `README.md` - Detailed usage instructions
- `requirements.txt` - Python dependencies
- Batch processing variants (where applicable)

## 📄 License

Use at your own discretion.

## 🤝 Contributing

This is a personal toolset, but suggestions and improvements are welcome.

## ⚠️ Notes

- Audio processing tools require significant disk space for AI models (~200-300MB)
- First-time use of demucs will download pretrained models
- Some operations are CPU/GPU intensive and may take time for large files
- Streaming tools require a YouTube Data API v3 key (free, but subject to daily quota limits)
