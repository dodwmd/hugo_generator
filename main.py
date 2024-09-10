import os
from config import HUGO_CONTENT_DIR, OPENAI_API_KEY, LOG_LEVEL
from topic_generator import choose_best_topic
from content_generator import generate_blog_post_content
from blog_post_formatter import format_blog_post
from exceptions import BlogGeneratorException
from logger import setup_logger

logger = setup_logger(__name__, LOG_LEVEL)

def setup():
    """Perform initial setup and checks."""
    if not OPENAI_API_KEY:
        logger.error("OpenAI API key is not set. Please set it in .env file")
        sys.exit(1)
    
    if not os.path.exists(HUGO_CONTENT_DIR):
        logger.error(f"Hugo content directory not found: {HUGO_CONTENT_DIR}")
        sys.exit(1)

def main():
    setup()
    
    try:
        chosen_topic = choose_best_topic()
        if not chosen_topic:
            logger.info("No new topics available. Exiting.")
            return

        logger.info(f"Chosen topic: {chosen_topic}")

        content = generate_blog_post_content(chosen_topic)
        logger.info("Generated blog post content")

        formatted_post, filename = format_blog_post(chosen_topic, content)
        logger.info("Formatted blog post")

        filepath = os.path.join(HUGO_CONTENT_DIR, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(formatted_post)

        logger.info(f"Blog post created: {filepath}")
        print(f"Blog post created: {filepath}")

    except BlogGeneratorException as e:
        logger.error(f"Blog generation error: {str(e)}")
        print(f"An error occurred: {str(e)}")
    except Exception as e:
        logger.exception("An unexpected error occurred")
        print("An unexpected error occurred. Please check the log file for details.")

if __name__ == "__main__":
    main()
