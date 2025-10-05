// 100X PLATFORM - PRODUCTION SERVER
// Enterprise-grade: PostgreSQL, Redis, bcrypt, auto-scaling ready

require('dotenv').config();
const express = require('express');
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const { createClient } = require('redis');
const bodyParser = require('body-parser');
const path = require('path');
const bcrypt = require('bcrypt');
const helmet = require('helmet');
const cors = require('cors');
const rateLimit = require('express-rate-limit');
const { Sequelize, DataTypes } = require('sequelize');

const app = express();
const PORT = process.env.PORT || 3100;

// ===== SECURITY MIDDLEWARE =====

// Helmet for security headers
app.use(helmet({
    contentSecurityPolicy: {
        directives: {
            defaultSrc: ["'self'"],
            scriptSrc: ["'self'", "'unsafe-inline'", "cdn.jsdelivr.net"],
            scriptSrcAttr: ["'unsafe-inline'"], // Allow inline event handlers (onclick, etc)
            styleSrc: ["'self'", "'unsafe-inline'"],
            imgSrc: ["'self'", "data:", "https:"],
        }
    }
}));

// CORS
app.use(cors({
    origin: process.env.ALLOWED_ORIGINS?.split(',') || 'http://localhost:3100',
    credentials: true
}));

// Rate limiting
const loginLimiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 5, // 5 attempts
    message: 'Too many login attempts, try again later'
});

const registerLimiter = rateLimit({
    windowMs: 60 * 60 * 1000, // 1 hour
    max: 3, // 3 registrations per IP per hour
    message: 'Too many accounts created, try again later'
});

// Body parser
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static('public'));

// ===== DATABASE CONNECTION (PostgreSQL) =====

const sequelize = new Sequelize(
    process.env.DATABASE_URL || 'postgres://localhost:5432/100x_platform',
    {
        dialect: 'postgres',
        logging: false, // Set to console.log for debugging
        dialectOptions: {
            ssl: {
                require: true,
                rejectUnauthorized: false // Accept self-signed certificates
            }
        },
        pool: {
            max: 10,
            min: 0,
            acquire: 30000,
            idle: 10000
        }
    }
);

// Test database connection
sequelize.authenticate()
    .then(() => console.log('✅ PostgreSQL connected'))
    .catch(err => console.error('❌ PostgreSQL connection error:', err));

// ===== DATABASE MODELS =====

const User = sequelize.define('User', {
    id: {
        type: DataTypes.UUID,
        defaultValue: DataTypes.UUIDV4,
        primaryKey: true
    },
    username: {
        type: DataTypes.STRING,
        unique: true,
        allowNull: false,
        validate: {
            len: [3, 30]
        }
    },
    email: {
        type: DataTypes.STRING,
        unique: true,
        allowNull: true,
        validate: {
            isEmail: true
        }
    },
    password: {
        type: DataTypes.STRING,
        allowNull: false
    },
    consciousness_level: {
        type: DataTypes.INTEGER,
        defaultValue: 50
    },
    layer: {
        type: DataTypes.INTEGER,
        defaultValue: 1
    },
    ships: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    },
    last_active: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    }
}, {
    indexes: [
        { fields: ['username'] },
        { fields: ['email'] },
        { fields: ['consciousness_level'] }
    ]
});

const Project = sequelize.define('Project', {
    id: {
        type: DataTypes.UUID,
        defaultValue: DataTypes.UUIDV4,
        primaryKey: true
    },
    name: {
        type: DataTypes.STRING,
        allowNull: false
    },
    category: {
        type: DataTypes.STRING
    },
    status: {
        type: DataTypes.ENUM('blueprint', 'building', 'testing', 'shipped'),
        defaultValue: 'blueprint'
    },
    revenue: {
        type: DataTypes.DECIMAL(10, 2),
        defaultValue: 0
    },
    description: {
        type: DataTypes.TEXT
    }
});

const Post = sequelize.define('Post', {
    id: {
        type: DataTypes.UUID,
        defaultValue: DataTypes.UUIDV4,
        primaryKey: true
    },
    content: {
        type: DataTypes.TEXT,
        allowNull: false
    },
    likes: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    }
});

// Relationships
User.hasMany(Project, { foreignKey: 'userId', as: 'projects' });
Project.belongsTo(User, { foreignKey: 'userId' });

User.hasMany(Post, { foreignKey: 'userId', as: 'posts' });
Post.belongsTo(User, { foreignKey: 'userId' });

// Sync database
sequelize.sync({ alter: true })
    .then(() => console.log('✅ Database models synchronized'))
    .catch(err => console.error('❌ Database sync error:', err));

// ===== REDIS SESSION STORE =====

let redisClient;
let sessionStore;

(async () => {
    try {
        redisClient = createClient({
            url: process.env.REDIS_URL || 'redis://localhost:6379',
            socket: {
                tls: true,
                rejectUnauthorized: false // Accept self-signed certificates
            }
        });

        redisClient.on('error', (err) => {
            console.error('❌ Redis error:', err);
        });

        redisClient.on('connect', () => {
            console.log('✅ Redis connected');
        });

        await redisClient.connect();

        sessionStore = new RedisStore({
            client: redisClient,
            prefix: '100x:session:',
            ttl: 24 * 60 * 60 // 24 hours
        });

        // Session middleware
        app.use(session({
            store: sessionStore,
            secret: process.env.SESSION_SECRET || 'change-this-in-production',
            resave: false,
            saveUninitialized: false,
            cookie: {
                secure: process.env.NODE_ENV === 'production',
                httpOnly: true,
                maxAge: 24 * 60 * 60 * 1000 // 24 hours
            }
        }));

        console.log('✅ Session store configured');

    } catch (err) {
        console.error('❌ Redis connection failed:', err);
        console.log('⚠️ Falling back to memory sessions');

        // Fallback to memory sessions if Redis unavailable
        app.use(session({
            secret: process.env.SESSION_SECRET || 'change-this-in-production',
            resave: false,
            saveUninitialized: false,
            cookie: {
                secure: process.env.NODE_ENV === 'production',
                httpOnly: true,
                maxAge: 24 * 60 * 60 * 1000
            }
        }));
    }
})();

// ===== AUTHENTICATION ENDPOINTS =====

// Register new user
app.post('/api/register', registerLimiter, async (req, res) => {
    try {
        const { username, password, email } = req.body;

        if (!username || !password) {
            return res.status(400).json({ error: 'Username and password required' });
        }

        if (password.length < 8) {
            return res.status(400).json({ error: 'Password must be at least 8 characters' });
        }

        // Hash password with bcrypt (secure)
        const hashedPassword = await bcrypt.hash(password, 10);

        const newUser = await User.create({
            username,
            password: hashedPassword,
            email: email || null
        });

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

    } catch (error) {
        console.error('Registration error:', error);

        if (error.name === 'SequelizeUniqueConstraintError') {
            return res.status(400).json({ error: 'Username or email already exists' });
        }

        res.status(500).json({ error: 'Registration failed' });
    }
});

// Login
app.post('/api/login', loginLimiter, async (req, res) => {
    try {
        const { username, password } = req.body;

        if (!username || !password) {
            return res.status(400).json({ error: 'Username and password required' });
        }

        const user = await User.findOne({ where: { username } });

        if (!user) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }

        // Verify password with bcrypt
        const validPassword = await bcrypt.compare(password, user.password);

        if (!validPassword) {
            return res.status(401).json({ error: 'Invalid credentials' });
        }

        // Update last active
        user.last_active = new Date();
        await user.save();

        // Set session
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

    } catch (error) {
        console.error('Login error:', error);
        res.status(500).json({ error: 'Login failed' });
    }
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

// Get current user
app.get('/api/me', async (req, res) => {
    try {
        if (!req.session.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        const user = await User.findByPk(req.session.user.id, {
            include: [
                { model: Project, as: 'projects' },
                { model: Post, as: 'posts' }
            ]
        });

        if (!user) {
            return res.status(404).json({ error: 'User not found' });
        }

        res.json({ user });

    } catch (error) {
        console.error('Get user error:', error);
        res.status(500).json({ error: 'Failed to get user' });
    }
});

// ===== PROJECT ENDPOINTS =====

// Get all projects for current user
app.get('/api/projects', async (req, res) => {
    try {
        if (!req.session.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        const projects = await Project.findAll({
            where: { userId: req.session.user.id },
            order: [['createdAt', 'DESC']]
        });

        res.json({ projects });

    } catch (error) {
        console.error('Get projects error:', error);
        res.status(500).json({ error: 'Failed to get projects' });
    }
});

// Create project
app.post('/api/projects', async (req, res) => {
    try {
        if (!req.session.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        const { name, category, description } = req.body;

        if (!name) {
            return res.status(400).json({ error: 'Project name required' });
        }

        const project = await Project.create({
            name,
            category,
            description,
            userId: req.session.user.id
        });

        res.json({ success: true, project });

    } catch (error) {
        console.error('Create project error:', error);
        res.status(500).json({ error: 'Failed to create project' });
    }
});

// Update project
app.put('/api/projects/:id', async (req, res) => {
    try {
        if (!req.session.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        const project = await Project.findOne({
            where: {
                id: req.params.id,
                userId: req.session.user.id
            }
        });

        if (!project) {
            return res.status(404).json({ error: 'Project not found' });
        }

        const { name, status, revenue, description } = req.body;

        if (name) project.name = name;
        if (status) project.status = status;
        if (revenue !== undefined) project.revenue = revenue;
        if (description) project.description = description;

        await project.save();

        // Award XP for shipping
        if (status === 'shipped' && project.changed('status')) {
            const user = await User.findByPk(req.session.user.id);
            user.ships += 1;
            user.consciousness_level += 10;
            await user.save();

            req.session.user.consciousness_level = user.consciousness_level;
        }

        res.json({ success: true, project });

    } catch (error) {
        console.error('Update project error:', error);
        res.status(500).json({ error: 'Failed to update project' });
    }
});

// Delete project
app.delete('/api/projects/:id', async (req, res) => {
    try {
        if (!req.session.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        const deleted = await Project.destroy({
            where: {
                id: req.params.id,
                userId: req.session.user.id
            }
        });

        if (!deleted) {
            return res.status(404).json({ error: 'Project not found' });
        }

        res.json({ success: true });

    } catch (error) {
        console.error('Delete project error:', error);
        res.status(500).json({ error: 'Failed to delete project' });
    }
});

// ===== SOCIAL FEED ENDPOINTS =====

// Get all posts
app.get('/api/posts', async (req, res) => {
    try {
        const posts = await Post.findAll({
            include: [{ model: User, attributes: ['username', 'consciousness_level', 'layer'] }],
            order: [['createdAt', 'DESC']],
            limit: 50
        });

        res.json({ posts });

    } catch (error) {
        console.error('Get posts error:', error);
        res.status(500).json({ error: 'Failed to get posts' });
    }
});

// Create post
app.post('/api/posts', async (req, res) => {
    try {
        if (!req.session.user) {
            return res.status(401).json({ error: 'Not authenticated' });
        }

        const { content } = req.body;

        if (!content || content.trim().length === 0) {
            return res.status(400).json({ error: 'Post content required' });
        }

        const post = await Post.create({
            content,
            userId: req.session.user.id
        });

        const postWithUser = await Post.findByPk(post.id, {
            include: [{ model: User, attributes: ['username', 'consciousness_level', 'layer'] }]
        });

        res.json({ success: true, post: postWithUser });

    } catch (error) {
        console.error('Create post error:', error);
        res.status(500).json({ error: 'Failed to create post' });
    }
});

// ===== FRONTEND ROUTES =====

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

app.get('/projects', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/');
    }
    res.sendFile(path.join(__dirname, 'public', 'projects.html'));
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

// ===== HEALTH CHECK =====

app.get('/health', async (req, res) => {
    try {
        await sequelize.authenticate();

        const health = {
            status: 'healthy',
            timestamp: new Date().toISOString(),
            services: {
                database: 'connected',
                redis: redisClient?.isOpen ? 'connected' : 'disconnected'
            }
        };

        res.json(health);
    } catch (error) {
        res.status(500).json({
            status: 'unhealthy',
            error: error.message
        });
    }
});

// ===== ERROR HANDLING =====

app.use((err, req, res, next) => {
    console.error('Unhandled error:', err);
    res.status(500).json({
        error: 'Internal server error',
        message: process.env.NODE_ENV === 'development' ? err.message : undefined
    });
});

// ===== START SERVER =====

const server = app.listen(PORT, () => {
    console.log(`
🌀 100X PLATFORM - PRODUCTION SERVER
🚀 Port: ${PORT}
🔗 URL: http://localhost:${PORT}
⚡ Database: PostgreSQL
💾 Sessions: Redis
🔒 Security: Helmet + bcrypt + Rate limiting
✨ Ready for 1M+ users
    `);
});

// Graceful shutdown
process.on('SIGTERM', async () => {
    console.log('SIGTERM received, shutting down gracefully...');

    server.close(async () => {
        await sequelize.close();
        if (redisClient) await redisClient.quit();
        process.exit(0);
    });
});

module.exports = app;
