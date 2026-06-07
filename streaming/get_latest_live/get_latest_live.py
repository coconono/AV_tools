#!/usr/bin/env python3
"""
YouTube Latest Live Stream Checker
Checks a YouTube channel for the latest scheduled live stream.
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

try:
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
    from dotenv import load_dotenv
    import yaml
except ImportError as e:
    print(f"Error: Missing required dependencies. Please install them using: pip install -r requirements.txt")
    print(f"Details: {e}")
    sys.exit(1)


def load_config():
    """Load configuration from environment variables or config file."""
    # Load environment variables from .env file if it exists
    load_dotenv()
    
    config = {
        'api_key': os.getenv('YOUTUBE_API_KEY'),
        'channel_id': os.getenv('YOUTUBE_CHANNEL_ID'),
        'channel_username': os.getenv('YOUTUBE_CHANNEL_USERNAME')
    }
    
    # Try to load from config.yaml if it exists
    config_file = Path(__file__).parent / 'config.yaml'
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                yaml_config = yaml.safe_load(f)
                if yaml_config:
                    config['api_key'] = config['api_key'] or yaml_config.get('youtube_api_key')
                    config['channel_id'] = config['channel_id'] or yaml_config.get('channel_id')
                    config['channel_username'] = config['channel_username'] or yaml_config.get('channel_username')
        except Exception as e:
            print(f"Warning: Could not load config.yaml: {e}")
    
    # Validate configuration
    if not config['api_key']:
        print("Error: YouTube API key not found. Please set YOUTUBE_API_KEY environment variable or add it to config.yaml")
        sys.exit(1)
    
    if not config['channel_id'] and not config['channel_username']:
        print("Error: Channel ID or username not found. Please set YOUTUBE_CHANNEL_ID/YOUTUBE_CHANNEL_USERNAME or add to config.yaml")
        sys.exit(1)
    
    return config


def get_channel_id(youtube, channel_username):
    """Convert channel username to channel ID."""
    try:
        request = youtube.channels().list(
            part='id',
            forUsername=channel_username
        )
        response = request.execute()
        
        if response['items']:
            return response['items'][0]['id']
        else:
            # Try searching by handle (modern YouTube format)
            request = youtube.search().list(
                part='id',
                q=channel_username,
                type='channel',
                maxResults=1
            )
            response = request.execute()
            if response['items']:
                return response['items'][0]['id']['channelId']
    except HttpError as e:
        print(f"Error retrieving channel ID: {e}")
    return None


def get_latest_live_stream(api_key, channel_id=None, channel_username=None):
    """
    Check YouTube channel for the latest scheduled live stream.
    
    Args:
        api_key: YouTube Data API v3 key
        channel_id: YouTube channel ID (optional if channel_username provided)
        channel_username: YouTube channel username (optional if channel_id provided)
    
    Returns:
        dict: Stream information or error message
    """
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Get channel ID if username was provided
        if not channel_id and channel_username:
            channel_id = get_channel_id(youtube, channel_username)
            if not channel_id:
                return {
                    'status': 'error',
                    'message': f'Could not find channel: {channel_username}'
                }
        
        # Search for upcoming live streams on the channel
        request = youtube.search().list(
            part='snippet',
            channelId=channel_id,
            type='video',
            eventType='upcoming',
            order='date',
            maxResults=1
        )
        response = request.execute()
        
        if not response['items']:
            return {
                'status': 'no_streams',
                'message': 'No live streams are currently scheduled.'
            }
        
        # Get the first (latest) scheduled stream
        stream = response['items'][0]
        video_id = stream['id']['videoId']
        title = stream['snippet']['title']
        scheduled_time = stream['snippet']['publishedAt']
        
        # Get additional video details
        video_request = youtube.videos().list(
            part='liveStreamingDetails,snippet',
            id=video_id
        )
        video_response = video_request.execute()
        
        if video_response['items']:
            video_details = video_response['items'][0]
            live_details = video_details.get('liveStreamingDetails', {})
            scheduled_start = live_details.get('scheduledStartTime', scheduled_time)
            
            return {
                'status': 'success',
                'title': title,
                'url': f'https://www.youtube.com/watch?v={video_id}',
                'video_id': video_id,
                'scheduled_start': scheduled_start,
                'channel_title': stream['snippet']['channelTitle']
            }
        
        return {
            'status': 'error',
            'message': 'Could not retrieve stream details.'
        }
        
    except HttpError as e:
        error_content = json.loads(e.content.decode('utf-8'))
        error_message = error_content.get('error', {}).get('message', str(e))
        return {
            'status': 'error',
            'message': f'YouTube API error: {error_message}'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': f'Unexpected error: {str(e)}'
        }


def format_output(result, format_type='text'):
    """Format the result for display."""
    if format_type == 'json':
        return json.dumps(result, indent=2)
    
    # Text format
    if result['status'] == 'success':
        scheduled = datetime.fromisoformat(result['scheduled_start'].replace('Z', '+00:00'))
        return f"""
✓ Upcoming Live Stream Found!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Title:     {result['title']}
Channel:   {result['channel_title']}
Scheduled: {scheduled.strftime('%Y-%m-%d %H:%M:%S %Z')}
URL:       {result['url']}
"""
    elif result['status'] == 'no_streams':
        return f"\n✗ {result['message']}\n"
    else:
        return f"\n✗ Error: {result['message']}\n"


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Check YouTube channel for latest scheduled live stream')
    parser.add_argument('--format', choices=['text', 'json'], default='text',
                        help='Output format (default: text)')
    parser.add_argument('--channel-id', help='YouTube channel ID (overrides config)')
    parser.add_argument('--channel-username', help='YouTube channel username (overrides config)')
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config()
    
    # Override with command-line arguments if provided
    channel_id = args.channel_id or config['channel_id']
    channel_username = args.channel_username or config['channel_username']
    
    # Get latest live stream
    result = get_latest_live_stream(
        config['api_key'],
        channel_id=channel_id,
        channel_username=channel_username
    )
    
    # Output result
    output = format_output(result, format_type=args.format)
    print(output)
    
    # Exit with appropriate code
    sys.exit(0 if result['status'] == 'success' else 1)


if __name__ == '__main__':
    main()
