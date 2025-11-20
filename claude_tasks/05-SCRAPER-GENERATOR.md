# Task 05: Python Scraper Code Generator

## Goal
Generate executable Python scraper functions as code strings. Each scraper should be a standalone function 
that uses BeautifulSoup and the detected CSS selectors to extract articles from a specific website.

## What The Generated Scraper Must Do

Each generated scraper is a Python file containing:
1. An `Article` class (dataclass)
2. A scraper function named `scrape_[site_name](homepage_url)`
3. The function should:
   - Fetch the homepage
   - Find all article links using the detected selector
   - Visit each article page
   - Extract title using the detected selector
   - Extract content using the detected selector
   - Return List[Article]
4. No LLM calls - it's pure web scraping code
5. Should be executable independently

## Implementation Tasks

### 1. Implement `_sanitize_name()` Helper

Create a method that converts any string to valid Python identifier:
- Remove `http://`, `https://`
- Remove domain extensions (`.com`, `.org`, etc.)
- Replace non-alphanumeric with underscore
- Remove leading/trailing underscores
- If starts with digit, prepend `site_`
- Return lowercase

Examples:
- `"http://example-site.com"` → `"example_site"`
- `"localhost:8000"` → `"localhost_8000"`
- `"my-cool-blog.io"` → `"my_cool_blog"`

### 2. Implement `generate_scraper()` Method

**Method signature:** `generate_scraper(site_name, selectors, metadata)`

**Purpose:** Generate complete Python scraper code as a string

**What to generate:**

Start with docstring explaining this is auto-generated.

Include imports:
- `from typing import List`
- `import requests`
- `from bs4 import BeautifulSoup`
- `from urllib.parse import urljoin`

Define Article class (dataclass with url, title, content).

Define scraper function with this structure:
1. **Setup:**
   - Create empty articles list
   - Create requests Session
   - Set User-Agent header
   
2. **Fetch homepage:**
   - GET request to homepage_url
   - Parse with BeautifulSoup
   - Handle errors (try/except, return empty on failure)
   
3. **Find article links:**
   - Use `soup.select()` with article_links selector
   - Extract href from each link element
   - Convert to absolute URL with urljoin
   - Store in a set (deduplicate)
   - Print count found
   
4. **For each article URL:**
   - Fetch the article page
   - Parse with BeautifulSoup
   - Extract title using `soup.select_one()` with title selector
   - Extract content using `soup.select_one()` with content selector
   - For content: get all `<p>` tags within content element, join their text
   - Create Article object if title and content found
   - Append to articles list
   - Print progress
   - Handle errors per article (continue on failure)
   
5. **Return articles list**

Add a `__main__` section for testing:
- Accept URL from command line args
- Call scraper function
- Print results summary

**String formatting:**
- Use f-strings to insert:
  - Function name (sanitized)
  - Selectors (as string literals)
  - Site name in docstrings/comments
- Ensure proper indentation (4 spaces)
- Escape quotes appropriately

### 3. Implement `save_scraper()` Method

**Method signature:** `save_scraper(site_name, code)`

**What to do:**
1. Create filename: `scraper_{sanitized_name}.py`
2. Ensure `scrapers/` directory exists
3. Write code string to file
4. Print confirmation with file path
5. Return the file path as string

### 4. Implement `generate_and_save()` Method

Convenience method that:
1. Calls `generate_scraper()`
2. Calls `save_scraper()`
3. Returns file path

This is the main public API of the class.

## Testing Strategy

Create `test_generator.py` that:
1. Starts local server for a test site
2. Uses HTMLAnalyzer + SelectorDetector to get selectors
3. Creates ScraperGenerator
4. Calls `generate_and_save()`
5. Reads the generated file
6. Verifies it's valid Python (try to compile it)
7. Dynamically imports the generated module
8. Finds the scraper function
9. Executes it with the local server URL
10. Validates returned articles:
    - Correct count
    - Have URLs, titles, content
    - No duplicates

Use `importlib.util` for dynamic import:
```python
spec = importlib.util.spec_from_file_location("generated", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
```

## Code Generation Best Practices

**Make generated code readable:**
- Clear variable names
- Comments explaining each section
- Proper indentation
- Consistent style

**Make it robust:**
- Try/except around network operations
- Continue on per-article errors (don't stop entire scrape)
- Return empty list if homepage fails
- Timeout on requests

**Make it informative:**
- Print how many articles found
- Print progress (e.g., "Scraped: Article Title...")
- Print errors (but don't crash)

**Avoid common pitfalls:**
- Escape quotes in selectors properly
- Handle newlines in generated code
- Test that generated code is syntactically valid

## Expected Generated Code Structure

```python
"""
Auto-generated scraper for [site_name]
"""

# Imports

class Article:
    # Dataclass

def scrape_[site_name](homepage_url: str) -> List[Article]:
    """Docstring"""
    # Session setup
    # Fetch homepage
    # Find article links with selector
    # For each article:
    #   Fetch, extract, create Article
    # Return articles

if __name__ == "__main__":
    # Test execution
```

## Testing Generated Scrapers

For each test site, generated scraper should:
- Find correct number of articles:
  - newsroom-hub: 18
  - tech-insights: 15
  - arts-review-quarterly: 22
  - health-wellness-daily: 19
  - travel-journal-atlas: 18
- Extract actual article titles (not navigation text)
- Extract substantial content (not empty)
- Not include duplicates

## Common Challenges

**Challenge**: String escaping issues (quotes in selectors)
**Solution**: Use triple-quotes for the entire code string, or escape carefully

**Challenge**: Generated code has syntax errors
**Solution**: Test by compiling with `compile(code, '<string>', 'exec')`

**Challenge**: Indentation issues in generated code
**Solution**: Be consistent - use 4 spaces, track indentation level

**Challenge**: Selector finds no elements in generated code but worked in testing
**Solution**: Verify selector strings are identical (no extra quotes/escaping)

## Success Criteria

✅ Generates valid Python code (no syntax errors)
✅ Generated code imports successfully
✅ Generated function executes without crashing
✅ Returns correct Article count for test sites
✅ Extracted titles and content are not empty
✅ No duplicate article URLs in results
✅ Code is readable and properly formatted
✅ Can generate scrapers for multiple sites

## Advanced: Pipeline Integration

Create `pipeline.py` with `ScraperPipeline` class that:
- Takes a site URL
- Runs complete flow:
  1. Use SelectorEnhancer to get selectors
  2. Use ScraperGenerator to create scraper
  3. Return path to generated scraper
- This becomes the main orchestration layer

Method signature: `generate_scraper_for_site(site_url) -> dict`

Return dict with:
- `scraper_path`: path to generated file
- `selectors`: the CSS selectors used
- `confidence`: detection confidence
- `metadata`: any relevant info

## Next Step
Once scraper generation works and produces valid, executable code, proceed to `06-DATABASE-SETUP.md` for persistent article storage.