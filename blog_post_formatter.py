import datetime
from slugify import slugify
from logger import setup_logger

logger = setup_logger(__name__, 'INFO')

def format_blog_post(topic, content):
    title = topic  # The topic is now the full title
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    url = f"/{date}/{slugify(title)}/"

    # Extract the image URL from the content if present
    image_url = None
    content_lines = content.split('\n')
    if content_lines[0].startswith('!['):
        image_url = content_lines[0].split('(')[1].split(')')[0]
        content = '\n'.join(content_lines[1:])

    # Determine the category based on the content
    category = determine_category(content)

    formatted_content = f"""---
categories:
  - {category}
comments: true
description: "A comprehensive guide to {title}"
headline: "{title}: Everything You Need to Know"
mathjax: null
modified: {date}
tags:
  - {category}
  - technology
  - programming
title: "{title}: A Deep Dive"
url: {url}
image: {image_url if image_url else ""}
---

{content}

"""
    filename = f"{date}-{slugify(title)}.md"
    logger.info(f"Formatted blog post: {filename}")
    return formatted_content, filename

def determine_category(content):
    # This is a simple example. You might want to use a more sophisticated method,
    # such as keyword analysis or even AI-based classification.
    categories = ['Technology', 'Programming', 'DevOps', 'Security', 'Data Science']
    for category in categories:
        if category.lower() in content.lower():
            return category.lower()
    return 'technology'  # Default category
