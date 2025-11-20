from dataclasses import dataclass
from typing import List, Dict, Callable
import re
import os
import sys
import importlib.util
from urllib.parse import urlparse

# Module-level cache for scrapers
_scraper_cache: Dict[str, Callable] = {}


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


def _create_site_id(homepage_url: str) -> str:
    """Create a unique identifier for a site from its URL."""
    parsed = urlparse(homepage_url)
    domain = parsed.netloc
    
    # Convert to valid identifier: remove dots, colons, etc.
    site_id = re.sub(r'[^a-zA-Z0-9]', '_', domain)
    return site_id.lower()


def get_articles(homepage_url: str) -> List[Article]:
    """
    Main orchestration function that generates and executes scrapers.
    
    Args:
        homepage_url: URL of the website to scrape
        
    Returns:
        List of Article objects scraped from the site
    """
    print(f"🚀 Starting article extraction from: {homepage_url}")
    
    try:
        # Step 1: Create site identifier
        site_id = _create_site_id(homepage_url)
        print(f"📝 Site ID: {site_id}")
        
        # Step 2: Check cache
        if site_id in _scraper_cache:
            print("⚡ Using cached scraper function")
            scraper_function = _scraper_cache[site_id]
        else:
            # Step 3: Generate scraper (if not cached)
            print("🔧 No cached scraper found, generating new one...")
            
            try:
                from src.pipeline import ScraperPipeline
                pipeline = ScraperPipeline()
                
                result = pipeline.generate_scraper_for_site(homepage_url)
                
                if 'error' in result:
                    print(f"❌ Pipeline generation failed: {result['error']}")
                    return []
                
                scraper_path = result['scraper_path']
                print(f"✅ Scraper generated: {scraper_path}")
                
                # Step 4: Load generated scraper
                print("📥 Loading scraper module...")
                spec = importlib.util.spec_from_file_location("generated_scraper", scraper_path)
                if not spec or not spec.loader:
                    print("❌ Failed to create module spec")
                    return []
                
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find the scraper function
                scraper_function = None
                for attr_name in dir(module):
                    if attr_name.startswith('scrape_') and callable(getattr(module, attr_name)):
                        scraper_function = getattr(module, attr_name)
                        break
                
                if not scraper_function:
                    print("❌ No scraper function found in generated module")
                    return []
                
                # Cache the function
                _scraper_cache[site_id] = scraper_function
                print(f"💾 Cached scraper function: {scraper_function.__name__}")
                
            except Exception as e:
                print(f"❌ Error during scraper generation: {e}")
                return []
        
        # Step 5: Execute scraper
        print("🏃 Executing scraper...")
        try:
            scraped_articles = scraper_function(homepage_url)
            print(f"📄 Raw scraper returned {len(scraped_articles)} articles")
        except Exception as e:
            print(f"❌ Scraper execution failed: {e}")
            return []
        
        # Step 6: Convert to Article objects and validate
        print("🔍 Converting and validating articles...")
        valid_articles = []
        
        for raw_article in scraped_articles:
            try:
                # Convert from scraper's Article class to our Article class
                article = Article(
                    url=raw_article.url,
                    title=raw_article.title,
                    content=raw_article.content
                )
                valid_articles.append(article)
            except ValueError as e:
                print(f"⚠️  Skipping invalid article: {e}")
                continue
            except Exception as e:
                print(f"⚠️  Skipping article due to error: {e}")
                continue
        
        print(f"✅ Validated {len(valid_articles)} articles")
        
        # Step 7: Save to database (optional)
        save_to_db = os.getenv('SAVE_TO_DB', 'true').lower() == 'true'
        if save_to_db and valid_articles:
            print("💾 Saving articles to database...")
            try:
                from src.database import Database
                
                db = Database()
                session_id = db.start_session(site_id)
                
                try:
                    save_result = db.save_articles(valid_articles, site_id)
                    db.finish_session(session_id, save_result['saved'])
                    
                    print(f"📊 Database save result: {save_result}")
                    if save_result['duplicates'] > 0:
                        print(f"ℹ️  Note: {save_result['duplicates']} articles were duplicates")
                        
                except Exception as e:
                    db.finish_session(session_id, 0, str(e))
                    print(f"⚠️  Database save failed: {e}")
                    # Don't fail the scraping, just log the error
                    
            except Exception as e:
                print(f"⚠️  Database initialization failed: {e}")
                # Don't fail the scraping, just log the error
        
        # Step 8: Return results
        print(f"🎉 Successfully extracted {len(valid_articles)} articles")
        return valid_articles
        
    except Exception as e:
        print(f"❌ Unexpected error in get_articles: {e}")
        import traceback
        traceback.print_exc()
        return []


def clear_cache():
    """Clear the scraper cache to force regeneration."""
    global _scraper_cache
    _scraper_cache.clear()
    print("🧹 Scraper cache cleared")


if __name__ == "__main__":
    """Command line testing interface."""
    if len(sys.argv) < 2:
        print("Usage: python src/main.py <homepage_url>")
        print("Example: python src/main.py http://localhost:8000")
        sys.exit(1)
    
    url = sys.argv[1]
    print(f"🔍 Testing article extraction from: {url}")
    print("=" * 60)
    
    # Extract articles
    articles = get_articles(url)
    
    print("\n" + "=" * 60)
    print("📊 RESULTS SUMMARY")
    print("=" * 60)
    print(f"Total articles extracted: {len(articles)}")
    
    if articles:
        print("\n📖 First few articles:")
        for i, article in enumerate(articles[:3], 1):
            print(f"\n{i}. {article.title}")
            print(f"   URL: {article.url}")
            print(f"   Content preview: {article.content[:100]}...")
            print(f"   Word count: {len(article.content.split())}")
    else:
        print("\n❌ No articles were extracted")
        
    print(f"\n🏁 Extraction complete!")
    
    # Show cache status
    print(f"\n💾 Cache status: {len(_scraper_cache)} scrapers cached")
    for site_id, func in _scraper_cache.items():
        print(f"   - {site_id}: {func.__name__}")
    
    sys.exit(0 if articles else 1)