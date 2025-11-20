from typing import List, Dict, Any, Optional
import sqlite3
from pathlib import Path
from contextlib import contextmanager
from src.main import Article


class Database:
    def __init__(self, db_path: str = "articles.db"):
        """Initialize database with path and create tables."""
        self.db_path = Path(db_path)
        self.init_db()
    
    @contextmanager
    def get_connection(self):
        """Context manager for database connections with proper error handling."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Allow column access by name
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
        
    def init_db(self):
        """Create tables and indexes if they don't exist."""
        with self.get_connection() as conn:
            # Create articles table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS articles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    url TEXT NOT NULL UNIQUE,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    site TEXT NOT NULL,
                    scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    word_count INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create scraping_sessions table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS scraping_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site TEXT NOT NULL,
                    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    finished_at TIMESTAMP,
                    articles_scraped INTEGER DEFAULT 0,
                    status TEXT DEFAULT 'running',
                    error_message TEXT
                )
            """)
            
            # Create indexes
            conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_url ON articles (url)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_articles_site ON articles (site)")
        
    def save_article(self, url: str, title: str, content: str, site: str) -> Optional[int]:
        """Save a single article, return article ID if saved or None if duplicate."""
        word_count = len(content.split())
        
        try:
            with self.get_connection() as conn:
                cursor = conn.execute("""
                    INSERT INTO articles (url, title, content, site, word_count)
                    VALUES (?, ?, ?, ?, ?)
                """, (url, title, content, site, word_count))
                return cursor.lastrowid
        except sqlite3.IntegrityError:
            # URL already exists
            return None
        
    def save_articles(self, articles: List[Article], site: str) -> Dict[str, int]:
        """Batch save multiple articles."""
        saved = 0
        duplicates = 0
        
        for article in articles:
            result = self.save_article(article.url, article.title, article.content, site)
            if result is not None:
                saved += 1
            else:
                duplicates += 1
        
        return {
            'saved': saved,
            'duplicates': duplicates,
            'total': len(articles)
        }
        
    def get_article_by_url(self, url: str) -> Optional[Dict[str, Any]]:
        """Retrieve article by URL."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM articles WHERE url = ?
            """, (url,))
            row = cursor.fetchone()
            return dict(row) if row else None
        
    def get_articles_by_site(self, site: str, limit: int = 100) -> List[Dict[str, Any]]:
        """Get articles for a specific site."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM articles 
                WHERE site = ? 
                ORDER BY scraped_at DESC 
                LIMIT ?
            """, (site, limit))
            return [dict(row) for row in cursor.fetchall()]
        
    def get_all_articles(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get all articles."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM articles 
                ORDER BY scraped_at DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]
        
    def get_stats(self) -> Dict[str, Any]:
        """Calculate database statistics."""
        with self.get_connection() as conn:
            # Total article count
            cursor = conn.execute("SELECT COUNT(*) as total FROM articles")
            total_articles = cursor.fetchone()['total']
            
            # Total words
            cursor = conn.execute("SELECT SUM(word_count) as total_words FROM articles")
            result = cursor.fetchone()
            total_words = result['total_words'] or 0
            
            # Articles per site
            cursor = conn.execute("""
                SELECT site, COUNT(*) as count 
                FROM articles 
                GROUP BY site
            """)
            articles_by_site = {row['site']: row['count'] for row in cursor.fetchall()}
            
            return {
                'total_articles': total_articles,
                'total_words': total_words,
                'articles_by_site': articles_by_site
            }
    
    def start_session(self, site: str) -> int:
        """Start a new scraping session."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO scraping_sessions (site)
                VALUES (?)
            """, (site,))
            return cursor.lastrowid
    
    def finish_session(self, session_id: int, articles_scraped: int, error_message: Optional[str] = None):
        """Finish a scraping session."""
        status = 'failed' if error_message else 'completed'
        
        with self.get_connection() as conn:
            conn.execute("""
                UPDATE scraping_sessions 
                SET finished_at = CURRENT_TIMESTAMP,
                    articles_scraped = ?,
                    status = ?,
                    error_message = ?
                WHERE id = ?
            """, (articles_scraped, status, error_message, session_id))
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent scraping sessions."""
        with self.get_connection() as conn:
            cursor = conn.execute("""
                SELECT * FROM scraping_sessions 
                ORDER BY started_at DESC 
                LIMIT ?
            """, (limit,))
            return [dict(row) for row in cursor.fetchall()]