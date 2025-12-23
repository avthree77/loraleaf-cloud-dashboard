# LoRaLeaf Website

Professional single-page marketing website for LoRaLeaf - a LoRa-based environmental monitoring system for agriculture and estates.

## Overview

This is a complete, production-ready website built for **loraleaf.com** and **loraleaf.co.uk**.

### Features

- ✅ Fully responsive single-page design
- ✅ Modern, clean UI with green/agricultural theme
- ✅ Real sensor data integration (dashboard preview)
- ✅ Contact form ready
- ✅ SEO optimized
- ✅ Fast loading, minimal dependencies
- ✅ Mobile-first responsive design

## Project Structure

```
loraleaf-website/
├── index.html          # Main HTML file
├── css/
│   └── style.css       # All styles
├── js/
│   └── main.js         # JavaScript functionality
├── images/
│   ├── loraleaf-logo.svg
│   ├── loraleaf-logo.png (optional)
│   ├── sensor_data_visualization.png
│   └── sensor_data_timeseries.png
└── README.md
```

## Technology Stack

- **HTML5** - Semantic markup
- **CSS3** - Custom styles, CSS Grid, Flexbox
- **Vanilla JavaScript** - No frameworks needed
- **Google Fonts** - Inter font family

## Setup & Deployment

### Local Development

1. Simply open `index.html` in a web browser
2. Or use a local server:
   ```bash
   python3 -m http.server 8000
   # Visit http://localhost:8000
   ```

### Deployment Options

#### Option 1: Netlify (Recommended)

1. Create account at [netlify.com](https://netlify.com)
2. Drag and drop the `loraleaf-website` folder
3. Configure custom domains:
   - loraleaf.com
   - loraleaf.co.uk
4. Enable HTTPS (automatic with Netlify)

#### Option 2: GitHub Pages

1. Create a GitHub repository
2. Push the website files
3. Enable GitHub Pages in repository settings
4. Configure custom domains in settings

#### Option 3: Vercel

1. Create account at [vercel.com](https://vercel.com)
2. Import the project
3. Configure custom domains

### Domain Configuration

For both **loraleaf.com** and **loraleaf.co.uk**:

1. Point DNS A record to hosting provider's IP
2. Or use CNAME record to provider's domain
3. Enable SSL/HTTPS
4. Set one domain as primary, other as redirect

Example DNS settings (Netlify):
```
Type: A
Name: @
Value: 75.2.60.5

Type: CNAME
Name: www
Value: your-site.netlify.app
```

## Contact Form Setup

The contact form currently uses a placeholder action. Choose one:

### Option 1: Formspree (Easiest)

1. Sign up at [formspree.io](https://formspree.io)
2. Create a new form
3. Replace in `index.html`:
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```

### Option 2: Netlify Forms

1. Add `netlify` attribute to form:
   ```html
   <form name="contact" method="POST" data-netlify="true">
   ```
2. Deploy to Netlify
3. Forms automatically work!

### Option 3: Custom Backend

Implement your own backend endpoint and update the form action URL.

## Customization

### Update Logo

Replace `images/loraleaf-logo.png` or `images/loraleaf-logo.svg` with your final logo.
Current logo is a placeholder SVG.

### Update Contact Email

In `index.html`, find and replace:
```html
<a href="mailto:info@loraleaf.com">info@loraleaf.com</a>
```

### Update Colors

In `css/style.css`, modify the CSS variables:
```css
:root {
    --color-primary: #2D5A27;    /* Deep green */
    --color-secondary: #7CB342;   /* Fresh leaf green */
    --color-accent: #5E8B47;      /* Mid green */
    /* ... */
}
```

### Add Hero Image

Replace the SVG illustration in the hero section with an actual photo:
```html
<div class="hero-image">
    <img src="images/hero-image.jpg" alt="LoRaLeaf sensors in field">
</div>
```

## Assets to Replace

Current placeholders to replace with professional assets:

1. **Logo** - `images/loraleaf-logo.png` (currently SVG placeholder)
2. **Hero Image** - Add professional photo of sensors in agricultural setting
3. **Product Photos** - Add images of actual sensor nodes
4. **Dashboard** - Currently uses real sensor data visualizations (keep these!)

## Real Data Integration

The website currently displays **real sensor data** from your LoRa network:

- 2,094 readings collected
- Temperature range: 15°C - 22°C (last 24 hours)
- 2 active sensor nodes (NODE_01 and NODE_02)

The dashboard preview shows actual data visualizations from `/images/sensor_data_visualization.png`.

## SEO

The site includes:
- Meta descriptions
- Open Graph tags for social sharing
- Semantic HTML structure
- Fast loading times
- Mobile-responsive design

### To improve SEO further:

1. Add `sitemap.xml`
2. Add `robots.txt`
3. Set up Google Analytics
4. Submit to Google Search Console
5. Add schema.org markup for LocalBusiness

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## Performance

- Minimal dependencies (only Google Fonts)
- Optimized images
- CSS and JS minification ready
- Lazy loading ready

## Next Steps (Phase 2)

Future enhancements not included in this version:

- [ ] Customer login portal
- [ ] Live dashboard integration
- [ ] Online ordering system
- [ ] Case studies section
- [ ] Blog/news section
- [ ] Multi-language support
- [ ] Advanced analytics

## Support & Maintenance

### Updating Content

All content is in `index.html` and easily editable:
- Section headings
- Feature descriptions
- Use cases
- Technical specifications
- Contact information

### Adding Analytics

Add Google Analytics or similar before `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

## License

© 2025 LoRaLeaf / AV3 Media. All rights reserved.

## Contact

Tom Harding
AV3 Media
Cornwall, UK
info@loraleaf.com

---

Built with attention to detail for professional agricultural technology marketing.
