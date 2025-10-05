// 🪙 CRYPTO NEWS AGGREGATOR - Learn Token Economics
// Purpose: Study how crypto projects distribute value to inform BUILDER token design

const axios = require('axios');
const Parser = require('rss-parser');
const fs = require('fs').promises;

const parser = new Parser({
    customFields: {
        item: ['description', 'content', 'content:encoded']
    }
});

// Crypto news RSS feeds
const CRYPTO_NEWS_FEEDS = [
    'https://cointelegraph.com/rss',
    'https://decrypt.co/feed',
    'https://www.coindesk.com/arc/outboundfeeds/rss/',
    'https://cryptoslate.com/feed/',
    'https://thedefiant.io/feed/'
];

// Keywords to identify tokenomics articles
const TOKENOMICS_KEYWORDS = [
    'staking', 'rewards', 'airdrop', 'token', 'tokenomics',
    'distribution', 'yield', 'APY', 'revenue share', 'dividend',
    'burn', 'buyback', 'governance', 'DAO', 'liquidity'
];

// Pattern database: How crypto projects pay users
const PAYOUT_PATTERNS = {
    staking: {
        description: 'Lock tokens to earn rewards',
        examples: ['Ethereum', 'Cardano', 'Polkadot'],
        applyTo100X: 'Stake BLD tokens → Earn platform revenue share'
    },
    profitSharing: {
        description: 'Distribute protocol fees to token holders',
        examples: ['GMX', 'dYdX', 'Synthetix'],
        applyTo100X: 'BLD holders get % of subscription revenue'
    },
    tokenBurns: {
        description: 'Buy back and burn tokens to reduce supply',
        examples: ['BNB', 'ETH (EIP-1559)', 'MKR'],
        applyTo100X: 'Use profit to buy + burn BLD quarterly'
    },
    airdrops: {
        description: 'Free token distribution to early users',
        examples: ['Uniswap', 'Optimism', 'Arbitrum'],
        applyTo100X: 'First 100 builders get BLD airdrop'
    },
    governanceMining: {
        description: 'Earn tokens by participating in governance',
        examples: ['Curve', 'Compound'],
        applyTo100X: 'Vote on features → Earn bonus BLD'
    },
    liquidityMining: {
        description: 'Provide liquidity to earn token rewards',
        examples: ['Uniswap', 'SushiSwap', 'PancakeSwap'],
        applyTo100X: 'Provide BLD/ETH liquidity → Earn fees + bonus BLD'
    }
};

// Fetch and parse all crypto news feeds
async function aggregateCryptoNews() {
    console.log('📰 Fetching crypto news from multiple sources...\n');

    const allArticles = [];

    for (const feedUrl of CRYPTO_NEWS_FEEDS) {
        try {
            console.log(`Fetching: ${feedUrl}`);
            const feed = await parser.parseURL(feedUrl);

            for (const item of feed.items) {
                const content = item.content || item['content:encoded'] || item.description || '';
                const fullText = `${item.title} ${content}`.toLowerCase();

                // Check if article mentions tokenomics
                const hasTokenomics = TOKENOMICS_KEYWORDS.some(keyword =>
                    fullText.includes(keyword)
                );

                if (hasTokenomics) {
                    allArticles.push({
                        title: item.title,
                        url: item.link,
                        pubDate: item.pubDate,
                        source: new URL(feedUrl).hostname,
                        content: content.substring(0, 500) + '...', // First 500 chars
                        keywords: extractKeywords(fullText)
                    });
                }
            }

            console.log(`✅ Found ${feed.items.length} articles\n`);

        } catch (error) {
            console.error(`❌ Error fetching ${feedUrl}:`, error.message);
        }
    }

    return allArticles;
}

// Extract relevant keywords from article
function extractKeywords(text) {
    const found = [];
    for (const keyword of TOKENOMICS_KEYWORDS) {
        if (text.includes(keyword)) {
            found.push(keyword);
        }
    }
    return found;
}

// Analyze articles for payout mechanisms
function analyzePayoutMechanisms(articles) {
    console.log('\n🔍 Analyzing payout mechanisms...\n');

    const insights = {
        total: articles.length,
        byPattern: {},
        projects: [],
        lessons: []
    };

    // Count pattern mentions
    for (const pattern in PAYOUT_PATTERNS) {
        insights.byPattern[pattern] = 0;
    }

    for (const article of articles) {
        const text = `${article.title} ${article.content}`.toLowerCase();

        // Detect which payout pattern is mentioned
        if (text.includes('staking') || text.includes('stake')) {
            insights.byPattern.staking++;
            insights.projects.push({
                title: article.title,
                pattern: 'Staking Rewards',
                url: article.url
            });
        }

        if (text.includes('airdrop')) {
            insights.byPattern.airdrops++;
            insights.projects.push({
                title: article.title,
                pattern: 'Airdrop',
                url: article.url
            });
        }

        if (text.includes('burn') || text.includes('buyback')) {
            insights.byPattern.tokenBurns++;
            insights.projects.push({
                title: article.title,
                pattern: 'Token Burns',
                url: article.url
            });
        }

        if (text.includes('revenue share') || text.includes('profit share') || text.includes('dividend')) {
            insights.byPattern.profitSharing++;
            insights.projects.push({
                title: article.title,
                pattern: 'Profit Sharing',
                url: article.url
            });
        }

        if (text.includes('governance') || text.includes('voting')) {
            insights.byPattern.governanceMining++;
            insights.projects.push({
                title: article.title,
                pattern: 'Governance',
                url: article.url
            });
        }

        if (text.includes('liquidity mining') || text.includes('LP rewards')) {
            insights.byPattern.liquidityMining++;
            insights.projects.push({
                title: article.title,
                pattern: 'Liquidity Mining',
                url: article.url
            });
        }
    }

    return insights;
}

// Generate lessons for BUILDER token
function generateLessons(insights) {
    const lessons = [];

    // Most popular pattern = proven model
    const sortedPatterns = Object.entries(insights.byPattern)
        .sort((a, b) => b[1] - a[1]);

    console.log('\n📊 PAYOUT PATTERN FREQUENCY:\n');
    for (const [pattern, count] of sortedPatterns) {
        const percentage = ((count / insights.total) * 100).toFixed(1);
        console.log(`${pattern}: ${count} mentions (${percentage}%)`);

        if (count > 0) {
            lessons.push({
                pattern: pattern,
                frequency: count,
                percentage: percentage,
                recommendation: PAYOUT_PATTERNS[pattern]?.applyTo100X || 'Study further'
            });
        }
    }

    return lessons;
}

// Save results to file
async function saveResults(articles, insights, lessons) {
    const timestamp = new Date().toISOString().split('T')[0];

    const report = {
        generatedAt: new Date().toISOString(),
        summary: {
            totalArticles: articles.length,
            patternCounts: insights.byPattern,
            topPatterns: lessons.slice(0, 5)
        },
        articles: articles.slice(0, 20), // Top 20 most recent
        projects: insights.projects.slice(0, 30), // Top 30 project mentions
        lessons: lessons,
        patternDatabase: PAYOUT_PATTERNS
    };

    const filename = `crypto_tokenomics_report_${timestamp}.json`;
    await fs.writeFile(filename, JSON.stringify(report, null, 2));

    console.log(`\n💾 Report saved to: ${filename}`);

    return report;
}

// Display key findings
function displayFindings(report) {
    console.log('\n' + '='.repeat(80));
    console.log('📈 KEY FINDINGS FOR BUILDER TOKEN DESIGN');
    console.log('='.repeat(80) + '\n');

    console.log('🏆 TOP 3 MOST POPULAR PAYOUT MECHANISMS:\n');

    const top3 = report.lessons.slice(0, 3);
    for (let i = 0; i < top3.length; i++) {
        const lesson = top3[i];
        console.log(`${i + 1}. ${lesson.pattern.toUpperCase()}`);
        console.log(`   Frequency: ${lesson.frequency} mentions (${lesson.percentage}%)`);
        console.log(`   Apply to 100X: ${lesson.recommendation}`);
        console.log('');
    }

    console.log('💡 RECOMMENDED BUILDER TOKEN FEATURES:\n');

    const recommendations = [];

    // Staking is popular → implement it
    if (report.summary.patternCounts.staking > 10) {
        recommendations.push('✅ STAKING: BLD holders stake tokens to earn platform revenue share');
    }

    // Profit sharing is proven → use it
    if (report.summary.patternCounts.profitSharing > 5) {
        recommendations.push('✅ PROFIT SHARING: Distribute 50% of monthly revenue to stakers');
    }

    // Burns create scarcity → consider it
    if (report.summary.patternCounts.tokenBurns > 8) {
        recommendations.push('✅ TOKEN BURNS: Use 10% of profit for quarterly buyback + burn');
    }

    // Airdrops for bootstrapping → launch strategy
    if (report.summary.patternCounts.airdrops > 5) {
        recommendations.push('✅ AIRDROP: Grant BLD to first 100 Genesis builders retroactively');
    }

    // Governance increases engagement → add voting
    if (report.summary.patternCounts.governanceMining > 5) {
        recommendations.push('✅ GOVERNANCE: BLD holders vote on features (founder retains veto)');
    }

    for (const rec of recommendations) {
        console.log(rec);
    }

    console.log('\n' + '='.repeat(80));
    console.log('🔗 INTERESTING PROJECTS TO STUDY FURTHER:\n');

    const uniqueProjects = [...new Set(report.projects.map(p => p.title))];
    for (let i = 0; i < Math.min(10, uniqueProjects.length); i++) {
        const project = report.projects.find(p => p.title === uniqueProjects[i]);
        console.log(`${i + 1}. ${project.title}`);
        console.log(`   Pattern: ${project.pattern}`);
        console.log(`   URL: ${project.url}`);
        console.log('');
    }

    console.log('='.repeat(80) + '\n');
}

// Main execution
async function main() {
    console.log('🚀 CRYPTO TOKENOMICS AGGREGATOR - Learning Phase\n');
    console.log('Purpose: Study how crypto projects pay users → Apply to BUILDER token\n');
    console.log('='.repeat(80) + '\n');

    try {
        // 1. Fetch all crypto news
        const articles = await aggregateCryptoNews();

        if (articles.length === 0) {
            console.log('❌ No tokenomics articles found. Try again later.');
            return;
        }

        console.log(`\n✅ Found ${articles.length} tokenomics-related articles\n`);

        // 2. Analyze payout mechanisms
        const insights = analyzePayoutMechanisms(articles);

        // 3. Generate lessons for BUILDER token
        const lessons = generateLessons(insights);

        // 4. Save results
        const report = await saveResults(articles, insights, lessons);

        // 5. Display findings
        displayFindings(report);

        console.log('🎯 NEXT STEPS:\n');
        console.log('1. Review the generated report JSON file');
        console.log('2. Click through interesting project URLs to study details');
        console.log('3. Apply proven patterns to BUILDER token smart contract');
        console.log('4. Avoid failed patterns (check projects that crashed)');
        console.log('5. Run this aggregator daily to stay updated\n');

        console.log('✅ Aggregation complete!\n');

    } catch (error) {
        console.error('❌ Error:', error.message);
        console.error(error.stack);
    }
}

// Run if executed directly
if (require.main === module) {
    main();
}

module.exports = { aggregateCryptoNews, analyzePayoutMechanisms, generateLessons };
