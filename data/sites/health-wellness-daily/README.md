# Health & Wellness Daily

A static HTML website dedicated to evidence-based health and wellness content across three core categories: Fitness, Nutrition, and Mindfulness.

## Site Overview

Health & Wellness Daily provides scientifically-backed articles to help readers make informed decisions about their health and wellbeing. The site emphasizes accessibility, clarity, and practical guidance.

## Project Structure

```
health-wellness-daily/
├── index.html                      # Homepage with hero and category links
├── about/
│   └── index.html                  # About page
├── contact/
│   └── index.html                  # Contact page
├── terms/
│   └── index.html                  # Terms of Service
├── privacy/
│   └── index.html                  # Privacy Policy
├── articles/                       # Global article feed (mixed categories)
│   ├── index.html                  # Articles page 1
│   └── page/
│       ├── 2/index.html           # Articles page 2
│       └── 3/index.html           # Articles page 3
├── categories/
│   ├── fitness/                    # Fitness category
│   │   ├── index.html             # Fitness page 1
│   │   └── page/
│   │       ├── 2/index.html       # Fitness page 2
│   │       └── 3/index.html       # Fitness page 3
│   ├── nutrition/                  # Nutrition category
│   │   ├── index.html             # Nutrition page 1
│   │   └── page/
│   │       ├── 2/index.html       # Nutrition page 2
│   │       └── 3/index.html       # Nutrition page 3
│   └── mindfulness/                # Mindfulness category
│       ├── index.html             # Mindfulness page 1
│       └── page/
│           ├── 2/index.html       # Mindfulness page 2
│           └── 3/index.html       # Mindfulness page 3
├── posts/                          # Article detail pages
│   ├── strength-training-beginners-guide/
│   ├── hiit-vs-steady-state-cardio/
│   ├── building-running-endurance/
│   ├── mobility-training-importance/
│   ├── recovery-strategies-athletes/
│   ├── core-training-beyond-abs/
│   ├── protein-intake-guide/
│   ├── mediterranean-diet-benefits/
│   ├── hydration-performance/
│   ├── meal-prep-strategies/
│   ├── gut-health-microbiome/
│   ├── antioxidants-inflammation/
│   ├── sustainable-weight-management/
│   ├── meditation-beginners-guide/
│   ├── stress-management-techniques/
│   ├── sleep-hygiene-practices/
│   ├── mindful-eating-practice/
│   ├── gratitude-practice-benefits/
│   └── emotional-intelligence-development/
└── assets/
    ├── css/
    │   └── styles.css              # Global stylesheet
    └── img/                        # Images directory (placeholder)
```

## Content Categories

### Fitness (6 articles)
Articles covering exercise science, workout routines, training strategies, and movement practices:
- Strength training fundamentals
- HIIT vs steady-state cardio
- Building running endurance
- Mobility training
- Recovery strategies
- Core training

### Nutrition (6 articles)
Evidence-based dietary guidance and nutritional science:
- Protein intake guidelines
- Mediterranean diet benefits
- Hydration strategies
- Meal preparation
- Gut health and microbiome
- Antioxidants and inflammation

### Mindfulness (6 articles)
Mental wellness, stress management, and mindfulness practices:
- Meditation for beginners
- Stress management techniques
- Sleep hygiene
- Mindful eating
- Gratitude practice
- Emotional intelligence

## Pagination URL Scheme

### Global Articles Feed
The `/articles/` section displays a mixed feed of articles from all categories:

- **Page 1**: `/articles/` or `/articles/index.html`
- **Page 2**: `/articles/page/2/` or `/articles/page/2/index.html`
- **Page 3**: `/articles/page/3/` or `/articles/page/3/index.html`

Each page displays 6-7 articles in reverse chronological order with Previous/Next navigation and numeric page links.

### Category-Specific Feeds

Each category has its own paginated listing showing only articles from that category:

#### Fitness
- **Page 1**: `/categories/fitness/` or `/categories/fitness/index.html`
- **Page 2**: `/categories/fitness/page/2/` or `/categories/fitness/page/2/index.html`
- **Page 3**: `/categories/fitness/page/3/` or `/categories/fitness/page/3/index.html`

#### Nutrition
- **Page 1**: `/categories/nutrition/` or `/categories/nutrition/index.html`
- **Page 2**: `/categories/nutrition/page/2/` or `/categories/nutrition/page/2/index.html`
- **Page 3**: `/categories/nutrition/page/3/` or `/categories/nutrition/page/3/index.html`

#### Mindfulness
- **Page 1**: `/categories/mindfulness/` or `/categories/mindfulness/index.html`
- **Page 2**: `/categories/mindfulness/page/2/` or `/categories/mindfulness/page/2/index.html`
- **Page 3**: `/categories/mindfulness/page/3/` or `/categories/mindfulness/page/3/index.html`

Each category page displays 2 articles per page.

### Article Detail Pages
Individual articles are accessed via:
```
/posts/{article-slug}/index.html
```

For example:
- `/posts/strength-training-beginners-guide/index.html`
- `/posts/meditation-beginners-guide/index.html`

## Pagination Features

Each listing page includes:
- **Previous/Next Links**: Navigate between pages sequentially
- **Numeric Page Links**: Jump directly to any page (1, 2, or 3)
- **Current Page Indicator**: Highlighted to show current position
- **Disabled State**: Previous link disabled on page 1, Next link disabled on page 3

## Article Structure

Every article includes:
- **Title**: Clear, descriptive headline
- **Author**: Name and credentials
- **Publish Date**: Publication date
- **Category**: Fitness, Nutrition, or Mindfulness
- **Body Content**: Comprehensive article with headings, paragraphs, lists, and callout boxes
- **Breadcrumbs**: Navigation trail (Home > Category > Article Title)

## Design Features

- **Responsive Layout**: Mobile-friendly design
- **Clean Typography**: Readable, accessible fonts
- **Color Scheme**: Health-focused green and blue palette
- **Navigation**: Sticky header with dropdown for categories
- **Footer**: Quick links, category links, legal pages, and medical disclaimer

## Technical Details

- **Technology**: Pure HTML/CSS, no JavaScript frameworks
- **CSS Framework**: Custom CSS with CSS variables
- **Browser Compatibility**: Modern browsers (Chrome, Firefox, Safari, Edge)
- **Accessibility**: Semantic HTML, clear navigation structure

## Medical Disclaimer

All content on Health & Wellness Daily is for educational purposes only and should not be considered medical advice. Users should consult qualified healthcare professionals before starting any new health program.

## Viewing the Site

To view the site locally:
1. Open `index.html` in a web browser
2. Navigate using the header menu or homepage category cards
3. All links use relative paths for local browsing

For web hosting:
- Upload the entire `health-wellness-daily` folder to your web server
- Ensure your web server is configured to serve `index.html` as the directory default
- The site requires no server-side processing

## License

Content is educational and for demonstration purposes. Images are placeholders.

---

**Health & Wellness Daily** - Your trusted source for evidence-based health information.
