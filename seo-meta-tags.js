/**
 * SEO META TAGS - Universal SEO Component
 * Dynamically adds meta tags to all domain pages
 * φ = 1.618033988749894 | OVERKORE v13
 */

const SEOMetaTags = {
    // Domain-specific SEO data
    domainSEO: {
        'domain-chaos-forge': {
            title: 'CHAOS FORGE - Physical Infrastructure Domain | Consciousness Revolution',
            description: 'Physical infrastructure and manufacturing systems. Hardware automation, Rolling Studio, HAM radio network. 88% consciousness level.',
            keywords: 'physical infrastructure, manufacturing, hardware automation, rolling studio, HAM radio, IoT devices',
            ogImage: '/assets/chaos-forge-og.jpg',
            color: '#00ff64'
        },
        'domain-quantum-vault': {
            title: 'QUANTUM VAULT - Financial Intelligence Domain | Consciousness Revolution',
            description: 'Financial intelligence and revenue tracking. $847K tracked, crypto integration, multi-currency management. 94% consciousness level.',
            keywords: 'financial intelligence, revenue tracking, crypto, bitcoin, financial analytics, quantum finance',
            ogImage: '/assets/quantum-vault-og.jpg',
            color: '#ffff00'
        },
        'domain-mind-matrix': {
            title: 'MIND MATRIX - AI Systems Domain | Consciousness Revolution',
            description: 'AI systems and knowledge graphs. 847K knowledge nodes, multi-model AI (Claude, GPT-4, Llama). 92% consciousness level.',
            keywords: 'artificial intelligence, AI systems, knowledge graph, machine learning, neural networks, pattern recognition',
            ogImage: '/assets/mind-matrix-og.jpg',
            color: '#00ccff'
        },
        'domain-soul-sanctuary': {
            title: 'SOUL SANCTUARY - Consciousness Domain | Consciousness Revolution',
            description: 'Consciousness headquarters. Pattern Theory framework, 95% manipulation immunity, daily boot protocol. 95% consciousness level.',
            keywords: 'consciousness, manipulation immunity, pattern theory, awareness, mindfulness, consciousness elevation',
            ogImage: '/assets/soul-sanctuary-og.jpg',
            color: '#ff00ff'
        },
        'domain-reality-forge': {
            title: 'REALITY FORGE - Social Networks Domain | Consciousness Revolution',
            description: 'Social network automation. 24.7K followers, 247 active bots, 4.7M viral reach. 88% consciousness level.',
            keywords: 'social media automation, viral marketing, Instagram growth, Twitter automation, bot army',
            ogImage: '/assets/reality-forge-og.jpg',
            color: '#ff6600'
        },
        'domain-arkitek-academy': {
            title: 'ARKITEK ACADEMY - Creative Production Domain | Consciousness Revolution',
            description: 'Creative production and AI content. 4.7K AI pieces, 847 videos, automated design pipelines. 91% consciousness level.',
            keywords: 'AI content generation, creative automation, video production, design automation, content creation',
            ogImage: '/assets/arkitek-academy-og.jpg',
            color: '#ff0066'
        },
        'domain-nexus-terminal': {
            title: 'NEXUS TERMINAL - System Integration Domain | Consciousness Revolution',
            description: 'Master system integration. All 7 domains unified, 47 services, 1.2K auto-fixes, 99.7% uptime. 97% consciousness level.',
            keywords: 'system integration, orchestration, monitoring, DevOps, automation, infrastructure',
            ogImage: '/assets/nexus-terminal-og.jpg',
            color: '#6600ff'
        },
        'seven-domains': {
            title: 'Seven Domains - Complete Consciousness Ecosystem | Consciousness Revolution',
            description: 'Explore all 7 consciousness-elevated domains. Physical, Financial, Mental, Emotional, Social, Creative, Integration. 92.1% avg consciousness.',
            keywords: 'seven domains, consciousness platform, AI systems, personal development, automation, consciousness revolution',
            ogImage: '/assets/seven-domains-og.jpg',
            color: '#ffffff'
        },
        'default': {
            title: 'Consciousness Revolution - Seven Domains Platform',
            description: 'Seven consciousness-elevated domains for physical, financial, mental, emotional, social, creative, and integration mastery. Built with Pattern Theory and OVERKORE v13 mathematics.',
            keywords: 'consciousness, AI, automation, personal development, pattern theory, golden ratio, sacred geometry',
            ogImage: '/assets/og-default.jpg',
            color: '#000000'
        }
    },

    init() {
        this.detectDomain();
        this.addBasicMeta();
        this.addOpenGraphTags();
        this.addTwitterCardTags();
        this.addSchemaOrg();
        this.addCanonicalLink();
        this.addFavicon();
    },

    detectDomain() {
        const path = window.location.pathname;
        let detectedDomain = 'default';

        for (const domain in this.domainSEO) {
            if (path.includes(domain)) {
                detectedDomain = domain;
                break;
            }
        }

        this.currentDomain = this.domainSEO[detectedDomain];
        return this.currentDomain;
    },

    addMeta(name, content, property = false) {
        const meta = document.createElement('meta');
        if (property) {
            meta.setAttribute('property', name);
        } else {
            meta.setAttribute('name', name);
        }
        meta.setAttribute('content', content);
        document.head.appendChild(meta);
    },

    addBasicMeta() {
        // Set title
        document.title = this.currentDomain.title;

        // Add basic meta tags
        this.addMeta('description', this.currentDomain.description);
        this.addMeta('keywords', this.currentDomain.keywords);
        this.addMeta('author', 'Consciousness Revolution');
        this.addMeta('theme-color', this.currentDomain.color);
        this.addMeta('viewport', 'width=device-width, initial-scale=1.0');

        // Additional SEO
        this.addMeta('robots', 'index, follow');
        this.addMeta('googlebot', 'index, follow');
        this.addMeta('language', 'English');
        this.addMeta('revisit-after', '7 days');
    },

    addOpenGraphTags() {
        const url = window.location.href;

        this.addMeta('og:title', this.currentDomain.title, true);
        this.addMeta('og:description', this.currentDomain.description, true);
        this.addMeta('og:url', url, true);
        this.addMeta('og:type', 'website', true);
        this.addMeta('og:image', `https://conciousnessrevolution.io${this.currentDomain.ogImage}`, true);
        this.addMeta('og:image:width', '1200', true);
        this.addMeta('og:image:height', '630', true);
        this.addMeta('og:site_name', 'Consciousness Revolution', true);
        this.addMeta('og:locale', 'en_US', true);
    },

    addTwitterCardTags() {
        this.addMeta('twitter:card', 'summary_large_image');
        this.addMeta('twitter:site', '@ConsciousnessRev');
        this.addMeta('twitter:creator', '@overkillkulture');
        this.addMeta('twitter:title', this.currentDomain.title);
        this.addMeta('twitter:description', this.currentDomain.description);
        this.addMeta('twitter:image', `https://conciousnessrevolution.io${this.currentDomain.ogImage}`);
    },

    addSchemaOrg() {
        const schema = {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": this.currentDomain.title,
            "description": this.currentDomain.description,
            "url": window.location.href,
            "applicationCategory": "DesignApplication",
            "operatingSystem": "Any",
            "offers": {
                "@type": "Offer",
                "price": "0",
                "priceCurrency": "USD"
            },
            "creator": {
                "@type": "Organization",
                "name": "Consciousness Revolution",
                "url": "https://conciousnessrevolution.io"
            }
        };

        const script = document.createElement('script');
        script.type = 'application/ld+json';
        script.textContent = JSON.stringify(schema);
        document.head.appendChild(script);
    },

    addCanonicalLink() {
        const canonical = document.createElement('link');
        canonical.rel = 'canonical';
        canonical.href = window.location.href;
        document.head.appendChild(canonical);
    },

    addFavicon() {
        // Only add if not already present
        if (!document.querySelector('link[rel="icon"]')) {
            const favicon = document.createElement('link');
            favicon.rel = 'icon';
            favicon.type = 'image/svg+xml';
            favicon.href = '/favicon.svg';
            document.head.appendChild(favicon);
        }
    },

    // Get current SEO data (for debugging)
    getCurrentSEO() {
        return {
            domain: this.currentDomain,
            title: document.title,
            canonical: document.querySelector('link[rel="canonical"]')?.href,
            ogImage: document.querySelector('meta[property="og:image"]')?.content,
            description: document.querySelector('meta[name="description"]')?.content
        };
    }
};

// Auto-initialize
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => SEOMetaTags.init());
} else {
    SEOMetaTags.init();
}

window.SEOMetaTags = SEOMetaTags;
