from typing import Dict, Any, List
import openai
import os
import json
import re
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    def __init__(self):
        """Initialize OpenAI client with OpenRouter base URL."""
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENROUTER_API_KEY not found. Please set it in your .env file.\n"
                "Get your API key from: https://openrouter.ai/"
            )
        
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1"
        )
        self.model = os.getenv("OPENROUTER_MODEL", "anthropic/claude-3.5-sonnet")
        
    def analyze_html_structure(self, homepage_html: str, article_htmls: List[str], detected_selectors: Dict[str, str]) -> Dict[str, Any]:
        """Send HTML samples to LLM for analysis and validation."""
        try:
            # Truncate HTML samples to manage token usage
            homepage_sample = homepage_html[:3000]
            article_samples = [html[:3000] for html in article_htmls[:2]]  # Use first 2 articles
            
            system_message = """You are an expert at analyzing HTML structure for web scraping. 
Your task is to validate and improve CSS selectors that will be used with BeautifulSoup's .select() method.

Goal: Find the best CSS selectors for:
- article_links: Links to individual articles on listing pages
- title: Article title on individual article pages  
- content: Main article content on individual article pages

Respond ONLY with valid JSON in the exact format shown below."""
            
            user_prompt = f"""Analyze this website structure and validate/improve the CSS selectors.

Homepage HTML sample:
```html
{homepage_sample}
```

Sample article HTML:
```html
{article_samples[0] if article_samples else 'No article sample available'}
```

Currently detected selectors:
{json.dumps(detected_selectors, indent=2)}

Please respond with ONLY this JSON format:
```json
{{
  "selectors": {{
    "article_links": "CSS selector for article links",
    "title": "CSS selector for article title", 
    "content": "CSS selector for article content"
  }},
  "confidence": "high|medium|low",
  "notes": "observations about the site structure",
  "potential_issues": ["list any concerns or potential issues"]
}}
```"""
            
            # Make API call
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            # Parse response
            content = response.choices[0].message.content.strip()
            
            # Try direct JSON parsing first
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # Try to extract JSON from markdown code blocks
                json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', content, re.DOTALL | re.IGNORECASE)
                if json_match:
                    return json.loads(json_match.group(1))
                
                # If all parsing fails, return error
                return {
                    "error": "Failed to parse LLM response as JSON",
                    "raw_response": content[:500]
                }
                
        except Exception as e:
            return {
                "error": f"LLM API call failed: {str(e)}",
                "fallback_selectors": detected_selectors
            }
        
    def validate_selectors(self, test_html: str, selectors: Dict[str, str]) -> Dict[str, bool]:
        """Test if selectors actually work on HTML."""
        results = {}
        
        try:
            soup = BeautifulSoup(test_html, 'lxml')
            
            for name, selector in selectors.items():
                try:
                    elements = soup.select(selector)
                    results[name] = len(elements) > 0
                except Exception:
                    # Invalid CSS selector
                    results[name] = False
            
            return results
            
        except Exception:
            # If parsing fails, assume all selectors failed
            return {name: False for name in selectors.keys()}
        
    def refine_selectors_with_feedback(self, selectors: Dict[str, str], validation_results: Dict[str, bool], homepage_html: str, article_html: str) -> Dict[str, str]:
        """Ask LLM to fix selectors that failed validation."""
        # Check which selectors failed
        failed_selectors = {name: selector for name, selector in selectors.items() 
                           if not validation_results.get(name, False)}
        
        # If all passed, return unchanged
        if not failed_selectors:
            return selectors
            
        try:
            failed_names = list(failed_selectors.keys())
            
            system_message = """You are an expert at CSS selectors for web scraping. Some selectors failed to find elements. 
Analyze the HTML and provide corrected selectors that will work with BeautifulSoup's .select() method."""
            
            user_prompt = f"""The following selectors failed to find elements:
{json.dumps(failed_selectors, indent=2)}

Context:
- "article_links" selector should find links on the HOMEPAGE that lead to articles
- "title" and "content" selectors should work on individual ARTICLE pages

Homepage HTML sample:
```html
{homepage_html[:2000]}
```

Article page HTML sample:
```html
{article_html[:2000]}
```

Please provide corrected selectors. Respond with ONLY JSON:
```json
{{
  "corrected_selectors": {{
    "selector_name": "corrected CSS selector"
  }},
  "explanation": "what was wrong and how you fixed it"
}}
```"""
            
            response = self.client.chat.completions.create(
                model=self.model,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": user_prompt}
                ]
            )
            
            content = response.choices[0].message.content.strip()
            
            # Parse response
            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                json_match = re.search(r'```(?:json)?\s*({.*?})\s*```', content, re.DOTALL | re.IGNORECASE)
                if json_match:
                    result = json.loads(json_match.group(1))
                else:
                    return selectors  # Return original if parsing fails
            
            # Update selectors with corrections
            updated_selectors = selectors.copy()
            corrected = result.get('corrected_selectors', {})
            
            for name, corrected_selector in corrected.items():
                if name in updated_selectors:
                    updated_selectors[name] = corrected_selector
                    
            return updated_selectors
            
        except Exception as e:
            print(f"Warning: Failed to refine selectors with LLM: {e}")
            return selectors  # Return original selectors if refinement fails