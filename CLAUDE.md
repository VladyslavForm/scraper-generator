# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an intelligent article scraper generator that automatically analyzes website structures and generates custom Python scrapers for extracting articles. The system must pass all test cases for 5 different test websites with varying HTML structures.

## Development Environment

- **Python Version**: 3.13+
- **Package Manager**: uv (modern Python package manager)
- **Dependencies**: requests, beautifulsoup4, lxml
- **LLM Integration**: OpenRouter API for enhanced selector detection

## Setup Commands

```bash
# Install dependencies using uv
uv sync

# Run the full test suite
./test.sh

# Set up environment variables (create .env file)
echo "OPENROUTER_API_KEY=your_key" > .env
echo "OPENROUTER_MODEL=anthropic/claude-3.5-sonnet" >> .env
```

## Current Architecture

The project implements a sophisticated pipeline that:

1. **Analyzes HTML structure** of target websites automatically
2. **Detects CSS selectors** for article links, titles, and content  
3. **Generates Python scraper functions** as executable code
4. **Executes scrapers** to extract all articles from a website
5. **Stores results** in SQLite database

### Core Components

- `src/analyzer.py` - HTML fetching and structural analysis
- `src/generator.py` - Python scraper code generation  
- `src/database.py` - SQLite operations for article storage
- `data/src/main.py` - Main entry point with `get_articles()` function
- `claude_tasks/` - Detailed implementation guidance (8 task files)

### Test Data Structure

The project includes 5 test websites in `data/sites/`:
- **newsroom-hub** (18 articles in `/articles/`) 
- **tech-insights** (15 articles in `/blog/`)
- **arts-review-quarterly** (22 articles in `/reviews/`)
- **health-wellness-daily** (19 articles in `/posts/`)
- **travel-journal-atlas** (18 articles in `/stories/`)

## Key Technical Constraints

1. **No LLM calls during scraping** - Generated scrapers must be standalone
2. **Exact article counts required** - Tests validate specific article counts
3. **No duplicate URLs** - Each article must be unique
4. **Exact title matching** - Article titles must match expected values
5. **Static HTML processing** - All test sites are static HTML files

## Article Data Structure

```python
@dataclass
class Article:
    url: str      # Full URL to article
    title: str    # Article title  
    content: str  # Full article text content
```

## Development Workflow

The project follows a pipeline architecture:

```
homepage_url → HTML Analysis → Selector Detection → Code Generation → Scraper Execution → Database Storage → List[Article]
```

**Critical insight**: The system generates reusable Python scraper functions that work without runtime LLM dependencies, making them fast and cost-effective for repeated use.

## Testing Strategy

Tests start local HTTP servers for each test site and validate:
- Correct article extraction counts
- No duplicate URLs
- Exact title matching
- Database persistence

Run tests with: `./test.sh`