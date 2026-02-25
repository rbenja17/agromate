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
    const [sourcesDropdownOpen, setSourcesDropdownOpen] = useState(false);  // NUEVO

    useEffect(() => {
        fetchSources().then(setSources);
    }, []);

    const handleChange = (key: keyof FilterState, value: string | string[] | null) => {
        onFilterChange({
            ...filters,
            [key]: value === '' ? null : value
        });
    };

    const hasActiveFilters = Object.values(filters).some(v => v !== null);

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-6 mb-6 border border-gray-200 dark:border-gray-700">
            <div
                className="flex items-center justify-between cursor-pointer"
                onClick={() => setIsExpanded(!isExpanded)}
            >
                <h3 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
                    Filtros
                    {hasActiveFilters && (
                        <span className="bg-blue-500 text-white text-xs px-2 py-0.5 rounded-full">
                            Activos
                        </span>
                    )}
                </h3>
                <svg
                    className={`w-5 h-5 text-gray-600 dark:text-gray-400 transition-transform ${isExpanded ? 'rotate-180' : ''}`}
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
            </div>

            {isExpanded && (
                <div className="mt-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {/* Source Filter - Multi-Select */}
                    <div className="relative">
                        <label className="block text-sm font-medium text-gray-700 mb-1">Fuentes</label>
                        <div className="relative">
                            <button
                                type="button"
                                onClick={() => setSourcesDropdownOpen(!sourcesDropdownOpen)}
                                className="w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-left text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent flex items-center justify-between"
                            >
                                <span className="text-sm">
                                    {!filters.source || filters.source.length === 0
                                        ? 'Todas las fuentes'
                                        : `${filters.source.length} seleccionada(s)`}
                                </span>
                                <svg className={`w-4 h-4 transition-transform ${sourcesDropdownOpen ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>

                            {sourcesDropdownOpen && (
                                <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-lg shadow-lg max-h-60 overflow-auto">
                                    {sources.map((source) => (
                                        <label
                                            key={source}
                                            className="flex items-center gap-2 px-3 py-2 hover:bg-gray-50 cursor-pointer"
                                        >
                                            <input
                                                type="checkbox"
                                                checked={filters.source?.includes(source) || false}
                                                onChange={(e) => {
                                                    const currentSources = filters.source || [];
                                                    const newSources = e.target.checked
                                                        ? [...currentSources, source]
                                                        : currentSources.filter(s => s !== source);
                                                    handleChange('source', newSources.length > 0 ? newSources : null);
                                                }}
                                                className="rounded text-blue-600 focus:ring-2 focus:ring-blue-500"
                                            />
                                            <span className="text-sm text-gray-700">{source}</span>
                                        </label>
                                    ))}
                                </div>
                            )}
                        </div>
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

                    {/* Commodity Filter */}
                    <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">Commodity</label>
                        <select
                            value={filters.commodity || ''}
                            onChange={(e) => handleChange('commodity', e.target.value)}
                            className="w-full bg-white border border-gray-300 rounded-lg px-3 py-2 text-gray-900 focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                        >
                            <option value="">Todos</option>
                            <option value="SOJA">Soja</option>
                            <option value="MAÍZ">Maíz</option>
                            <option value="TRIGO">Trigo</option>
                            <option value="GIRASOL">Girasol</option>
                            <option value="CEBADA">Cebada</option>
                            <option value="SORGO">Sorgo</option>
                            <option value="GENERAL">General</option>
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
