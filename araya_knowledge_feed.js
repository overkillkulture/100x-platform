/**
 * ARAYA KNOWLEDGE FEED
 *
 * Integrates Cyclotron knowledge into Araya AI's context
 * Provides methods for Araya to query and consume accumulated knowledge atoms
 */

const fs = require('fs');
const path = require('path');

class ArayaKnowledgeFeed {
    constructor(knowledgePath = './araya_knowledge.json') {
        this.knowledgePath = knowledgePath;
    }

    // Load all accumulated knowledge
    loadKnowledge() {
        try {
            if (fs.existsSync(this.knowledgePath)) {
                const data = fs.readFileSync(this.knowledgePath, 'utf8');
                return JSON.parse(data);
            }
        } catch (error) {
            console.error('Error loading Araya knowledge:', error);
        }
        return null;
    }

    // Get recent knowledge (last N items)
    getRecentKnowledge(limit = 10) {
        const knowledge = this.loadKnowledge();
        if (!knowledge) return [];

        const recent = [];

        // Get recent GitHub repos
        if (knowledge.github_repos) {
            recent.push(...knowledge.github_repos
                .slice(-limit)
                .map(repo => ({
                    type: 'github',
                    title: repo.title,
                    description: repo.description,
                    url: repo.url,
                    stars: repo.stars,
                    language: repo.language,
                    relevance: 'high'
                }))
            );
        }

        // Get recent discussions
        if (knowledge.news) {
            recent.push(...knowledge.news
                .slice(-limit)
                .map(post => ({
                    type: 'discussion',
                    title: post.title,
                    description: post.description,
                    url: post.url,
                    score: post.score,
                    category: post.category || post.subreddit,
                    relevance: 'medium'
                }))
            );
        }

        // Get recent Q&A
        if (knowledge.stackoverflow) {
            recent.push(...knowledge.stackoverflow
                .slice(-limit)
                .map(q => ({
                    type: 'qa',
                    title: q.title,
                    description: q.description,
                    url: q.url,
                    score: q.score,
                    answers: q.answers,
                    relevance: 'high'
                }))
            );
        }

        return recent;
    }

    // Search knowledge by keyword
    searchKnowledge(keyword) {
        const knowledge = this.loadKnowledge();
        if (!knowledge) return [];

        const results = [];
        const searchTerm = keyword.toLowerCase();

        // Search GitHub repos
        if (knowledge.github_repos) {
            knowledge.github_repos.forEach(repo => {
                if (repo.title.toLowerCase().includes(searchTerm) ||
                    repo.description?.toLowerCase().includes(searchTerm) ||
                    repo.topics?.some(t => t.toLowerCase().includes(searchTerm))) {
                    results.push({
                        type: 'github',
                        title: repo.title,
                        description: repo.description,
                        url: repo.url,
                        stars: repo.stars,
                        match: 'keyword'
                    });
                }
            });
        }

        // Search discussions
        if (knowledge.news) {
            knowledge.news.forEach(post => {
                if (post.title.toLowerCase().includes(searchTerm) ||
                    post.description?.toLowerCase().includes(searchTerm)) {
                    results.push({
                        type: 'discussion',
                        title: post.title,
                        description: post.description,
                        url: post.url,
                        score: post.score,
                        match: 'keyword'
                    });
                }
            });
        }

        return results;
    }

    // Get knowledge by category
    getKnowledgeByCategory(category) {
        const knowledge = this.loadKnowledge();
        if (!knowledge) return [];

        const categoryMap = {
            'code': knowledge.github_repos || [],
            'discussions': knowledge.news || [],
            'qa': knowledge.stackoverflow || [],
            'all': [
                ...(knowledge.github_repos || []),
                ...(knowledge.news || []),
                ...(knowledge.stackoverflow || [])
            ]
        };

        return categoryMap[category] || [];
    }

    // Get knowledge insights
    getInsights() {
        const knowledge = this.loadKnowledge();
        if (!knowledge) return [];

        return knowledge.insights || [];
    }

    // Get knowledge statistics
    getStats() {
        const knowledge = this.loadKnowledge();
        if (!knowledge) return null;

        return {
            total_sessions: knowledge.total_sessions || 0,
            total_github_repos: knowledge.github_repos?.length || 0,
            total_discussions: knowledge.news?.length || 0,
            total_qa: knowledge.stackoverflow?.length || 0,
            total_insights: knowledge.insights?.length || 0,
            last_update: knowledge.last_update || 'unknown',
            total_knowledge_atoms: (knowledge.github_repos?.length || 0) +
                                   (knowledge.news?.length || 0) +
                                   (knowledge.stackoverflow?.length || 0)
        };
    }

    // Generate context summary for Araya AI
    generateContextSummary(maxItems = 20) {
        const knowledge = this.loadKnowledge();
        if (!knowledge) return "No knowledge available.";

        const stats = this.getStats();
        const recent = this.getRecentKnowledge(maxItems);

        let summary = `ARAYA KNOWLEDGE BASE SUMMARY:\n\n`;
        summary += `Total Knowledge Atoms: ${stats.total_knowledge_atoms}\n`;
        summary += `Sessions: ${stats.total_sessions}\n`;
        summary += `Last Updated: ${stats.last_update}\n\n`;

        summary += `KNOWLEDGE BREAKDOWN:\n`;
        summary += `- GitHub Repos: ${stats.total_github_repos}\n`;
        summary += `- Discussions: ${stats.total_discussions}\n`;
        summary += `- Q&A: ${stats.total_qa}\n`;
        summary += `- Insights: ${stats.total_insights}\n\n`;

        summary += `RECENT KNOWLEDGE (Last ${maxItems} atoms):\n\n`;

        recent.slice(0, maxItems).forEach((item, index) => {
            summary += `${index + 1}. [${item.type.toUpperCase()}] ${item.title}\n`;
            if (item.description && item.description !== 'Discussion thread' && item.description !== 'Technical question') {
                summary += `   ${item.description.substring(0, 100)}${item.description.length > 100 ? '...' : ''}\n`;
            }
            summary += `   URL: ${item.url}\n\n`;
        });

        return summary;
    }

    // Export knowledge as JSON for AI consumption
    exportForAI(format = 'full') {
        const knowledge = this.loadKnowledge();
        if (!knowledge) return null;

        if (format === 'summary') {
            return {
                stats: this.getStats(),
                insights: this.getInsights(),
                recent: this.getRecentKnowledge(20)
            };
        }

        return knowledge; // full export
    }
}

// Export
module.exports = ArayaKnowledgeFeed;

// CLI interface
if (require.main === module) {
    const feed = new ArayaKnowledgeFeed();

    const command = process.argv[2];

    switch (command) {
        case 'stats':
            console.log(JSON.stringify(feed.getStats(), null, 2));
            break;
        case 'recent':
            const limit = parseInt(process.argv[3]) || 10;
            console.log(JSON.stringify(feed.getRecentKnowledge(limit), null, 2));
            break;
        case 'search':
            const keyword = process.argv[3];
            console.log(JSON.stringify(feed.searchKnowledge(keyword), null, 2));
            break;
        case 'summary':
            console.log(feed.generateContextSummary());
            break;
        case 'insights':
            console.log(JSON.stringify(feed.getInsights(), null, 2));
            break;
        default:
            console.log(`
ARAYA KNOWLEDGE FEED - CLI
Usage:
  node araya_knowledge_feed.js stats     - Show knowledge statistics
  node araya_knowledge_feed.js recent 10 - Show recent 10 items
  node araya_knowledge_feed.js search AI - Search for keyword
  node araya_knowledge_feed.js summary   - Generate context summary
  node araya_knowledge_feed.js insights  - Show extracted insights
            `);
    }
}
