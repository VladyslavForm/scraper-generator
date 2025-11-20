from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import time


class HTMLAnalyzer:
    def __init__(self, base_url: str):
        """Initialize with base URL and create requests session."""
        self.base_url = base_url.rstrip('/')  # Remove trailing slash
        self.domain = urlparse(base_url).netloc
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; ScraperBot/1.0)'
        })
        
    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse HTML page."""
        try:
            # Convert relative URLs to absolute
            if not url.startswith('http'):
                url = urljoin(self.base_url, url)
            
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Parse HTML with lxml parser
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
            
        except (requests.exceptions.RequestException, Exception) as e:
            print(f"Error fetching {url}: {e}")
            return None
        
    def is_article_url(self, url: str) -> bool:
        """Check if URL looks like an article."""
        url_lower = url.lower()
        
        # Check exclude patterns first
        exclude_patterns = [
            r'/about',
            r'/contact',
            r'/privacy',
            r'/terms',
            r'/category',
            r'/categories',
            r'/tag',
            r'/tags',
            r'/author',
            r'/authors',
            r'/page/\d+',  # pagination
            r'/(blog|articles|posts|reviews|stories)/?$',  # index pages
        ]
        
        for pattern in exclude_patterns:
            if re.search(pattern, url_lower):
                return False
        
        # Check include patterns
        include_patterns = [
            r'/articles?/',
            r'/posts?/',
            r'/blog/',
            r'/news/',
            r'/reviews?/',
            r'/stories/',
            r'/\d{4}/\d{2}/',  # date patterns like /2024/03/
        ]
        
        for pattern in include_patterns:
            if re.search(pattern, url_lower):
                return True
                
        return False
        
    def find_article_links(self, soup: BeautifulSoup) -> List[str]:
        """Find article URLs on a page."""
        article_urls = set()  # Use set to avoid duplicates
        
        # Find all links with href attribute
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href')
            if not href:
                continue
                
            # Convert to absolute URL
            absolute_url = urljoin(self.base_url, href)
            
            # Check if it's from the same domain
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc != self.domain:
                continue
                
            # Check if it looks like an article
            if self.is_article_url(absolute_url):
                article_urls.add(absolute_url)
        
        return list(article_urls)
    
    def find_pagination_links(self, soup: BeautifulSoup) -> List[str]:
        """Find pagination URLs on a page."""
        pagination_urls = set()
        
        # Find all links with href attribute
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href')
            if not href:
                continue
                
            # Convert to absolute URL
            absolute_url = urljoin(self.base_url, href)
            
            # Check if it's from the same domain
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc != self.domain:
                continue
                
            # Check if it's a pagination URL
            url_lower = absolute_url.lower()
            if re.search(r'/page/\d+', url_lower):
                pagination_urls.add(absolute_url)
        
        return list(pagination_urls)
        
    def find_content_section_links(self, soup: BeautifulSoup) -> List[str]:
        """Find links to potential content sections like /blog/, /articles/, etc."""
        content_sections = set()
        
        # Look for navigation links that might lead to content sections
        nav_links = soup.find_all('a', href=True)
        
        for link in nav_links:
            href = link.get('href')
            if not href:
                continue
                
            # Convert to absolute URL
            absolute_url = urljoin(self.base_url, href)
            
            # Check if it's from the same domain
            parsed_url = urlparse(absolute_url)
            if parsed_url.netloc != self.domain:
                continue
                
            # Check if it looks like a content section
            url_lower = absolute_url.lower()
            content_patterns = [
                r'/blog/?$',
                r'/articles/?$', 
                r'/posts/?$',
                r'/news/?$',
                r'/reviews/?$',
                r'/stories/?$'
            ]
            
            for pattern in content_patterns:
                if re.search(pattern, url_lower):
                    content_sections.add(absolute_url)
                    break
        
        return list(content_sections)
    
    def analyze_homepage(self) -> Dict[str, Any]:
        """Analyze homepage structure."""
        print(f"Analyzing homepage: {self.base_url}")
        
        all_article_links = set()
        pages_crawled = 0
        
        # Start with the homepage
        pages_to_crawl = [self.base_url]
        crawled_pages = set()
        content_sections_to_check = set()
        
        while pages_to_crawl and pages_crawled < 10:  # Limit to prevent infinite loops
            current_url = pages_to_crawl.pop(0)
            
            if current_url in crawled_pages:
                continue
                
            print(f"Crawling page: {current_url}")
            soup = self.fetch_page(current_url)
            if not soup:
                continue
                
            crawled_pages.add(current_url)
            pages_crawled += 1
            
            # Find article links on this page
            article_links = self.find_article_links(soup)
            all_article_links.update(article_links)
            
            # Find pagination links (only from listing pages)
            pagination_links = self.find_pagination_links(soup)
            for page_url in pagination_links:
                if page_url not in crawled_pages:
                    pages_to_crawl.append(page_url)
            
            # Find content section links (only from homepage)
            if current_url == self.base_url:
                content_sections = self.find_content_section_links(soup)
                content_sections_to_check.update(content_sections)
                # Store homepage HTML for LLM
                homepage_html = str(soup)[:5000]
        
        # Now check content sections we discovered
        for section_url in content_sections_to_check:
            if section_url not in crawled_pages and pages_crawled < 10:
                print(f"Checking content section: {section_url}")
                soup = self.fetch_page(section_url)
                if soup:
                    crawled_pages.add(section_url)
                    pages_crawled += 1
                    
                    # Find articles in this section
                    article_links = self.find_article_links(soup)
                    all_article_links.update(article_links)
                    
                    # Find pagination in this section
                    pagination_links = self.find_pagination_links(soup)
                    for page_url in pagination_links:
                        if page_url not in crawled_pages:
                            pages_to_crawl.append(page_url)
        
        # Continue with any remaining pagination pages
        while pages_to_crawl and pages_crawled < 15:  # Increased limit
            current_url = pages_to_crawl.pop(0)
            
            if current_url in crawled_pages:
                continue
                
            print(f"Crawling pagination page: {current_url}")
            soup = self.fetch_page(current_url)
            if not soup:
                continue
                
            crawled_pages.add(current_url)
            pages_crawled += 1
            
            # Find article links on this page
            article_links = self.find_article_links(soup)
            all_article_links.update(article_links)
        
        article_links_list = list(all_article_links)
        print(f"Found {len(article_links_list)} total article links across {pages_crawled} pages")
        
        # Select up to 5 sample articles
        sample_articles = article_links_list[:5]
        
        return {
            'homepage_url': self.base_url,
            'total_article_links': len(article_links_list),
            'article_links': article_links_list,
            'sample_article_urls': sample_articles,
            'homepage_html': homepage_html if 'homepage_html' in locals() else '',
            'pages_crawled': pages_crawled
        }
        
    def analyze_article_page(self, url: str) -> Dict[str, Any]:
        """Analyze an article page structure."""
        soup = self.fetch_page(url)
        if not soup:
            return {
                'url': url,
                'error': 'Could not fetch page',
                'html_sample': '',
                'possible_titles': [],
                'content_candidates': []
            }
        
        # Find possible title elements
        possible_titles = []
        
        # Check h1 first
        h1_tags = soup.find_all('h1')
        for h1 in h1_tags:
            text = h1.get_text(strip=True)
            if text:
                possible_titles.append(('h1', text))
        
        # Check h2/h3 with title-related classes
        for tag_name in ['h2', 'h3']:
            headers = soup.find_all(tag_name, class_=re.compile(r'title', re.I))
            for header in headers:
                text = header.get_text(strip=True)
                if text:
                    possible_titles.append((tag_name, text))
        
        # Find content candidates
        content_candidates = []
        
        # Check for semantic HTML elements
        if soup.find('article'):
            content_candidates.append('article')
        if soup.find('main'):
            content_candidates.append('main')
        
        # Check for divs with content-related classes
        content_classes = ['content', 'article', 'post', 'entry', 'text', 'body']
        for class_name in content_classes:
            if soup.find('div', class_=re.compile(class_name, re.I)):
                content_candidates.append(f'div[class*="{class_name}"]')
        
        # Get HTML sample
        html_sample = str(soup)[:5000]
        
        return {
            'url': url,
            'html_sample': html_sample,
            'possible_titles': possible_titles,
            'content_candidates': content_candidates
        }
        
    def analyze_site(self) -> Dict[str, Any]:
        """Do complete site analysis."""
        print(f"\nStarting complete site analysis for: {self.base_url}")
        
        # Analyze homepage
        homepage_analysis = self.analyze_homepage()
        
        if 'error' in homepage_analysis:
            return {
                'base_url': self.base_url,
                'homepage': homepage_analysis,
                'sample_articles': []
            }
        
        # Analyze sample articles
        sample_articles = []
        sample_urls = homepage_analysis['sample_article_urls']
        
        for i, article_url in enumerate(sample_urls, 1):
            print(f"Analyzing article {i}/{len(sample_urls)}: {article_url}")
            article_analysis = self.analyze_article_page(article_url)
            sample_articles.append(article_analysis)
            time.sleep(0.5)  # Be respectful with requests
        
        print(f"Site analysis complete!")
        
        return {
            'base_url': self.base_url,
            'homepage': homepage_analysis,
            'sample_articles': sample_articles
        }