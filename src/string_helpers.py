"""
This module contains helper functions for string manipulation.
"""
import re
import textwrap

from bs4 import BeautifulSoup

MAX_URL_LENGTH = 50
MAX_CONTENT_WIDTH = 110


def list_to_plain_text(data_list):
    return "\n".join([dict_to_plain_text(item) for item in data_list])


def dict_to_plain_text(data):
    # Format list items
    labels = ", ".join(data.get("labels", []))

    # Wrap content to 115 characters per line
    content_value = data.get("content") or ""
    content = textwrap.fill(content_value, width=MAX_CONTENT_WIDTH)

    # Generate plain text format
    plain_text = f"""
title: {data.get('title', '')},
sent_date: {data.get('sent_date', '')},
content: {content},
from: {data.get('from', '')},
to: {data.get('to', '')},
cc: {data.get('cc', 'null')},
bcc: {data.get('bcc', 'null')},
labels: {labels}
threadId: {data.get('other_metadata', {}).get('threadId', '')},
mimeType: {data.get('other_metadata', {}).get('mimeType', '')}
"""

    return plain_text


def shorten_urls(text):
    """Define a regex pattern to identify URLs starting with http or https"""
    # print(text)
    url_pattern = re.compile(r"http[s]?://[^\s]+")

    def repl(match):
        return match.group()[:MAX_URL_LENGTH]

    # Use the re.sub() function with the repl function to shorten URLs
    return url_pattern.sub(repl, text)


def clean_up_content(content):
    """Clean up the provided content by removing tags and extra whitespace."""

    soup = BeautifulSoup(content, "html.parser")

    for data in soup(["style", "script", "other_tags"]):
        # Remove tags
        data.decompose()

    cleaned_content = " ".join(soup.stripped_strings)
    # Remove zero-width spaces
    cleaned_content = cleaned_content.replace("\u200c", "")
    # Remove non-breaking spaces
    cleaned_content = cleaned_content.replace("\u00a0", "")
    # Remove extra whitespace
    cleaned_content = " ".join(cleaned_content.split())
    # Remove URLs
    cleaned_content = shorten_urls(cleaned_content)

    return cleaned_content
