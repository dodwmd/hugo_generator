import openai
import requests
from bs4 import BeautifulSoup
from config import OPENAI_API_KEY, UNSPLASH_ACCESS_KEY
from exceptions import ContentGenerationError
from logger import setup_logger

logger = setup_logger(__name__, 'INFO')

openai.api_key = OPENAI_API_KEY

def generate_blog_post_content(topic):
    prompt = f"""
    Write a comprehensive blog post about {topic}. The post should include:
    1. An in-depth explanation of what {topic} is
    2. Why it's important and relevant in today's tech landscape
    3. How to set up or implement it (if applicable), with code examples
    4. Technical details and considerations
    5. Best practices and common pitfalls
    6. Real-world applications and case studies
    7. Future trends and potential developments
    8. A conclusion summarizing the key points and encouraging reader engagement

    Format the content in Markdown, including appropriate headings, subheadings, and bullet points.
    Include at least 5 relevant links to authoritative sources, documentation, or tools related to the topic.
    Suggest a relevant image that could be used to illustrate the topic.

    The blog post should be at least 1500 words long.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that writes comprehensive technical blog posts."},
                {"role": "user", "content": prompt}
            ]
        )
        content = response.choices[0].message['content']
        
        # Fetch an image for the blog post
        image_url = fetch_relevant_image(topic)
        if image_url:
            content = f"![{topic}]({image_url})\n\n" + content
        
        return content
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {str(e)}")
        raise ContentGenerationError(f"Failed to generate content: {str(e)}")

def fetch_relevant_image(topic):
    try:
        url = "https://api.unsplash.com/search/photos"
        headers = {
            "Authorization": f"Client-ID {UNSPLASH_ACCESS_KEY}"
        }
        params = {
            "query": topic,
            "per_page": 1
        }
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        if data['results']:
            return data['results'][0]['urls']['regular']
    except Exception as e:
        logger.error(f"Failed to fetch image: {str(e)}")
    return None
