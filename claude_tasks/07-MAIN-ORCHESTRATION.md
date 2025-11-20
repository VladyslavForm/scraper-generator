# Task 07: Main Orchestration - Connecting Everything

## Goal
Implement the main `get_articles()` function in `src/main.py` that orchestrates the entire pipeline from analysis
to final results. This is the entry point that the tests will call.

## The Big Picture

The `get_articles()` function should:
1. Take homepage_url as input
2. Check if scraper already generated (cache)
3. If not cached: analyze → detect → generate → save scraper
4. Load and execute the scraper function
5. Validate results
6. Save to database (optional but recommended)
7. Return List[Article]

## Implementation Tasks

### 1. Implement `get_articles(homepage_url)` in src/main.py

**Flow:**

**Step 1: Create site identifier**
- Extract domain and port from URL
- Create unique ID like "localhost_8001" or "example_com"
- Use this for caching and database

**Step 2: Check cache**
- Create module-level dict: `_scraper_cache = {}`
- Check if `site_id` is in cache
- If yes, skip to execution
- If no, continue to generation

**Step 3: Generate scraper (if not cached)**
- Create ScraperPipeline instance
- Call `pipeline.generate_scraper_for_site(homepage_url)`
- Get back dict with scraper_path, selectors, etc.
- Handle errors gracefully (return empty list)

**Step 4: Load generated scraper**
- Use `importlib.util.spec_from_file_location()` to load the Python file
- Create module from spec
- Execute module to get functions
- Find the scraper function (starts with `scrape_`)
- Store function in cache

**Step 5: Execute scraper**
- Call scraper function with homepage_url
- Catch any exceptions
- If fails, return empty list

**Step 6: Convert to Article objects**
- Generated scraper returns its own Article class instances
- Convert to your Article dataclass
- Validate each article (URL, title, content not empty)
- Skip invalid articles

**Step 7: Save to database (optional)**
- Check environment variable `SAVE_TO_DB` (default true)
- If true:
  - Create Database instance
  - Start session
  - Save articles
  - Finish session
- Handle database errors gracefully (don't crash scraping)

**Step 8: Return results**
- Return List[Article]

Add informative print statements showing progress.

### 2. Create `clear_cache()` Function

Helper function to reset scraper cache:
- Clear the `_scraper_cache` dict
- Useful for testing

### 3. Add `if __name__ == "__main__"` Section

For testing from command line:
- Accept URL from command line args
- Call `get_articles(url)`
- Print summary:
  - Total count
  - First few titles
  - Sample content

### 4. Create config.py

Configuration management class:

**Config class should have:**
- Class variables for all settings:
  - OPENROUTER_API_KEY (from env)
  - OPENROUTER_MODEL (from env, default value)
  - DATABASE_PATH (from env, default "articles.db")
  - SAVE_TO_DB (from env, default true)
  - USER_AGENT (constant)
  - REQUEST_TIMEOUT (from env, default 10)
  
- `validate()` class method:
  - Check required settings present
  - Raise clear error if API key missing
  
- `print_config()` class method:
  - Display current configuration
  - Hide sensitive data (show "✅ Set" not actual key)

### 5. Create cli.py

Command-line interface with subcommands:

**Subcommands:**

**scrape**: `python cli.py scrape <url>`
- Call `get_articles(url)`
- Print results
- Options:
  - `--output file.txt` to save results
  - `--clear-cache` to force regeneration

**stats**: `python cli.py stats`
- Load database
- Call `get_stats()`
- Display formatted statistics:
  - Total articles
  - Total words
  - Breakdown by site

**sessions**: `python cli.py sessions`
- Load database
- Get recent sessions
- Display formatted session history:
  - Session ID
  - Site
  - Time
  - Articles scraped
  - Status

**config**: `python cli.py config`
- Display current configuration
- Show what's set, what's missing

Use `argparse` for CLI parsing.

## Testing Strategy

Create `test_system.py` that runs complete end-to-end test:

For each test site:
1. Start local HTTP server
2. Clear scraper cache
3. Call `get_articles()`
4. Verify:
   - Correct article count
   - All articles have URL, title, content
   - No duplicates
   - Titles look reasonable
5. Check database was updated
6. Try again (should use cache, be faster)

Test all 5 sites in sequence.

## Error Handling Strategy

Each step should handle errors:
- Pipeline generation fails → return empty list, log error
- Scraper loading fails → return empty list, log error
- Scraper execution fails → return empty list, log error
- Database save fails → log warning, continue (don't fail scrape)

Never crash. Always return something useful or empty list.

## Caching Strategy

**Why cache?**
- Avoid regenerating scrapers for same site
- Much faster on second run
- Saves API costs

**Cache key:**
- Use domain + port as key
- "localhost:8000" → "localhost_8000"
- "example.com" → "example_com"

**When to clear cache?**
- During testing (force fresh generation)
- If scraper is broken (regenerate)
- Command-line flag

## Performance Considerations

**First run (no cache):**
- Analysis: ~5-10 seconds
- LLM call: ~5 seconds
- Generation: ~1 second
- Execution: ~10-30 seconds depending on article count
- **Total: ~20-45 seconds**

**Cached run:**
- Check cache: instant
- Execution: ~10-30 seconds
- **Total: ~10-30 seconds**

## Expected Behavior for Test Sites

When calling `get_articles()` for each site:

| Site | Articles | Time (first) | Time (cached) |
|------|----------|--------------|---------------|
| newsroom-hub | 18 | ~30s | ~15s |
| tech-insights | 15 | ~30s | ~12s |
| arts-review-quarterly | 22 | ~40s | ~20s |
| health-wellness-daily | 19 | ~35s | ~15s |
| travel-journal-atlas | 18 | ~30s | ~15s |

## Integration Points

The `get_articles()` function is called by:
- Test suite (`tests/test_main.py`)
- CLI tool (`cli.py`)
- Your own testing scripts

It uses:
- ScraperPipeline (orchestrates generation)
- Database (stores results)
- Config (settings)

## Common Challenges

**Challenge**: Cache not working (regenerates every time)
**Solution**: Verify site_id is consistent, check cache dict isn't being cleared

**Challenge**: Module import fails
**Solution**: Check file path is correct, Python file has no syntax errors

**Challenge**: Function not found in loaded module
**Solution**: Search dir(module) for functions starting with "scrape_"

**Challenge**: Database permission error
**Solution**: Ensure DB file location is writable

**Challenge**: Out of memory with large sites
**Solution**: Could add limits on article count (but not needed for test sites)

## CLI Usage Examples

```bash
# Scrape a site
python cli.py scrape http://localhost:8000

# Scrape and save to file
python cli.py scrape http://localhost:8000 --output results.txt

# Force regenerate scraper
python cli.py scrape http://localhost:8000 --clear-cache

# View database stats
python cli.py stats

# View scraping history
python cli.py sessions

# Check configuration
python cli.py config
```

## Success Criteria

✅ `get_articles()` works end-to-end
✅ Returns correct article count for each test site
✅ Caching works (second run is faster)
✅ Database saves articles successfully
✅ Error handling prevents crashes
✅ CLI provides useful interface
✅ Config management works
✅ Can run from command line
✅ All 5 test sites work

## Next Step
Once main orchestration works, proceed to `08-TESTING-VALIDATION.md` to ensure everything passes the official tests and handle edge cases.