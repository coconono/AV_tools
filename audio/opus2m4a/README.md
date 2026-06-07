# Audio Processing Tools

Python scripts for audio file conversion and manipulation.

## Tools

1. **M4A Converter** - Convert audio files to M4A format
2. **Drum Removal** - Remove drums from audio files using AI
3. **Vocal Extraction** - Extract vocals from audio files using AI

## Requirements

- Python 3.6+
- ffmpeg
- demucs (for drum removal)

### Installing ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from https://ffmpeg.org/download.html

### Installing Python Dependencies

**Option 1: Install from requirements.txt (recommended)**
```bash
pip3 install -r requirements.txt
```

**Option 2: Install manually**
```bash
pip3 install demucs
```

Note: Demucs uses AI models (~200-300MB) which will be downloaded on first use.

---

## Usage

### M4A Conversion

#### Basic conversion
```bash
python convert_to_m4a.py input.opus
```
This will create `input.m4a` in the same directory.

### Specify output filename
```bash
python convert_to_m4a.py input.opus output.m4a
```

### Specify audio bitrate
```bash
python convert_to_m4a.py input.opus output.m4a 256k
```

### Batch conversion
```bash
python batch_convert.py /path/to/audio/files
```

---

### M4A Converter
- Converts any audio format supported by ffmpeg (opus, mp3, wav, flac, etc.)
- Customizable audio bitrate (default: 192k)
- Automatic output filename generation
- Error handling and validation
- Progress feedback
- Batch processing support

### Drum Removal
- AI-powered audio source separation using Demucs
- Removes drums while preserving vocals, bass, and other instruments
- Multiple quality models available
- Works with any audio format (m4a, mp3, wav, flac, etc.)
- Option to keep separated stems (drums + no-drums)
- Batch processing support

### Vocal Extraction
- AI-powered vocal isolation using Demucs
- Extracts clean vocals from any audio track
- Removes instrumentals, drums, bass, and other sounds
- Multiple quality models available
- Works with any audio format (m4a, mp3, wav, flac, etc.)
- Option to keep all separated stems (vocals, drums, bass, other)
- Batch processing support.py input.m4a
```
This will create `input_no_drums.m4a` in the same directory.

#### Specify output filename
```bash
python remove_drums.py input.m4a output.m4a
```

#### Use different AI model
```bash
python remove_drums.py input.m4a --model htdemucs_ft
```

Available models:
- `htdemucs` - Default, good balance of quality and speed
- `htdemucs_ft` - Fine-tuned version, slightly better quality
- `mdx_extra` - Highest quality, slower

#### Keep separated stems
```bash
python remove_drums.py input.m4a --keep-temp
```
This keeps both the no-drums version and the isolated drums.

#### Batch drum removal
```bash
python batch_remove_drums.py /path/to/audio/files
```

---

### Vocal Extraction

#### Extract vocals from a single file
```bash
python extract_vocals.py input.m4a
```
This will create `input_vocals.m4a` in the same directory.

#### Specify output filename
```bash
python extract_vocals.py input.m4a vocals.m4a
```

#### Use different AI model
```bash
python extract_vocals.py input.m4a --model htdemucs_ft
```

#### Keep all separated stems
```bash
python extract_vocals.py input.m4a --keep-temp
```
This keeps all separated stems: vocals, drums, bass, and other instruments.

#### Batch vocal extraction
```bash
python batch_extract_vocals.py /path/to/audio/files
```

---

### M4A Converter
- The script uses AAC codec for audio encoding

### Vocal Extraction
- First run will download AI models (~200-300MB)
- Processing time depends on file length and hardware
- Works better with GPU but also runs on CPU (slower)
- The AI separation is not perfect but generally very good
- Best results with studio recordings and clear vocals
- Useful for creating karaoke tracks or acapella versions
- Video streams are automatically disabled
- Output files are overwritten without prompt

### Drum Removal
- First run will download AI models (~200-300MB)
- Processing time depends on file length and hardware
- Works better with GPU but also runs on CPU (slower)
- The AI separation is not perfect but generally very good
- Best results with studio recordings and clear drum patternseg (opus, mp3, wav, flac, etc.)
- Customizable audio bitrate (default: 192k)
- Automatic output filename generation
- Error handling and validation
- Progress feedback

## Notes

- The script uses AAC codec for audio encoding
- Video streams are automatically disabled
- Output files are overwritten without prompt
