# Task 06: Database for Article Storage

## Goal
Create a SQLite database layer for persistently storing scraped articles and tracking scraping sessions. 
This allows tracking what has been scraped and provides a queryable store.

## Why Database?

- Persist articles across runs
- Track scraping history
- Avoid re-scraping same articles
- Query articles by site
- Generate statistics

## Database Schema

You need two tables:

**articles table:**
- `id` - INTEGER PRIMARY KEY AUTOINCREMENT
- `url` - TEXT NOT NULL UNIQUE (prevents duplicates)
- `title` - TEXT NOT NULL
- `content` - TEXT NOT NULL
- `site` - TEXT NOT NULL (which site it came from)
- `scraped_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `word_count` - INTEGER (calculated from content)
- `created_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP

**Indexes:**
- On `url` (for fast duplicate checking)
- On `site` (for filtering by site)

**scraping_sessions table:**
- `id` - INTEGER PRIMARY KEY AUTOINCREMENT
- `site` - TEXT NOT NULL
- `started_at` - TIMESTAMP DEFAULT CURRENT_TIMESTAMP
- `finished_at` - TIMESTAMP (NULL until finished)
- `articles_scraped` - INTEGER DEFAULT 0
- `status` - TEXT DEFAULT 'running' (running/completed/failed)
- `error_message` - TEXT (NULL unless failed)

## Implementation Tasks

### 1. Implement `__init__(db_path)`

Initialize database:
- Store db_path as instance variable
- Call `init_db()` to ensure tables exist
- Default db_path to "articles.db"

### 2. Create `get_connection()` Context Manager

Create a context manager method using `@contextmanager` decorator:
- Connects to SQLite database
- Sets row_factory to sqlite3.Row (allows column access by name)
- Yields connection
- Commits on success
- Rolls back on error
- Always closes connection

This ensures proper connection handling and automatic commit/rollback.

### 3. Implement `init_db()`

Create tables if they don't exist:
- Use `CREATE TABLE IF NOT EXISTS`
- Execute SQL for both tables
- Create indexes
- Use `with self.get_connection()` for automatic handling
- Don't fail if tables already exist

### 4. Implement `save_article(url, title, content, site)`

Save a single article:
- Calculate word_count (split content and count)
- Use INSERT with parameters (prevent SQL injection)
- Catch `sqlite3.IntegrityError` for duplicate URLs
- Return article ID if saved successfully
- Return None if duplicate (URL already exists)
- Use parameterized query: `INSERT INTO articles (url, title, content, site, word_count) VALUES (?, ?, ?, ?, ?)`

### 5. Implement `save_articles(articles, site)`

Batch save multiple articles:
- Loop through articles list
- Call `save_article()` for each
- Count successes and duplicates
- Return dict with:
  ```python
  {
      'saved': count_of_new_articles,
      'duplicates': count_of_existing_articles,
      'total': len(articles)
  }
  ```

### 6. Implement `get_article_by_url(url)`

Retrieve article by URL:
- SELECT query with WHERE url = ?
- Return dict of article data if found
- Return None if not found
- Convert row to dict: `dict(row)`

### 7. Implement `get_articles_by_site(site, limit=100)`

Get articles for a specific site:
- SELECT query with WHERE site = ?
- ORDER BY scraped_at DESC (newest first)
- Use LIMIT parameter
- Return list of article dicts

### 8. Implement `get_all_articles(limit=100)`

Get all articles:
- Similar to above but no WHERE clause
- Order by scraped_at DESC
- Apply limit
- Return list of dicts

### 9. Implement `get_stats()`

Calculate database statistics:
- Total article count: `SELECT COUNT(*) FROM articles`
- Articles per site: `SELECT site, COUNT(*) FROM articles GROUP BY site`
- Total words: `SELECT SUM(word_count) FROM articles`
- Return dict with:
  ```python
  {
      'total_articles': int,
      'total_words': int,
      'articles_by_site': {site: count, ...}
  }
  ```

### 10. Implement Session Tracking Methods

**`start_session(site)`:**
- INSERT new session record with site name
- Status defaults to 'running'
- Return session ID (lastrowid)

**`finish_session(session_id, articles_scraped, error_message=None)`:**
- UPDATE session record
- Set finished_at to CURRENT_TIMESTAMP
- Set articles_scraped count
- Set status to 'completed' or 'failed' based on error_message
- Set error_message if provided

**`get_recent_sessions(limit=10)`:**
- SELECT from scraping_sessions
- ORDER BY started_at DESC
- LIMIT to requested count
- Return list of session dicts

## Testing Strategy

Create `test_database.py` that:
1. Creates temporary test database
2. Tests each method:
   - Save single article
   - Try to save duplicate (should return None)
   - Batch save multiple articles
   - Retrieve by URL
   - Get articles by site
   - Get statistics
   - Session tracking
3. Verify:
   - Duplicate URLs rejected
   - Counts are correct
   - Stats calculate properly
   - Sessions track properly
4. Delete test database at end

Use temporary DB for testing to avoid polluting main DB.

## SQL Best Practices

**Parameterized queries:**
Always use `?` placeholders:
```python
cursor.execute("INSERT INTO articles (url, title) VALUES (?, ?)", (url, title))
```
Never string interpolation (prevents SQL injection)

**Connection management:**
Always use context manager to ensure connections close

**Error handling:**
Catch specific exceptions:
- `sqlite3.IntegrityError` for duplicates
- General exceptions for other DB errors

**NULL handling:**
Use `IS NULL` in SQL, not `= NULL`

## Common Challenges

**Challenge**: IntegrityError not caught
**Solution**: Import sqlite3 at top, catch `sqlite3.IntegrityError` specifically

**Challenge**: Row returns tuple instead of dict
**Solution**: Set `row_factory = sqlite3.Row` on connection

**Challenge**: Connection not closed
**Solution**: Always use context manager

**Challenge**: Word count incorrect
**Solution**: Use `content.split()` not `len(content)`

## Expected Behavior

After saving articles from all 5 test sites:
```python
stats = db.get_stats()
# stats['total_articles'] should be 92 (18+15+22+19+18)
# stats['articles_by_site'] should have 5 entries
```

Each site's articles should be:
- Retrievable by site name
- Counted correctly
- No duplicates

## Integration Notes

The database will be used by:
- Main orchestrator (save articles after scraping)
- CLI tool (query articles, show stats)
- Testing (verify articles saved correctly)

The database should be transparent - if save fails, don't crash the scraper.

## Success Criteria

✅ Tables created successfully
✅ Can save articles without errors
✅ Duplicate URLs are rejected (return None)
✅ Batch save works correctly
✅ Can retrieve articles by URL
✅ Can query by site
✅ Statistics calculate correctly
✅ Session tracking works
✅ No SQL injection vulnerabilities
✅ Connections always close properly

## Next Step
Once database operations work reliably, proceed to `07-MAIN-ORCHESTRATION.md` to connect all components and implement the main `get_articles()` function.