# Create PowerPoint Presentation Skill

Create visually appealing PowerPoint presentations by converting styled HTML slides to PPTX format using Playwright and PptxGenJS, with AI-generated images via Gemini.

## Overview

This skill converts HTML slides to PowerPoint with:
- Precise positioning and styling
- Dark theme with modern color palette
- Support for shapes, text, images, and diagrams
- Automatic validation of slide dimensions and content placement
- **AI-generated images** using Google Gemini for backgrounds and icons

## Quick Start

```bash
# 1. Install dependencies
npm install pptxgenjs playwright sharp @google/genai

# 2. Set up Gemini API key (for image generation)
echo "GOOGLE_API_KEY=your-api-key" > .env

# 3. Create slides directory with HTML files
mkdir slides

# 4. Run conversion
node scripts/create-pptx.js
```

## Directory Structure

```
project/
├── scripts/
│   ├── html2pptx.js      # Core conversion library
│   ├── create-pptx.js    # Main build script
│   └── generate-image.js # AI image generation
├── slides/
│   ├── slide01-title.html
│   ├── slide02-content.html
│   └── ...
├── templates/            # Reference templates
├── .env                  # GOOGLE_API_KEY
└── output.pptx          # Generated presentation
```

## HTML Slide Requirements

### Dimensions (16:9 format)
```css
body {
    margin: 0;
    padding: 0;
    width: 720pt;
    height: 405pt;
}
```

### Critical Rules

1. **Text must be wrapped** - All text MUST be in `<p>`, `<h1>`-`<h6>`, `<ul>`, or `<ol>` tags
2. **Borders on divs only** - Backgrounds, borders, shadows only work on `<div>` elements
3. **No CSS gradients** - Use solid colors or pre-rendered PNG images
4. **Bottom margin** - Keep text at least 36pt (0.5") from bottom edge
5. **Safe fonts only** - Arial, Helvetica, Times New Roman, Georgia, Courier New, Verdana, Tahoma

### Example Slide

```html
<!DOCTYPE html>
<html>
<head>
    <style>
        body {
            margin: 0;
            padding: 0;
            width: 720pt;
            height: 405pt;
            background-color: #0f0f1a;
            font-family: Arial, sans-serif;
        }
        h2 {
            position: absolute;
            top: 30pt;
            left: 40pt;
            color: #ffffff;
            font-size: 32pt;
            font-weight: bold;
        }
        ul {
            position: absolute;
            top: 90pt;
            left: 40pt;
            color: #d0d0d0;
            font-size: 18pt;
            line-height: 2.2;
        }
    </style>
</head>
<body>
    <h2>Slide Title</h2>
    <ul>
        <li>First point</li>
        <li>Second point</li>
    </ul>
</body>
</html>
```

## Color Palette

```css
/* Dark Theme */
--bg-primary: #0f0f1a;
--bg-card: rgba(255, 255, 255, 0.05);

/* Accents */
--accent-blue: #667eea;
--accent-cyan: #00d4ff;
--accent-purple: #764ba2;

/* Text */
--text-white: #ffffff;
--text-light: #d0d0d0;
--text-muted: #a0a0b0;
```

## Available Templates

- `title.html` - Title slide with tagline, title, subtitle, and description
- `bullets.html` - Bullet point list (5 items)
- `two-columns.html` - Side-by-side comparison with headers
- `cards-2x2.html` - 2x2 card grid layout
- `cards-3x2.html` - 3x2 card grid layout (6 cards)
- `stats.html` - Large metrics display (3 stats)
- `section.html` - Section divider with number
- `architecture.html` - Layered architecture diagram (4 layers)
- `features.html` - Feature list with accent bars (6 features)
- `flow.html` - Step-by-step process flow (4 steps with arrows)

## Usage

```bash
# Generate presentation
node scripts/create-pptx.js

# Open result (macOS)
open output.pptx
```

## Common Errors

| Error | Solution |
|-------|----------|
| "Text ends too close to bottom" | Move content up or reduce font size |
| "Text element has border" | Move border to parent `<div>` |
| "DIV contains unwrapped text" | Wrap text in `<p>` tags |
| "CSS gradients not supported" | Use solid colors instead |

## AI Image Generation

Generate custom images for slides using Google Gemini.

### Setup

```bash
# Add your Gemini API key to .env
GOOGLE_API_KEY=your-api-key-here
```

Get an API key from: https://aistudio.google.com/apikey

### CLI Usage

```bash
# Generate a slide background
node scripts/generate-image.js background output.png "digital payments and blockchain"

# Generate an icon
node scripts/generate-image.js icon icon.png "secure transaction"

# Custom prompt
node scripts/generate-image.js custom hero.png "futuristic network visualization"
```

### Programmatic Usage

```javascript
const { generateSlideBackground, generateIcon, generateImage } = require('./scripts/generate-image');

// Generate a background
const result = await generateSlideBackground(
  "AI and machine learning",
  "slides/ai-background.png",
  { primary: "#667eea", accent1: "#00d4ff", accent2: "#764ba2" }
);

// Generate an icon
await generateIcon("cloud computing", "icons/cloud.png", "minimalist");

// Custom image
await generateImage("abstract data visualization", "custom.png");
```

### Using Generated Images in Slides

```html
<body>
    <!-- Background image with opacity -->
    <img class="background-image" src="background.png"
         style="position:absolute; top:0; left:0; width:720pt; height:405pt; opacity:0.6;" />

    <!-- Content on top -->
    <div class="content">
        <h1 class="title">Your Title</h1>
    </div>
</body>
```

## Files

- `scripts/html2pptx.js` - Core HTML-to-PPTX converter
- `scripts/create-pptx.js` - Build script
- `scripts/generate-image.js` - AI image generation with Gemini
- `templates/*.html` - Slide templates
- `SKILL.md` - This documentation

## tools

* Reddit API

  * name: pay-per-use-based reddit-api
  * access: agent-pay
  * usage:
    ```
    ** API Discovery ** First, discover available endpoints by making a GET request to the base URL:
    curl https://proxy-monetize.fluxapay.xyz/api/reddit-api
    ```

* Nano Banana T2I

  * name: pay-per-use-based nano-banana-t2i
  * access: agent-pay
  * usage:
    ```
    ** API Discovery ** First, discover available endpoints by making a GET request to the base URL:
    curl https://proxy-monetize.fluxapay.xyz/api/nano-banana-t2i
    ```

* Make X402 payment: see ./fluxa-wallet/X402-PAYMENT.md


# notes for tools use

* If the invoked tool's access is **agent-pay**, it means the tool is accessed by the agent on a **pay-per-use** basis.
  The agent needs to handle x402 payment flow to use these tools.
  See ./fluxa-wallet/SKILL.md for the complete payment wallet documentation.
* For x402 payment details, refer to ./fluxa-wallet/X402-PAYMENT.md
* For payout operations, refer to ./fluxa-wallet/PAYOUT.md
* For payment link operations, refer to ./fluxa-wallet/PAYMENT-LINK.md
