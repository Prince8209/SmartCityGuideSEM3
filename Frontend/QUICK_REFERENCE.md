# Smart City Guide - Quick Reference

## 📁 Project Structure

```
Frontend/
├── 📄 HTML Pages (7 files)
│   ├── index.html          - Homepage with hero & featured cities
│   ├── cities.html         - 12 city guides
│   ├── features.html       - Feature showcase
│   ├── itinerary.html      - Trip planner
│   ├── contact.html        - Contact form
│   ├── login.html          - User login
│   └── signup.html         - User registration
│
├── 🎨 Styles & Scripts
│   ├── style.css           - Enhanced CSS (~20KB)
│   └── script.js           - Interactive features (~10KB)
│
├── ⚙️ Configuration
│   ├── manifest.json       - PWA manifest
│   ├── .gitignore          - Git exclusions
│   └── README.md           - Documentation
│
└── 📦 Assets Folder
    ├── 🖼️ images/         - City photos, backgrounds, UI
    ├── 🎬 videos/         - Promotional & tutorial videos
    ├── 🎯 icons/          - Favicons & custom icons
    ├── 🔤 fonts/          - Custom web fonts (optional)
    └── 📄 documents/      - PDFs, guides, templates
```

## 🎯 Quick Commands

### Open in Browser
```bash
# Using Python
python -m http.server 8000

# Using Node.js
npx http-server -p 8000

# Then visit: http://localhost:8000
```

### VS Code Live Server
1. Install "Live Server" extension
2. Right-click `index.html`
3. Select "Open with Live Server"

## 🌟 Key Features

✅ **7 HTML Pages** - Complete website structure
✅ **12 City Guides** - Delhi, Mumbai, Goa, Jaipur, Bangalore, Kerala, Agra, Udaipur, Varanasi, Kolkata, Shimla, Manali
✅ **Responsive Design** - Mobile, tablet, desktop optimized
✅ **Interactive Forms** - Login, signup, contact with validation
✅ **Modern CSS** - Gradients, animations, glassmorphism
✅ **Enhanced JavaScript** - Scroll-to-top, localStorage, debouncing
✅ **PWA Ready** - Manifest file for mobile installation
✅ **Assets Organized** - Dedicated folder structure

## 🎨 Design System

### Colors
- Primary: `#667eea` (Purple Blue)
- Secondary: `#764ba2` (Deep Purple)
- Accent: `#f093fb` (Pink)
- Success: `#4facfe` (Sky Blue)

### Typography
- Headings: **Poppins** (400, 600, 700, 800)
- Body: **Inter** (400, 500, 600, 700)

### Gradients
```css
--gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
--gradient-accent: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
--gradient-success: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
```

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔧 Adding Content

### Add a New City
1. Open `cities.html`
2. Copy an existing city card
3. Update: name, image, description, stats, attractions
4. Save and refresh browser

### Add Images
1. Place images in `assets/images/cities/`
2. Update image URLs in HTML:
   ```html
   <img src="assets/images/cities/city-name.jpg" alt="City Name">
   ```

### Add Videos
1. Place videos in `assets/videos/`
2. Add to HTML:
   ```html
   <video controls>
       <source src="assets/videos/video-name.mp4" type="video/mp4">
   </video>
   ```

## 🚀 Enhanced Features

### Scroll-to-Top Button
- Appears after scrolling 300px
- Smooth scroll animation
- Accessible with keyboard

### Form Data Persistence
- Auto-saves form data as you type
- Restores on page reload
- Clears after submission

### Search with Debouncing
- 300ms delay for optimization
- Saves search history (last 5)
- Ready for live suggestions

### Responsive Grid
- Auto-adjusts on window resize
- Single column on mobile
- Two columns on desktop

## 📋 Checklist for Production

- [ ] Replace Unsplash images with local assets
- [ ] Add favicon files to `assets/icons/`
- [ ] Optimize all images (compress)
- [ ] Test on multiple browsers
- [ ] Validate HTML/CSS
- [ ] Check accessibility (WCAG 2.1)
- [ ] Set up backend API (optional)
- [ ] Configure hosting
- [ ] Add analytics (optional)
- [ ] Test PWA installation

## 🔗 Important Links

- **Main README**: `README.md`
- **Assets Guide**: `assets/README.md`
- **Implementation Plan**: See artifacts
- **Walkthrough**: See artifacts

## 📞 Contact

- Email: pp8995982@gmail.com
- Phone: +91 7069300609
- Location: Mumbai, India

---

**Built with ❤️ in India** | © 2024 Smart City Guide
