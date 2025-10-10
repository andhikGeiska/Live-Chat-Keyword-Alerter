# Import the necessary library
from TikTokLive import TikTokLiveClient
from TikTokLive.events import CommentEvent
from TikTokLive.client.errors import SignAPIError
import time
import sys
import argparse
import logging
from datetime import datetime


# --- CONFIGURATION ---

# Default configuration
DEFAULT_USERNAME = '@popmart.malaysia.shop'
DEFAULT_KEYWORDS = ['buy', 'link', 'price', 'how much', 'purchase', 'restock']
DEFAULT_MAX_RETRIES = 5
DEFAULT_BACKOFF = 2


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
    parser = argparse.ArgumentParser(description='Monitor TikTok live chat for keywords')
    parser.add_argument('--username', default=DEFAULT_USERNAME,
                       help='TikTok username to monitor (include @, default: %(default)s)')
    parser.add_argument('--keywords', nargs='+', default=DEFAULT_KEYWORDS,
                       help='Keywords to search for (default: %(default)s)')
    parser.add_argument('--max-retries', type=int, default=DEFAULT_MAX_RETRIES,
                       help='Maximum retry attempts (default: %(default)s)')
    parser.add_argument('--backoff', type=int, default=DEFAULT_BACKOFF,
                       help='Retry backoff multiplier (default: %(default)s)')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose logging')
    return parser.parse_args()

# --- SCRIPT LOGIC ---

# Global variables for tracking
alerts_count = 0
logger = None
keywords = []


def create_comment_handler(keywords_list, logger_instance):
    """Create a comment handler with the specified keywords and logger"""
    async def on_tiktok_comment(event: CommentEvent):
        global alerts_count
        
        # Get the comment text and the author's name
        comment_text = event.comment.lower()
        author_name = event.user.nickname
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Check if any of our keywords are in the message
        for keyword in keywords_list:
            if keyword.lower() in comment_text:
                alerts_count += 1
                logger_instance.warning("KEYWORD ALERT #%d: Found '%s'", alerts_count, keyword)
                print("-" * 60)
                print(f"🚨 TIKTOK ALERT #{alerts_count}: Found keyword '{keyword}' 🚨")
                print(f"👤 Author: {author_name}")
                print(f"💬 Comment: {event.comment}")
                print(f"⏰ Time: {timestamp}")
                print("-" * 60)
    
    return on_tiktok_comment

# --- RUN THE SCRIPT ---
def main():
    """Main function"""
    global logger
    
    args = parse_arguments()
    logger = setup_logging(args.verbose)
    
    # Validate username format
    username = args.username.strip()
    if not username.startswith('@'):
        logger.error("Username must start with @")
        return 1
    
    logger.info("Starting TikTok Live Chat Monitor")
    logger.info("Username: %s", username)
    logger.info("Keywords: %s", args.keywords)
    logger.info("Max retries: %d, Backoff: %d", args.max_retries, args.backoff)
    
    # Create comment handler with current keywords and logger
    comment_handler = create_comment_handler(args.keywords, logger)
    
    attempt = 0
    while attempt < args.max_retries:
        # Create a fresh client instance per attempt to avoid event loop issues
        try:
            logger.info("Creating TikTok client (attempt %d/%d)", attempt + 1, args.max_retries)
            client = TikTokLiveClient(unique_id=username)
            # Register the handler on this client instance
            client.on(CommentEvent)(comment_handler)
            
            logger.info("Connecting to TikTok Live for %s...", username)
            logger.info("Listening for comments... Press Ctrl+C to stop.")
            
            client.run()
            logger.info("TikTok client finished successfully")
            break  # normally client.run() blocks until interrupted
            
        except KeyboardInterrupt:
            logger.info('Interrupted by user; shutting down.')
            try:
                client.stop()
            except Exception:
                pass
            return 0
            
        except SignAPIError as e:
            attempt += 1
            logger.error("Sign API error (attempt %d/%d): %s", attempt, args.max_retries, e)
            try:
                client.stop()
            except Exception:
                pass
            
            if attempt >= args.max_retries:
                logger.error("Max retries reached; exiting.")
                return 1
                
            sleep_for = args.backoff ** attempt
            logger.info("Retrying in %d seconds...", sleep_for)
            time.sleep(sleep_for)
            
        except Exception as e:
            # For any other errors, print and exit
            logger.error("Unexpected error while running TikTok client: %s", e)
            try:
                client.stop()
            except Exception:
                pass
            return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(main())