/**
 * Main Dashboard — Premium Bento Grid with Segmented Controls.
 */

'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Article, SentimentStats, FilterState } from '@/types';
import { fetchNews, fetchStats, triggerPipeline, fetchDailyTrends, fetchSourceTrends, fetchSentimentTimeline, fetchPipelineStatus } from '@/lib/api';
import NewsCard from './NewsCard';
import TrendChart from './TrendChart';
import SourcePieChart from './SourcePieChart';
import SentimentTimeline from './SentimentTimeline';
import FilterPanel from './FilterPanel';
import MarketOverview from './MarketOverview';
import DailySummary from './DailySummary';
import PriceHistory from './PriceHistory';
import DivergenceAlert from './DivergenceAlert';
import DollarCorrelation from './DollarCorrelation';
import ThemeToggle from './ThemeToggle';
import ResponsiveAd from './ResponsiveAd';

const TABS = [
    { id: 'resumen', label: 'Resumen', icon: '📊' },
    { id: 'noticias', label: 'Noticias', icon: '📰' },
    { id: 'tendencias', label: 'Tendencias', icon: '📈' },
    { id: 'mercado', label: 'Mercado', icon: '💹' },
] as const;

type TabId = typeof TABS[number]['id'];

function getTimeAgo(dateStr: string): string {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMin = Math.floor(diffMs / 60000);
    if (diffMin < 1) return 'hace instantes';
    if (diffMin < 60) return `hace ${diffMin} min`;
    const diffHours = Math.floor(diffMin / 60);
    if (diffHours < 24) return `hace ${diffHours}h`;
    return `hace ${Math.floor(diffHours / 24)}d`;
}

export default function Dashboard() {
    const [activeTab, setActiveTab] = useState<TabId>('resumen');
    const [news, setNews] = useState<Article[]>([]);
    const [stats, setStats] = useState<SentimentStats | null>(null);
    const [dailyTrends, setDailyTrends] = useState<any>(null);
    const [sourceTrends, setSourceTrends] = useState<any>(null);
    const [timeline, setTimeline] = useState<any>(null);
    const [lastUpdate, setLastUpdate] = useState<string | null>(null);
    const [filters, setFilters] = useState<FilterState>({
        source: null, sentiment: null, commodity: null, dateFrom: null, dateTo: null
    });
    const [loading, setLoading] = useState(true);
    const [updating, setUpdating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => { loadData(); loadPipelineStatus(); }, []);

    const loadPipelineStatus = async () => {
        try {
            const status = await fetchPipelineStatus();
            setLastUpdate(status.last_article_date || status.last_pipeline_run);
        } catch { }
    };

    const loadData = async () => {
        try {
            setLoading(true);
            setError(null);
            const f = {
                sentiment: filters.sentiment || undefined,
                source: filters.source?.length ? filters.source : undefined,
                commodity: filters.commodity || undefined,
                dateFrom: filters.dateFrom || undefined,
                dateTo: filters.dateTo || undefined
            };
            const [newsData, statsData, trendsDaily, trendsSource, trendsTimeline] = await Promise.all([
                fetchNews(50, f), fetchStats(), fetchDailyTrends(7, f), fetchSourceTrends(f), fetchSentimentTimeline(7, f)
            ]);
            setNews(newsData.articles);
            setStats(statsData);
            setDailyTrends(trendsDaily);
            setSourceTrends(trendsSource);
            setTimeline(trendsTimeline);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error al cargar datos');
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateAnalysis = async () => {
        try {
            setUpdating(true);
            setError(null);
            const response = await triggerPipeline();
            alert(`Pipeline iniciado: ${response.message}`);
            setTimeout(() => { loadData(); loadPipelineStatus(); }, 3000);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error al ejecutar pipeline');
        } finally {
            setUpdating(false);
        }
    };

    const handleFilterChange = (newFilters: FilterState) => setFilters(newFilters);
    const handleApplyFilters = () => loadData();
    const handleClearFilters = () => {
        setFilters({ source: null, sentiment: null, commodity: null, dateFrom: null, dateTo: null });
        setTimeout(loadData, 100);
    };

    // Helper: insert sponsored ad every 6th item
    const renderNewsWithAds = () => {
        const items: React.ReactNode[] = [];
        news.forEach((article, i) => {
            items.push(<NewsCard key={article.id} article={article} />);
            if ((i + 1) % 6 === 0) {
                items.push(<ResponsiveAd key={`ad-${i}`} variant="sponsored" />);
            }
        });
        return items;
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-slate-950">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mb-4"></div>
                    <p className="text-gray-500 dark:text-gray-400 text-sm">Cargando dashboard...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center min-h-screen bg-gray-50 dark:bg-slate-950">
                <div className="glass-card rounded-xl p-8 max-w-md text-center">
                    <p className="text-red-400 font-medium mb-2">Error</p>
                    <p className="text-red-300 text-sm mb-4">{error}</p>
                    <button onClick={loadData} className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm hover:bg-red-700">Reintentar</button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-slate-950 transition-colors">
            {/* ─────── HEADER ─────── */}
            <header className="sticky top-0 z-50 bg-white/80 dark:bg-slate-950/80 backdrop-blur-xl border-b border-gray-200 dark:border-white/5">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between py-3">
                        {/* Logo + Status */}
                        <div className="flex items-center gap-4">
                            <h1 className="text-xl font-bold text-gray-900 dark:text-white tracking-tight">
                                🌾 Agromate
                            </h1>
                            {lastUpdate && (
                                <span className="hidden sm:inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] font-medium bg-green-50 dark:bg-green-500/10 text-green-700 dark:text-green-400 border border-green-200 dark:border-green-500/20">
                                    <span className="w-1.5 h-1.5 bg-green-500 rounded-full live-pulse"></span>
                                    Live · {getTimeAgo(lastUpdate)}
                                </span>
                            )}
                        </div>

                        {/* Actions */}
                        <div className="flex items-center gap-2">
                            <ThemeToggle />
                            <button
                                onClick={handleUpdateAnalysis}
                                disabled={updating}
                                className="px-4 py-2 bg-blue-600 text-white text-xs font-medium rounded-lg hover:bg-blue-700 disabled:opacity-40 transition-all flex items-center gap-1.5"
                            >
                                {updating ? (
                                    <><div className="animate-spin rounded-full h-3 w-3 border-b-2 border-white"></div>Analizando...</>
                                ) : (
                                    <><svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" /></svg>Actualizar</>
                                )}
                            </button>
                        </div>
                    </div>

                    {/* ─── Segmented Control ─── */}
                    <div className="pb-3">
                        <div className="relative inline-flex items-center bg-gray-100 dark:bg-white/5 rounded-xl p-1 gap-0.5">
                            {TABS.map(tab => (
                                <button
                                    key={tab.id}
                                    onClick={() => setActiveTab(tab.id)}
                                    className={`relative z-10 flex items-center gap-1.5 px-4 py-2 text-sm font-medium rounded-lg transition-colors duration-200 ${activeTab === tab.id
                                            ? 'text-gray-900 dark:text-white'
                                            : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300'
                                        }`}
                                >
                                    <span className="text-sm">{tab.icon}</span>
                                    <span className="hidden sm:inline">{tab.label}</span>
                                </button>
                            ))}

                            {/* Animated highlight pill */}
                            <motion.div
                                className="absolute top-1 bottom-1 bg-white dark:bg-white/10 rounded-lg shadow-sm"
                                layoutId="activeTab"
                                transition={{ type: 'spring', stiffness: 400, damping: 30 }}
                                style={{
                                    left: `calc(${TABS.findIndex(t => t.id === activeTab)} * 25% + 4px)`,
                                    width: `calc(25% - 6px)`
                                }}
                            />
                        </div>
                    </div>
                </div>
            </header>

            {/* ─────── CONTENT ─────── */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">

                {/* ═══ TAB: RESUMEN ═══ */}
                {activeTab === 'resumen' && (
                    <div className="space-y-4">
                        {/* Bento Grid */}
                        <div className="bento-grid">
                            {/* Row 1: Market Overview (full width) */}
                            <div className="bento-wide">
                                <MarketOverview />
                            </div>

                            {/* Ad Banner between market and stats */}
                            <div className="bento-wide">
                                <ResponsiveAd variant="banner" />
                            </div>

                            {/* Row 2: Stats Cards */}
                            {stats && (
                                <>
                                    <div className="glass-card rounded-xl p-5 border-l-4 border-blue-500">
                                        <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Total Noticias</p>
                                        <p className="text-3xl font-bold font-mono text-gray-900 dark:text-white mt-2">{stats.total}</p>
                                    </div>
                                    <div className="glass-card rounded-xl p-5 border-l-4 border-green-500">
                                        <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Alcistas</p>
                                        <p className="text-3xl font-bold font-mono text-green-500 mt-2">{stats.alcista}</p>
                                        <p className="text-xs font-mono text-gray-500 dark:text-gray-500 mt-1">{stats.alcista_percentage.toFixed(1)}%</p>
                                    </div>
                                    <div className="glass-card rounded-xl p-5 border-l-4 border-red-500">
                                        <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Bajistas</p>
                                        <p className="text-3xl font-bold font-mono text-red-500 mt-2">{stats.bajista}</p>
                                        <p className="text-xs font-mono text-gray-500 dark:text-gray-500 mt-1">{stats.bajista_percentage.toFixed(1)}%</p>
                                    </div>
                                    <div className="glass-card rounded-xl p-5 border-l-4 border-gray-500">
                                        <p className="text-xs font-medium text-gray-500 dark:text-gray-400 uppercase tracking-wider">Neutrales</p>
                                        <p className="text-3xl font-bold font-mono text-gray-400 mt-2">{stats.neutral}</p>
                                        <p className="text-xs font-mono text-gray-500 dark:text-gray-500 mt-1">{stats.neutral_percentage.toFixed(1)}%</p>
                                    </div>
                                </>
                            )}

                            {/* Row 3: AI Summary (half) + Divergence (half) */}
                            <div className="bento-half">
                                <DailySummary />
                            </div>
                            <div className="bento-half">
                                <DivergenceAlert />
                            </div>
                        </div>
                    </div>
                )}

                {/* ═══ TAB: NOTICIAS ═══ */}
                {activeTab === 'noticias' && (
                    <div className="space-y-6">
                        <FilterPanel
                            filters={filters}
                            onFilterChange={handleFilterChange}
                            onApply={handleApplyFilters}
                            onClear={handleClearFilters}
                        />
                        <h2 className="text-xl font-bold text-gray-900 dark:text-white">
                            Últimas Noticias Analizadas
                        </h2>
                        {news.length === 0 ? (
                            <div className="glass-card rounded-xl p-12 text-center">
                                <p className="text-gray-500 dark:text-gray-400">No hay noticias. Presioná &quot;Actualizar&quot; para analizar.</p>
                            </div>
                        ) : (
                            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                                {renderNewsWithAds()}
                            </div>
                        )}
                    </div>
                )}

                {/* ═══ TAB: TENDENCIAS ═══ */}
                {activeTab === 'tendencias' && (
                    <div className="space-y-6">
                        {dailyTrends && sourceTrends && timeline ? (
                            <>
                                <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                                    <TrendChart data={dailyTrends.data} />
                                    <SourcePieChart data={sourceTrends.data} />
                                </div>
                                <SentimentTimeline data={timeline.data} />
                            </>
                        ) : (
                            <div className="glass-card rounded-xl p-12 text-center">
                                <p className="text-gray-500 dark:text-gray-400">No hay datos de tendencias.</p>
                            </div>
                        )}
                    </div>
                )}

                {/* ═══ TAB: MERCADO ═══ */}
                {activeTab === 'mercado' && (
                    <div className="space-y-6">
                        <MarketOverview />
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                            <PriceHistory />
                            <DollarCorrelation />
                        </div>
                    </div>
                )}
            </main>
        </div>
    );
}
