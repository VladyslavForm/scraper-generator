from typing import Dict, Any
from src.selector_enhancer import SelectorEnhancer
from src.generator import ScraperGenerator
from src.database import Database


class ScraperPipeline:
    def __init__(self):
        """Initialize pipeline components."""
        self.generator = ScraperGenerator()
        self.database = Database()
        
    def generate_scraper_for_site(self, site_url: str) -> Dict[str, Any]:
        """Complete scraper generation pipeline for a site.
        
        Args:
            site_url: URL of the website to generate scraper for
            
        Returns:
            Dict with scraper_path, selectors, confidence, and metadata
        """
        print(f"\n🚀 Starting complete scraper generation pipeline for: {site_url}")
        
        try:
            # Step 1: Enhanced selector detection
            print("🔍 Step 1: Analyzing site and detecting selectors...")
            enhancer = SelectorEnhancer(site_url)
            selector_result = enhancer.get_enhanced_selectors()
            
            if 'error' in selector_result:
                return {
                    'error': f"Selector detection failed: {selector_result['error']}",
                    'scraper_path': None,
                    'selectors': {},
                    'confidence': 'none'
                }
            
            # Step 2: Generate scraper code
            print("🛠️  Step 2: Generating scraper code...")
            site_name = site_url.split('//')[-1].split('/')[0]  # Extract domain
            
            scraper_path = self.generator.generate_and_save(
                site_name=site_name,
                selectors=selector_result['selectors'],
                metadata={
                    'site_url': site_url,
                    'method': selector_result['method'],
                    'confidence': selector_result['confidence'],
                    'article_count': selector_result.get('total_articles', 0),
                    'article_urls': selector_result.get('article_urls', [])
                }
            )
            
            # Step 3: Return results
            result = {
                'scraper_path': scraper_path,
                'selectors': selector_result['selectors'],
                'confidence': selector_result['confidence'],
                'method': selector_result['method'],
                'notes': selector_result.get('notes', ''),
                'total_articles': selector_result.get('total_articles', 0),
                'site_name': site_name
            }
            
            print(f"\n🎉 Pipeline complete!")
            print(f"   💾 Scraper saved to: {scraper_path}")
            print(f"   🎯 Method: {result['method']}")
            print(f"   🕰️ Confidence: {result['confidence']}")
            print(f"   📄 Articles found: {result['total_articles']}")
            
            return result
            
        except Exception as e:
            return {
                'error': f"Pipeline failed: {str(e)}",
                'scraper_path': None,
                'selectors': {},
                'confidence': 'none'
            }