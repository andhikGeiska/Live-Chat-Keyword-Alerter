# Live Chat Keyword Alerter

Monitor live chat streams on YouTube and TikTok for specific keywords and get real-time alerts when they appear.

## Features

- **YouTube Live Chat Monitoring**: Monitor YouTube live streams using the YouTube Data API v3
- **TikTok Live Chat Monitoring**: Monitor TikTok live streams using the TikTokLive library
- **Keyword Detection**: Search for multiple keywords in chat messages
- **Real-time Alerts**: Get immediate notifications when keywords are found
- **Command Line Interface**: Configure monitoring via CLI arguments
- **Robust Error Handling**: Automatic retries and graceful error recovery
- **Logging**: Detailed logging with configurable verbosity levels

## Requirements

- Python 3.10+ (tested with 3.12)
- A virtual environment (recommended)
- For YouTube: Google API client library + YouTube Data API v3 key
- For TikTok: TikTokLive library

## Setup

1. Create and activate a virtual environment in the project root:

```bash
python -m venv venv
source ./venv/bin/activate
```

1. Install dependencies:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## YouTube Monitor Setup

1. Get a YouTube Data API v3 key:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable the YouTube Data API v3
   - Create credentials (API key)
   - Restrict the key to YouTube Data API v3 (recommended)

1. Set the `API_KEY` environment variable:

```bash
export API_KEY="YOUR_YOUTUBE_API_KEY_HERE"
```

**Important**: Never commit your API key to source control!

## Usage

### YouTube Live Chat Monitor

Monitor a YouTube live stream for keywords:

```bash
# Basic usage with default settings
source ./venv/bin/activate
python chat_monitor.py

# Monitor specific video with custom keywords
python chat_monitor.py --video-id "YOUR_VIDEO_ID" --keywords "buy" "price" "link" --interval 5

# Enable verbose logging
python chat_monitor.py --verbose

# Get help
python chat_monitor.py --help
```

**Command line options:**

- `--video-id`: YouTube video ID to monitor (found in video URL)
- `--keywords`: Space-separated list of keywords to search for
- `--interval`: Polling interval in seconds (default: 10)
- `--verbose`: Enable detailed logging

### TikTok Live Chat Monitor

Monitor a TikTok live stream for keywords:

```bash
# Basic usage with default settings
source ./venv/bin/activate
python tiktok_monitor.py

# Monitor specific user with custom keywords
python tiktok_monitor.py --username "@your_username" --keywords "buy" "price" "restock"

# Configure retry behavior
python tiktok_monitor.py --max-retries 10 --backoff 3

# Enable verbose logging
python tiktok_monitor.py --verbose

# Get help
python tiktok_monitor.py --help
```

**Command line options:**

- `--username`: TikTok username to monitor (must include @)
- `--keywords`: Space-separated list of keywords to search for
- `--max-retries`: Maximum retry attempts for connection issues (default: 5)
- `--backoff`: Retry backoff multiplier (default: 2)
- `--verbose`: Enable detailed logging

## Configuration

### Default Keywords

Both monitors search for these keywords by default:

- `buy`, `link`, `price`, `how much`, `purchase`
- TikTok monitor also includes: `restock`

### Default Settings

- **YouTube polling interval**: 10 seconds
- **TikTok max retries**: 5 attempts
- **TikTok backoff**: Exponential (2^attempt seconds)

## Troubleshooting

### YouTube Issues

**"Could not find live chat"**

- Verify the video is currently live
- Check that live chat is enabled for the stream
- Ensure your API key has the correct permissions

**"YouTube API quota exceeded"**

- You've hit the daily API quota limit
- Wait until quota resets (usually next day)
- Consider optimizing polling intervals

**API Key Issues**

- Ensure `API_KEY` environment variable is set
- Verify the key is valid and not restricted
- Check that YouTube Data API v3 is enabled

### TikTok Issues

**"Sign API error" or "504 error"**

- These are usually temporary TikTok infrastructure issues
- The monitor will automatically retry with exponential backoff
- Try again later if persistent

**"Event loop" errors**

- Fixed in current version with fresh client creation per retry
- Restart the monitor if you see this error

**Connection Issues**

- Verify the username exists and is currently live
- Check your internet connection
- Some regions may have restrictions

### General Issues

**Import errors**

- Ensure virtual environment is activated
- Reinstall requirements: `pip install -r requirements.txt`
- Check Python version (3.10+ required)

**VS Code showing unresolved imports**

- Set interpreter to `./venv/bin/python` in VS Code
- Reload VS Code window after setting interpreter

## Examples

### YouTube Examples

```bash
# Monitor a specific live stream for purchase-related keywords
python chat_monitor.py --video-id "dQw4w9WgXcQ" --keywords "buy" "purchase" "order" "price"

# Quick polling for high-activity streams
python chat_monitor.py --interval 5 --verbose

# Monitor with many keywords
python chat_monitor.py --keywords "buy" "sell" "trade" "price" "cost" "link" "website" "store"
```

### TikTok Examples

```bash
# Monitor a specific user for business keywords
python tiktok_monitor.py --username "@shop_account" --keywords "available" "stock" "order"

# Aggressive retry settings for unstable connections
python tiktok_monitor.py --max-retries 10 --backoff 3 --verbose

# Monitor for restocking alerts
python tiktok_monitor.py --keywords "restock" "new drop" "available now"
```

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on:

- How to report bugs and request features
- Development setup and coding standards
- Pull request process
- Code of conduct

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

- **YouTube**: Respect YouTube's Terms of Service and API quotas
- **TikTok**: This tool uses unofficial TikTok APIs that may change
- **Rate Limiting**: Be mindful of API rate limits and polling frequencies
- **Personal Use**: Intended for personal monitoring, not commercial data collection
