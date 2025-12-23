# LoRaLeaf Website - Deployment Guide

Quick guide to get your LoRaLeaf website live on loraleaf.com and loraleaf.co.uk

## Quick Start (Netlify - Recommended)

### Step 1: Deploy to Netlify

1. Go to [https://netlify.com](https://netlify.com) and sign up (free)
2. Click "Add new site" → "Deploy manually"
3. Drag and drop the entire `loraleaf-website` folder
4. Your site will be live in seconds at a temporary URL like `random-name-123.netlify.app`

### Step 2: Configure Custom Domains

1. In Netlify dashboard, go to **Site settings** → **Domain management**
2. Click **Add custom domain**
3. Add `loraleaf.com`
4. Add `loraleaf.co.uk`
5. Netlify will provide DNS settings

### Step 3: Update DNS (at your domain registrar)

For **loraleaf.com** and **loraleaf.co.uk**:

#### If using Netlify DNS (easiest):
1. Update nameservers at your domain registrar to Netlify's nameservers
2. Netlify handles everything else automatically

#### If using external DNS:
Add these records at your domain registrar:

```
Type: A
Name: @ (or leave blank for root domain)
Value: 75.2.60.5

Type: CNAME
Name: www
Value: your-site-name.netlify.app
```

Repeat for both `.com` and `.co.uk` domains.

### Step 4: Enable HTTPS
- Netlify automatically provisions SSL certificates
- Usually takes 1-2 minutes after DNS propagates
- Check "HTTPS" section in domain settings

### Step 5: Set up Contact Form
1. In `index.html`, find the contact form
2. Add `data-netlify="true"` attribute:
   ```html
   <form class="contact-form" id="contactForm"
         name="contact" method="POST" data-netlify="true">
   ```
3. Redeploy the site
4. Forms will appear in your Netlify dashboard under "Forms"

## Alternative: GitHub Pages

### Step 1: Create GitHub Repository
```bash
cd /home/av3/loraleaf-website
git init
git add .
git commit -m "Initial LoRaLeaf website"
gh repo create loraleaf-website --public --source=. --remote=origin
git push -u origin main
```

### Step 2: Enable GitHub Pages
1. Go to repository Settings → Pages
2. Source: Deploy from branch → main → / (root)
3. Click Save

### Step 3: Configure Custom Domain
1. In Pages settings, add custom domain: `loraleaf.com`
2. Create a file `CNAME` in the root with content: `loraleaf.com`
3. Update DNS at your registrar:
   ```
   Type: A
   Name: @
   Values:
     185.199.108.153
     185.199.109.153
     185.199.110.153
     185.199.111.153

   Type: CNAME
   Name: www
   Value: yourusername.github.io
   ```

### Step 4: Contact Form (GitHub Pages)
Use Formspree:
1. Sign up at [formspree.io](https://formspree.io) (free tier available)
2. Create a new form
3. Get your form endpoint (e.g., `https://formspree.io/f/xyzabc123`)
4. Update `index.html`:
   ```html
   <form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
   ```

## Alternative: Vercel

### Step 1: Deploy
```bash
cd /home/av3/loraleaf-website
npm install -g vercel  # if not installed
vercel
```

### Step 2: Follow prompts
- Link to existing project or create new
- Accept defaults
- Deploy!

### Step 3: Add domains in Vercel dashboard
Similar process to Netlify

## Pre-Deployment Checklist

- [ ] Replace logo with final version (currently using SVG placeholder)
- [ ] Update email address in contact section
- [ ] Set up contact form (Netlify Forms, Formspree, or custom)
- [ ] Test on mobile devices
- [ ] Test all links
- [ ] Add Google Analytics (optional)
- [ ] Test contact form submission
- [ ] Verify dashboard images are displaying correctly

## Post-Deployment

### 1. Test Everything
- [ ] All navigation links work
- [ ] Contact form submits successfully
- [ ] Images load correctly
- [ ] Site is responsive on mobile
- [ ] HTTPS is working
- [ ] Both .com and .co.uk domains work

### 2. SEO Setup
- [ ] Submit to [Google Search Console](https://search.google.com/search-console)
- [ ] Submit to [Bing Webmaster Tools](https://www.bing.com/webmasters)
- [ ] Create and submit sitemap (optional for single page site)

### 3. Analytics (Optional)
Add Google Analytics before `</head>` in `index.html`:
```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

### 4. Social Media
Share your new site! The Open Graph tags are already set up for nice previews on:
- Facebook
- Twitter/X
- LinkedIn

## Domain Setup Timeline

- **DNS propagation**: 1-48 hours (usually < 4 hours)
- **SSL certificate**: Automatic once DNS propagates
- **Site live**: Immediately after DNS resolves

## Troubleshooting

### Site not loading after DNS change
- Wait 1-4 hours for DNS to propagate
- Check DNS with: `dig loraleaf.com` or [whatsmydns.net](https://whatsmydns.net)

### Contact form not working
- Make sure form action is set to your Formspree endpoint, or
- Make sure `data-netlify="true"` is added if using Netlify

### Images not loading
- Check that all images are in the `images/` folder
- Verify paths in HTML are correct (case-sensitive)

### HTTPS showing as "Not Secure"
- Wait for SSL certificate to provision (1-10 minutes)
- Verify HTTPS is enabled in hosting dashboard

## Need Help?

1. Netlify Docs: [docs.netlify.com](https://docs.netlify.com)
2. GitHub Pages Docs: [docs.github.com/pages](https://docs.github.com/pages)
3. Vercel Docs: [vercel.com/docs](https://vercel.com/docs)

---

**Estimated Time to Deploy**: 15-30 minutes (plus DNS propagation time)

Good luck with the launch! 🚀
