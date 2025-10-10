import os
import time
import argparse
import logging
from datetime import datetime
from googleapiclient.discovery import build  # requires google-api-python-client
from googleapiclient.errors import HttpError


# --- CONFIGURATION ---

# Default configuration that can be overridden by CLI args
DEFAULT_VIDEO_ID = 'jJZnziRAyac'
DEFAULT_KEYWORDS = ['buy', 'link', 'price', 'how much', 'purchase']
DEFAULT_POLL_INTERVAL = 10


def setup_logging(verbose=False):
    """Setup logging configuration"""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    return logging.getLogger(__name__)


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Monitor YouTube live chat for keywords')
    parser.add_argument('--video-id', default=DEFAULT_VIDEO_ID,
                       help='YouTube video ID to monitor (default: %(default)s)')
    parser.add_argument('--keywords', nargs='+', default=DEFAULT_KEYWORDS,
                       help='Keywords to search for (default: %(default)s)')
    parser.add_argument('--interval', type=int, default=DEFAULT_POLL_INTERVAL,
                       help='Polling interval in seconds (default: %(default)s)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    return parser.parse_args()
from googleapiclient.discovery import build  # requires google-api-python-client


# --- CONFIGURATION ---

API_KEY = os.environ.get("API_KEY")

# The ID of the YouTube video that is currently live.
# You find this in the URL of the video (e.g., https://www.youtube.com/watch?v=VIDEO_ID)
VIDEO_ID = 'nL5H_f37WRE' 

# The keywords you want to search for
KEYWORDS = ['buy', 'link', 'price', 'how much', 'purchase']

# --- SCRIPT LOGIC ---

youtube = None


# Function to get the ID of the live chat
def get_live_chat_id(video_id, logger):
    """Get live chat ID for a YouTube video"""
    try:
        request = youtube.videos().list(
            part="liveStreamingDetails",
            id=video_id
        )
        response = request.execute()
        
        items = response.get('items') or []
        if not items:
            logger.error('No video found with ID: %s', video_id)
            logger.debug('Full API response: %s', response)
            return None

        details = items[0].get('liveStreamingDetails') or {}
        live_chat_id = details.get('activeLiveChatId')
        
        if live_chat_id:
            logger.info("Successfully found Live Chat ID: %s", live_chat_id)
            return live_chat_id

        # If we got here, the video either isn't live or doesn't have chat enabled
        logger.warning('Video has liveStreamingDetails but no activeLiveChatId')
        logger.debug('Full liveStreamingDetails: %s', details)
        
        # Check if video is actually live
        if details.get('actualStartTime') and not details.get('actualEndTime'):
            logger.info('Video appears to be live but chat may be disabled')
        else:
            logger.info('Video does not appear to be currently live')
            
        return None
        
    except HttpError as e:
        logger.error('YouTube API error: %s', e)
        return None
    except Exception as e:
        logger.error('Unexpected error getting live chat ID: %s', e)
        return None

# Main function to monitor the chat
def monitor_chat(live_chat_id, keywords, poll_interval, logger):
    """Monitor live chat for keywords"""
    next_page_token = None
    logger.info("Starting Chat Monitor - watching for keywords: %s", keywords)
    logger.info("Polling every %d seconds", poll_interval)
    
    alerts_count = 0
    
    while True:
        try:
            # Request new chat messages
            request = youtube.liveChatMessages().list(
                liveChatId=live_chat_id,
                part="snippet,authorDetails",
                pageToken=next_page_token
            )
            response = request.execute()

            items = response.get('items') or []
            new_messages = len(items)
            
            if new_messages > 0:
                logger.debug("Processing %d new messages", new_messages)
            
            for item in items:
                snippet = item.get('snippet', {})
                author_details = item.get('authorDetails', {})
                message = snippet.get('displayMessage', '').lower()
                author = author_details.get('displayName', 'Unknown')
                timestamp = snippet.get('publishedAt', '')
                
                # Check if any of our keywords are in the message
                for keyword in keywords:
                    if keyword.lower() in message:
                        alerts_count += 1
                        logger.warning("KEYWORD ALERT #%d: Found '%s'", alerts_count, keyword)
                        print("-" * 60)
                        print(f"🚨 ALERT #{alerts_count}: Found keyword '{keyword}' 🚨")
                        print(f"📺 Author: {author}")
                        print(f"💬 Message: {snippet.get('displayMessage', '')}")
                        print(f"⏰ Time: {timestamp}")
                        print("-" * 60)

            # Save the token for the next request to get only new messages
            next_page_token = response.get('nextPageToken')
            
            # Wait before checking for new messages
            time.sleep(poll_interval)

        except HttpError as e:
            if e.resp.status == 403:
                logger.error("YouTube API quota exceeded or permissions issue")
                break
            elif e.resp.status == 404:
                logger.error("Live chat not found - stream may have ended")
                break
            else:
                logger.error("YouTube API error: %s", e)
                time.sleep(poll_interval * 2)
        except KeyboardInterrupt:
            logger.info("Interrupted by user")
            break
        except Exception as e:
            logger.error("Unexpected error: %s", e)
            time.sleep(poll_interval * 2)

# --- RUN THE SCRIPT ---
# --- RUN THE SCRIPT ---
def main():
    """Main function"""
    args = parse_arguments()
    logger = setup_logging(args.verbose)
    
    # Check for API key
    api_key = os.environ.get("API_KEY")
    if not api_key:
        logger.error("API_KEY environment variable not set")
        logger.info("Please set your YouTube Data API v3 key: export API_KEY='your_key_here'")
        return 1

    # Initialize the YouTube API client
    global youtube
    try:
        youtube = build('youtube', 'v3', developerKey=api_key)
        logger.info("YouTube API client initialized successfully")
    except Exception as e:
        logger.error("Failed to initialize YouTube API client: %s", e)
        return 1

    logger.info("Starting YouTube Live Chat Monitor")
    logger.info("Video ID: %s", args.video_id)
    logger.info("Keywords: %s", args.keywords)
    
    # Get live chat ID
    live_chat_id = get_live_chat_id(args.video_id, logger)
    if not live_chat_id:
        logger.error("Could not find live chat for video %s", args.video_id)
        logger.info("Make sure the video is live and has chat enabled")
        return 1

    # Start monitoring
    try:
        monitor_chat(live_chat_id, args.keywords, args.interval, logger)
    except KeyboardInterrupt:
        logger.info("Monitoring stopped by user")
    except Exception as e:
        logger.error("Monitoring failed: %s", e)
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())