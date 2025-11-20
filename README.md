# Auto Scraper Generator

Intelligent article scraper generator that automatically analyzes website structures and creates custom Python scrapers for extracting articles. The system uses LLM integration for enhanced CSS selector detection.

## 🚀 Quick Start

### 1. Install Dependencies

```bash
# Install via uv (recommended)
uv sync

# Or via pip
pip install requests beautifulsoup4 lxml openai python-dotenv
```

### 2. Setup API Key

Create a `.env` file in the project root:

```bash
echo "OPENROUTER_API_KEY=your_api_key_here" > .env
echo "OPENROUTER_MODEL=anthropic/claude-3.5-sonnet" >> .env
```

### 3. Basic Usage

```python
from src.pipeline import ScraperPipeline

# Create scraper generator
pipeline = ScraperPipeline()

# Generate scraper for a website
result = pipeline.generate_scraper_for_site("https://example-news.com")

# Result contains path to generated scraper
print(f"Scraper created: {result['scraper_path']}")
```

### 4. Extract Articles

```python
from data.src.main import get_articles

# Extract all articles from a website
articles = get_articles("https://example-news.com")

# Each article contains:
for article in articles:
    print(f"URL: {article.url}")
    print(f"Title: {article.title}")
    print(f"Content: {article.content[:100]}...")
```

## 🛠️ System Components

- **HTML Analyzer** (`src/analyzer.py`) - analyzes website structure
- **Selector Detector** (`src/selector_detector.py`) - finds CSS selectors
- **LLM Client** (`src/llm_client.py`) - enhances selectors via AI
- **Code Generator** (`src/generator.py`) - creates ready-to-use scrapers
- **Database** (`src/database.py`) - stores extracted articles

## 🧪 Testing

```bash
# Run full test suite
./test.sh

# Or via uv
uv run python -m pytest
```

## 📊 View Results

Articles are saved to SQLite database `articles.db`. To view:

```bash
# Via SQLite CLI
sqlite3 articles.db
> SELECT COUNT(*) FROM articles;
> SELECT site, COUNT(*) FROM articles GROUP BY site;
```