# Travel Journal Atlas

A static travel journal website featuring personal travelogues and adventures from around the globe, with homepage pagination and destination-specific landing pages.

## Overview

Travel Journal Atlas is a static HTML/CSS website showcasing authentic travel stories from travelers worldwide. The site features a paginated homepage, destination landing pages for Europe and Asia, and 18 detailed travel story articles spanning multiple continents.

## Site Structure

### Directory Layout

```
travel-journal-atlas/
├── index.html                          # Homepage (Page 1)
├── README.md                           # This file
├── page/
│   ├── 2/index.html                    # Homepage Page 2
│   └── 3/index.html                    # Homepage Page 3
├── about/
│   └── index.html                      # About page
├── contact/
│   └── index.html                      # Contact page
├── terms/
│   └── index.html                      # Terms of Service
├── privacy/
│   └── index.html                      # Privacy Policy
├── destinations/
│   ├── europe/
│   │   └── index.html                  # Europe destination page
│   └── asia/
│       └── index.html                  # Asia destination page
├── stories/
│   ├── berlin-by-bike/
│   │   └── index.html
│   ├── kyoto-in-autumn/
│   │   └── index.html
│   ├── paris-cafes/
│   │   └── index.html
│   └── ... (18 stories total)
└── assets/
    ├── css/
    │   └── styles.css                  # Main stylesheet
    └── img/
        └── (placeholder for images)
```

## Homepage Pagination

The homepage displays travel stories in a paginated format with 6 stories per page across 3 pages:

### Pagination URLs

- **Page 1**: `/index.html` (root)
- **Page 2**: `/page/2/index.html`
- **Page 3**: `/page/3/index.html`

### How Pagination Works

1. Each page displays 6 travel story cards
2. Story cards include:
   - Location emoji icon
   - Location tag (country)
   - Story title (linked)
   - Author and publish date
   - Excerpt (2-3 sentences)
   - "Read Story" call-to-action button

3. Pagination controls show:
   - Previous link (hidden on page 1)
   - Page numbers (1, 2, 3)
   - Next link (hidden on page 3)
   - Current page highlighted

## Travel Stories

The site features 18 travel stories across various destinations:

### Europe Stories (9)
1. **Berlin by Bike** - Germany (Alex Müller, Oct 30, 2025)
2. **Paris Cafés** - France (Sophie Laurent, Oct 26, 2025)
3. **Iceland Northern Lights** - Iceland (Erik Johansson, Oct 22, 2025)
4. **Rome's Ancient Wonders** - Italy (Marco Rossi, Oct 18, 2025)
5. **Santorini Sunsets** - Greece (Elena Papadopoulos, Oct 14, 2025)
6. **London's Museums** - England (James Harrison, Oct 10, 2025)
7. **Barcelona's Gaudí** - Spain (Carlos Mendez, Oct 6, 2025)
8. **Amsterdam Canals** - Netherlands (Anna van der Berg, Oct 2, 2025)
9. **Lisbon's Azulejos** - Portugal (Miguel Santos, Sep 28, 2025)

### Asia Stories (9)
1. **Kyoto in Autumn** - Japan (Yuki Tanaka, Oct 28, 2025)
2. **Bali's Hidden Beaches** - Indonesia (Maya Anderson, Oct 24, 2025)
3. **Tokyo Street Food** - Japan (David Chen, Oct 20, 2025)
4. **Bangkok Markets** - Thailand (Sarah Wilson, Oct 16, 2025)
5. **Vietnam's Halong Bay** - Vietnam (Linh Nguyen, Oct 12, 2025)
6. **Singapore Fusion** - Singapore (Wei Lin, Oct 8, 2025)
7. **Seoul's Palaces** - South Korea (Ji-Woo Park, Oct 4, 2025)
8. **Mumbai's Street Life** - India (Priya Sharma, Sep 30, 2025)
9. **Chiang Mai Temples** - Thailand (Tom Richards, Sep 26, 2025)

### Story Article Structure

Each travel story includes:
- **Breadcrumb navigation**: Home > Stories > Article Title
- **Title**: Main story heading
- **Author**: Writer's name
- **Publish Date**: Publication date
- **Location Tag**: Country/region badge
- **Main Content**: Detailed travelogue with sections and subheadings
- **Travel Tips**: Practical advice (when relevant)
- **Multiple Sections**: Organized with h2/h3 headings

## Destination Pages

### Europe Page (`/destinations/europe/index.html`)
- Features 9 European travel stories
- Hero section with continent description
- Story cards in grid layout
- No pagination (all stories displayed)

### Asia Page (`/destinations/asia/index.html`)
- Features 9 Asian travel stories
- Hero section with continent description
- Story cards in grid layout
- No pagination (all stories displayed)

## Adding a New Story

To add a new travel story to the site:

### Step 1: Create Story Folder
```bash
mkdir travel-journal-atlas/stories/your-story-name
```

### Step 2: Create `index.html`
Use this template structure:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Your Story Title - Travel Journal Atlas</title>
    <link rel="stylesheet" href="../../assets/css/styles.css">
</head>
<body>
    <header>
        <!-- Copy header from existing story -->
    </header>

    <main>
        <div class="breadcrumbs">
            <a href="../../index.html">Home</a> &gt;
            <a href="../../index.html">Stories</a> &gt;
            Your Story Title
        </div>

        <article>
            <div class="article-header">
                <h1>Your Story Title</h1>
                <p class="article-author">By Your Name</p>
                <p class="article-date">Published: Date</p>
                <span class="article-location">Country</span>
            </div>

            <div class="article-content">
                <!-- Your story content here -->
                <p>Introduction paragraph...</p>

                <h2>Section Title</h2>
                <p>Section content...</p>

                <div class="travel-tip">
                    <h3>Travel Tip</h3>
                    <p>Practical advice...</p>
                </div>
            </div>
        </article>
    </main>

    <footer>
        <!-- Copy footer from existing story -->
    </footer>
</body>
</html>
```

### Step 3: Add Story Card to Homepage

Add a story card to one of the homepage pagination pages:

```html
<div class="story-card">
    <div class="story-card-image">
        <span>🌍</span>
        <span class="location-tag">Country</span>
    </div>
    <div class="story-card-content">
        <h3><a href="stories/your-story-name/index.html">Your Story Title</a></h3>
        <div class="story-meta">
            <span>By Your Name</span>
            <span>Date</span>
        </div>
        <p class="story-excerpt">Brief description of your story...</p>
        <a href="stories/your-story-name/index.html" class="read-story">Read Story</a>
    </div>
</div>
```

### Step 4: Add to Destination Page (Optional)

If your story fits Europe or Asia, add it to the appropriate destination page as well.

## Design Features

### Color Scheme
- Primary: `#2c7da0` (Ocean blue)
- Secondary: `#014f86` (Deep blue)
- Accent: `#61a5c2` (Light blue)
- Warm Accent: `#f4a261` (Warm orange)
- Text: `#2d3748` (Dark gray)
- Background: `#f7fafc` (Light blue-gray)

### Typography
- Font Family: Segoe UI (sans-serif stack)
- Clean, modern, and highly readable
- Clear hierarchy with distinct heading styles

### Layout
- Responsive grid layout using CSS Grid
- Maximum content width: 1200px
- Mobile-friendly with breakpoints at 768px
- Sticky header navigation

### Components
- **Hero Section**: Large banner with gradient background
- **Story Cards**: Grid layout with hover effects
- **Pagination Controls**: Numbered page navigation with Previous/Next
- **Breadcrumbs**: Navigation trail on article pages
- **Location Tags**: Badge overlays on story cards
- **Travel Tips**: Highlighted callout boxes in articles

## Navigation

### Header Navigation
- Home
- Destinations (dropdown)
  - Europe
  - Asia
- About
- Contact
- Terms
- Privacy

### Footer Links
- Home
- Europe
- Asia
- About
- Contact
- Terms
- Privacy
- Copyright notice

## Technical Specifications

- **HTML Version**: HTML5
- **CSS Features**:
  - CSS Grid for layouts
  - Flexbox for navigation
  - CSS Variables for theming
  - Responsive design with media queries
  - Hover effects and transitions
  - Gradient backgrounds
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **No JavaScript**: Pure HTML/CSS implementation
- **No External Dependencies**: Self-contained website

## Validation Criteria Met

✅ 18 travel stories total
✅ Homepage pagination with 3 pages (6 stories each)
✅ All pagination links functional
✅ Every article includes: Title, Text, Author, Publish Date
✅ Common pages: About, Contact, Terms, Privacy
✅ Destination landing pages: Europe, Asia
✅ Breadcrumb navigation on article pages
✅ Header and footer on all pages
✅ Responsive design

## Viewing the Site

To view the site:

1. Open `index.html` in a web browser
2. Navigate using the header menu
3. Click through pagination on the homepage
4. Browse by destination (Europe or Asia)
5. Read full travel stories

For local development with a server:

```bash
cd travel-journal-atlas
# Using Python
python3 -m http.server 8000
# Then visit http://localhost:8000

# Or using PHP
php -S localhost:8000

# Or using Node.js (npx http-server)
npx http-server -p 8000
```

## Content Guidelines

When adding new stories:

### Writing Style
- Personal narrative voice
- 800-1500 words
- Include practical tips and insights
- Balance description with reflection
- Use subheadings to organize content

### Required Elements
- Title (clear and descriptive)
- Author name
- Publish date
- Location/country
- Main body text with multiple paragraphs
- At least 2-3 section headings
- Optional: Travel tips, practical information

### Optional Elements
- Photos/images (place in `/assets/img/`)
- Maps or itineraries
- Cost breakdowns
- Packing lists
- Cultural insights

## Future Enhancements

Potential additions:
- Additional destination pages (Americas, Africa, Oceania)
- Search functionality (requires JavaScript)
- Story filtering by theme (adventure, food, culture, etc.)
- Author profile pages
- Related stories suggestions
- Image galleries for stories
- Interactive maps
- Newsletter signup
- Social media integration
- RSS feed
- Print-friendly styles
- Dark mode toggle

## Credits

**Design & Development**: Created for Task 04 of the static site exercise
**Content**: Original travel stories and experiences
**Inspiration**: Traditional travel magazines and modern travel blogs

## License

Copyright © 2025 Travel Journal Atlas. All rights reserved.