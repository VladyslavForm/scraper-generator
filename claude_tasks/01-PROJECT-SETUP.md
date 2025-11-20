# Task 01: Project Setup & Foundation

## Goal
Set up the project structure, install dependencies, create base files and 
data models that will be used throughout the project.

## What You Need to Accomplish

### 1. Update Dependencies

Add these packages to `pyproject.toml` dependencies array:
- `openai>=1.0.0` - for OpenRouter API (compatible client)
- `python-dotenv>=1.0.0` - for environment variables

The file already has: requests, beautifulsoup4, lxml

### 2. Create Environment Configuration

Create two files in project root:

**`.env`** - actual configuration (don't commit this):
- OPENROUTER_API_KEY (your key from openrouter.ai)
- OPENROUTER_MODEL (suggest: anthropic/claude-3.5-sonnet)

**`.env.example`** - template for others:
- Same keys but with empty/placeholder values

### 3. Improve Article Data Model

Update `src/main.py`:
- Change `Article` from a class to a `@dataclass`
- Add validation in `__post_init__` method:
  - URL must start with 'http'
  - Title cannot be empty
  - Content cannot be empty
- Keep the empty `get_articles()` function for now

### 4. Create Module Skeletons

Create these files with class/function definitions (empty implementations with `pass`):

**`src/analyzer.py`**
- `HTMLAnalyzer` class with:
  - `__init__(base_url)` - store base URL, create requests session
  - `fetch_page(url)` - will fetch and parse HTML
  - `is_article_url(url)` - will check if URL looks like an article
  - `find_article_links(soup)` - will find article URLs on a page
  - `analyze_homepage()` - will analyze homepage structure
  - `analyze_article_page(url)` - will analyze an article page
  - `analyze_site()` - will do complete site analysis

**`src/selector_detector.py`**
- `SelectorDetector` class with:
  - `find_article_link_pattern(soup)` - find pattern for article links
  - `detect_title_selector(soups)` - find CSS selector for titles
  - `detect_content_selector(soups)` - find CSS selector for content
  - `detect_selectors(homepage_soup, article_soups)` - combine all

**`src/llm_client.py`**
- `LLMClient` class with:
  - `__init__()` - initialize OpenAI client with OpenRouter base URL
  - `analyze_html_structure(...)` - send HTML to LLM for analysis
  - `validate_selectors(...)` - test if selectors work
  - `refine_selectors_with_feedback(...)` - improve failed selectors

**`src/scraper_generator.py`**
- `ScraperGenerator` class with:
  - `generate_scraper(site_name, selectors, metadata)` - generate Python code
  - `save_scraper(site_name, code)` - save to file
  - `generate_and_save(...)` - convenience method

**`src/database.py`**
- `Database` class with:
  - `__init__(db_path)` - initialize DB connection
  - `init_db()` - create tables
  - `save_article(...)` - save single article
  - `save_articles(...)` - save multiple articles
  - `get_articles_by_site(site)` - retrieve articles
  - `get_stats()` - database statistics

### 5. Create Supporting Files

**`src/selector_enhancer.py`**
- `SelectorEnhancer` class that combines auto-detection with LLM
- Methods: `__init__`, `get_enhanced_selectors()`

**`src/pipeline.py`**
- `ScraperPipeline` class that orchestrates everything
- Methods: `__init__`, `generate_scraper_for_site(url)`

**`config.py`** in project root
- `Config` class with:
  - Class variables for all settings (read from environment)
  - `validate()` method to check required config
  - `print_config()` method to display current config

### 6. Create Directories

Create `scrapers/` directory with a README.md explaining it will contain generated scrapers.

### 7. Install Dependencies

Run: `uv sync`

## How to Verify Success

1. All imports work without errors:
```python
from src.main import Article
from src.analyzer import HTMLAnalyzer
from src.selector_detector import SelectorDetector
from src.llm_client import LLMClient
from src.scraper_generator import ScraperGenerator
from src.database import Database
```

2. Can create Article instance and validation works:
```python
article = Article(
    url="http://example.com/article",
    title="Test",
    content="Content"
)
```

3. LLMClient initializes with API key from .env

4. All class instantiation works (even though methods are empty)

## Important Technical Notes

- **OpenRouter API**: Use `openai` package with base_url="https://openrouter.ai/api/v1"
- **BeautifulSoup**: Use 'lxml' parser for better performance
- **URL handling**: Use `urllib.parse` for URL manipulation
- **File paths**: Use `pathlib.Path` not string concatenation
- **Dataclass**: Import from `dataclasses`

## What NOT to Do

- Don't implement the actual logic yet - just structure
- Don't worry about tests yet - they'll fail, that's expected
- Don't add extra dependencies beyond what's specified
- Don't commit .env file (add to .gitignore)

## Expected Result

After this task:
- Project structure is ready
- All imports work
- No implementation yet, just scaffolding
- Ready to implement actual logic in next tasks

## Next Step
Proceed to `02-HTML-ANALYZER.md` to implement the HTML analysis logic.