/**
 * KNOWLEDGE SCRAPER MODULE
 *
 * Pulls real knowledge from the internet to feed Araya AI
 * Sources: GitHub, Stack Overflow, Documentation, News, Research
 */

const https = require('https');
const http = require('http');
const fs = require('fs');

class KnowledgeScraper {
    constructor() {
        this.knowledgeBase = [];
        this.sources = {
            github: 'https://api.github.com',
            stackoverflow: 'https://api.stackexchange.com/2.3',
            news: 'https://www.reddit.com/r/programming/.json',
            consciousness: 'https://www.reddit.com/r/consciousness/.json',
            ai: 'https://www.reddit.com/r/artificial/.json'
        };
    }

    // Fetch data from URL
    async fetchData(url) {
        return new Promise((resolve, reject) => {
            const client = url.startsWith('https') ? https : http;

            const options = {
                headers: {
                    'User-Agent': 'Cyclotron-Knowledge-Engine/1.0'
                }
            };

            client.get(url, options, (res) => {
                let data = '';

                res.on('data', (chunk) => {
                    data += chunk;
                });

                res.on('end', () => {
                    try {
                        resolve(JSON.parse(data));
                    } catch (e) {
                        resolve(data);
                    }
                });
            }).on('error', (err) => {
                reject(err);
            });
        });
    }

    // Scrape GitHub trending repositories
    async scrapeGitHub() {
        try {
            // Search for ARAYA-specific topics: computer control, screen vision, AI automation
            const queries = [
                'computer+control+AI+automation',
                'screen+vision+AI+assistant',
                'consciousness+AI+language:javascript'
            ];

            const query = queries[Math.floor(Math.random() * queries.length)];
            const url = `${this.sources.github}/search/repositories?q=${query}&sort=stars&order=desc&per_page=10`;

            const data = await this.fetchData(url);

            if (data.items && data.items.length > 0) {
                return data.items.map(repo => ({
                    type: 'github_repo',
                    title: repo.name,
                    description: repo.description || 'No description',
                    url: repo.html_url,
                    stars: repo.stargazers_count,
                    language: repo.language,
                    topics: repo.topics || [],
                    timestamp: new Date().toISOString()
                }));
            }
        } catch (error) {
            console.error('GitHub scrape error:', error.message);
        }
        return [];
    }

    // Scrape Reddit for consciousness/AI discussions
    async scrapeReddit(subreddit = 'programming') {
        try {
            const url = `https://www.reddit.com/r/${subreddit}/hot.json?limit=20`;
            const data = await this.fetchData(url);

            if (data.data && data.data.children) {
                return data.data.children
                    .filter(post => post.data.score > 100) // Only popular posts
                    .slice(0, 5)
                    .map(post => ({
                        type: 'reddit_post',
                        subreddit: subreddit,
                        title: post.data.title,
                        description: post.data.selftext?.substring(0, 200) || 'Discussion thread',
                        url: `https://reddit.com${post.data.permalink}`,
                        score: post.data.score,
                        comments: post.data.num_comments,
                        timestamp: new Date().toISOString()
                    }));
            }
        } catch (error) {
            console.error(`Reddit scrape error (${subreddit}):`, error.message);
        }
        return [];
    }

    // Scrape Stack Overflow for AI/programming questions
    async scrapeStackOverflow() {
        try {
            const tags = 'artificial-intelligence;javascript;node.js';
            const url = `${this.sources.stackoverflow}/questions?order=desc&sort=votes&tagged=${tags}&site=stackoverflow&pagesize=10`;

            const data = await this.fetchData(url);

            if (data.items && data.items.length > 0) {
                return data.items.map(question => ({
                    type: 'stackoverflow_question',
                    title: question.title,
                    description: question.body?.substring(0, 200) || 'Technical question',
                    url: question.link,
                    score: question.score,
                    answers: question.answer_count,
                    views: question.view_count,
                    tags: question.tags || [],
                    timestamp: new Date().toISOString()
                }));
            }
        } catch (error) {
            console.error('StackOverflow scrape error:', error.message);
        }
        return [];
    }

    // Get tech news and updates
    async getTechNews() {
        try {
            const sources = [
                { name: 'programming', category: 'Programming' },
                { name: 'artificial', category: 'AI' },
                { name: 'consciousness', category: 'Consciousness' },
                { name: 'MachineLearning', category: 'ML' },
                { name: 'computervision', category: 'Computer Vision' }
            ];

            const allNews = [];

            for (const source of sources) {
                const news = await this.scrapeReddit(source.name);
                allNews.push(...news.map(n => ({ ...n, category: source.category })));
            }

            return allNews;
        } catch (error) {
            console.error('Tech news scrape error:', error.message);
        }
        return [];
    }

    // Main knowledge gathering function
    async gatherKnowledge() {
        console.log('🔍 Gathering knowledge from the internet...');

        const knowledge = {
            github_repos: [],
            discussions: [],
            stackoverflow: [],
            news: [],
            gathered_at: new Date().toISOString()
        };

        try {
            // Parallel fetching for speed
            const [github, news, stackoverflow] = await Promise.all([
                this.scrapeGitHub(),
                this.getTechNews(),
                this.scrapeStackOverflow()
            ]);

            knowledge.github_repos = github;
            knowledge.news = news;
            knowledge.stackoverflow = stackoverflow;

            // Calculate total atoms
            const totalAtoms = github.length + news.length + stackoverflow.length;

            console.log(`✅ Gathered ${totalAtoms} knowledge atoms:`);
            console.log(`   - ${github.length} GitHub repositories`);
            console.log(`   - ${news.length} discussions/news`);
            console.log(`   - ${stackoverflow.length} Stack Overflow Q&A`);

            return { knowledge, atoms: totalAtoms };
        } catch (error) {
            console.error('Knowledge gathering error:', error);
            return { knowledge, atoms: 0 };
        }
    }

    // Extract key insights for Araya
    extractInsights(knowledge) {
        const insights = [];

        // From GitHub
        if (knowledge.github_repos) {
            knowledge.github_repos.forEach(repo => {
                insights.push({
                    source: 'GitHub',
                    type: 'Repository',
                    title: repo.title,
                    insight: `Popular ${repo.language} project: ${repo.description}`,
                    relevance: repo.stars,
                    url: repo.url
                });
            });
        }

        // From discussions
        if (knowledge.news) {
            knowledge.news.slice(0, 5).forEach(post => {
                insights.push({
                    source: post.subreddit,
                    type: 'Discussion',
                    title: post.title,
                    insight: post.description,
                    relevance: post.score,
                    url: post.url
                });
            });
        }

        // From Stack Overflow
        if (knowledge.stackoverflow) {
            knowledge.stackoverflow.forEach(question => {
                insights.push({
                    source: 'Stack Overflow',
                    type: 'Q&A',
                    title: question.title,
                    insight: question.description,
                    relevance: question.score,
                    url: question.url
                });
            });
        }

        return insights;
    }

    // Save knowledge to file
    saveKnowledge(knowledge, filename = 'araya_knowledge.json') {
        try {
            const existing = this.loadKnowledge(filename);

            // Merge new knowledge with existing
            const merged = {
                last_update: new Date().toISOString(),
                total_sessions: (existing.total_sessions || 0) + 1,
                github_repos: [...(existing.github_repos || []), ...knowledge.github_repos],
                news: [...(existing.news || []), ...knowledge.news],
                stackoverflow: [...(existing.stackoverflow || []), ...knowledge.stackoverflow],
                insights: this.extractInsights(knowledge)
            };

            // Keep only recent items (last 100 per category)
            merged.github_repos = merged.github_repos.slice(-100);
            merged.news = merged.news.slice(-100);
            merged.stackoverflow = merged.stackoverflow.slice(-100);

            fs.writeFileSync(filename, JSON.stringify(merged, null, 2));
            console.log(`💾 Knowledge saved to ${filename}`);
            return merged;
        } catch (error) {
            console.error('Error saving knowledge:', error);
            return knowledge;
        }
    }

    // Load existing knowledge
    loadKnowledge(filename = 'araya_knowledge.json') {
        try {
            if (fs.existsSync(filename)) {
                const data = fs.readFileSync(filename, 'utf8');
                return JSON.parse(data);
            }
        } catch (error) {
            console.error('Error loading knowledge:', error);
        }
        return {};
    }
}

// Export
module.exports = KnowledgeScraper;

// CLI interface
if (require.main === module) {
    const scraper = new KnowledgeScraper();

    console.log('🌐 Starting knowledge gathering...\n');

    scraper.gatherKnowledge().then(result => {
        console.log(`\n✅ Total atoms gathered: ${result.atoms}`);

        const saved = scraper.saveKnowledge(result.knowledge);

        console.log('\n📊 Knowledge Summary:');
        console.log(`   Total sessions: ${saved.total_sessions}`);
        console.log(`   GitHub repos: ${saved.github_repos.length}`);
        console.log(`   Discussions: ${saved.news.length}`);
        console.log(`   Q&A: ${saved.stackoverflow.length}`);

        console.log('\n🧠 Ready for Araya AI consumption!');
    });
}
