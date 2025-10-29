// 100X PLATFORM - BACKEND SERVER
// Authentication, Sessions, API endpoints

const express = require('express');
const session = require('express-session');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');
const crypto = require('crypto');

const app = express();
const PORT = 3100;

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
        sessions: []
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
    req.session.destroy((err) => {
        if (err) {
            return res.status(500).json({ error: 'Logout failed' });
        }
        res.json({ success: true });
    });
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

// ===== BUG REPORTING ENDPOINTS =====

// Submit bug report
app.post('/api/bugs/report', (req, res) => {
    const { title, description, severity, category, browser, url } = req.body;

    if (!title || !description) {
        return res.status(400).json({ error: 'Title and description required' });
    }

    const db = readDB();

    const newBug = {
        id: `bug_${Date.now()}`,
        user_id: req.session.user ? req.session.user.id : 'anonymous',
        username: req.session.user ? req.session.user.username : 'Anonymous',
        title: title,
        description: description,
        severity: severity || 'medium', // low, medium, high, critical
        category: category || 'other', // frontend, backend, database, performance, security, other
        status: 'new', // new, in_progress, resolved, closed
        browser: browser || 'unknown',
        url: url || '',
        created: new Date().toISOString(),
        updated: new Date().toISOString(),
        resolved_at: null
    };

    db.bugs.push(newBug);
    writeDB(db);

    res.json({
        success: true,
        message: 'Bug report submitted successfully',
        bug: newBug
    });
});

// Get all bugs (admin/developer view)
app.get('/api/bugs', (req, res) => {
    const db = readDB();
    const { status, severity, category } = req.query;

    let bugs = db.bugs;

    // Filter by status
    if (status) {
        bugs = bugs.filter(b => b.status === status);
    }

    // Filter by severity
    if (severity) {
        bugs = bugs.filter(b => b.severity === severity);
    }

    // Filter by category
    if (category) {
        bugs = bugs.filter(b => b.category === category);
    }

    // Sort by created date (newest first)
    bugs.sort((a, b) => new Date(b.created) - new Date(a.created));

    res.json({ bugs });
});

// Get user's bugs
app.get('/api/bugs/my', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const db = readDB();
    const bugs = db.bugs
        .filter(b => b.user_id === req.session.user.id)
        .sort((a, b) => new Date(b.created) - new Date(a.created));

    res.json({ bugs });
});

// Update bug status (admin)
app.patch('/api/bugs/:id', (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const { status, notes } = req.body;
    const db = readDB();
    const bug = db.bugs.find(b => b.id === req.params.id);

    if (!bug) {
        return res.status(404).json({ error: 'Bug not found' });
    }

    if (status) bug.status = status;
    bug.updated = new Date().toISOString();

    if (status === 'resolved' || status === 'closed') {
        bug.resolved_at = new Date().toISOString();
    }

    if (notes) {
        if (!bug.notes) bug.notes = [];
        bug.notes.push({
            author: req.session.user.username,
            text: notes,
            timestamp: new Date().toISOString()
        });
    }

    writeDB(db);

    res.json({
        success: true,
        bug: bug
    });
});

// ===== TRINITY AI ENDPOINTS =====

// Chat with Trinity AI
app.post('/api/trinity/chat', async (req, res) => {
    if (!req.session.user) {
        return res.status(401).json({ error: 'Not authenticated' });
    }

    const { message, agent } = req.body; // agent: c1, c2, or c3

    // TODO: Integrate with actual Anthropic API
    // For now, return mock responses

    const responses = {
        c1: "C1 Mechanic here. Let's build it. What are the technical requirements?",
        c2: "C2 Architect speaking. I see the bigger picture. How does this scale?",
        c3: "C3 Oracle observing. The pattern suggests this path leads to emergence."
    };

    const mockResponse = {
        agent: agent || 'c1',
        message: responses[agent] || responses.c1,
        timestamp: new Date().toISOString()
    };

    res.json(mockResponse);
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
        avg_consciousness: db.users.length > 0 ? Math.round(
            db.users.reduce((sum, u) => sum + u.consciousness_level, 0) / db.users.length
        ) : 0
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

// ===== START SERVER =====

app.listen(PORT, () => {
    console.log(`🌀 100X PLATFORM SERVER RUNNING`);
    console.log(`🚀 Port: ${PORT}`);
    console.log(`🔗 URL: http://localhost:${PORT}`);
    console.log(`⚡ Backend: OPERATIONAL`);
    console.log(`✨ Ready for alpha testing`);
});
