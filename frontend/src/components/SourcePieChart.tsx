"use client";

import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

interface SourceData {
    source: string;
    alcista: number;
    bajista: number;
    neutral: number;
    total: number;
}

interface SourcePieChartProps {
    data: SourceData[];
}

const COLORS = ['#3b82f6', '#8b5cf6', '#ec4899', '#f59e0b', '#10b981'];

export default function SourcePieChart({ data }: SourcePieChartProps) {
    // Empty state
    if (!data || data.length === 0) {
        return (
            <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
                <h3 className="text-xl font-bold text-gray-900 mb-4">Distribución por Fuente</h3>
                <div className="flex items-center justify-center h-64 text-gray-500">
                    <div className="text-center">
                        <svg className="w-16 h-16 mx-auto mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
                        </svg>
                        <p className="font-medium">No hay datos de fuentes para este período</p>
                        <p className="text-sm mt-2">Ejecutá "Actualizar Análisis" para obtener datos</p>
                    </div>
                </div>
            </div>
        );
    }

    // Transform data for pie chart
    const pieData = data.map((item, index) => ({
        name: item.source,
        value: item.total,
        color: COLORS[index % COLORS.length]
    }));

    return (
        <div className="bg-white rounded-lg shadow-md p-6 border border-gray-200">
            <h3 className="text-xl font-bold text-gray-900 mb-4">Distribución por Fuente</h3>

            <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                    <Pie
                        data={pieData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                        outerRadius={80}
                        fill="#8884d8"
                        dataKey="value"
                    >
                        {pieData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                    </Pie>
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#1f2937',
                            border: '1px solid #374151',
                            borderRadius: '8px',
                            color: '#fff'
                        }}
                    />
                    <Legend />
                </PieChart>
            </ResponsiveContainer>

            {/* Details table */}
            <div className="mt-4 space-y-2">
                {data.map((item, index) => (
                    <div key={item.source} className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2">
                            <div
                                className="w-3 h-3 rounded-full"
                                style={{ backgroundColor: COLORS[index % COLORS.length] }}
                            />
                            <span className="text-gray-700">{item.source}</span>
                        </div>
                        <div className="flex gap-3 text-xs">
                            <span className="text-green-600">{item.alcista}</span>
                            <span className="text-red-600">{item.bajista}</span>
                            <span className="text-gray-600">{item.neutral}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
