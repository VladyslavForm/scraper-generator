# Task 08: Testing & Validation

## Goal
Ensure your complete system passes all provided tests, handles edge cases, and meets all success criteria. This is the final validation before considering the project complete.

## The Official Test Suite

Your project includes `tests/test_main.py` which tests:
- All 5 sites
- Correct article counts
- No duplicate URLs
- Exact title matching
- All URLs from same domain

## Running The Tests

```bash
./test.sh
```

Or directly:
```bash
python -m pytest tests/ -v
```

## Expected Test Results

All tests should pass:
- `test_arts_review_quarterly` - 22 articles
- `test_health_wellness_daily` - 19 articles
- `test_newsroom_hub` - 18 articles
- `test_tech_insights` - 15 articles
- `test_travel_journal_atlas` - 18 articles

## Debugging Failed Tests

### Create Debug Script

Build `debug_test.py` that:
1. Tests one site at a time
2. Shows detailed information:
   - Expected vs actual article count
   - All scraped titles
   - Any duplicate URLs found
   - Any URLs from wrong domain
3. Compares results with expected titles

**For each site, show:**
- ✅/❌ Article count correct
- ✅/❌ No duplicates
- ✅/❌ All titles match expected
- List of any issues found

### Common Test Failures

**Scenario: Too few articles**

Possible causes:
- Article link selector not matching all articles
- Some articles failing to scrape (check for errors)
- Content selector not finding content (articles skipped)

Debug approach:
- Print all URLs found by article link selector
- Check if all expected URLs are in the list
- For each article, print whether title/content found
- Check generated scraper code for issues

**Scenario: Too many articles**

Possible causes:
- Link selector matching non-article links (tags, categories)
- Including pagination pages as articles
- Including navigation items

Debug approach:
- Print all URLs found
- Check which URLs shouldn't be there
- Improve `is_article_url()` heuristics
- Make article link selector more specific

**Scenario: Wrong titles**

Possible causes:
- Title selector selecting wrong element
- Multiple h1 tags, selecting wrong one
- Getting site title instead of article title

Debug approach:
- Fetch one article manually
- Try title selector in browser DevTools
- Check what element it actually selects
- Refine selector to be more specific

**Scenario: Duplicates**

Possible causes:
- Same article URL appears twice on homepage
- Relative URL treated as different from absolute

Debug approach:
- Print all URLs before deduplication
- Check if duplicates are really identical
- Ensure URLs are normalized (all absolute)
- Use set for deduplication in scraper

## Improving Selector Detection

If automatic detection consistently fails:

### For Article Links

Improve heuristics in `is_article_url()`:
- Add more patterns specific to test sites
- Check URL length (articles usually have longer paths)
- Look at link text (articles have substantial text)
- Consider link parent container

### For Titles

Improve detection in `detect_title_selector()`:
- Prefer h1 inside semantic containers (article, main)
- Deprioritize h1 if there are multiple
- Consider heading classes (title, heading, headline)
- Use most consistent selector across samples

### For Content

Improve detection in `detect_content_selector()`:
- Require minimum paragraph count (2+)
- Calculate text density (high = more content)
- Prefer semantic HTML (article, main)
- Check for common class patterns

## Validation Script

Create `test_report.py` that:
1. Tests all 5 sites
2. Generates comprehensive report:
   - Success/failure for each site
   - Detailed metrics for each
   - Overall success rate
   - Summary of issues found

**For each site report:**
- Site name
- Expected count vs actual
- Number of duplicates (should be 0)
- Number of wrong URLs (should be 0)
- List of titles found
- Pass/fail status

## Fine-Tuning Process

If tests don't pass initially:

1. **Identify which site(s) fail**
2. **Run debug script for that site**
3. **Analyze the specific issue:**
   - Article count off? → Check link selector
   - Wrong titles? → Check title selector
   - No content? → Check content selector
   - Duplicates? → Check URL normalization
4. **Fix the root cause:**
   - Adjust heuristics in SelectorDetector
   - Improve prompts to LLM
   - Fix bugs in generated scraper code
5. **Test again**
6. **Repeat until all pass**

## Common Adjustments Needed

### Article Link Detection

If finding wrong links:
- Make `is_article_url()` more restrictive
- Add exclude patterns for your specific sites
- Check link text length/content

If missing links:
- Make `is_article_url()` less restrictive
- Add include patterns for URL structures you're missing
- Check if links are in unusual places (JavaScript, etc.)

### Title Extraction

If getting wrong titles:
- Prefer `article h1` over bare `h1`
- Skip h1 that appears multiple times
- Look for title in specific classes

If missing titles:
- Fall back to h2 if no h1
- Check page title tag as fallback
- Look at first heading in content area

### Content Extraction

If content is empty:
- Check selector actually matches
- Get all p tags, not just first
- Check for content in different locations

If content has extra stuff:
- Be more specific with selector
- Filter out sidebars, related articles
- Use content area markers

## Test Data Validation

Ensure test expectations are correct:
- Check actual HTML files in `sites/`
- Count articles manually if needed
- Verify expected title lists in tests
- Make sure you understand what test expects

## Performance Testing

Time your implementation:
- First run: should complete in <60s per site
- Cached run: should complete in <30s per site
- All 5 sites: should complete in <5 minutes total

If too slow:
- Check for unnecessary LLM calls
- Optimize HTML fetching (reuse sessions)
- Consider concurrent article fetching (advanced)

## Final Validation Checklist

Before considering the project complete:

✅ **All 5 official tests pass**
✅ **No test failures or errors**
✅ **Article counts exactly match expected:**
   - arts-review-quarterly: 22
   - health-wellness-daily: 19
   - newsroom-hub: 18
   - tech-insights: 15
   - travel-journal-atlas: 18
✅ **No duplicate URLs in any result**
✅ **All article titles match expected titles**
✅ **All URLs are from correct domain**
✅ **Generated scrapers work without LLM calls**
✅ **Database stores articles successfully**
✅ **Error handling works (no crashes)**
✅ **Caching works (faster second run)**
✅ **CLI tools are functional**

## Documentation

Once everything passes, document your system:

Create `SOLUTION.md` that explains:
- Overall architecture
- How components work together
- Key design decisions
- How to run/use the system
- Troubleshooting tips

## Success Celebration

When `./test.sh` shows all green:

```
test_arts_review_quarterly ... ok
test_health_wellness_daily ... ok
test_newsroom_hub ... ok
test_tech_insights ... ok
test_travel_journal_atlas ... ok

----------------------------------------------------------------------
Ran 5 tests in 45.123s

OK
```

**You're done! 🎉**

## What You've Built

A complete system that:
- Automatically analyzes website structures
- Detects CSS selectors intelligently
- Uses LLM for complex cases
- Generates executable Python scrapers
- Stores articles in database
- Handles errors gracefully
- Passes all tests
- Is maintainable and extensible

## Optional Enhancements

If you want to go further:
- Add pagination support (multi-page article lists)
- Implement concurrent scraping (faster)
- Add content deduplication (similar articles)
- Create web UI for scraper management
- Add scheduling for periodic scraping
- Export articles to different formats
- Add full-text search on articles

But for the assignment, passing all tests is success!

## Troubleshooting Resources

If stuck:
1. Read test error messages carefully
2. Use debug scripts to isolate issues
3. Check generated scraper code manually
4. Test selectors in browser DevTools
5. Review HTML structure of problematic sites
6. Adjust detection heuristics iteratively

## Project Complete

Congratulations on building an intelligent article scraper generator! 

Your system demonstrates:
- Web scraping expertise
- LLM integration skills  
- Code generation capabilities
- Database management
- Error handling
- Test-driven development
- System architecture design

This is a production-ready foundation that could be extended for real-world use cases.