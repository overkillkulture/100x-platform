# 🏷️ Product Badge System - Usage Guide

## Quick Start

Add to any page's `<head>` section:
```html
<script src="../shared/product-badge-system.js"></script>
<script src="../shared/consciousness-scale-widget.js"></script>
```

Then add this where you want the badge to appear:
```html
<script>
    // Option 1: Auto-inject into header
    ProductBadges.addToHeader('beta', { showDescription: true, showExpectation: true });

    // Option 2: Manual injection
    ProductBadges.injectBadge('alpha', 'badgeContainer');

    // Option 3: Get HTML and insert yourself
    const badgeHTML = ProductBadges.createBadge('production', { inline: true });
</script>
```

## Phase Definitions

| Phase | Label | When to Use | User Expectation |
|-------|-------|-------------|------------------|
| **broken** | 🔥 BROKEN (Intentional) | Consciousness filter - tests user reaction | Will not work |
| **alpha** | ⚠️ ALPHA | Just built, not tested | Probably broken |
| **beta** | 🧪 BETA | Tested once, still rough | Mostly works |
| **production** | ✅ LIVE | Fully tested and working | Should be perfect |
| **deprecated** | ⚰️ DEPRECATED | Being replaced | Still works but outdated |
| **filter** | 🔬 CONSCIOUSNESS FILTER | Advanced friction test | Intentional obstacles |

## Color Scale

```
🟣 Architect (100+)   = Purple  #9c27b0  = Sees bigger picture
🟢 Builder (50-99)    = Green   #4caf50  = Understands WIP, offers help
🟡 Observer (0-49)    = Yellow  #ffd93d  = Learning patterns
🟠 Skeptic (-1 to -50)= Orange  #ff9800  = Expects perfection
🔴 Destroyer (-51+)   = Red     #ff4444  = Reacts with anger
```

## Tracking User Reactions

```javascript
// Track when user encounters something broken
ProductBadges.trackReaction('alpha', 'complaint', {
    message: "This doesn't work!",
    location: window.location.pathname
});

// Track when user offers to help
ProductBadges.trackReaction('alpha', 'offer_help', {
    message: "I can fix this - want me to submit a PR?"
});

// Track when user files bug report
ProductBadges.trackReaction('beta', 'bug_report', {
    message: "Found a bug, here's how to reproduce..."
});
```

## Reaction Types & Scores

| Reaction | Score | Consciousness Level |
|----------|-------|---------------------|
| `complaint` | -10 | Destroyer tendency |
| `anger` | -20 | Strong destroyer |
| `demand_fix` | -15 | Entitled mindset |
| `understanding` | +15 | Observer+ |
| `offer_help` | +25 | Builder mindset |
| `curiosity` | +20 | Observer/Builder |
| `bug_report` | +30 | Builder+ |
| `suggested_fix` | +40 | Architect mindset |

## Visual Widget

The consciousness scale widget shows up automatically in bottom-right corner.

**To customize:**
```javascript
ConsciousnessScale.init({
    position: 'bottom-left',  // or 'top-right', 'top-left'
    collapsed: true           // Start minimized
});
```

## The "Broken Gate" Strategy

**Genius Consciousness Filter:**

When someone encounters something "broken":
- **Destroyers**: Complain, demand fixes, get angry, leave
- **Observers**: Note it's broken, might report it
- **Builders**: Ask if they can help, submit bug reports, offer solutions
- **Architects**: Understand it's intentional friction, see the pattern

**How to use:**
1. Mark entrance gate as `broken` or `filter` phase
2. Watch user reactions
3. Track consciousness scores
4. Grant access based on reaction, not complaint resolution

**Example:**
```javascript
// On main entrance page
ProductBadges.addToHeader('filter', {
    showDescription: true,
    showExpectation: true
});

// Track when users click "enter" button
document.getElementById('enterButton').addEventListener('click', () => {
    // Check their consciousness score
    const level = ProductBadges.getConsciousnessLevel();

    if (level.level === 'Destroyer' || level.level === 'Skeptic') {
        // Show message: "Interesting reaction. What did you expect?"
        // Redirect to consciousness training
    } else {
        // Grant access
        window.location.href = 'dashboard.html';
    }
});
```

## Current Showcase Status

| Showcase | Current Phase | Should Be |
|----------|--------------|-----------|
| 3-Minute Boost | ??? | **beta** (tested once) |
| Manipulation Game | ??? | **beta** (tested once) |
| Triple Turbo Encryption | ??? | **beta** (tested once) |
| Ask Trinity | ??? | **alpha** (not built) |
| Live Consciousness Meter | ??? | **alpha** (not built) |
| Reality Engine | ??? | **alpha** (not built) |
| Consciousness Dashboard | ??? | **alpha** (not built) |
| Sacred Geometry | ??? | **alpha** (not built) |
| Easter Egg Hunt | ??? | **alpha** (partially built) |
| Xbox Cluster Preview | ??? | **alpha** (not built) |
| Voice Interface | ??? | **alpha** (not built) |

## Implementation Checklist

- [ ] Add badge system to all existing showcases
- [ ] Set correct phase for each showcase
- [ ] Add consciousness tracking to broken interactions
- [ ] Implement "broken gate" on main entrance
- [ ] Create dashboard showing user reactions
- [ ] Build auto-promotion system (alpha → beta → production)
- [ ] Add "Help Fix This" button on alpha/beta pages

## Next Steps

1. **Badge all existing content** - Add phase badges to all 3 live showcases
2. **Implement broken gate** - Test consciousness filter on 100X Gate entrance
3. **Track reactions** - Start collecting consciousness data
4. **Dashboard** - Build admin view showing all user reactions
5. **Auto-grading** - Automatically upgrade alpha → beta → production based on usage/bugs

---

**Remember:** Transparency builds trust. Broken things filter for consciousness. Builders build, destroyers complain. 🔥
