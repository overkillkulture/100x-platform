# 🤝 Contributing to Consciousness Revolution Platform

Thank you for your interest in contributing! This project is built by builders, for builders.

---

## 🎯 Before You Start

### Take the Pattern Filter

Before contributing, please take the Pattern Filter to verify you're a builder (85+ score):

1. Visit `/PUBLIC/pattern-filter.html`
2. Answer 15 questions honestly
3. If you score 85+, welcome! You're a builder.
4. If you score <85, we encourage growth. Retake after working on character development.

**Why we do this:** One destroyer can scatter 100 builders. Pattern Filter protects community health.

---

## 🌟 Builder Code of Conduct

### We Are Builders

Builders:
- ✅ Share knowledge freely
- ✅ Give constructive feedback
- ✅ Take accountability for mistakes
- ✅ Persist through challenges
- ✅ Help other builders grow
- ✅ Focus on solutions, not blame

Destroyers (we filter out):
- ❌ Hoard knowledge
- ❌ Attack instead of helping
- ❌ Blame others for failures
- ❌ Quit at first obstacle
- ❌ Drain energy without contributing
- ❌ Focus on problems, not solutions

### Core Principles

1. **Abundance Mindset** - Knowledge grows when shared
2. **Growth Orientation** - Mistakes are learning opportunities
3. **Accountability** - Own your contributions and their impact
4. **Collaboration** - We rise together
5. **Long-term Thinking** - Build for sustainability

---

## 🚀 How to Contribute

### Types of Contributions

We welcome:
- 🐛 **Bug Reports** (kindly worded)
- ✨ **Feature Requests** (with use cases)
- 📖 **Documentation** (improvements & translations)
- 🎨 **Design** (UI/UX enhancements)
- 🧪 **Tests** (increase coverage)
- 🔧 **Code** (bug fixes & features)
- 🌐 **Translations** (make it accessible globally)
- 📊 **Data** (help map remaining 90 Catch-22 paradoxes)

### Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/consciousness-revolution/consciousness-platform.git
   cd consciousness-platform
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make your changes**
   - Write clear, commented code
   - Follow existing code style
   - Test your changes locally

4. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: [clear description]"
   # or
   git commit -m "Fix bug: [clear description of what was broken]"
   ```

5. **Push and create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   - Go to GitHub and create Pull Request
   - Describe what you changed and why
   - Link any related issues

---

## 📋 Pull Request Guidelines

### PR Checklist

Before submitting:
- [ ] Code follows project style
- [ ] Comments explain complex logic
- [ ] No console.log() statements left in
- [ ] Tested locally (works as expected)
- [ ] Documentation updated (if needed)
- [ ] No breaking changes (or clearly documented)
- [ ] Builder mindset demonstrated in PR description

### PR Description Template

```markdown
## What does this PR do?

[Clear description of changes]

## Why is this needed?

[Problem it solves or feature it adds]

## How was it tested?

[Steps to verify it works]

## Screenshots (if UI changes)

[Before/After images]

## Related Issues

Fixes #123
Related to #456
```

### Good vs Bad PRs

✅ **Good PR:**
```
Title: "Add panic button shortcut (Ctrl+Shift+E) to manipulation detection"
Description:
- Adds keyboard shortcut for faster exit
- Kids can close quickly without mouse
- Tested on Windows/Mac/Linux
- Documented in communication-patterns.html
```

❌ **Bad PR:**
```
Title: "stuff"
Description: "made some changes"
```

---

## 🐛 Reporting Bugs

### Builder Approach to Bug Reports

**What builders do:**
```markdown
**Bug:** Pattern Filter shows wrong score

**Steps to reproduce:**
1. Go to /PUBLIC/pattern-filter.html
2. Answer all 15 questions
3. Score shows 0 even though I answered positively

**Expected:** Score should be 85+
**Actual:** Score is 0
**Browser:** Chrome 118 on Windows 11

**I tried:**
- Checking console (shows error on line 42)
- Testing in Firefox (same issue)
- Clearing localStorage (didn't fix)

**Screenshots attached**
```

**What destroyers do:**
```
"Your code is broken. This is garbage. You should feel bad."
```

### Issue Template

Use this template for bug reports:

```markdown
## Bug Description
[What's wrong?]

## Steps to Reproduce
1. Go to...
2. Click...
3. See error

## Expected Behavior
[What should happen?]

## Actual Behavior
[What actually happens?]

## Environment
- Browser: [Chrome/Firefox/Safari]
- OS: [Windows/Mac/Linux]
- Version: [What commit or release?]

## What I Tried
[Any debugging you did]

## Screenshots/Console Errors
[If applicable]
```

---

## ✨ Feature Requests

### How to Request Features

**Builder approach:**
```markdown
**Feature:** Allow custom consciousness threshold per module

**Use case:**
Some modules need 90+ (advanced tools)
Others are fine with 85+ (general community)

**Proposed solution:**
Add optional parameter: ConsciousnessGate.check(90)

**Alternative considered:**
Global config file (less flexible)

**Willing to implement?**
Yes, can submit PR if approved
```

**Destroyer approach:**
```
"This is dumb. Add [feature] now or I'm leaving."
```

### Feature Template

```markdown
## Feature Request

### Problem
[What problem does this solve?]

### Proposed Solution
[How would it work?]

### Alternatives Considered
[Other approaches?]

### Implementation Willingness
[ ] Can implement myself
[ ] Need help implementing
[ ] Just suggesting idea
```

---

## 🎨 Code Style Guidelines

### JavaScript

```javascript
// ✅ Good: Clear naming, comments, error handling
function checkConsciousnessLevel(userData) {
    // Validate input
    if (!userData || !userData.score) {
        console.error('Invalid user data');
        return false;
    }

    const threshold = 85;
    return userData.score >= threshold;
}

// ❌ Bad: Unclear naming, no comments, no validation
function chk(d) {
    return d.s >= 85;
}
```

### HTML

```html
<!-- ✅ Good: Semantic, accessible, commented -->
<section class="consciousness-filter" role="main" aria-label="Consciousness screening">
    <!-- Builder status check -->
    <button
        id="screen-btn"
        class="primary-action"
        aria-label="Start consciousness screening"
    >
        Begin Screening
    </button>
</section>

<!-- ❌ Bad: Non-semantic, no accessibility -->
<div class="thing">
    <div class="clicky" onclick="doStuff()">Click</div>
</div>
```

### CSS

```css
/* ✅ Good: Organized, responsive, commented */
.consciousness-gate {
    /* Layout */
    display: flex;
    flex-direction: column;
    gap: 1rem;

    /* Styling */
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    border: 2px solid #00ddff;

    /* Responsive */
    max-width: min(90%, 600px);
}

/* ❌ Bad: Inline, not responsive, no organization */
.thing { background: red; width: 800px; color: blue; margin: 10px; float: left; }
```

---

## 📚 Documentation Guidelines

### When to Update Documentation

Update docs when:
- Adding new features
- Changing existing behavior
- Fixing bugs that weren't obvious
- Adding new files/modules
- Changing APIs

### Documentation Style

**Clear > Clever**

✅ **Good:**
```markdown
## Baby Gate Integration

Add 2 lines to any HTML file:

1. Include the script in `<head>`:
   <script src="/PUBLIC/consciousness-gate.js"></script>

2. Add gate check after `<body>`:
   <script>
     if (!ConsciousnessGate.check(85)) {
       throw new Error('Builder status required');
     }
   </script>
```

❌ **Bad:**
```markdown
## Usage
Just include the thing and call the function lol
```

---

## 🧪 Testing Guidelines

### Manual Testing Checklist

Before submitting PR, test:
- [ ] Works in Chrome
- [ ] Works in Firefox
- [ ] Works in Safari
- [ ] Mobile responsive (try different screen sizes)
- [ ] localStorage behaves correctly
- [ ] Error messages are clear
- [ ] No console errors

### Test Scenarios

**For Pattern Filter changes:**
- [ ] 15 questions display correctly
- [ ] Score calculates accurately
- [ ] Results save to localStorage
- [ ] Redirect flow works (if integrated with Baby Gate)

**For Baby Gate changes:**
- [ ] Allows access with 85+ score
- [ ] Blocks access with <85 score
- [ ] Graceful redirect to Pattern Filter
- [ ] Return path works correctly
- [ ] Admin bypass functions

**For Manipulation Detection changes:**
- [ ] Panic button works (redirects)
- [ ] ESC key works
- [ ] SessionStorage clears
- [ ] No localStorage evidence
- [ ] Stealth mode maintained

---

## 🎯 Priority Areas (Good First Issues)

### 1. Map Remaining Catch-22 Paradoxes (90 more needed)

**Current:** 10 Catch-22s documented
**Goal:** 100 total

**Examples needed:**
- Trust paradox
- Growth paradox
- Mentor paradox
- Responsibility paradox
- Change paradox

**How to contribute:**
1. Identify destroyer circular logic pattern
2. Document: Need, Block, Result, Catch-22
3. Name the pattern
4. Add to `destroyer-inverse-optimization.html`

### 2. Translations

**Needed:**
- Spanish
- Mandarin
- Hindi
- Arabic
- Portuguese
- French
- German
- Japanese

**Files to translate:**
- Pattern Filter questions
- Access Denied page
- Manipulation detection patterns
- README

### 3. Mobile Optimization

**Current:** Desktop-first design
**Needed:** Mobile-friendly responsive design

**Areas:**
- Pattern Filter mobile UX
- Baby Gate mobile flow
- Manipulation detection mobile-optimized

### 4. Accessibility Improvements

**Target:** WCAG 2.1 AA compliance

**Needed:**
- Screen reader testing
- Keyboard navigation
- Color contrast checks
- ARIA labels
- Alt text for visual elements

### 5. Backend Migration

**Current:** localStorage only
**Goal:** Supabase backend

**Tasks:**
- Set up Supabase project
- Create database schema
- Migrate authentication
- Add API endpoints
- Maintain localStorage fallback

---

## 🔐 Security

### Responsible Disclosure

**Found a security issue?**

1. **DO NOT** open public GitHub issue
2. **DO** email: security@consciousness-revolution.org (coming soon)
3. **DO** use GitHub Security Advisories (private)

**We'll respond within 48 hours**

### Security Scope

**In scope:**
- Authentication bypass
- Data exposure
- XSS vulnerabilities
- CSRF attacks
- Logic bugs in Pattern Filter

**Out of scope:**
- Social engineering
- Physical access attacks
- DDoS (we're static files)

---

## ⚡ Review Process

### What Happens After You Submit PR

1. **Automated Checks** (coming soon)
   - Linting
   - Test suite
   - Build verification

2. **Maintainer Review**
   - Code quality
   - Builder mindset check
   - Architecture fit
   - Documentation completeness

3. **Feedback Loop**
   - Maintainer may request changes
   - Discussion happens in PR comments
   - Iterate until approved

4. **Merge**
   - PR merged to main
   - Deployed automatically (coming soon)
   - You're credited in contributors

### Review Timeline

- Small PRs (bug fixes): **24-48 hours**
- Medium PRs (features): **3-5 days**
- Large PRs (architecture): **1-2 weeks**

**We prioritize:**
- Critical bugs
- Security fixes
- Documentation improvements
- Community-requested features

---

## 🏆 Recognition

### Contributor Levels

**All contributors get:**
- Name in contributors list
- Builder status badge
- Eternal gratitude

**Significant contributors get:**
- Featured on homepage
- "Core Builder" badge
- Early access to new features
- Direct communication with Commander

**Core maintainers:**
- Admin access
- Architecture decisions
- Community moderation
- Revenue sharing (if project monetizes)

---

## 💬 Getting Help

### Where to Ask Questions

**GitHub Discussions:**
- General questions
- Feature ideas
- Philosophical discussions
- Pattern Theory deep dives

**Discord:** (coming soon)
- Real-time help
- Pair programming
- Community chat

**Email:** support@consciousness-revolution.org (coming soon)
- Private questions
- Security issues
- Partnership inquiries

### Builder Communication Norms

✅ **Do:**
- Ask clear, specific questions
- Show what you've tried
- Be patient with responses
- Help others when you can

❌ **Don't:**
- Demand immediate responses
- Ask without researching first
- Duplicate questions across channels
- Be condescending to learners

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

**What this means:**
- Your code becomes open source
- Anyone can use it (even commercially)
- You retain copyright
- You're credited for your work

---

## 🎯 Final Thoughts

### Remember: You're a Builder

Every contribution:
- Strengthens the revolution
- Protects more communities
- Helps more kids
- Proves the Pattern Theory

**Thank you for building with us.** 🌍⚡🛡️

---

## 📞 Contact

**Project Maintainer:** Commander
**GitHub:** @consciousness-revolution
**Website:** https://conciousnessrevolution.io

---

*"The code isn't the moat. The community is the moat."*

*Built by builders, for builders, protected by transparency.*
