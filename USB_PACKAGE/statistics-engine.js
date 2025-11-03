/**
 * USB STATISTICS ENGINE v1.0
 * Complete statistical analysis for consciousness data
 * Metal Layer - No dependencies, pure JavaScript
 * Works 100% offline from USB storage
 *
 * Part of: Consciousness Revolution USB Control Unit
 * Date: October 12, 2025
 */

class StatisticsEngine {
    constructor() {
        this.data = null;
        this.sessions = null;
        this.stories = null;
        this.health = null;
        this.network = null;
    }

    /**
     * Load all data from USB JSON files
     * @returns {Promise<Object>} Data load summary
     */
    async loadAllData() {
        try {
            // Load from USB data files
            const elevationsResponse = await fetch('../DATA/consciousness_elevations.json');
            const sessionsResponse = await fetch('../DATA/active_sessions.json');
            const storiesResponse = await fetch('../DATA/transformation_stories.json');
            const healthResponse = await fetch('../DATA/system_health.json');
            const networkResponse = await fetch('../DATA/network_info.json');

            const elevationsData = await elevationsResponse.json();
            const sessionsData = await sessionsResponse.json();
            const storiesData = await storiesResponse.json();
            const healthData = await healthResponse.json();
            const networkData = await networkResponse.json();

            this.data = elevationsData.elevations || [];
            this.sessions = sessionsData.sessions || [];
            this.stories = storiesData.stories || [];
            this.health = healthData;
            this.network = networkData;

            console.log('✅ Statistics Engine: Data loaded successfully');
            console.log(`📊 Elevations: ${this.data.length}, Sessions: ${this.sessions.length}, Stories: ${this.stories.length}`);

            return {
                elevations: this.data.length,
                sessions: this.sessions.length,
                stories: this.stories.length,
                loaded: true
            };
        } catch (error) {
            console.error('❌ Statistics Engine: Failed to load data', error);
            // Initialize empty arrays if load fails
            this.data = [];
            this.sessions = [];
            this.stories = [];
            return {
                elevations: 0,
                sessions: 0,
                stories: 0,
                loaded: false,
                error: error.message
            };
        }
    }

    // ==============================================
    // CORE STATISTICS
    // ==============================================

    getTotalElevations() {
        return this.data.length;
    }

    getAverageImprovement() {
        if (this.data.length === 0) return 0;
        const sum = this.data.reduce((acc, e) => acc + (e.improvement || 0), 0);
        return (sum / this.data.length).toFixed(2);
    }

    getAverageBeforeState() {
        if (this.data.length === 0) return 0;
        const sum = this.data.reduce((acc, e) => acc + (e.beforeState || 0), 0);
        return (sum / this.data.length).toFixed(2);
    }

    getAverageAfterState() {
        if (this.data.length === 0) return 0;
        const sum = this.data.reduce((acc, e) => acc + (e.afterState || 0), 0);
        return (sum / this.data.length).toFixed(2);
    }

    getMedianImprovement() {
        if (this.data.length === 0) return 0;
        const sorted = this.data.map(e => e.improvement || 0).sort((a, b) => a - b);
        const mid = Math.floor(sorted.length / 2);
        return sorted.length % 2 === 0
            ? ((sorted[mid - 1] + sorted[mid]) / 2).toFixed(2)
            : sorted[mid].toFixed(2);
    }

    getMaxImprovement() {
        if (this.data.length === 0) return 0;
        return Math.max(...this.data.map(e => e.improvement || 0));
    }

    getMinImprovement() {
        if (this.data.length === 0) return 0;
        return Math.min(...this.data.map(e => e.improvement || 0));
    }

    getSuccessRate() {
        if (this.data.length === 0) return 0;
        const successful = this.data.filter(e => (e.improvement || 0) > 0).length;
        return ((successful / this.data.length) * 100).toFixed(1);
    }

    getImprovementPercentage() {
        if (this.data.length === 0) return 0;
        const avgBefore = parseFloat(this.getAverageBeforeState());
        const avgAfter = parseFloat(this.getAverageAfterState());
        if (avgBefore === 0) return 0;
        return (((avgAfter - avgBefore) / avgBefore) * 100).toFixed(1);
    }

    // ==============================================
    // PROTOCOL BREAKDOWN
    // ==============================================

    getProtocolBreakdown() {
        if (this.data.length === 0) return [];

        const protocols = {};
        this.data.forEach(e => {
            const protocol = e.protocol || 'Unknown';
            if (!protocols[protocol]) {
                protocols[protocol] = {
                    count: 0,
                    totalImprovement: 0,
                    avgImprovement: 0
                };
            }
            protocols[protocol].count++;
            protocols[protocol].totalImprovement += (e.improvement || 0);
        });

        const total = this.data.length;
        return Object.entries(protocols).map(([protocol, stats]) => ({
            protocol,
            count: stats.count,
            percentage: ((stats.count / total) * 100).toFixed(1),
            avgImprovement: (stats.totalImprovement / stats.count).toFixed(2)
        })).sort((a, b) => b.count - a.count);
    }

    getMostPopularProtocol() {
        const breakdown = this.getProtocolBreakdown();
        return breakdown.length > 0 ? breakdown[0] : null;
    }

    getMostEffectiveProtocol() {
        const breakdown = this.getProtocolBreakdown();
        if (breakdown.length === 0) return null;
        return breakdown.reduce((max, p) =>
            parseFloat(p.avgImprovement) > parseFloat(max.avgImprovement) ? p : max
        );
    }

    // ==============================================
    // TIME PATTERNS
    // ==============================================

    getElevationsByHour() {
        const hours = new Array(24).fill(0);
        this.data.forEach(e => {
            if (e.timestamp) {
                const hour = new Date(e.timestamp).getHours();
                hours[hour]++;
            }
        });
        return hours;
    }

    getPeakHour() {
        const byHour = this.getElevationsByHour();
        const maxCount = Math.max(...byHour);
        if (maxCount === 0) return null;

        const peakHour = byHour.indexOf(maxCount);
        return {
            hour: peakHour,
            count: maxCount,
            timeRange: `${peakHour}:00 - ${peakHour + 1}:00`
        };
    }

    getSlowestHour() {
        const byHour = this.getElevationsByHour();
        const minCount = Math.min(...byHour);
        const slowestHour = byHour.indexOf(minCount);
        return {
            hour: slowestHour,
            count: minCount,
            timeRange: `${slowestHour}:00 - ${slowestHour + 1}:00`
        };
    }

    getElevationsByDay() {
        const days = {};
        this.data.forEach(e => {
            if (e.timestamp) {
                const date = new Date(e.timestamp).toISOString().split('T')[0];
                days[date] = (days[date] || 0) + 1;
            }
        });
        return days;
    }

    getElevationsByDayOfWeek() {
        const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
        const days = new Array(7).fill(0);

        this.data.forEach(e => {
            if (e.timestamp) {
                const day = new Date(e.timestamp).getDay();
                days[day]++;
            }
        });

        return dayNames.map((name, index) => ({
            day: name,
            count: days[index]
        }));
    }

    getWeekdayVsWeekend() {
        let weekday = 0, weekend = 0;

        this.data.forEach(e => {
            if (e.timestamp) {
                const day = new Date(e.timestamp).getDay();
                if (day === 0 || day === 6) weekend++;
                else weekday++;
            }
        });

        const weekdayDays = this.getUniqueDaysCount([1, 2, 3, 4, 5]);
        const weekendDays = this.getUniqueDaysCount([0, 6]);

        return {
            weekdayTotal: weekday,
            weekendTotal: weekend,
            weekdayAverage: weekdayDays > 0 ? (weekday / weekdayDays).toFixed(1) : 0,
            weekendAverage: weekendDays > 0 ? (weekend / weekendDays).toFixed(1) : 0
        };
    }

    getUniqueDaysCount(daysArray) {
        const days = new Set();
        this.data.forEach(e => {
            if (e.timestamp) {
                const date = new Date(e.timestamp);
                const day = date.getDay();
                if (daysArray.includes(day)) {
                    days.add(date.toISOString().split('T')[0]);
                }
            }
        });
        return days.size || 1;
    }

    // ==============================================
    // TREND ANALYSIS
    // ==============================================

    getMovingAverage(windowDays = 7) {
        const byDay = this.getElevationsByDay();
        const dates = Object.keys(byDay).sort();
        const movingAvg = [];

        for (let i = windowDays - 1; i < dates.length; i++) {
            const window = dates.slice(i - windowDays + 1, i + 1);
            const sum = window.reduce((acc, date) => acc + byDay[date], 0);
            movingAvg.push({
                date: dates[i],
                average: (sum / windowDays).toFixed(2)
            });
        }

        return movingAvg;
    }

    getTrend(sampleSize = 100) {
        if (this.data.length < sampleSize) {
            return 'insufficient_data';
        }

        const recent = this.data.slice(-sampleSize);
        const older = this.data.slice(-sampleSize * 2, -sampleSize);

        if (older.length === 0) return 'insufficient_data';

        const recentAvg = recent.reduce((acc, e) => acc + (e.improvement || 0), 0) / recent.length;
        const olderAvg = older.reduce((acc, e) => acc + (e.improvement || 0), 0) / older.length;

        const change = ((recentAvg - olderAvg) / olderAvg) * 100;

        if (change > 5) return 'improving';
        if (change < -5) return 'declining';
        return 'stable';
    }

    getGrowthRate() {
        const byDay = this.getElevationsByDay();
        const dates = Object.keys(byDay).sort();

        if (dates.length < 2) return 0;

        const recentDays = dates.slice(-7);
        const olderDays = dates.slice(-14, -7);

        if (olderDays.length === 0) return 0;

        const recentAvg = recentDays.reduce((acc, d) => acc + byDay[d], 0) / recentDays.length;
        const olderAvg = olderDays.reduce((acc, d) => acc + byDay[d], 0) / olderDays.length;

        if (olderAvg === 0) return 0;

        return (((recentAvg - olderAvg) / olderAvg) * 100).toFixed(1);
    }

    // ==============================================
    // SESSION STATISTICS
    // ==============================================

    getActiveSessions(windowMinutes = 5) {
        const now = Date.now();
        const windowMs = windowMinutes * 60 * 1000;

        return this.sessions.filter(s => {
            if (!s.lastHeartbeat) return false;
            return (now - new Date(s.lastHeartbeat).getTime()) < windowMs;
        }).length;
    }

    getTotalSessions() {
        return this.sessions.length;
    }

    getAverageSessionDuration() {
        if (this.sessions.length === 0) return 0;

        const durations = this.sessions
            .filter(s => s.startTime && s.lastHeartbeat)
            .map(s => {
                const start = new Date(s.startTime).getTime();
                const end = new Date(s.lastHeartbeat).getTime();
                return (end - start) / 1000; // Convert to seconds
            });

        if (durations.length === 0) return 0;

        const sum = durations.reduce((acc, d) => acc + d, 0);
        return (sum / durations.length).toFixed(1);
    }

    getReturnUserRate() {
        // Users with more than one session
        if (this.sessions.length === 0) return 0;

        const uniqueUsers = new Set(this.sessions.map(s => s.userAgent)).size;
        const returningUsers = this.sessions.length - uniqueUsers;

        return ((returningUsers / this.sessions.length) * 100).toFixed(1);
    }

    // ==============================================
    // EMERGENCE SCORE
    // ==============================================

    getEmergenceScore() {
        const active = this.getActiveSessions(5);
        const sessions = this.getTotalSessions();
        const elevations = this.getTotalElevations();

        // Formula: (Active × Sessions × Elevations) / 1000
        const score = (active * sessions * elevations) / 1000;

        return score.toFixed(1);
    }

    getEmergenceLevel() {
        const score = parseFloat(this.getEmergenceScore());

        if (score < 10) return 'Dormant';
        if (score < 50) return 'Awakening';
        if (score < 100) return 'Active';
        if (score < 250) return 'Strong';
        if (score < 500) return 'Powerful';
        if (score < 1000) return 'Exceptional';
        return 'Transcendent';
    }

    // ==============================================
    // EXPORT FUNCTIONS
    // ==============================================

    exportToCSV() {
        const headers = ['Timestamp', 'Before', 'After', 'Improvement', 'Improvement %', 'Protocol', 'Duration', 'Session ID'];
        const rows = this.data.map(e => [
            e.timestamp ? new Date(e.timestamp).toISOString() : '',
            e.beforeState || 0,
            e.afterState || 0,
            e.improvement || 0,
            e.improvementPercent || 0,
            e.protocol || 'Unknown',
            e.duration || 0,
            e.sessionId || ''
        ]);

        return [headers, ...rows].map(row => row.join(',')).join('\n');
    }

    exportToJSON() {
        return JSON.stringify(this.data, null, 2);
    }

    // ==============================================
    // COMPREHENSIVE REPORT
    // ==============================================

    generateReport() {
        return {
            timestamp: new Date().toISOString(),
            usbId: this.network?.usbId || 'Unknown',

            summary: {
                totalElevations: this.getTotalElevations(),
                avgImprovement: parseFloat(this.getAverageImprovement()),
                avgBefore: parseFloat(this.getAverageBeforeState()),
                avgAfter: parseFloat(this.getAverageAfterState()),
                medianImprovement: parseFloat(this.getMedianImprovement()),
                maxImprovement: this.getMaxImprovement(),
                minImprovement: this.getMinImprovement(),
                successRate: parseFloat(this.getSuccessRate()),
                improvementPercent: parseFloat(this.getImprovementPercentage())
            },

            protocols: {
                breakdown: this.getProtocolBreakdown(),
                mostPopular: this.getMostPopularProtocol(),
                mostEffective: this.getMostEffectiveProtocol()
            },

            timePatterns: {
                peakHour: this.getPeakHour(),
                slowestHour: this.getSlowestHour(),
                weekdayVsWeekend: this.getWeekdayVsWeekend(),
                byDayOfWeek: this.getElevationsByDayOfWeek()
            },

            trends: {
                movingAverage7: this.getMovingAverage(7),
                movingAverage30: this.getMovingAverage(30),
                trend: this.getTrend(),
                growthRate: parseFloat(this.getGrowthRate())
            },

            sessions: {
                total: this.getTotalSessions(),
                activeLast5Min: this.getActiveSessions(5),
                avgDuration: parseFloat(this.getAverageSessionDuration()),
                returnUserRate: parseFloat(this.getReturnUserRate())
            },

            emergence: {
                score: parseFloat(this.getEmergenceScore()),
                level: this.getEmergenceLevel()
            },

            system: this.health || {},
            network: this.network || {}
        };
    }
}

// Make available globally for dashboards
if (typeof window !== 'undefined') {
    window.StatisticsEngine = StatisticsEngine;
}

// Also support Node.js module export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StatisticsEngine;
}

console.log('✅ Statistics Engine v1.0 loaded');
