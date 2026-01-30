---
name: remotion-video-creator
description: Create animated videos using Remotion (React-based video framework). Use when the user wants to create demo videos, animated explainers, walkthroughs, or slideshow-style presentations from UI concepts, screenshots, or descriptions. Handles scene design, TypeScript component creation, spring-based animations, typewriter effects, and video export.
---

# Remotion Video Creator

## Prerequisites

Check if the `remotion-best-practices` skill is installed (look in both `.claude/skills/remotion-best-practices/` and `~/.claude/skills/remotion-best-practices/`). If not found, prompt the user to install it - it provides essential Remotion technical knowledge (spring configs, transitions API, sequencing, text animations, etc.).

## Workflow

Creating a Remotion video involves these steps:

1. Gather requirements (story, assets, aspect ratio)
2. Analyze reference images
3. Break down into scenes
4. Recreate images as animated TSX components
5. Extract reusable components
6. Sequence scenes with transitions
7. Preview, iterate, and export

### 1. Gather Requirements

Ask the user:
- What should the video communicate?
- Any images/assets to use? (screenshots, logos, mockups)
- Aspect ratio? 16:9 (YouTube), 9:16 (Reels/Shorts), 4:3, 1:1 (Instagram)

### 2. Analyze Reference Images

When the user provides UI screenshots or mockups:

1. **Read each image** to understand its content, layout, colors, and typography
2. **Identify the story** - what flow or process do the images represent?
3. **Extract details** - exact text, amounts, colors, element positions, branding
4. **Note relationships** - which elements repeat across images? What's the narrative order?

This analysis informs every subsequent step. The goal is to understand the images deeply enough to faithfully recreate them as animated components.

### 3. Break Down into Scenes

Map each image (or logical group) to a scene. For each, identify:
- **Purpose**: What it communicates
- **Elements**: Visual components needed
- **Entrance**: How elements appear (fade, slide, spring)
- **Duration**: Time on screen (frames at 30fps)

Example:
```
Scene 1: Intro (100 frames) - Logo reveal + tagline
Scene 2: Problem (120 frames) - Show pain point
Scene 3: Solution (150 frames) - Demonstrate product
Scene 4: Result (90 frames) - Success state
```

### 4. Recreate Images as Animated TSX Components

Rather than displaying static images, rebuild each scene as a TSX component with animations:

1. **Reproduce the layout** - match the original image's structure (cards, bubbles, tables, etc.)
2. **Match visual details** - colors, fonts, spacing, borders, shadows from the reference
3. **Add motion** - make elements animate in rather than appearing all at once:
   - Text: typewriter effect (reveal characters over time)
   - Tables/lists: staggered row entrance
   - Cards/bubbles: spring-based slide + fade in
   - Loaders/spinners: continuous rotation
4. **Preserve the content** - use the exact text, amounts, labels from the reference images

Design each scene in two dimensions:

**Layers** (spatial):
1. Background (color, gradient, glow)
2. Main content (cards, images, text)
3. Decorative (shadows, particles)

**Time** (temporal):
1. What appears first?
2. What follows? (stagger delays)
3. What loops? (spinners, pulses)

### 5. Extract Reusable Components

Move repeated elements to `src/components/`:
- Avatars, icons, branded elements
- Card/bubble layouts
- Animation wrappers

Important: Use unique IDs for SVG gradients to avoid conflicts across component instances.

### 6. Sequence with Transitions

Use `TransitionSeries` from `@remotion/transitions`. Match transition to content:
- **fade**: Universal, clean (chat pauses, state changes)
- **slide**: Spatial navigation (app screens, page turns)
- **wipe**: Dramatic reveals

### 7. Preview, Iterate, Export

```bash
npm start                                              # Preview
npx remotion render <CompositionId> output/video.mp4   # Export
```

## Scene Design Principles

- Animate in reading order; guide the eye with motion
- Don't animate everything at once; let elements breathe
- Same easing for same animation types; consistent palette
- Timing: fast (15-20 frames), medium (25-35), slow (40-60)

## Duration Calculation

Total = Sum of scene durations - Sum of transition durations

Transitions overlap adjacent scenes. Update `TOTAL_DURATION` in Root.tsx after changes.

## File Structure

```
<project-name>/
├── public/           # Static assets (images, logos)
├── src/
│   ├── Root.tsx      # Composition config (dimensions, fps, duration)
│   ├── MainVideo.tsx # Scene sequencing with TransitionSeries
│   ├── components/   # Reusable elements
│   └── scenes/       # Individual scene components
├── output/           # Rendered videos
└── package.json
```
