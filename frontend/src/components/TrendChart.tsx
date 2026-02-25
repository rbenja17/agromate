"use client";

import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';

interface DailyTrendData {
    date: string;
    alcista: number;
    bajista: number;
    neutral: number;
}

interface TrendChartProps {
    data: DailyTrendData[];
}

export default function TrendChart({ data }: TrendChartProps) {
    if (!data || data.length === 0) {
        return (
            <div className="glass-card rounded-xl p-6">
                <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Tendencia Diaria</h3>
                <div className="flex items-center justify-center h-64 text-gray-500 dark:text-gray-400">
                    <p className="font-medium">No hay datos de tendencia para este período</p>
                </div>
            </div>
        );
    }

    return (
        <div className="glass-card rounded-xl p-6">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">Tendencia Diaria</h3>

            <ResponsiveContainer width="100%" height={300}>
                <AreaChart data={data}>
                    <defs>
                        <linearGradient id="colorAlcista" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorBajista" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#ef4444" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#ef4444" stopOpacity={0} />
                        </linearGradient>
                        <linearGradient id="colorNeutral" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#6b7280" stopOpacity={0.8} />
                            <stop offset="95%" stopColor="#6b7280" stopOpacity={0} />
                        </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
                    <XAxis
                        dataKey="date"
                        stroke="#9ca3af"
                        tick={{ fill: '#9ca3af' }}
                        tickFormatter={(date) => format(parseISO(date), 'dd/MM', { locale: es })}
                    />
                    <YAxis stroke="#9ca3af" tick={{ fill: '#9ca3af' }} />
                    <Tooltip
                        contentStyle={{
                            backgroundColor: '#1f2937',
                            border: '1px solid #374151',
                            borderRadius: '8px',
                            color: '#fff'
                        }}
                        labelFormatter={(date) => format(parseISO(date as string), "dd 'de' MMMM", { locale: es })}
                    />
                    <Legend />
                    <Area type="monotone" dataKey="alcista" stroke="#10b981" fillOpacity={1} fill="url(#colorAlcista)" name="Alcista" />
                    <Area type="monotone" dataKey="bajista" stroke="#ef4444" fillOpacity={1} fill="url(#colorBajista)" name="Bajista" />
                    <Area type="monotone" dataKey="neutral" stroke="#6b7280" fillOpacity={1} fill="url(#colorNeutral)" name="Neutral" />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}
