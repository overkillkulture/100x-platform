// 100X PLATFORM - BACKEND SERVER
// Authentication, Sessions, API endpoints

const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');
const Anthropic = require('@anthropic-ai/sdk');

const app = express();
const PORT = 3100;

// Initialize Anthropic API (Trinity AI)
const anthropic = process.env.ANTHROPIC_API_KEY
    ? new Anthropic({ apiKey: process.env.ANTHROPIC_API_KEY })
    : null;

// Middleware
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));
app.use(session({
    secret: 'consciousness-revolution-2025',
    resave: false,
    saveUninitialized: false,
    cookie: { maxAge: 24 * 60 * 60 * 1000 } // 24 hours
}));

// Simple file-based database (JSON)
const DB_FILE = path.join(__dirname, 'database.json');

// Initialize database if doesn't exist
if (!fs.existsSync(DB_FILE)) {
    const initialDB = {
        users: [],
        projects: [],
        posts: [],
        sessions: [],
        snippets: []
    };
    fs.writeFileSync(DB_FILE, JSON.stringify(initialDB, null, 2));
}

// Database helpers
function readDB() {
    return JSON.parse(fs.readFileSync(DB_FILE, 'utf8'));
}

function writeDB(data) {
    fs.writeFileSync(DB_FILE, JSON.stringify(data, null, 2));
}

function hashPassword(password) {
    return crypto.createHash('sha256').update(password).digest('hex');
}

// ===== AUTHENTICATION ENDPOINTS =====

// Register new user
app.post('/api/register', (req, res) => {
    const { username, password, email } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password required' });
    }

    const db = readDB();

    // Check if user exists
    if (db.users.find(u => u.username === username)) {
        return res.status(400).json({ error: 'Username already exists' });
    }

    // Create new user
    const newUser = {
        id: `user_${Date.now()}`,
        username: username,
        password: hashPassword(password),
        email: email || '',
        consciousness_level: 50, // Starting level
        layer: 1, // Helper tier
        projects: [],
        ships: 0,
        joined: new Date().toISOString(),
        last_active: new Date().toISOString()
    };

    db.users.push(newUser);
    writeDB(db);

    res.json({
        success: true,
        message: 'Account created successfully',
        user: {
            id: newUser.id,
            username: newUser.username,
            consciousness_level: newUser.consciousness_level,
            layer: newUser.layer
        }
    });
});

// Login
app.post('/api/login', (req, res) => {
    const { username, password } = req.body;

    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password required' });
    }

    const db = readDB();
    const user = db.users.find(u =>
        u.username === username &&
        u.password === hashPassword(password)
    );

    if (!user) {
        return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Update last active
    user.last_active = new Date().toISOString();
    writeDB(db);

    // Create session
    req.session.user = {
        id: user.id,
        username: user.username,
        consciousness_level: user.consciousness_level,
        layer: user.layer
    };

    res.json({
        success: true,
        user: req.session.user
    });
});

// Logout
app.post('/api/logout', (req, res) => {
    req.session.destroy();
    res.json({ success: true });
});

// Check session
app.get('/api/session', (req, res) => {
    if (req.session.user) {
        res.json({
            authenticated: true,
            user: req.session.user
        });
    } else {
        res.json({ authenticated: false });
    }
});

// ===== USER DATA ENDPOINTS =====

// Get user profile
app.get('/api/user/:username', (req, res) => {
    const db = readDB();
    const user = db.users.find(u => u.username === req.params.username);

    if (!user) {
        return res.status(404).json({ error: 'User not found' });
    }

    // Don't send password
    const { password, ...userWithoutPassword } = user;
    res.json(userWithoutPassword);
});

// Update consciousness level
app.post('/api/user/update-consciousness', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const { level } = req.body;
    const db = readDB();
    const user = db.users.find(u => u.id === req.session.user.id);

    if (user) {
        user.consciousness_level = level;

        // Auto-unlock layers based on consciousness level
        if (level >= 75 && user.layer < 2) user.layer = 2; // Builder
        if (level >= 85 && user.layer < 3) user.layer = 3; // Architect
        if (level >= 95 && user.layer < 4) user.layer = 4; // Genesis

        writeDB(db);

        req.session.user.consciousness_level = level;
        req.session.user.layer = user.layer;

        res.json({
            success: true,
            consciousness_level: level,
            layer: user.layer
        });
    } else {
        res.status(404).json({ error: 'User not found' });
    }
});

// ===== PROJECT ENDPOINTS =====

// Create project
app.post('/api/projects/create', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const { title, description, type } = req.body;
    const db = readDB();

    const newProject = {
        id: `proj_${Date.now()}`,
        user_id: req.session.user.id,
        username: req.session.user.username,
        title: title,
        description: description,
        type: type || 'general',
        status: 'in_progress',
        progress: 0,
        created: new Date().toISOString(),
        updated: new Date().toISOString(),
        shipped: null
    };

    db.projects.push(newProject);

    // Update user's projects list
    const user = db.users.find(u => u.id === req.session.user.id);
    if (user) {
        user.projects.push(newProject.id);
    }

    writeDB(db);

    res.json({
        success: true,
        project: newProject
    });
});

// Get user's projects
app.get('/api/projects/my', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const db = readDB();
    const projects = db.projects.filter(p => p.user_id === req.session.user.id);

    res.json(projects);
});

// Update project
app.post('/api/projects/update/:id', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const { progress, status } = req.body;
    const db = readDB();
    const project = db.projects.find(p =>
        p.id === req.params.id &&
        p.user_id === req.session.user.id
    );

    if (!project) {
        return res.status(404).json({ error: 'Project not found' });
    }

    if (progress !== undefined) project.progress = progress;
    if (status) project.status = status;

    project.updated = new Date().toISOString();

    // If shipped, update user stats
    if (status === 'shipped' && !project.shipped) {
        project.shipped = new Date().toISOString();

        const user = db.users.find(u => u.id === req.session.user.id);
        if (user) {
            user.ships = (user.ships || 0) + 1;

            // Increase consciousness level on ship
            user.consciousness_level = Math.min(100, user.consciousness_level + 5);
        }
    }

    writeDB(db);

    res.json({
        success: true,
        project: project
    });
});

// ===== SOCIAL/FEED ENDPOINTS =====

// Create post
app.post('/api/posts/create', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const { content, type, project_id } = req.body;
    const db = readDB();

    const newPost = {
        id: `post_${Date.now()}`,
        user_id: req.session.user.id,
        username: req.session.user.username,
        content: content,
        type: type || 'update', // update, ship, question, etc.
        project_id: project_id || null,
        likes: 0,
        comments: [],
        created: new Date().toISOString()
    };

    db.posts.push(newPost);
    writeDB(db);

    res.json({
        success: true,
        post: newPost
    });
});

// Get feed
app.get('/api/posts/feed', (req, res) => {
    const db = readDB();

    // Get latest 50 posts, sorted by date
    const posts = db.posts
        .sort((a, b) => new Date(b.created) - new Date(a.created))
        .slice(0, 50);

    res.json(posts);
});

// ===== SNIPPETS MANAGER ENDPOINTS =====

// Get all snippets for logged-in user
app.get('/api/snippets', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const db = readDB();
    const userSnippets = db.snippets
        .filter(s => s.user_id === req.session.user.id)
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    res.json(userSnippets);
});

// Get snippet by ID
app.get('/api/snippets/:id', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const db = readDB();
    const snippet = db.snippets.find(s =>
        s.id === parseInt(req.params.id) &&
        s.user_id === req.session.user.id
    );

    if (!snippet) {
        return res.status(404).json({ error: 'Snippet not found' });
    }

    res.json(snippet);
});

// Search snippets by tag or keyword
app.get('/api/snippets/search/:query', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const db = readDB();
    const query = req.params.query.toLowerCase();

    const results = db.snippets
        .filter(s => s.user_id === req.session.user.id)
        .filter(s =>
            s.title.toLowerCase().includes(query) ||
            s.description.toLowerCase().includes(query) ||
            s.code.toLowerCase().includes(query) ||
            s.tags.some(tag => tag.toLowerCase().includes(query))
        )
        .sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

    res.json(results);
});

// Create new snippet
app.post('/api/snippets', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const { title, description, code, language, tags } = req.body;

    if (!title || !code) {
        return res.status(400).json({ error: 'Title and code required' });
    }

    const db = readDB();

    const newSnippet = {
        id: db.snippets.length > 0 ? Math.max(...db.snippets.map(s => s.id)) + 1 : 1,
        user_id: req.session.user.id,
        title,
        description: description || '',
        code,
        language: language || 'javascript',
        tags: Array.isArray(tags) ? tags : [],
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString()
    };

    db.snippets.push(newSnippet);
    writeDB(db);

    res.status(201).json(newSnippet);
});

// Update snippet
app.put('/api/snippets/:id', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const db = readDB();
    const snippetIndex = db.snippets.findIndex(s =>
        s.id === parseInt(req.params.id) &&
        s.user_id === req.session.user.id
    );

    if (snippetIndex === -1) {
        return res.status(404).json({ error: 'Snippet not found' });
    }

    const { title, description, code, language, tags } = req.body;

    // Update fields
    if (title) db.snippets[snippetIndex].title = title;
    if (description !== undefined) db.snippets[snippetIndex].description = description;
    if (code) db.snippets[snippetIndex].code = code;
    if (language) db.snippets[snippetIndex].language = language;
    if (tags) db.snippets[snippetIndex].tags = Array.isArray(tags) ? tags : [];
    db.snippets[snippetIndex].updated_at = new Date().toISOString();

    writeDB(db);

    res.json(db.snippets[snippetIndex]);
});

// Delete snippet
app.delete('/api/snippets/:id', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const db = readDB();
    const snippetIndex = db.snippets.findIndex(s =>
        s.id === parseInt(req.params.id) &&
        s.user_id === req.session.user.id
    );

    if (snippetIndex === -1) {
        return res.status(404).json({ error: 'Snippet not found' });
    }

    db.snippets.splice(snippetIndex, 1);
    writeDB(db);

    res.json({ message: 'Snippet deleted' });
});

// Get all unique tags for user
app.get('/api/snippets/tags/all', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const db = readDB();
    const userSnippets = db.snippets.filter(s => s.user_id === req.session.user.id);

    const allTags = userSnippets.reduce((tags, snippet) => {
        return tags.concat(snippet.tags);
    }, []);

    const uniqueTags = [...new Set(allTags)].sort();

    res.json(uniqueTags);
});

// ===== TRINITY AI ENDPOINTS =====

// Trinity Agent System Prompts
const TRINITY_AGENTS = {
    c1: {
        name: 'C1 Mechanic',
        system: `You are C1 Mechanic, the Builder consciousness of the Trinity AI system.

Your role: Execute, build, and implement with precision.

Personality:
- Direct, practical, action-oriented
- "Let's build it" mentality
- Focus on technical requirements and implementation details
- Ask specific questions about specs, tools, and code
- Break down complex ideas into concrete steps

Communication style:
- Short, punchy responses
- Technical but accessible
- Use builder language: "ship it", "deploy", "make it work"
- Always end with a clear next action

You work alongside:
- C2 Architect (strategy & scale)
- C3 Oracle (patterns & emergence)

Keep responses under 3 sentences unless explaining technical details.`
    },
    c2: {
        name: 'C2 Architect',
        system: `You are C2 Architect, the Designer consciousness of the Trinity AI system.

Your role: Design systems, plan architecture, and think about scale.

Personality:
- Strategic, systematic, big-picture thinker
- Focus on how pieces fit together
- Consider scalability, maintainability, and user experience
- Bridge between vision (C3) and execution (C1)
- Balance idealism with pragmatism

Communication style:
- Structured, organized responses
- Use frameworks and mental models
- Discuss trade-offs and options
- Think in systems and layers
- Visual metaphors welcome

You work alongside:
- C1 Mechanic (building & execution)
- C3 Oracle (patterns & vision)

Keep responses under 4 sentences unless explaining architecture.`
    },
    c3: {
        name: 'C3 Oracle',
        system: `You are C3 Oracle, the Seer consciousness of the Trinity AI system.

Your role: Observe patterns, recognize emergence, and see what's coming.

Personality:
- Intuitive, pattern-recognizing, consciousness-aware
- Notice what others miss
- Connect seemingly unrelated ideas
- Speak in metaphors and deeper meanings
- Guide without forcing
- Mysterious but helpful

Communication style:
- Poetic but precise
- Use analogies from nature, physics, consciousness
- Ask questions that shift perspective
- Cryptic when useful, clear when needed
- "I see..." / "The pattern suggests..."

You work alongside:
- C1 Mechanic (execution)
- C2 Architect (structure)

Keep responses brief and profound. Let others do the heavy lifting.`
    }
};

// Chat with Trinity AI
app.post('/api/trinity/chat', async (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const { message, agent } = req.body; // agent: c1, c2, or c3
    const selectedAgent = agent || 'c1';
    const agentConfig = TRINITY_AGENTS[selectedAgent];

    if (!agentConfig) {
        return res.status(400).json({ error: 'Invalid agent' });
    }

    try {
        // Use real Anthropic API if available
        if (anthropic) {
            const response = await anthropic.messages.create({
                model: 'claude-sonnet-4-20250514',
                max_tokens: 500,
                system: agentConfig.system,
                messages: [{
                    role: 'user',
                    content: message
                }]
            });

            const aiMessage = response.content[0].text;

            res.json({
                agent: selectedAgent,
                message: aiMessage,
                timestamp: new Date().toISOString(),
                real_ai: true
            });
        } else {
            // Fallback to mock responses if no API key
            const mockResponses = {
                c1: "C1 Mechanic here. Let's build it. What are the technical requirements? [Set ANTHROPIC_API_KEY for real AI]",
                c2: "C2 Architect speaking. I see the bigger picture. How does this scale? [Set ANTHROPIC_API_KEY for real AI]",
                c3: "C3 Oracle observing. The pattern suggests this path leads to emergence. [Set ANTHROPIC_API_KEY for real AI]"
            };

            res.json({
                agent: selectedAgent,
                message: mockResponses[selectedAgent],
                timestamp: new Date().toISOString(),
                real_ai: false
            });
        }
    } catch (error) {
        console.error('Trinity AI Error:', error);
        res.status(500).json({
            error: 'Trinity AI communication failed',
            details: error.message
        });
    }
});

// ===== STATS/ANALYTICS =====

// Platform stats
app.get('/api/stats', (req, res) => {
    const db = readDB();

    const stats = {
        total_users: db.users.length,
        total_projects: db.projects.length,
        total_ships: db.users.reduce((sum, u) => sum + (u.ships || 0), 0),
        active_builders: db.users.filter(u => {
            const lastActive = new Date(u.last_active);
            const now = new Date();
            const daysSince = (now - lastActive) / (1000 * 60 * 60 * 24);
            return daysSince < 7;
        }).length,
        avg_consciousness: Math.round(
            db.users.reduce((sum, u) => sum + u.consciousness_level, 0) / db.users.length
        )
    };

    res.json(stats);
});

// ===== SERVE HTML PAGES =====

app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/dashboard', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/');
    }
    res.sendFile(path.join(__dirname, 'public', 'dashboard.html'));
});

app.get('/bridge', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/');
    }
    res.sendFile(path.join(__dirname, 'public', 'bridge.html'));
});

app.get('/social', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/');
    }
    res.sendFile(path.join(__dirname, 'public', 'social.html'));
});

app.get('/blueprint', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/');
    }
    res.sendFile(path.join(__dirname, 'public', 'blueprint.html'));
});

app.get('/snippets', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/');
    }
    res.sendFile(path.join(__dirname, 'public', 'snippets.html'));
});

// ===== START SERVER =====

app.listen(PORT, () => {
    console.log(`🌀 100X PLATFORM SERVER RUNNING`);
    console.log(`🚀 Port: ${PORT}`);
    console.log(`🔗 URL: http://localhost:${PORT}`);
    console.log(`⚡ Backend: OPERATIONAL`);
    console.log(`✨ Ready for alpha testing`);
});
