from typing import List, Dict, Any
from bs4 import BeautifulSoup, Tag
from collections import Counter
import re


class SelectorDetector:
    
    def _get_css_selector(self, element: Tag) -> str:
        """Generate CSS selector for a BeautifulSoup element."""
        if not element or not hasattr(element, 'name'):
            return ''
            
        tag = element.name
        
        # Prefer ID if it exists
        if element.get('id'):
            return f"{tag}#{element.get('id')}"
        
        # Use classes if available
        classes = element.get('class', [])
        if classes:
            # Filter out very specific classes (with numbers, unique IDs)
            clean_classes = []
            for cls in classes:
                if not re.search(r'\d+|uuid|unique|id-', str(cls), re.I):
                    clean_classes.append(str(cls))
            
            if clean_classes:
                class_str = '.'.join(clean_classes)
                return f"{tag}.{class_str}"
        
        # Fallback to just tag name
        return tag
    
    def _get_text_density(self, element: Tag) -> float:
        """Calculate text-to-HTML ratio for an element."""
        if not element:
            return 0.0
            
        text_content = element.get_text(strip=True)
        html_content = str(element)
        
        if len(html_content) == 0:
            return 0.0
            
        return len(text_content) / len(html_content)
    
    def _count_paragraphs(self, element: Tag) -> int:
        """Count <p> tags within an element."""
        if not element:
            return 0
        return len(element.find_all('p'))
    
    def find_article_link_pattern(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """Find pattern for article links."""
        # Find all links that could be article links
        all_links = soup.find_all('a', href=True)
        
        container_patterns = Counter()
        link_selectors = Counter()
        
        for link in all_links:
            href = link.get('href', '')
            
            # Skip obvious non-article links
            if any(pattern in href.lower() for pattern in ['/about', '/contact', '/terms', '/privacy']):
                continue
                
            # Look at the link's parent containers
            parent = link.parent
            for level in range(3):  # Check 3 levels up
                if not parent or not hasattr(parent, 'name'):
                    break
                    
                # Check if this container looks like an article container
                container_classes = parent.get('class', [])
                container_class_str = ' '.join(container_classes).lower()
                
                # Look for article-like container patterns
                article_patterns = ['article', 'post', 'card', 'item', 'entry', 'story', 'review']
                if (parent.name in ['article', 'div', 'section'] and 
                    any(pattern in container_class_str for pattern in article_patterns)):
                    
                    container_selector = self._get_css_selector(parent)
                    link_selector = f"{container_selector} a"
                    
                    container_patterns[container_selector] += 1
                    link_selectors[link_selector] += 1
                    break
                    
                parent = parent.parent
        
        # Return the most common pattern
        if container_patterns:
            most_common_container = container_patterns.most_common(1)[0]
            most_common_link = link_selectors.most_common(1)[0]
            
            return {
                'container_selector': most_common_container[0],
                'count': most_common_container[1],
                'link_selector': most_common_link[0]
            }
        
        # Fallback
        return {
            'container_selector': 'article',
            'count': 0,
            'link_selector': 'article a'
        }
    
    def detect_title_selector(self, soups: List[BeautifulSoup]) -> str:
        """Find CSS selector for titles by analyzing multiple article pages."""
        title_selectors = Counter()
        
        for soup in soups:
            candidates = []
            
            # Level 1: Look for h1 inside semantic containers (most specific)
            for container in soup.find_all(['article', 'main']):
                h1_tags = container.find_all('h1')
                for h1 in h1_tags:
                    candidates.append((f"{container.name} h1", 3))  # High priority
            
            # Level 2: Look for h1 with title-related classes
            h1_with_classes = soup.find_all('h1', class_=True)
            for h1 in h1_with_classes:
                classes = h1.get('class', [])
                class_str = ' '.join(classes).lower()
                if any(word in class_str for word in ['title', 'heading', 'headline']):
                    selector = self._get_css_selector(h1)
                    candidates.append((selector, 2))  # Medium priority
            
            # Level 3: Look for any h1 (fallback)
            h1_tags = soup.find_all('h1')
            for h1 in h1_tags:
                candidates.append(('h1', 1))  # Low priority
            
            # Level 4: Check h2 with title classes as backup
            h2_with_title = soup.find_all(['h2', 'h3'], class_=re.compile(r'title|heading', re.I))
            for h2 in h2_with_title:
                selector = self._get_css_selector(h2)
                candidates.append((selector, 1))  # Low priority
            
            # Choose the highest priority candidate
            if candidates:
                best_candidate = max(candidates, key=lambda x: x[1])
                title_selectors[best_candidate[0]] += 1
        
        # Return the most common selector
        if title_selectors:
            return title_selectors.most_common(1)[0][0]
        
        return 'h1'  # Ultimate fallback
    
    def detect_content_selector(self, soups: List[BeautifulSoup]) -> str:
        """Find CSS selector for content by analyzing multiple article pages."""
        content_selectors = Counter()
        
        for soup in soups:
            candidates = []
            
            # Level 1: Check for article tag (semantic HTML)
            articles = soup.find_all('article')
            for article in articles:
                paragraph_count = self._count_paragraphs(article)
                text_density = self._get_text_density(article)
                
                if paragraph_count >= 2:  # Must have substantial content
                    # Look for content divs inside article first
                    content_divs = article.find_all('div', class_=re.compile(r'content|body|text', re.I))
                    if content_divs:
                        for div in content_divs:
                            div_paragraphs = self._count_paragraphs(div)
                            if div_paragraphs >= 2:
                                selector = f"article {self._get_css_selector(div)}"
                                score = div_paragraphs * 10 + text_density * 5
                                candidates.append((selector, score))
                    else:
                        # Use article itself
                        score = paragraph_count * 8 + text_density * 5
                        candidates.append(('article', score))
            
            # Level 2: Check for main tag
            main_tags = soup.find_all('main')
            for main in main_tags:
                paragraph_count = self._count_paragraphs(main)
                text_density = self._get_text_density(main)
                if paragraph_count >= 2:
                    score = paragraph_count * 7 + text_density * 5
                    candidates.append(('main', score))
            
            # Level 3: Look for divs with content-related classes
            content_patterns = ['content', 'article-content', 'post-content', 'body', 
                              'article-body', 'post-body', 'text', 'entry-content']
            
            for pattern in content_patterns:
                divs = soup.find_all('div', class_=re.compile(pattern, re.I))
                for div in divs:
                    paragraph_count = self._count_paragraphs(div)
                    text_density = self._get_text_density(div)
                    
                    if paragraph_count >= 2:
                        selector = self._get_css_selector(div)
                        score = paragraph_count * 6 + text_density * 5
                        candidates.append((selector, score))
            
            # Choose the highest scoring candidate
            if candidates:
                best_candidate = max(candidates, key=lambda x: x[1])
                content_selectors[best_candidate[0]] += 1
        
        # Return the most common selector
        if content_selectors:
            return content_selectors.most_common(1)[0][0]
        
        return 'article'  # Ultimate fallback
    
    def detect_selectors(self, homepage_soup: BeautifulSoup, article_soups: List[BeautifulSoup]) -> Dict[str, str]:
        """Combine all selector detection."""
        print(f"Detecting selectors from {len(article_soups)} article pages...")
        
        # Find article link pattern
        link_pattern = self.find_article_link_pattern(homepage_soup)
        article_links_selector = link_pattern['link_selector']
        
        print(f"Article link pattern found: {article_links_selector} (appears {link_pattern['count']} times)")
        
        # Detect title selector
        title_selector = self.detect_title_selector(article_soups)
        print(f"Title selector detected: {title_selector}")
        
        # Detect content selector
        content_selector = self.detect_content_selector(article_soups)
        print(f"Content selector detected: {content_selector}")
        
        return {
            'article_links': article_links_selector,
            'title': title_selector,
            'content': content_selector
        }