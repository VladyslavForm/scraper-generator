from typing import Dict, Any
from src.analyzer import HTMLAnalyzer
from src.selector_detector import SelectorDetector
from src.llm_client import LLMClient


class SelectorEnhancer:
    def __init__(self, base_url: str):
        """Initialize with base URL and all required components."""
        self.base_url = base_url
        self.analyzer = HTMLAnalyzer(base_url)
        self.detector = SelectorDetector()
        
        try:
            self.llm_client = LLMClient()
            self.has_llm = True
        except ValueError as e:
            print(f"Warning: LLM not available: {e}")
            print("Will use automatic detection only.")
            self.llm_client = None
            self.has_llm = False
    
    def get_enhanced_selectors(self) -> Dict[str, Any]:
        """Complete analysis flow combining automatic detection with LLM enhancement."""
        print(f"\n🔍 Starting enhanced selector detection for: {self.base_url}")
        
        # Step 1: Analyze site structure
        print("📊 Analyzing site structure...")
        site_analysis = self.analyzer.analyze_site()
        
        if 'error' in site_analysis.get('homepage', {}):
            return {
                'error': f"Failed to analyze site: {site_analysis['homepage']['error']}",
                'selectors': {},
                'method': 'failed',
                'confidence': 'none'
            }
        
        # Get soups for processing
        homepage_soup = self.analyzer.fetch_page(self.base_url)
        article_soups = []
        sample_urls = site_analysis['homepage']['sample_article_urls'][:3]
        
        print(f"📄 Fetching {len(sample_urls)} sample articles for analysis...")
        for url in sample_urls:
            soup = self.analyzer.fetch_page(url)
            if soup:
                article_soups.append(soup)
        
        if not article_soups:
            return {
                'error': "No article pages could be fetched for analysis",
                'selectors': {},
                'method': 'failed',
                'confidence': 'none'
            }
        
        # Step 2: Automatic selector detection
        print("🤖 Running automatic selector detection...")
        auto_selectors = self.detector.detect_selectors(homepage_soup, article_soups)
        print(f"   Detected: {auto_selectors}")
        
        # Step 3: LLM enhancement (if available)
        final_selectors = auto_selectors.copy()
        method = 'automatic'
        confidence = 'medium'
        notes = "Automatic detection completed"
        
        if self.has_llm:
            print("🧠 Enhancing selectors with LLM analysis...")
            
            # Prepare HTML samples for LLM
            homepage_html = str(homepage_soup)
            article_htmls = [str(soup) for soup in article_soups]
            
            # Get LLM analysis
            llm_result = self.llm_client.analyze_html_structure(
                homepage_html, article_htmls, auto_selectors
            )
            
            if 'error' not in llm_result:
                print("   ✅ LLM analysis successful")
                final_selectors = llm_result.get('selectors', auto_selectors)
                confidence = llm_result.get('confidence', 'medium')
                notes = llm_result.get('notes', 'LLM enhanced selectors')
                method = 'llm_enhanced'
                
                # Step 4: Validate selectors
                print("🧪 Validating enhanced selectors...")
                
                # Validate article_links on homepage, title/content on article pages
                homepage_html = str(homepage_soup)
                article_html = article_htmls[0]
                
                # Test article_links on homepage
                homepage_validation = self.llm_client.validate_selectors(
                    homepage_html, {'article_links': final_selectors['article_links']}
                )
                
                # Test title/content on article page
                article_validation = self.llm_client.validate_selectors(
                    article_html, {
                        'title': final_selectors['title'],
                        'content': final_selectors['content']
                    }
                )
                
                # Combine validation results
                validation_results = {**homepage_validation, **article_validation}
                
                failed_selectors = [name for name, passed in validation_results.items() if not passed]
                
                if failed_selectors:
                    print(f"   ⚠️  Some selectors failed validation: {failed_selectors}")
                    print("🔧 Refining failed selectors...")
                    
                    refined_selectors = self.llm_client.refine_selectors_with_feedback(
                        final_selectors, validation_results, homepage_html, article_html
                    )
                    
                    final_selectors = refined_selectors
                    method = 'llm_refined'
                    notes += " (refined after validation)"
                else:
                    print("   ✅ All selectors passed validation")
            else:
                print(f"   ⚠️  LLM analysis failed: {llm_result.get('error')}")
                print("   Falling back to automatic selectors")
        
        # Final result
        result = {
            'selectors': final_selectors,
            'method': method,
            'confidence': confidence,
            'notes': notes,
            'article_urls': site_analysis['homepage']['article_links'],
            'total_articles': site_analysis['homepage']['total_article_links']
        }
        
        print(f"\n🎯 Final Results:")
        print(f"   Method: {method}")
        print(f"   Confidence: {confidence}")
        print(f"   Articles found: {result['total_articles']}")
        print(f"   Selectors: {final_selectors}")
        if notes:
            print(f"   Notes: {notes}")
        
        return result