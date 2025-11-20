# Task 02: HTML Analyzer Implementation

## Goal
Implement the HTML analyzer that can fetch web pages, identify article URLs, 
and analyze site structure to prepare for selector detection.

## What This Component Does

The HTMLAnalyzer is responsible for:
1. Fetching HTML content from URLs
2. Distinguishing article URLs from non-article URLs (like "about", "contact", etc.)
3. Finding all article links on the homepage
4. Analyzing sample article pages to understand their structure
5. Providing structured data about the site to other components

## Implementation Tasks

### 1. Implement `fetch_page(url)` Method

This method should:
- Accept a URL (can be relative or absolute)
- Convert relative URLs to absolute using the base_url
- Make HTTP request with requests library
- Parse HTML with BeautifulSoup (use 'lxml' parser)
- Return BeautifulSoup object on success, None on error
- Handle network errors gracefully (timeout, connection errors)
- Use the session created in `__init__` for efficiency
- Set a reasonable timeout (10 seconds)

### 2. Implement `is_article_url(url)` Method

Create heuristics to detect if a URL is likely an article:

**Should return True for URLs containing:**
- `/article` or `/articles/`
- `/post` or `/posts/`
- `/blog/`
- `/news/`
- `/review` or `/reviews/`
- `/story` or `/stories/`
- Date patterns like `/2024/03/`

**Should return False for URLs containing:**
- `/about`
- `/contact`
- `/privacy` or `/terms`
- `/category` or `/categories`
- `/tag` or `/tags`
- `/author` or `/authors`
- `/page/` followed by numbers (pagination)

Use regular expressions to check these patterns. Make checks case-insensitive.

### 3. Implement `find_article_links(soup)` Method

This method should:
- Take a BeautifulSoup object (usually of homepage)
- Find all `<a>` tags with href attribute
- For each link:
  - Convert to absolute URL
  - Check if it's from the same domain
  - Check if it looks like an article (using `is_article_url`)
- Return list of unique article URLs
- Store URLs in a set during processing to avoid duplicates

**Technical details:**
- Use `soup.find_all('a', href=True)` to get links
- Use `urljoin(base_url, href)` for URL resolution
- Use `urlparse()` to check domain matching
- Filter out external links

### 4. Implement `analyze_homepage()` Method

This method should:
- Fetch the homepage using `fetch_page`
- Find all article links using `find_article_links`
- Select up to 5 sample articles for deeper analysis
- Return a dictionary with:
  - `homepage_url`: the base URL
  - `total_article_links`: count of found article URLs
  - `article_links`: list of all article URLs
  - `sample_article_urls`: list of 3-5 URLs for analysis
  - `homepage_html`: first 5000 characters of HTML (for LLM)

### 5. Implement `analyze_article_page(article_url)` Method

This method should:
- Fetch the article page
- Try to identify key elements:
  - Possible title elements (h1, h2 with "title" class, etc.)
  - Possible content containers (article tag, main tag, divs with "content"/"post" classes)
- Return dictionary with:
  - `url`: the article URL
  - `html_sample`: first 5000 chars of HTML
  - `possible_titles`: list of tuples (tag_name, text)
  - `content_candidates`: list of potential CSS selectors

**Heuristics for finding elements:**
- Titles: Look at h1 first, then h2/h3 with title-related classes
- Content: Check `<article>`, `<main>`, divs with classes containing "content", "article", "post", "entry"

### 6. Implement `analyze_site()` Method

This method should:
- Call `analyze_homepage()` to get article links
- For each sample article URL, call `analyze_article_page()`
- Return complete analysis dictionary with:
  - `homepage`: results from homepage analysis
  - `sample_articles`: list of article analyses
  - `base_url`: the site's base URL

Add print statements to show progress (e.g., "Found 18 article links", "Analyzing article X/5")

## Testing Your Implementation

Create a test script `test_analyzer.py` that:
1. Starts a local HTTP server for one test site (use subprocess)
2. Creates HTMLAnalyzer instance
3. Runs `analyze_site()`
4. Prints results
5. Verifies:
   - Found correct number of articles
   - URLs look reasonable
   - Sample articles were analyzed

Use this pattern to test:
```python
# Start server
process = subprocess.Popen(
    ['python', '-m', 'http.server', '8000'],
    cwd='sites/newsroom-hub'
)
time.sleep(2)

# Test analyzer
analyzer = HTMLAnalyzer('http://localhost:8000')
result = analyzer.analyze_site()

# Check results
print(f"Found {len(result['homepage']['article_links'])} articles")

# Stop server
process.terminate()
```

## Expected Behavior for Test Sites

When analyzing each test site:

**newsroom-hub**: Should find ~18 article URLs in `/articles/` directory
**tech-insights**: Should find ~15 article URLs in `/blog/` directory
**arts-review-quarterly**: Should find ~22 article URLs in `/reviews/` directory
**health-wellness-daily**: Should find ~19 article URLs in `/posts/` directory
**travel-journal-atlas**: Should find ~18 article URLs in `/stories/` directory

## Common Challenges

**Challenge**: Finding too many URLs (including tags, categories, etc.)
**Solution**: Make `is_article_url()` more restrictive, check for exclude patterns first

**Challenge**: Finding too few URLs
**Solution**: Check if your patterns match the actual URL structure, look at real HTML

**Challenge**: Same article counted multiple times
**Solution**: Use set to deduplicate URLs

**Challenge**: Relative vs absolute URLs
**Solution**: Always convert to absolute early, use `urljoin()`

## Technical Reminders

- Store `self.base_url` without trailing slash in `__init__`
- Use `self.session` for all requests (reuses connection)
- Parse domain from base_url once in `__init__`: `urlparse(base_url).netloc`
- Add User-Agent header to session
- Handle encoding properly (let requests detect it)

## Success Criteria

✅ Can fetch any page from test sites
✅ Correctly identifies article URLs vs other URLs
✅ Finds all article links on homepage
✅ Can analyze individual article pages
✅ `analyze_site()` returns structured data
✅ Works with all 5 test sites
✅ Doesn't crash on network errors

## Next Step
Once analyzer finds article links correctly, proceed to `03-STRUCTURE-DETECTOR.md` to implement CSS selector detection.