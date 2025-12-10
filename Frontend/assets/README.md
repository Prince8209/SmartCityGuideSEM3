# Assets Folder

This folder contains all static assets for the Smart City Guide website.

## Folder Structure

```
assets/
├── images/          # Images for cities, backgrounds, and UI elements
├── videos/          # Video content for promotional or tutorial purposes
├── icons/           # Custom icons and favicons
├── fonts/           # Custom web fonts (if needed)
└── documents/       # PDFs, guides, and downloadable content
```

## Usage Guidelines

### Images (`images/`)

**Recommended formats:**
- `.jpg` / `.jpeg` - For photographs and city images
- `.png` - For logos, icons with transparency
- `.webp` - For optimized web images (best performance)
- `.svg` - For scalable graphics and logos

**Naming convention:**
- Use lowercase with hyphens: `city-name-landmark.jpg`
- Be descriptive: `delhi-red-fort-sunset.jpg`
- Include dimensions for variants: `logo-512x512.png`

**Optimization tips:**
- Compress images before uploading
- Use appropriate dimensions (max 1920px width for full-width images)
- Consider using WebP format for better compression

**Example structure:**
```
images/
├── cities/
│   ├── delhi-red-fort.jpg
│   ├── mumbai-gateway.jpg
│   └── goa-beach.jpg
├── backgrounds/
│   ├── hero-bg.jpg
│   └── pattern-overlay.png
└── ui/
    ├── logo.png
    └── placeholder.svg
```

### Videos (`videos/`)

**Recommended formats:**
- `.mp4` - Best compatibility (H.264 codec)
- `.webm` - Modern browsers, good compression
- `.ogv` - Fallback for older browsers

**Naming convention:**
- `city-name-tour.mp4`
- `feature-demo.mp4`
- `testimonial-user-name.mp4`

**Optimization tips:**
- Keep file sizes under 10MB when possible
- Use 720p or 1080p resolution
- Include poster images (thumbnail)
- Provide multiple formats for compatibility

### Icons (`icons/`)

**Recommended formats:**
- `.svg` - Scalable vector graphics (preferred)
- `.png` - Raster icons (multiple sizes: 16x16, 32x32, 64x64, 128x128, 256x256, 512x512)
- `.ico` - Favicon for browsers

**Required icons:**
- `favicon.ico` - Browser tab icon
- `apple-touch-icon.png` - iOS home screen (180x180)
- `android-chrome-192x192.png` - Android home screen
- `android-chrome-512x512.png` - Android splash screen

### Fonts (`fonts/`)

**Note:** Currently using Google Fonts CDN (Poppins & Inter)

If you need custom fonts:
- `.woff2` - Modern browsers (best compression)
- `.woff` - Fallback for older browsers
- `.ttf` / `.otf` - Desktop fonts

**Usage in CSS:**
```css
@font-face {
    font-family: 'CustomFont';
    src: url('../assets/fonts/custom-font.woff2') format('woff2'),
         url('../assets/fonts/custom-font.woff') format('woff');
    font-weight: normal;
    font-style: normal;
}
```

### Documents (`documents/`)

**Recommended formats:**
- `.pdf` - Guides, brochures, itineraries
- `.docx` - Editable documents
- `.xlsx` - Budget templates, checklists

**Example files:**
- `travel-guide-delhi.pdf`
- `budget-template.xlsx`
- `packing-checklist.pdf`

## Integration with HTML

### Images
```html
<!-- Relative path from HTML file -->
<img src="assets/images/cities/delhi-red-fort.jpg" alt="Red Fort, Delhi">

<!-- With responsive images -->
<picture>
    <source srcset="assets/images/cities/delhi-red-fort.webp" type="image/webp">
    <img src="assets/images/cities/delhi-red-fort.jpg" alt="Red Fort, Delhi">
</picture>
```

### Videos
```html
<video controls poster="assets/images/video-poster.jpg">
    <source src="assets/videos/city-tour.mp4" type="video/mp4">
    <source src="assets/videos/city-tour.webm" type="video/webm">
    Your browser does not support the video tag.
</video>
```

### Background Images (CSS)
```css
.hero {
    background-image: url('../assets/images/backgrounds/hero-bg.jpg');
}
```

## Best Practices

1. **Optimize all assets** before uploading
2. **Use descriptive names** for better organization
3. **Maintain consistent naming** conventions
4. **Provide alt text** for all images (accessibility)
5. **Use lazy loading** for images below the fold
6. **Compress videos** to reduce bandwidth
7. **Version control** - Don't commit large binary files if possible
8. **Use CDN** for frequently accessed assets (optional)

## Tools for Optimization

### Image Optimization
- [TinyPNG](https://tinypng.com/) - PNG/JPG compression
- [Squoosh](https://squoosh.app/) - Image converter and compressor
- [ImageOptim](https://imageoptim.com/) - Mac app for image optimization

### Video Optimization
- [HandBrake](https://handbrake.fr/) - Video transcoder
- [FFmpeg](https://ffmpeg.org/) - Command-line video processing

### Icon Generation
- [Favicon Generator](https://realfavicongenerator.net/) - Generate all favicon sizes
- [SVGOMG](https://jakearchibald.github.io/svgomg/) - SVG optimizer

## Current Assets

Currently, the website uses:
- **External CDN images** from Unsplash for city photos
- **Font Awesome icons** from CDN
- **Google Fonts** (Poppins, Inter) from CDN

To use local assets instead:
1. Download images and save to `assets/images/cities/`
2. Update image URLs in HTML files
3. Download fonts and update CSS `@font-face` rules
4. Generate and add favicon files to `assets/icons/`

## .gitignore Considerations

Large assets (>1MB) should be excluded from version control:
```
# Add to .gitignore
assets/videos/*.mp4
assets/videos/*.webm
assets/images/originals/
```

---

**Need help?** Contact the development team or refer to the main README.md
