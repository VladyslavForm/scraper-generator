# Task 03: CSS Selector Detection

## Goal
Implement intelligent CSS selector detection that automatically finds the right selectors
for extracting article titles and content across different website structures.

## The Challenge

Different sites structure their HTML differently:
- Some use semantic HTML (`<article>`, `<main>`)
- Some use divs with classes like `.post-content`, `.article-body`
- Title might be in `<h1>`, or `<h2 class="title">`, or in page `<title>`
- Content might be in `<article>`, `<div class="content">`, or just multiple `<p>` tags

Your detector must find patterns that work consistently across multiple articles on the same site.

## Implementation Tasks

### 1. Helper Method: `_get_css_selector(element)`

Create a method that generates a CSS selector for a BeautifulSoup element:
- If element has an ID, return `tag#id` (most specific)
- If element has classes, return `tag.class1.class2`
- Otherwise return just the tag name
- Handle special characters in class names (join with dots)

### 2. Helper Method: `_get_text_density(element)`

Calculate how "text-heavy" an element is:
- Get text content (stripped)
- Get HTML content
- Return ratio: len(text) / len(html)
- Higher density = more content, less markup
- Use this to identify main content areas

### 3. Helper Method: `_count_paragraphs(element)`

Count `<p>` tags within an element:
- Use `element.find_all('p')`
- Return count
- Content areas typically have multiple paragraphs

### 4. Implement `find_article_link_pattern(soup)`

Find the common pattern for article links on a listing page:

**Strategy:**
- Find all links on the page
- For each link, look at its parent container
- Identify containers that have article-like characteristics:
  - Named "article", "post", "card", "item", etc.
  - Contain multiple links with similar structure
- Count which container type appears most often
- Return the most common pattern as a CSS selector

**Return dictionary with:**
- `container_selector`: CSS selector for the container
- `count`: how many times it appears
- `link_selector`: full selector like "div.article-card a"

### 5. Implement `detect_title_selector(soups)`

Detect title selector by analyzing MULTIPLE article pages (passed as list):

**Strategy:**
- For each article page:
  - Find `<h1>` tags (most common for titles)
  - Look for headings in semantic containers (`<article>`, `<main>`)
  - Check for headings with title-related classes
  - Record what selector found the title
- Count which selector appears most consistently across all articles
- Return the most common selector

**Specificity levels (prefer more specific):**
1. `article h1` or `main h1` (inside semantic container)
2. `h1.title` or `h1.heading` (with title class)
3. `h1` (fallback)

**Return:** The CSS selector string

### 6. Implement `detect_content_selector(soups)`

Detect content selector by analyzing MULTIPLE article pages:

**Strategy for each page:**
- Check for `<article>` tag first (semantic HTML)
  - If found, look for content divs inside it
  - Or use the article tag itself
- Check for `<main>` tag
- Look for divs with content-related classes:
  - "content", "article-content", "post-content"
  - "body", "article-body", "post-body"
  - "text", "entry-content"
- For each candidate:
  - Calculate text density
  - Count paragraphs
  - Elements with high paragraph count and decent density are likely content

**Scoring:**
- Prioritize high paragraph count (more content = better)
- Consider text density (but some markup is okay)
- Ignore elements with <2 paragraphs (too small)

**Return:** The most common content selector across all analyzed pages

### 7. Implement `detect_selectors(homepage_soup, article_soups)`

Main method that combines everything:
- Takes homepage BeautifulSoup and list of article BeautifulSoup objects
- Calls `find_article_link_pattern()` with homepage
- Calls `detect_title_selector()` with article soups
- Calls `detect_content_selector()` with article soups
- Returns dictionary:
  ```python
  {
      'article_links': 'selector for finding article links',
      'title': 'selector for article title',
      'content': 'selector for article content'
  }
  ```

## Testing Strategy

Create `test_selectors.py` that:
1. Starts local server for a test site
2. Creates HTMLAnalyzer, fetches homepage and sample articles
3. Creates SelectorDetector
4. Calls `detect_selectors()`
5. Prints detected selectors
6. Validates by actually using the selectors:
   - Use `soup.select()` with detected selectors
   - Check if they find elements
7. Test with multiple sites to see consistency

## Expected Results

For **newsroom-hub**, selectors should look like:
- article_links: Something matching `.article-card a` or similar
- title: `article h1` or `h1`
- content: `article` or `.article-content`

For **tech-insights**, might be:
- article_links: Something matching blog post cards
- title: `article h1` or `h1`
- content: `article` or `.post-content`

Selectors will differ by site, but should be consistent within each site.

## Common Challenges

**Challenge**: Selector too specific (includes IDs or unique classes)
**Solution**: In `_get_css_selector()`, prefer tag + common class over IDs

**Challenge**: Different selectors for different articles on same site
**Solution**: Take the MOST COMMON selector, use Counter from collections

**Challenge**: Content selector matches sidebar or footer too
**Solution**: Use paragraph count and text density to filter

**Challenge**: Multiple h1 tags on page (site title + article title)
**Solution**: Prefer h1 inside `<article>` or `<main>` over standalone h1

## Key Insights

**Why analyze multiple articles?**
- Single article might have quirks
- Multiple articles reveal consistent patterns
- Most common pattern is likely the right one

**Why prefer semantic HTML?**
- More reliable (`<article>`, `<main>` have specific meaning)
- Less likely to break if CSS classes change
- Better fallback if classes are complex

**What makes a good selector?**
- Specific enough to find the right element
- General enough to work across all articles on that site
- Uses semantic tags or common patterns
- Doesn't rely on content-specific attributes

## Success Criteria

✅ Detects different selectors for different sites
✅ Same selectors work across all articles on one site
✅ Selectors actually find elements when used with `soup.select()`
✅ Title selector finds exactly one title per article
✅ Content selector finds substantial text content
✅ Works reliably on all 5 test sites

## Next Step
Once selector detection works, proceed to `04-LLM-INTEGRATION.md` to add LLM-powered analysis for complex cases.