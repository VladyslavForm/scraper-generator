# Tech Insights - Static Tech Publication

Tech Insights is a static HTML tech publication featuring technology news, tutorials, and opinion pieces. Built with pure HTML and CSS, no JavaScript frameworks required.

## Project Structure

```
tech-insights/
├── index.html                          # Homepage with featured posts
├── about/
│   └── index.html                      # About page
├── contact/
│   └── index.html                      # Contact page
├── terms/
│   └── index.html                      # Terms of Service
├── privacy/
│   └── index.html                      # Privacy Policy
├── blog/
│   ├── index.html                      # Blog page 1 (articles 1-5)
│   ├── page/
│   │   ├── 2/
│   │   │   └── index.html              # Blog page 2 (articles 6-10)
│   │   └── 3/
│   │       └── index.html              # Blog page 3 (articles 11-15)
│   ├── getting-started-python/
│   │   └── index.html                  # Article 1
│   ├── machine-learning-basics/
│   │   └── index.html                  # Article 2
│   └── [... 13 more articles ...]
└── assets/
    ├── css/
    │   └── styles.css                  # Global styles
    └── img/                            # Images directory
```

## Pagination URL Structure

The blog uses a clean, SEO-friendly pagination structure:

- **Page 1 (Latest posts):** `/blog/` or `/blog/index.html`
- **Page 2:** `/blog/page/2/` or `/blog/page/2/index.html`
- **Page 3:** `/blog/page/3/` or `/blog/page/3/index.html`

Each pagination page displays 5 articles with navigation controls to move between pages.

## How to Add a New Blog Post

Follow these steps to add a new article to the site:

### Step 1: Create Article Folder

Create a new folder in the `blog/` directory with a URL-friendly slug:

```bash
mkdir blog/your-article-slug
```

**Naming conventions:**
- Use lowercase letters
- Separate words with hyphens (kebab-case)
- Keep it concise but descriptive
- Examples: `python-best-practices`, `aws-lambda-tutorial`, `react-performance-tips`

### Step 2: Create Article File

Create an `index.html` file in your article folder:

```bash
touch blog/your-article-slug/index.html
```

### Step 3: Article Template

Use this template for your article HTML:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Article Title - Tech Insights</title>
    <link rel="stylesheet" href="/assets/css/styles.css">
</head>
<body>
    <header>
        <div class="container">
            <a href="/" class="site-title">Tech Insights</a>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/blog/">Blog</a></li>
                    <li><a href="/about/">About</a></li>
                    <li><a href="/contact/">Contact</a></li>
                    <li><a href="/terms/">Terms</a></li>
                    <li><a href="/privacy/">Privacy</a></li>
                </ul>
            </nav>
        </div>
    </header>

    <main>
        <a href="/blog/" class="back-to-blog">← Back to Blog</a>

        <article class="article-content">
            <header class="article-header">
                <h1 class="article-title">Your Article Title</h1>
                <div class="article-byline">
                    <span><strong>Author:</strong> Author Name</span>
                    <span><strong>Published:</strong> Month Day, Year</span>
                </div>
            </header>

            <!-- Your article content here -->
            <p>Article introduction...</p>

            <h2>Section Heading</h2>
            <p>Section content...</p>

            <!-- Code examples -->
            <pre><code>// Your code here
const example = "Hello World";
console.log(example);</code></pre>

            <!-- Navigation links -->
            <div class="article-nav">
                <div class="prev-next">
                    <a href="/blog/previous-article/" class="nav-link">← Previous: Previous Article Title</a>
                    <a href="/blog/next-article/" class="nav-link">Next: Next Article Title →</a>
                </div>
            </div>
        </article>
    </main>

    <footer>
        <div class="container">
            <div class="footer-content">
                <div class="footer-section">
                    <h4>About Tech Insights</h4>
                    <p style="color: var(--text-light);">Your trusted source for technology news, tutorials, and expert
                        opinions on the latest developments in software engineering and tech industry.</p>
                </div>
                <div class="footer-section">
                    <h4>Quick Links</h4>
                    <ul>
                        <li><a href="/">Home</a></li>
                        <li><a href="/blog/">Blog</a></li>
                        <li><a href="/about/">About</a></li>
                        <li><a href="/contact/">Contact</a></li>
                        <li><a href="/terms/">Terms of Service</a></li>
                        <li><a href="/privacy/">Privacy Policy</a></li>
                    </ul>
                </div>
                <div class="footer-section">
                    <h4>Newsletter</h4>
                    <div class="newsletter-signup">
                        <input type="email" placeholder="Enter your email">
                        <button>Subscribe</button>
                    </div>
                </div>
            </div>
            <div class="copyright">
                &copy; 2025 Tech Insights. All rights reserved.
            </div>
        </div>
    </footer>
</body>
</html>
```

### Step 4: Add Article to Blog Listing

Add a card for your article to the appropriate pagination page (`/blog/index.html`, `/blog/page/2/index.html`, or `/blog/page/3/index.html`):

```html
<div class="article-card">
    <h3><a href="/blog/your-article-slug/">Your Article Title</a></h3>
    <div class="article-meta">
        <span>By Author Name</span>
        <span>Month Day, Year</span>
    </div>
    <p class="article-summary">Brief 1-2 sentence summary of your article...</p>
    <div class="tags">
        <span class="tag">Tag1</span>
        <span class="tag">Tag2</span>
        <span class="tag">Tag3</span>
    </div>
    <a href="/blog/your-article-slug/" class="read-more">Read more →</a>
</div>
```

### Step 5: Update Homepage (Optional)

If your article is featured, add it to the featured articles section on `/index.html`.

## Article Content Guidelines

### Required Elements

Every article must include:
- **Title** (`<h1>` with class `article-title`)
- **Author** (in the article byline)
- **Publish Date** (in the article byline)
- **Main Content** (body text with headings and paragraphs)

### Recommended Elements

- **Section headings** (`<h2>`, `<h3>`)
- **Code examples** (wrapped in `<pre><code>` tags)
- **Lists** (ordered or unordered)
- **Tags** (3-5 relevant tags)
- **Previous/Next navigation** (links to related articles)

### Styling Classes

Available CSS classes for article content:

- `.article-content` - Main article container
- `.article-header` - Article header section
- `.article-title` - Article title
- `.article-byline` - Author and date information
- `.article-summary` - Short summary on listing pages
- `.article-meta` - Metadata on listing pages
- `.tags` - Container for tag badges
- `.tag` - Individual tag badge
- `.read-more` - "Read more" link
- `.back-to-blog` - Back to blog link
- `.article-nav` - Navigation section
- `.prev-next` - Previous/next links container

## Managing Pagination

When you have more than 15 articles, you'll need to add additional pagination pages:

### Adding Page 4

1. Create directory: `mkdir -p blog/page/4`
2. Create file: `touch blog/page/4/index.html`
3. Copy template from existing pagination page
4. Update page number in title and pagination controls
5. Add 5 new articles (articles 16-20)
6. Update pagination links on page 3 to include page 4

### Pagination Controls Template

```html
<div class="pagination">
    <a href="/blog/page/[N-1]/">← Previous</a>
    <a href="/blog/">1</a>
    <a href="/blog/page/2/">2</a>
    <a href="/blog/page/3/">3</a>
    <span class="current">4</span>
    <a href="/blog/page/5/">5</a>
    <a href="/blog/page/5/">Next →</a>
</div>
```

## Running the Site Locally

### Option 1: Python HTTP Server

```bash
cd tech-insights
python -m http.server 8000
# Visit http://localhost:8000
```

### Option 2: Node.js HTTP Server

```bash
cd tech-insights
npx http-server -p 8000
# Visit http://localhost:8000
```

### Option 3: PHP Built-in Server

```bash
cd tech-insights
php -S localhost:8000
# Visit http://localhost:8000
```

## Deployment

This is a static site and can be deployed to any static hosting service:

- **Netlify:** Drop the `tech-insights` folder or connect to Git
- **GitHub Pages:** Push to a GitHub repository and enable Pages
- **Vercel:** Import from Git repository
- **AWS S3 + CloudFront:** Upload files to S3 bucket
- **Traditional Web Hosting:** Upload via FTP/SFTP

## Current Article List

1. Getting Started with Python Programming
2. Machine Learning Fundamentals Explained
3. Complete Guide to Cloud Computing
4. Introduction to Docker Containers
5. Kubernetes Deployment Strategies
6. API Design Best Practices
7. Database Optimization Tips
8. Essential Cybersecurity Fundamentals
9. Web Performance Tuning Guide
10. Advanced Git Workflows
11. React Hooks: A Complete Guide
12. TypeScript Benefits for Large Projects
13. Building Microservices Architecture
14. Essential DevOps Practices
15. CI/CD Pipeline Setup Guide

## Customization

### Changing Colors

Edit CSS variables in `/assets/css/styles.css`:

```css
:root {
    --primary-color: #2563eb;
    --secondary-color: #1e40af;
    --text-color: #1f2937;
    /* ... */
}
```

### Adding Images

1. Place images in `/assets/img/`
2. Reference in HTML: `<img src="/assets/img/your-image.jpg" alt="Description">`

### Modifying Navigation

Update the navigation in the `<header>` section of each page.

## Best Practices

- **URLs:** Always use trailing slashes for consistency (`/blog/` not `/blog`)
- **Links:** Use absolute paths starting with `/` for reliability
- **Images:** Optimize images before adding (use WebP when possible)
- **Accessibility:** Include alt text for all images
- **Mobile:** Test on mobile devices regularly
- **SEO:** Update page titles and meta descriptions for each page

## License

Copyright 2025 Tech Insights. All rights reserved.

## Support

For questions or issues, contact us at hello@techinsights.com or visit our [Contact Page](/contact/).
