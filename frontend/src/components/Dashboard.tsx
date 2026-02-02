/**
 * Main Dashboard component for Agromate.
 * Displays sentiment statistics and news articles.
 */

'use client';

import { useState, useEffect } from 'react';
import { Article, SentimentStats, FilterState } from '@/types';
import { fetchNews, fetchStats, triggerPipeline, fetchDailyTrends, fetchSourceTrends, fetchSentimentTimeline } from '@/lib/api';
import NewsCard from './NewsCard';
import TrendChart from './TrendChart';
import SourcePieChart from './SourcePieChart';
import SentimentTimeline from './SentimentTimeline';
import FilterPanel from './FilterPanel';

export default function Dashboard() {
    const [news, setNews] = useState<Article[]>([]);
    const [stats, setStats] = useState<SentimentStats | null>(null);
    const [dailyTrends, setDailyTrends] = useState<any>(null);
    const [sourceTrends, setSourceTrends] = useState<any>(null);
    const [timeline, setTimeline] = useState<any>(null);
    const [filters, setFilters] = useState<FilterState>({
        source: null,
        sentiment: null,
        dateFrom: null,
        dateTo: null
    });
    const [loading, setLoading] = useState(true);
    const [updating, setUpdating] = useState(false);
    const [error, setError] = useState<string | null>(null);

    // Load data on mount
    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            setError(null);

            // Build filters object
            const currentFilters = {
                sentiment: filters.sentiment || undefined,
                source: filters.source || undefined,
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
            dateFrom: null,
            dateTo: null
        });
        // Reload with no filters
        setTimeout(loadData, 100);
    };

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
                    <p className="text-gray-600">Cargando análisis de mercado...</p>
                </div>
            </div>
        );
    }

    if (error) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="bg-red-50 border border-red-200 rounded-lg p-6 max-w-md">
                    <h3 className="text-red-800 font-semibold mb-2">Error</h3>
                    <p className="text-red-600">{error}</p>
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
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-3xl font-bold text-gray-900">
                                🌾 Agromate
                            </h1>
                            <p className="text-sm text-gray-600 mt-1">
                                Análisis de sentimiento del mercado agropecuario argentino
                            </p>
                        </div>
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
            </header>

            {/* Main content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {/* Stats cards */}
                {stats && (
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                        {/* Total */}
                        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-blue-500">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600">Total Noticias</p>
                                    <p className="text-3xl font-bold text-gray-900 mt-1">{stats.total}</p>
                                </div>
                                <div className="bg-blue-100 rounded-full p-3">
                                    <svg className="w-6 h-6 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        {/* Alcista */}
                        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-green-500">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600">Alcistas</p>
                                    <p className="text-3xl font-bold text-green-600 mt-1">{stats.alcista}</p>
                                    <p className="text-xs text-gray-500 mt-1">{stats.alcista_percentage.toFixed(1)}%</p>
                                </div>
                                <div className="bg-green-100 rounded-full p-3">
                                    <svg className="w-6 h-6 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        {/* Bajista */}
                        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-red-500">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600">Bajistas</p>
                                    <p className="text-3xl font-bold text-red-600 mt-1">{stats.bajista}</p>
                                    <p className="text-xs text-gray-500 mt-1">{stats.bajista_percentage.toFixed(1)}%</p>
                                </div>
                                <div className="bg-red-100 rounded-full p-3">
                                    <svg className="w-6 h-6 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
                                    </svg>
                                </div>
                            </div>
                        </div>

                        {/* Neutral */}
                        <div className="bg-white rounded-lg shadow-md p-6 border-l-4 border-gray-500">
                            <div className="flex items-center justify-between">
                                <div>
                                    <p className="text-sm font-medium text-gray-600">Neutrales</p>
                                    <p className="text-3xl font-bold text-gray-700 mt-1">{stats.neutral}</p>
                                    <p className="text-xs text-gray-500 mt-1">{stats.neutral_percentage.toFixed(1)}%</p>
                                </div>
                                <div className="bg-gray-100 rounded-full p-3">
                                    <svg className="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
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
                        <h2 className="text-2xl font-bold text-gray-900 mb-6">
                            Análisis de Tendencias
                        </h2>

                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                            <TrendChart data={dailyTrends.data} />
                            <SourcePieChart data={sourceTrends.data} />
                        </div>

                        <SentimentTimeline data={timeline.data} />
                    </div>
                )}

                {/* News grid */}
                <div>
                    <h2 className="text-2xl font-bold text-gray-900 mb-6">
                        Últimas Noticias Analizadas
                    </h2>

                    {news.length === 0 ? (
                        <div className="bg-white rounded-lg shadow-md p-12 text-center">
                            <p className="text-gray-600">No hay noticias disponibles. Ejecutá "Actualizar Análisis" para obtener datos.</p>
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
