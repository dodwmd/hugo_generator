import random
import requests
import json
import openai
import os
from datetime import datetime, timedelta
from config import INTERESTS, OPENAI_API_KEY  # Add OPENAI_API_KEY here
from exceptions import APIError
from logger import setup_logger

logger = setup_logger(__name__, 'INFO')

openai.api_key = OPENAI_API_KEY

TOPICS_FILE = 'generated_topics.json'

def load_generated_topics():
    if os.path.exists(TOPICS_FILE):
        with open(TOPICS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_generated_topics(topics):
    with open(TOPICS_FILE, 'w') as f:
        json.dump(topics, f)

def fetch_trending_topics():
    """Fetch trending topics from various sources."""
    trending_topics = []
    
    # Example: Fetch trending topics from GitHub
    try:
        response = requests.get("https://api.github.com/search/repositories?q=created:>2023-01-01&sort=stars&order=desc")
        response.raise_for_status()
        data = response.json()
        trending_topics.extend([repo['name'] for repo in data['items'][:10]])
    except requests.RequestException:
        logger.error("Failed to fetch trending topics from GitHub")
    
    # Example: Fetch trending topics from Hacker News
    try:
        response = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")
        response.raise_for_status()
        story_ids = response.json()[:10]
        for story_id in story_ids:
            story_response = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json?print=pretty")
            story_response.raise_for_status()
            story_data = story_response.json()
            trending_topics.append(story_data['title'])
    except requests.RequestException:
        logger.error("Failed to fetch trending topics from Hacker News")
    
    return trending_topics

def generate_ai_topics():
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates trending tech topics."},
                {"role": "user", "content": f"Generate 5 trending tech topics related to {', '.join(INTERESTS)}. Provide each topic on a new line."}
            ],
            max_tokens=150,
            n=1,
            temperature=0.7,
        )
        topics = response.choices[0].message['content'].strip().split('\n')
        return [topic.strip('1234567890. ') for topic in topics]
    except openai.error.OpenAIError as e:
        logger.error(f"Failed to generate AI topics: {str(e)}")
        return []

def generate_topic_suggestions():
    """Generate topic suggestions based on interests and trending topics."""
    trending_topics = fetch_trending_topics()
    ai_topics = generate_ai_topics()
    
    all_topics = trending_topics + ai_topics
    
    # Combine topics with interests
    combined_topics = []
    for interest in INTERESTS:
        for topic in all_topics:
            combined_topics.append(f"{interest}: {topic}")
    
    return combined_topics

def rank_topics(topics):
    ranked_topics = []
    for topic in topics:
        score = 0
        # Prefer longer topics (more detailed)
        score += len(topic.split()) * 0.1
        # Prefer topics with technical terms
        technical_terms = ['API', 'framework', 'algorithm', 'database', 'cloud', 'security', 'ML', 'AI']
        score += sum(term.lower() in topic.lower() for term in technical_terms) * 2
        # Prefer topics from certain sources
        if 'GitHub' in topic:
            score += 3
        elif 'Hacker News' in topic:
            score += 2
        
        ranked_topics.append((topic, score))
    
    # Sort topics by score in descending order
    ranked_topics.sort(key=lambda x: x[1], reverse=True)
    return ranked_topics

def choose_best_topic():
    generated_topics = load_generated_topics()
    
    for _ in range(10):  # Try up to 10 times to find a new topic
        topics = generate_topic_suggestions()
        ranked_topics = rank_topics(topics)
        
        for topic, _ in ranked_topics:
            # Extract the actual topic without the interest
            actual_topic = topic.split(': ', 1)[1] if ': ' in topic else topic
            if actual_topic not in generated_topics:
                generated_topics.append(actual_topic)
                save_generated_topics(generated_topics)
                logger.info(f"Chosen topic: {actual_topic}")
                return actual_topic
    
    logger.error("Failed to find a new topic after 10 attempts")
    return None

if __name__ == "__main__":
    print(choose_best_topic())
