# Beta Testing System - Developer Guide

## Overview
The Overkore UI now has a comprehensive beta testing system to help users understand the status of features and encourage bug reporting.

## Components

### 1. BetaNotice (Global Banner)
**Location**: Appears at the top of every page
**Purpose**: Alert all users that the system is in beta and encourage bug reporting

**Features**:
- Fixed position at top of screen
- Bright orange color for visibility
- Click to minimize/expand
- Provides guidance on how to help test

**Auto-included**: Yes, added to `layout.tsx` - no additional code needed

---

### 2. SymbolLegend (Floating Help Button)
**Location**: Bottom-right corner of every page
**Purpose**: Explains all status symbols used throughout the site

**Features**:
- Floating "?" button
- Click to open modal with full legend
- Lists all 7 symbol types with descriptions
- Reminds users about beta status

**Auto-included**: Yes, added to `layout.tsx` - no additional code needed

---

### 3. BetaBadge (Inline Status Indicator)
**Location**: Place next to any feature/button/section
**Purpose**: Mark individual features with their current status

**Usage**:
```tsx
import BetaBadge from './components/BetaBadge';

// Basic usage
<button>My Feature <BetaBadge /></button>

// With specific type
<button>My Feature <BetaBadge type="beta" /></button>

// With custom text
<button>My Feature <BetaBadge type="construction" text="WIP" /></button>

// Different sizes
<h1>Big Feature <BetaBadge type="core" size="large" /></h1>
<p>Small feature <BetaBadge type="new" size="small" /></p>
```

## Badge Types

| Type | Icon | Color | Use When |
|------|------|-------|----------|
| `beta` | 🔧 | Orange | Feature is rough draft/work in progress |
| `stable` | ✅ | Green | Feature is tested and working reliably |
| `construction` | 🚧 | Yellow | Feature is actively being built |
| `live` | ⚡ | Cyan | Shows real-time data / active system |
| `caution` | ⚠️ | Red | Known issues or experimental feature |
| `core` | 🎯 | Green | Essential system component |
| `new` | 💡 | Yellow | Recently added feature |

## Badge Sizes

- `small` - For inline text, small buttons (default)
- `medium` - For standard buttons, section headers
- `large` - For page titles, major features

## Examples

### Example 1: Button with Beta Badge
```tsx
<button onClick={handleClick}>
  Deploy Module
  <BetaBadge type="beta" />
</button>
```

### Example 2: Section Header
```tsx
<h2>
  Advanced Analytics
  <BetaBadge type="construction" size="medium" />
</h2>
```

### Example 3: Live Data Indicator
```tsx
<div>
  Connection Status
  <BetaBadge type="live" text="LIVE DATA" />
</div>
```

### Example 4: Multiple Badges
```tsx
<div>
  Experimental AI System
  <BetaBadge type="new" />
  <BetaBadge type="caution" />
</div>
```

## Best Practices

1. **Be Honest**: Mark features with their actual status
2. **Use Beta Liberally**: If unsure, mark as beta - better safe than sorry
3. **Update as Progress**: Change badges from construction → beta → stable as features mature
4. **Core Features**: Mark essential systems with `core` badge
5. **New Features**: Use `new` badge for recently added functionality (remove after ~1 week)
6. **Live Data**: Always mark real-time data displays with `live` badge

## User Benefits

- **Clarity**: Users know what to expect from each feature
- **Confidence**: Users can trust marked-stable features more
- **Engagement**: Users encouraged to report bugs on beta features
- **Guidance**: Symbol legend helps users understand the system

## Developer Benefits

- **Communication**: Clear status communication with users
- **Feedback Loop**: More targeted bug reports on work-in-progress features
- **Version Control**: Visual tracking of feature maturity
- **User Empathy**: Users are more patient with beta-marked features

## Customization

### Changing Colors
Edit `BetaBadge.tsx` and update the `configs` object:

```tsx
const configs = {
  beta: {
    icon: '🔧',
    label: 'BETA',
    bg: '#ff6b00',  // ← Change this
    color: '#000'    // ← And this
  },
  // ...
};
```

### Adding New Badge Types
1. Add to `BetaBadgeType` union in `BetaBadge.tsx`
2. Add configuration to `configs` object
3. Add to legend in `SymbolLegend.tsx`

### Customizing Banner Text
Edit `BetaNotice.tsx` to change messaging

## File Structure

```
app/
├── components/
│   ├── BetaNotice.tsx       # Global top banner
│   ├── SymbolLegend.tsx     # Floating help button
│   └── BetaBadge.tsx        # Inline status badges
├── layout.tsx               # Includes BetaNotice + SymbolLegend
└── components/ButtonPanel.tsx  # Example usage
```

## Testing

View your changes:
1. Start dev server: `npm run dev`
2. Open http://localhost:3000
3. Check for:
   - Orange banner at top
   - "?" button in bottom-right
   - Badges on module buttons

## Questions?

Contact the development team or check the live site to see examples of proper badge usage.

---

**Remember**: This is a beta testing tool to help improve the product. Use it liberally and update it as features mature!
