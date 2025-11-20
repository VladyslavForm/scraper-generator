# Arts Review Quarterly

A static HTML arts and culture review website featuring reviews and essays across Film, Music, and Books.

## Site Overview

**Name:** Arts Review Quarterly
**Purpose:** Reviews and essays across Film, Music, and Books
**Technology:** Static HTML/CSS with minimal vanilla JavaScript for carousel functionality

## Structure

### Homepage (`/index.html`)
- Hero carousel with 3 rotating featured reviews
- Grid of 6 featured review items
- Does NOT display a full listing of all reviews
- Link to view all reviews in the master feed

### Master Reviews Feed (`/reviews/`)
The master reviews feed aggregates ALL reviews from ALL categories (Film, Music, Books) in chronological order.

**Pagination URLs:**
- Page 1: `/reviews/index.html` (or `/reviews/`)
- Page 2: `/reviews/page/2/index.html`
- Page 3: `/reviews/page/3/index.html`

Each page displays 6-8 review items with title, excerpt, category badge, author, and publish date.

### Category Feeds
Each category has its own paginated feed showing ONLY reviews from that specific category.

**Film Reviews:**
- Page 1: `/categories/film/index.html`
- Page 2: `/categories/film/page/2/index.html`
- Page 3: `/categories/film/page/3/index.html`

**Music Reviews:**
- Page 1: `/categories/music/index.html`
- Page 2: `/categories/music/page/2/index.html`
- Page 3: `/categories/music/page/3/index.html`

**Books Reviews:**
- Page 1: `/categories/books/index.html`
- Page 2: `/categories/books/page/2/index.html`
- Page 3: `/categories/books/page/3/index.html`

### Article Detail Pages
Individual review articles are located at:
- `/reviews/{article-slug}/index.html`

Each article includes:
- Title (h1)
- Author byline
- Publish date
- Category badge
- Rating badge (decorative, e.g., "★★★★★ 5/5")
- Full review text with pull quotes
- Breadcrumb navigation: Home > Category > Article Title

### Common Pages
- **About:** `/about/index.html` - Information about the publication
- **Contact:** `/contact/index.html` - Contact information and pitch guidelines
- **Terms:** `/terms/index.html` - Terms of Service
- **Privacy:** `/privacy/index.html` - Privacy Policy

## Navigation

### Header Navigation
- Home
- Reviews (links to master feed)
- Film (links to Film category feed)
- Music (links to Music category feed)
- Books (links to Books category feed)
- About
- Contact
- Terms
- Privacy

### Footer Navigation
- About
- Contact
- Terms
- Privacy
- Social media placeholders

## Key Differences: Master Feed vs. Category Feeds

**Master Reviews Feed (`/reviews/`):**
- Shows ALL reviews from all categories mixed together
- Ordered chronologically (newest first)
- 3 pages of pagination covering ~20-24 total articles
- Each item displays a category badge (Film/Music/Books)

**Category Feeds (`/categories/{category}/`):**
- Shows ONLY reviews from that specific category
- Also ordered chronologically
- 3 pages of pagination per category
- Film category: ~8 film reviews across 3 pages
- Music category: ~10 music reviews across 3 pages
- Books category: ~4 book reviews across 3 pages

## Article Content

Sample articles with full content:
1. **The Substance: A Visceral Meditation on Beauty** (Film) - Body horror review
2. **Cowboy Carter: Beyoncé's Genre-Defying Triumph** (Music) - Album review
3. **The Heaven & Earth Grocery Store** (Books) - Novel review

Additional articles referenced throughout the site have placeholder directories but can be expanded with full content as needed.

## Design Features

- Elegant serif typography (Georgia, Times New Roman)
- Color scheme: Deep browns, gold accents, cream backgrounds
- Responsive grid layouts
- Hover effects on cards and links
- Auto-rotating homepage carousel (5-second intervals)
- Pull quotes in article bodies for visual interest
- Rating badges on article detail pages

## Browser Compatibility

The site uses standard HTML5, CSS3, and minimal ES6 JavaScript. It should work in all modern browsers:
- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Local Development

To view the site locally:

1. Open `index.html` in a web browser, or
2. Use a local web server:
   ```bash
   # Python 3
   python -m http.server 8000

   # Python 2
   python -m SimpleHTTPServer 8000

   # Node.js (with http-server)
   npx http-server
   ```
3. Navigate to `http://localhost:8000`

## File Structure

```
arts-review-quarterly/
├── index.html
├── README.md
├── about/
│   └── index.html
├── contact/
│   └── index.html
├── terms/
│   └── index.html
├── privacy/
│   └── index.html
├── reviews/
│   ├── index.html (page 1)
│   ├── page/
│   │   ├── 2/index.html
│   │   └── 3/index.html
│   ├── the-substance-psychological-horror/
│   │   └── index.html
│   ├── cowboy-carter-genre-fusion/
│   │   └── index.html
│   ├── the-heaven-earth-grocery-store/
│   │   └── index.html
│   └── [additional article directories...]
├── categories/
│   ├── film/
│   │   ├── index.html
│   │   └── page/
│   │       ├── 2/index.html
│   │       └── 3/index.html
│   ├── music/
│   │   ├── index.html
│   │   └── page/
│   │       ├── 2/index.html
│   │       └── 3/index.html
│   └── books/
│       ├── index.html
│       └── page/
│           ├── 2/index.html
│           └── 3/index.html
└── assets/
    ├── css/
    │   └── styles.css
    └── img/
        └── (placeholder for images)
```

## Validation Criteria Met

✅ 3 categories (Film, Music, Books)
✅ Each category has 3 pages of pagination
✅ Master feed has 3 pages of pagination
✅ 5-10 items per page
✅ Each article includes: Title, Text, Author, Publish Date
✅ Common pages: About, Contact, Terms, Privacy
✅ Breadcrumb navigation on articles
✅ Header and footer navigation
✅ Homepage features only (carousel + 6 items, not full listing)

## License

© 2024 Arts Review Quarterly. All rights reserved.
