# YouTube Latest Live Stream Checker

A tool to check a YouTube channel for the latest scheduled live stream and return its details.

## Features

- ✅ Check for upcoming scheduled live streams on any YouTube channel
- ✅ Returns stream title, URL, scheduled time, and channel info
- ✅ Supports both channel ID and username/handle
- ✅ Multiple configuration methods (environment variables, config file)
- ✅ JSON or formatted text output
- ✅ Comprehensive error handling
- ✅ Automated setup script with virtual environment management

## Prerequisites

- Python 3.7 or higher
- YouTube Data API v3 key ([Get one here](https://console.cloud.google.com/apis/credentials))

## Setup

### 1. Get YouTube API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the YouTube Data API v3
4. Create credentials (API key)
5. Copy your API key

### 2. Install Dependencies

You can use the automated shell script (recommended) or manual setup:

#### Option A: Using the Shell Script (Recommended)

```bash
./get_latest_live.sh
```

The script will automatically:

- Create a virtual environment if needed
- Install all required dependencies
- Run the checker script

#### Option B: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate  # On Windows

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key and Channel

Choose one of the following methods:

#### Option A: Environment Variables (via .env file)

Create a `.env` file in this directory:

```env
YOUTUBE_API_KEY=your_api_key_here
YOUTUBE_CHANNEL_ID=your_channel_id
# Or use username instead:
# YOUTUBE_CHANNEL_USERNAME=your_channel_username
```

#### Option B: Configuration File

Copy the example config and edit it:

```bash
cp config.yaml.example config.yaml
```

Edit `config.yaml` with your API key and channel information:

```yaml
youtube_api_key: "your_api_key_here"
channel_id: "UCxxxxxxxxxxxxx"
# Or use username:
# channel_username: "your_channel_username"
```

## Usage

### Using the Shell Script (Easiest)

```bash
# Check for latest live stream (text output)
./get_latest_live.sh

# Get JSON output
./get_latest_live.sh --format json

# Override channel from command line
./get_latest_live.sh --channel-id UCxxxxxxxxxxxxx
./get_latest_live.sh --channel-username your_channel_name
```

### Direct Python Script

If you prefer to run the Python script directly:

```bash
# Activate virtual environment first
source venv/bin/activate

# Run the script
python get_latest_live.py

# With options
python get_latest_live.py --format json
python get_latest_live.py --channel-id UCxxxxxxxxxxxxx
```

## Command Line Options

- `--format [text|json]` - Output format (default: text)
- `--channel-id CHANNEL_ID` - Override the configured channel ID
- `--channel-username USERNAME` - Override the configured channel username

## Output Examples

### Text Format (Default)

```sh
✓ Upcoming Live Stream Found!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:     My Awesome Live Stream
Channel:   My Channel Name
Scheduled: 2026-06-08 15:00:00 UTC
URL:       https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

### JSON Format

```json
{
  "status": "success",
  "title": "My Awesome Live Stream",
  "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
  "video_id": "dQw4w9WgXcQ",
  "scheduled_start": "2026-06-08T15:00:00Z",
  "channel_title": "My Channel Name"
}
```

### No Scheduled Streams

```sh
✗ No live streams are currently scheduled.
```

## Error Handling

The script handles various error conditions:

- Missing or invalid API key
- Channel not found
- API quota exceeded
- Network errors
- Invalid configuration

Exit codes:

- `0` - Success (live stream found)
- `1` - Error or no streams found

## File Structure

```sh
get_latest_live/
├── get_latest_live.py       # Main Python script
├── get_latest_live.sh       # Shell wrapper script
├── requirements.txt         # Python dependencies
├── config.yaml.example      # Example configuration
├── .gitignore              # Git ignore rules
├── .env                    # Environment variables (not in git)
├── config.yaml             # Configuration file (not in git)
└── README.md               # This file
```

## Troubleshooting

### "YouTube API key not found"

- Ensure you've created either a `.env` file or `config.yaml` with your API key

### "Channel ID or username not found"

- Make sure you've specified either `YOUTUBE_CHANNEL_ID` or `YOUTUBE_CHANNEL_USERNAME`

### "API quota exceeded"

- YouTube Data API has daily quota limits
- Wait until the quota resets (usually midnight Pacific Time)
- Check your quota usage in Google Cloud Console

### "Could not find channel"

- Verify the channel ID or username is correct
- For modern YouTube channels, try using the @handle format

## License

This tool is provided as-is for personal use.

## API Limits

The YouTube Data API v3 has quota limits:

- Default quota: 10,000 units per day
- This script uses approximately 100-103 units per run
- You can make about 97-100 requests per day with the default quota

## Contributing

Feel free to submit issues or pull requests for improvements!
