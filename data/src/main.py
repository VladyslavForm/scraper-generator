from dataclasses import dataclass
from typing import List


@dataclass
class Article:
    url: str
    title: str
    content: str
    
    def __post_init__(self):
        if not self.url.startswith('http'):
            raise ValueError("URL must start with 'http'")
        if not self.title.strip():
            raise ValueError("Title cannot be empty")
        if not self.content.strip():
            raise ValueError("Content cannot be empty")


def get_articles(homepage_url: str) -> List[Article]:
    return []