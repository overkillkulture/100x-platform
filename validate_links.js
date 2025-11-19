#!/usr/bin/env node
/**
 * 100X PLATFORM - LINK VALIDATOR
 * Recursively checks all HTML files for broken links and dead ends
 * Generates automated gap analysis
 */

const fs = require('fs');
const path = require('path');

// Configuration
const ROOT_DIR = __dirname;
const IGNORE_DIRS = ['node_modules', '.git', 'overkor-site', '.cache'];
const IGNORE_FILES = ['index_old.html', 'index_airtable_backup.html', 'index_netlify_forms.html'];

// Results storage
const results = {
    htmlFiles: [],
    links: [],
    deadEnds: [],
    workingLinks: [],
    externalLinks: [],
    missingFiles: new Set()
};

/**
 * Find all HTML files recursively
 */
function findHTMLFiles(dir) {
    const files = fs.readdirSync(dir);

    files.forEach(file => {
        const filePath = path.join(dir, file);
        const stat = fs.statSync(filePath);

        if (stat.isDirectory() && !IGNORE_DIRS.includes(file)) {
            findHTMLFiles(filePath);
        } else if (file.endsWith('.html') && !IGNORE_FILES.includes(file)) {
            results.htmlFiles.push(filePath.replace(ROOT_DIR, '.'));
        }
    });
}

/**
 * Extract links from HTML file
 */
function extractLinks(htmlFile) {
    const content = fs.readFileSync(path.join(ROOT_DIR, htmlFile.slice(2)), 'utf-8');
    const links = [];

    // Extract onclick="openSystem('...')"
    const onclickMatches = content.matchAll(/onclick="openSystem\('([^']+)'\)"/g);
    for (const match of onclickMatches) {
        links.push({ type: 'openSystem', target: match[1], source: htmlFile });
    }

    // Extract onclick="window.open('...', '_blank')"
    const windowOpenMatches = content.matchAll(/window\.open\('([^']+)',\s*'_blank'\)/g);
    for (const match of windowOpenMatches) {
        links.push({ type: 'windowOpen', target: match[1], source: htmlFile });
    }

    // Extract href="..."
    const hrefMatches = content.matchAll(/href="([^"]+)"/g);
    for (const match of hrefMatches) {
        if (!match[1].startsWith('http') && !match[1].startsWith('#') && !match[1].startsWith('mailto:')) {
            links.push({ type: 'href', target: match[1], source: htmlFile });
        } else if (match[1].startsWith('http')) {
            results.externalLinks.push({ url: match[1], source: htmlFile });
        }
    }

    // Extract src="..." (scripts and images)
    const srcMatches = content.matchAll(/src="([^"]+)"/g);
    for (const match of srcMatches) {
        if (!match[1].startsWith('http') && !match[1].startsWith('data:')) {
            links.push({ type: 'src', target: match[1], source: htmlFile });
        }
    }

    return links;
}

/**
 * Resolve link target to file path
 */
function resolveLinkTarget(link) {
    // Handle openSystem mappings
    const systemMappings = {
        'todo': 'PLATFORM/todo-master.html',
        'pattern': 'PUBLIC/pattern-filter.html',
        'training': 'PUBLIC/pattern-theory-training.html',
        'partnership': 'PUBLIC/partnership.html',
        'analytics': 'ANALYTICS_DASHBOARD_LIVE.html',
        'video': 'PLATFORM/construction.html',
        'brain': 'PLATFORM/construction.html',
        'trinity': 'PLATFORM/construction.html',
        'observer': 'PLATFORM/construction.html',
        'community': 'PLATFORM/construction.html'
    };

    if (link.type === 'openSystem') {
        return systemMappings[link.target] || link.target;
    }

    // Remove query strings and anchors
    let target = link.target.split('?')[0].split('#')[0];

    return target;
}

/**
 * Check if file exists
 */
function checkFileExists(target) {
    const fullPath = path.join(ROOT_DIR, target);
    return fs.existsSync(fullPath);
}

/**
 * Validate all links
 */
function validateLinks() {
    results.htmlFiles.forEach(htmlFile => {
        const links = extractLinks(htmlFile);

        links.forEach(link => {
            const target = resolveLinkTarget(link);
            const exists = checkFileExists(target);

            const linkInfo = {
                source: htmlFile,
                type: link.type,
                target: target,
                exists: exists
            };

            results.links.push(linkInfo);

            if (exists) {
                results.workingLinks.push(linkInfo);
            } else {
                results.deadEnds.push(linkInfo);
                results.missingFiles.add(target);
            }
        });
    });
}

/**
 * Generate report
 */
function generateReport() {
    console.log('\n🔍 100X PLATFORM - LINK VALIDATION REPORT');
    console.log('═══════════════════════════════════════════\n');

    console.log(`📄 HTML Files Scanned: ${results.htmlFiles.length}`);
    console.log(`🔗 Total Links Found: ${results.links.length}`);
    console.log(`✅ Working Links: ${results.workingLinks.length}`);
    console.log(`❌ Broken Links: ${results.deadEnds.length}`);
    console.log(`🌐 External Links: ${results.externalLinks.length}`);
    console.log(`📁 Missing Files: ${results.missingFiles.size}\n`);

    if (results.deadEnds.length > 0) {
        console.log('🔴 DEAD ENDS FOUND:\n');
        results.deadEnds.forEach(link => {
            console.log(`   ❌ ${link.source}`);
            console.log(`      → ${link.type}: ${link.target}`);
            console.log(`      Status: FILE NOT FOUND\n`);
        });
    }

    if (results.missingFiles.size > 0) {
        console.log('\n📋 MISSING FILES (unique):\n');
        Array.from(results.missingFiles).forEach(file => {
            console.log(`   • ${file}`);
        });
    }

    console.log('\n═══════════════════════════════════════════');

    // Calculate health score
    const healthScore = Math.round((results.workingLinks.length / results.links.length) * 100);
    console.log(`\n💪 PLATFORM HEALTH: ${healthScore}%\n`);

    if (healthScore === 100) {
        console.log('✨ PERFECT! No broken links found.\n');
    } else if (healthScore >= 80) {
        console.log('✅ GOOD - Minor fixes needed.\n');
    } else if (healthScore >= 60) {
        console.log('⚠️  NEEDS ATTENTION - Multiple broken links.\n');
    } else {
        console.log('🚨 CRITICAL - Many broken links found!\n');
    }
}

/**
 * Main execution
 */
console.log('🚀 Starting link validation...\n');
findHTMLFiles(ROOT_DIR);
validateLinks();
generateReport();

// Exit with error code if broken links found
process.exit(results.deadEnds.length > 0 ? 1 : 0);
