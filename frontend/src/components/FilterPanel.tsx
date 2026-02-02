"use client";

import React, { useState, useEffect } from 'react';
import { FilterState, SentimentType } from '@/types';
import { fetchSources } from '@/lib/api';

interface FilterPanelProps {
    filters: FilterState;
    onFilterChange: (filters: FilterState) => void;
    onApply: () => void;
    onClear: () => void;
}

export default function FilterPanel({
    filters,
    onFilterChange,
    onApply,
    onClear
}: FilterPanelProps) {
    const [sources, setSources] = useState<string[]>([]);
    const [isExpanded, setIsExpanded] = useState(false);

    useEffect(() => {
        fetchSources().then(setSources);
    }, []);

    const handleChange = (key: keyof FilterState, value: string | null) => {
        onFilterChange({
            ...filters,
            [key]: value === '' ? null : value
        });
    };

    const hasActiveFilters = Object.values(filters).some(v => v !== null);

    return (
        <div className="bg-white rounded-lg shadow-md p-6 mb-6 border border-gray-200">
            <div
                className="flex items-center justify-between cursor-pointer"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <h3 className="text-lg font-semibold text-gray-900 flex items-center gap-2">
                    Filtros
                    {hasActiveFilters && (
                        <span className="bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full">
                            Activos
                        </span>
                    )}
                </h3>
                <svg
                    className={`w-5 h-5 text-gray-600 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
            </div>

            {isExpanded && (
                <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                    {/* Source Filter */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Fuente</label>
                        <select
                            value={filters.source || ''}
                            onChange={(e) => handleChange('source', e.target.value)}
                            className="w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Todas las fuentes</option>
                            {sources.map((source) => (
                                <option key={source} value={source}>{source}</option>
                            ))}
                        </select>
                    </div>

                    {/* Sentiment Filter */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Sentimiento</label>
                        <select
                            value={filters.sentiment || ''}
                            onChange={(e) => handleChange('sentiment', e.target.value as SentimentType | null)}
                            className="w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Todos</option>
                            <option value="ALCISTA">Alcista</option>
                            <option value="BAJISTA">Bajista</option>
                            <option value="NEUTRAL">Neutral</option>
                        </select>
                    </div>

                    {/* Date From */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Desde</label>
                        <input
                            type="date"
                            value={filters.dateFrom || ''}
                            onChange={(e) => handleChange('dateFrom', e.target.value)}
                            className="w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Date To */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Hasta</label>
                        <input
                            type="date"
                            value={filters.dateTo || ''}
                            onChange={(e) => handleChange('dateTo', e.target.value)}
                            className="w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        />
                    </div>

                    {/* Action Buttons */}
                    <div className="md:col-span-2 lg:col-span-4 flex gap-3 justify-end mt-2">
                        <button
                            onClick={onClear}
                            className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors font-medium"
                        >
                            Limpiar
                        </button>
                        <button
                            onClick={onApply}
                            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
                        >
                            Aplicar Filtros
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}
