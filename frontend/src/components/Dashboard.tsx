/**
 * Main Dashboard component for Agromate.
 * Displays sentiment statistics, market data, AI summary, and news articles.
 */

'use client';

import { useState, useEffect } from 'react';
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

function getTimeAgo(dateStr: string): string {
    const date = new Date(dateStr);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMin = Math.floor(diffMs / 60000);
    if (diffMin < 1) return 'hace instantes';
    if (diffMin < 60) return `hace ${diffMin} min`;
    const diffHours = Math.floor(diffMin / 60);
    if (diffHours < 24) return `hace ${diffHours}h`;
    const diffDays = Math.floor(diffHours / 24);
    return `hace ${diffDays}d`;
}

export default function Dashboard() {
    const [news, setNews] = useState<Article[]>([]);
    const [stats, setStats] = useState<SentimentStats | null>(null);
    const [dailyTrends, setDailyTrends] = useState<any>(null);
    const [sourceTrends, setSourceTrends] = useState<any>(null);
    const [timeline, setTimeline] = useState<any>(null);
    const [lastUpdate, setLastUpdate] = useState<string | null>(null);
    const [filters, setFilters] = useState<FilterState>({
        source: null,
        sentiment: null,
        commodity: null,
        dateFrom: null,
        dateTo: null
    });
    const [loading, setLoading] = useState(true);
    const [updating, setUpdating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Load data on mount
    useEffect(() => {
        loadData();
        loadPipelineStatus();
    }, []);

    const loadPipelineStatus = async () => {
        try {
            const status = await fetchPipelineStatus();
            setLastUpdate(status.last_article_date || status.last_pipeline_run);
        } catch (e) { }
    };

    const loadData = async () => {
        try {
            setLoading(true);
            setError(null);

            // Build filters object
            const currentFilters = {
                sentiment: filters.sentiment || undefined,
                source: filters.source && filters.source.length > 0 ? filters.source : undefined,
                commodity: filters.commodity || undefined,
                dateFrom: filters.dateFrom || undefined,
                dateTo: filters.dateTo || undefined
            };

            // Fetch all data in parallel
            const [newsData, statsData, trendsDaily, trendsSource, trendsTimeline] = await Promise.all([
                fetchNews(50, currentFilters),
                fetchStats(),
                fetchDailyTrends(7, currentFilters),
                fetchSourceTrends(currentFilters),
                fetchSentimentTimeline(7, currentFilters)
            ]);

            setNews(newsData.articles);
            setStats(statsData);
            setDailyTrends(trendsDaily);
            setSourceTrends(trendsSource);
            setTimeline(trendsTimeline);
        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error al cargar datos');
            console.error('Error loading data:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleUpdateAnalysis = async () => {
        try {
            setUpdating(true);
            setError(null);

            const response = await triggerPipeline();

            // Show success message
            alert(`Pipeline iniciado: ${response.message}`);

            // Reload data after a delay
            setTimeout(() => {
                loadData();
                loadPipelineStatus();
            }, 3000);

        } catch (err) {
            setError(err instanceof Error ? err.message : 'Error al ejecutar pipeline');
            console.error('Error triggering pipeline:', err);
        } finally {
            setUpdating(false);
        }
    };

    const handleFilterChange = (newFilters: FilterState) => {
        setFilters(newFilters);
    };

    const handleApplyFilters = () => {
        loadData();
    };

    const handleClearFilters = () => {
        setFilters({
            source: null,
            sentiment: null,
            commodity: null,
            dateFrom: null,
            dateTo: null
        });
        // Reload with no filters
        setTimeout(loadData, 100);
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen dark:bg-gray-900">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                    <p className="text-gray-600 dark:text-gray-400">Cargando análisis de mercado...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center min-h-screen dark:bg-gray-900">
                <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 rounded-lg p-6 max-w-md">
                    <h3 className="text-red-800 dark:text-red-300 font-semibold mb-2">Error</h3>
                    <p className="text-red-600 dark:text-red-400">{error}</p>
                    <button
                        onClick={loadData}
                        className="mt-4 px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700"
                    >
                        Reintentar
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors">
            {/* Header */}
            <header className="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                                🌾 Agromate
                            </h1>
                            <div className="flex items-center gap-3 mt-1">
                                <p className="text-sm text-gray-600 dark:text-gray-400">
                                    Análisis de sentimiento del mercado agropecuario argentino
                                </p>
                                {lastUpdate && (
                                    <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-xs bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400">
                                        <span className="w-1.5 h-1.5 bg-green-500 rounded-full animate-pulse"></span>
                                        Actualizado {getTimeAgo(lastUpdate)}
                                    </span>
                                )}
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <ThemeToggle />
                            <button
                                onClick={handleUpdateAnalysis}
                                disabled={updating}
                                className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-blue-300 disabled:cursor-not-allowed transition-colors font-medium flex items-center gap-2"
                            >
                                {updating ? (
                                    <>
                                        <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                                        Actualizando...
                                    </>
                                ) : (
                                    <>
                                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                                        </svg>
                                        Actualizar Análisis
                                    </>
                                )}
                            </button>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Market Overview */}
                <MarketOverview />

                {/* AI Daily Summary */}
                <DailySummary />

                {/* Divergence Alerts */}
                <DivergenceAlert />

                {/* Stats cards */}
                {stats && (
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                        {/* Total */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Total Noticias</p>
                                    <p className="text-3xl font-bold text-gray-900 dark:text-white mt-1">{stats.total}</p>
                                </div>
                                <div className="bg-blue-100 dark:bg-blue-900/30 rounded-full p-3">
                                    <svg className="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        {/* Alcista */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-green-500">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Alcistas</p>
                                    <p className="text-3xl font-bold text-green-600 dark:text-green-400 mt-1">{stats.alcista}</p>
                                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">{stats.alcista_percentage.toFixed(1)}%</p>
                                </div>
                                <div className="bg-green-100 dark:bg-green-900/30 rounded-full p-3">
                                    <svg className="w-6 h-6 text-green-600 dark:text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        {/* Bajista */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-red-500">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Bajistas</p>
                                    <p className="text-3xl font-bold text-red-600 dark:text-red-400 mt-1">{stats.bajista}</p>
                                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">{stats.bajista_percentage.toFixed(1)}%</p>
                                </div>
                                <div className="bg-red-100 dark:bg-red-900/30 rounded-full p-3">
                                    <svg className="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        {/* Neutral */}
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 border-l-4 border-gray-500">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600 dark:text-gray-400">Neutrales</p>
                                    <p className="text-3xl font-bold text-gray-700 dark:text-gray-300 mt-1">{stats.neutral}</p>
                                    <p className="text-xs text-gray-500 dark:text-gray-500 mt-1">{stats.neutral_percentage.toFixed(1)}%</p>
                                </div>
                                <div className="bg-gray-100 dark:bg-gray-700 rounded-full p-3">
                                    <svg className="w-6 h-6 text-gray-600 dark:text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h14" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {/* Filter Panel */}
                <FilterPanel
                    filters={filters}
                    onFilterChange={handleFilterChange}
                    onApply={handleApplyFilters}
                    onClear={handleClearFilters}
                />

                {/* Visualizations */}
                {dailyTrends && sourceTrends && timeline && (
                    <div className="mb-8">
                        <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                            Análisis de Tendencias
                        </h2>

                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                            <TrendChart data={dailyTrends.data} />
                            <SourcePieChart data={sourceTrends.data} />
                        </div>

                        <SentimentTimeline data={timeline.data} />
                    </div>
                )}

                {/* Historical Prices & Dollar Correlation */}
                <div className="mb-8">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                        Datos de Mercado
                    </h2>
                    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                        <PriceHistory />
                        <DollarCorrelation />
                    </div>
                </div>

                {/* News grid */}
                <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                        Últimas Noticias Analizadas
                    </h2>

                    {news.length === 0 ? (
                        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-12 text-center">
                            <p className="text-gray-600 dark:text-gray-400">No hay noticias disponibles. Ejecutá "Actualizar Análisis" para obtener datos.</p>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                            {news.map((article) => (
                                <NewsCard key={article.id} article={article} />
                            ))}
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}
