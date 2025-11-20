# Article Scraper Generator - Project Overview

## Mission
Build an intelligent system that automatically analyzes website structures and generates 
custom Python scraper functions for extracting articles. The system must pass all provided test cases.

## The Challenge

You have 5 different test websites with articles, each with unique HTML structure:
- **newsroom-hub** - 18 articles in `/articles/`
- **tech-insights** - 15 articles in `/blog/`
- **arts-review-quarterly** - 22 articles in `/reviews/`
- **health-wellness-daily** - 19 articles in `/posts/`
- **travel-journal-atlas** - 18 articles in `/stories/`

Your system must:
1. Analyze each site's HTML structure automatically
2. Find where articles are located
3. Detect CSS selectors for extracting title and content
4. Generate a Python scraper function for that specific site
5. Execute the scraper to extract all articles
6. Save articles to a database

**Critical constraint:** Generated scrapers must work WITHOUT calling LLM during scraping.
LLM is only used for analysis and code generation.

## What Already Exists

Your project has:
- `sites/` folder with 5 test websites (HTML files)
- `tests/test_main.py` - test suite that validates your solution
- `src/main.py` - empty implementation with `get_articles(homepage_url)` function signature
- `pyproject.toml` - with requests, beautifulsoup4, lxml dependencies

## What You Must Build

### Core Components

**1. HTML Analyzer**
- Fetches HTML pages
- Identifies article URLs vs non-article URLs (about, contact, etc)
- Analyzes sample article pages to understand structure

**2. Selector Detector**
- Automatically finds CSS selectors for:
  - Article links on homepage
  - Article titles on article pages
  - Article content on article pages
- Uses heuristics like text density, tag types, common patterns

**3. LLM Integration**
- Uses OpenRouter API to enhance selector detection
- Sends HTML samples to LLM for analysis
- Receives improved CSS selectors from LLM
- Validates selectors work correctly

**4. Scraper Generator**
- Generates Python code as a string
- Creates standalone scraper function that:
  - Takes homepage URL as input
  - Fetches all article pages
  - Extracts title and content using CSS selectors
  - Returns List[Article]
- Saves generated code to `scrapers/` directory

**5. Database Layer**
- SQLite database for storing articles
- Tables for articles and scraping sessions
- Methods to save/retrieve articles

**6. Main Orchestrator**
- Implements `get_articles(homepage_url)` in `src/main.py`
- Coordinates: analysis → detection → generation → execution → storage
- Caches generated scrapers to avoid regenerating

## Technical Architecture

```
Input: homepage_url
  ↓
[Analyze HTML structure]
  ↓
[Detect CSS selectors] ←→ [LLM enhancement]
  ↓
[Generate Python scraper code]
  ↓
[Execute generated scraper]
  ↓
[Save to database]
  ↓
Output: List[Article]
```

## Success Criteria

Your implementation passes when:

1. ✅ All 5 test sites pass: `./test.sh` succeeds
2. ✅ Correct article counts:
   - arts-review-quarterly: 22
   - health-wellness-daily: 19
   - newsroom-hub: 18
   - tech-insights: 15
   - travel-journal-atlas: 18
3. ✅ No duplicate URLs
4. ✅ All article titles match expected titles exactly
5. ✅ Generated scrapers work without LLM calls
6. ✅ Database stores articles successfully

## Expected Article Class

```python
@dataclass
class Article:
    url: str      # Full URL to article
    title: str    # Article title
    content: str  # Full article text
```

## Project Structure You'll Create

```
src/
├── analyzer.py          # HTML fetching and analysis
├── selector_detector.py # CSS selector detection
├── llm_client.py        # OpenRouter integration
├── scraper_generator.py # Python code generation
├── selector_enhancer.py # Combines auto + LLM detection
├── pipeline.py          # Orchestration
├── database.py          # SQLite operations
└── main.py              # Entry point (update this)

scrapers/                # Generated scraper files
├── scraper_site1.py
└── scraper_site2.py

config.py                # Configuration
cli.py                   # Command-line interface
.env                     # API keys (create this)
articles.db              # Database (auto-created)
```

## Key Technical Decisions

**Why separate detection and LLM?**
- Auto-detection is fast and free
- LLM is slower and costs money
- Use LLM only when auto-detection is uncertain

**Why generate code instead of dynamic scraping?**
- Generated code is inspectable
- Can be version controlled
- No runtime LLM dependency
- Faster execution (no LLM calls)

**Why BeautifulSoup?**
- Simple and reliable
- Works with static HTML
- Test sites are static HTML files

## Environment Setup

You'll need:
```bash
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=anthropic/claude-3.5-sonnet
```

Get API key from: https://openrouter.ai/

## Testing Approach

Tests start a local HTTP server for each site:
```python
# Pseudo-code
start_http_server('sites/newsroom-hub', port=8001)
articles = get_articles('http://localhost:8001')
assert len(articles) == 18
assert all titles match expected
```

## Common Challenges You'll Face

1. **Different URL patterns**: `/articles/`, `/blog/`, `/posts/`, `/reviews/`, `/stories/`
2. **Different HTML structures**: Some use `<article>`, some use `<div class="post">`
3. **Multiple h1 tags**: Need to find the right one
4. **Pagination**: Some sites have multiple listing pages
5. **Related articles sections**: Don't count these as separate articles

## Development Strategy

Recommended approach:
1. Start with one site (newsroom-hub is simplest)
2. Get it working end-to-end
3. Test with second site (tech-insights)
4. Generalize your code to handle differences
5. Test with remaining sites
6. Refine until all tests pass

## Next Steps

Follow the numbered task files in sequence. Each task builds on the previous one and includes specific guidance on what to implement.

Start with `01-PROJECT-SETUP.md`