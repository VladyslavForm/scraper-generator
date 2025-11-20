# Newsroom Hub - Static News Site

A static HTML news portal showcasing latest stories with pagination and comprehensive article coverage.

## Project Structure

```
newsroom-hub/
├── index.html                  # Homepage (Page 1)
├── about/
│   └── index.html             # About page
├── contact/
│   └── index.html             # Contact page
├── terms/
│   └── index.html             # Terms of Service
├── privacy/
│   └── index.html             # Privacy Policy
├── page/
│   ├── 2/
│   │   └── index.html         # Page 2 of articles
│   └── 3/
│       └── index.html         # Page 3 of articles
├── articles/
│   ├── tech-revolution-2024/
│   │   └── index.html
│   ├── climate-action-summit/
│   │   └── index.html
│   ├── [... 16 more article folders]
│   └── scientific-discovery-2024/
│       └── index.html
├── assets/
│   ├── css/
│   │   └── styles.css         # Main stylesheet
│   └── img/                   # Images (if any)
└── README.md                  # This file
```

## Pagination System

### How Pagination Works

The site uses a **folder-based pagination system** where each page is represented by a folder containing an `index.html` file:

- **Page 1**: `/index.html` (root)
- **Page 2**: `/page/2/index.html`
- **Page 3**: `/page/3/index.html`

### URL Structure

- Homepage: `https://yourdomain.com/` or `https://yourdomain.com/index.html`
- Page 2: `https://yourdomain.com/page/2/`
- Page 3: `https://yourdomain.com/page/3/`

### Pagination Navigation

Each pagination page includes navigation controls at the bottom:
- **Previous/Next buttons**: Navigate between adjacent pages
- **Page numbers (1, 2, 3)**: Direct links to specific pages
- **Current page indicator**: Highlighted button showing active page
- **Disabled states**: Previous button disabled on page 1, Next button disabled on page 3

### Articles Per Page

Currently configured with **6 articles per page** across 3 pages (18 total articles). This can be adjusted based on your needs.

## Adding New Articles

### Step 1: Create Article Folder

Create a new folder in the `articles/` directory with a URL-friendly slug:

```bash
mkdir articles/your-article-slug
```

**Best practices for slugs:**
- Use lowercase letters
- Separate words with hyphens (-)
- Keep it short but descriptive
- Example: `climate-policy-2024` or `ai-breakthrough-research`

### Step 2: Create Article HTML File

Create `index.html` inside your new article folder. Use this template:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Article Title - Newsroom Hub</title>
    <link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body>
    <header>
        <div class="container">
            <h1><a href="/">Newsroom Hub</a></h1>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/about/">About</a></li>
                    <li><a href="/contact/">Contact</a></li>
                    <li><a href="/terms/">Terms</a></li>
                    <li><a href="/privacy/">Privacy</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main class="container">
        <div class="breadcrumb">
            <a href="/">Home</a> &gt; Your Article Title
        </div>

        <article class="article-detail">
            <h1>Your Article Title</h1>
            <div class="article-meta">
                By Author Name | Month Day, Year
            </div>

            <div class="article-content">
                <p>
                    Your article content goes here...
                </p>

                <h2>Subheading</h2>

                <p>
                    More content...
                </p>
            </div>

            <div class="related-articles">
                <h2>Related Articles</h2>
                <ul>
                    <li><a href="/articles/related-article-1/">Related Article Title 1</a></li>
                    <li><a href="/articles/related-article-2/">Related Article Title 2</a></li>
                    <li><a href="/articles/related-article-3/">Related Article Title 3</a></li>
                </ul>
            </div>
        </article>
    </main>

    <footer>
        <div class="container">
            <div class="footer-links">
                <a href="/">Home</a>
                <a href="/about/">About</a>
                <a href="/contact/">Contact</a>
                <a href="/terms/">Terms of Service</a>
                <a href="/privacy/">Privacy Policy</a>
            </div>
            <p class="copyright">&copy; 2024 Newsroom Hub. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>
```

### Step 3: Add Article to Pagination Page

Edit the appropriate pagination page (`index.html`, `page/2/index.html`, or `page/3/index.html`) to include your new article card:

```html
<article class="article-card">
    <div class="article-card-content">
        <h2><a href="/articles/your-article-slug/">Your Article Title</a></h2>
        <div class="article-meta">
            By Author Name | Month Day, Year
        </div>
        <p class="article-excerpt">
            Brief excerpt or summary of your article (2-3 sentences)...
        </p>
        <a href="/articles/your-article-slug/" class="read-more">Read more →</a>
    </div>
</article>
```

### Step 4: Add Pagination Page (if needed)

If you have more than 18 articles and need a 4th page:

1. Create the folder: `mkdir -p page/4`
2. Copy `page/3/index.html` to `page/4/index.html`
3. Update the article cards with new articles
4. Update pagination controls:
   - Change "current" class to page 4
   - Update Previous/Next links
   - Add page number 4 to pagination

## Article Requirements

Each article must include:

1. **Title**: Main `<h1>` heading
2. **Author**: Name of the writer
3. **Publish Date**: In readable format (e.g., "March 15, 2024")
4. **Main Content**: Article body with paragraphs and optional subheadings
5. **Breadcrumb**: Navigation trail (Home > Article Title)
6. **Related Articles**: 2-4 links to related content

## Styling Guidelines

### CSS Classes

- `.article-card`: Article teaser on listing pages
- `.article-card-content`: Content wrapper inside card
- `.article-meta`: Author and date information
- `.article-excerpt`: Brief summary text
- `.article-detail`: Full article page container
- `.article-content`: Main article content area
- `.related-articles`: Related articles section
- `.breadcrumb`: Navigation breadcrumbs
- `.pagination`: Pagination controls

### Responsive Design

The site is fully responsive with breakpoints at:
- Mobile: < 768px
- Tablet/Desktop: ≥ 768px

## Deployment

This is a static site and can be hosted on any static hosting service:

- **GitHub Pages**: Push to GitHub and enable Pages
- **Netlify**: Drag and drop the `newsroom-hub` folder
- **Vercel**: Import from Git repository
- **Traditional Web Hosting**: Upload via FTP to public_html or www directory

### Local Testing

To test locally, you can use any simple HTTP server:

```bash
# Python 3
python -m http.server 8000

# Node.js (http-server)
npx http-server

# PHP
php -S localhost:8000
```

Then visit `http://localhost:8000` in your browser.

## Maintenance

### Updating Content

- **Edit articles**: Directly edit the HTML files in `articles/` folders
- **Update common pages**: Edit files in `about/`, `contact/`, `terms/`, `privacy/`
- **Modify styling**: Edit `assets/css/styles.css`

### Best Practices

1. **Maintain consistent formatting** across all pages
2. **Update pagination** when adding/removing articles
3. **Check all links** after making changes
4. **Keep related articles relevant** and up-to-date
5. **Use proper HTML semantics** for accessibility
6. **Test on multiple devices** and browsers

## License

Copyright © 2024 Newsroom Hub. All rights reserved.

---

For questions or support, contact: info@newsroomhub.com