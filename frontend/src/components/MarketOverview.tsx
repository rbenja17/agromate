"use client";

import { useEffect, useState } from 'react';
import { fetchMarketData } from '@/lib/api';

interface MarketData {
    price: number;
    currency: string;
    change_percent: number;
    symbol: string;
}

interface MarketResponse {
    timestamp: string;
    data: {
        [key: string]: MarketData | { error: string, symbol: string };
    };
}

export default function MarketOverview() {
    const [data, setData] = useState<MarketResponse | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const loadMarket = async () => {
            try {
                const result = await fetchMarketData();
                setData(result);
            } catch (err) {
                setError("Datos no disponibles");
            } finally {
                setLoading(false);
            }
        };

        loadMarket();
        const interval = setInterval(loadMarket, 60000);
        return () => clearInterval(interval);
    }, []);

    if (loading) {
        return (
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
                {[1, 2, 3, 4, 5].map((i) => (
                    <div key={i} className="glass-card rounded-xl p-5 animate-pulse">
                        <div className="h-3 bg-gray-200 dark:bg-white/10 rounded w-1/2 mb-3"></div>
                        <div className="h-6 bg-gray-200 dark:bg-white/10 rounded w-2/3"></div>
                    </div>
                ))}
            </div>
        );
    }

    if (error || !data || !data.data) {
        return (
            <div className="glass-card rounded-xl p-4 text-center">
                <p className="text-sm text-gray-500 dark:text-gray-400">Datos de mercado no disponibles</p>
            </div>
        );
    }

    const commodities = [
        { key: 'soja_rosario', name: 'Soja', icon: '🌱' },
        { key: 'maiz_rosario', name: 'Maíz', icon: '🌽' },
        { key: 'trigo_rosario', name: 'Trigo', icon: '🌾' },
        { key: 'dolar', name: 'USD Oficial', icon: '💵' },
        { key: 'dolar_blue', name: 'USD Blue', icon: '💸' }
    ];

    return (
        <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
            {commodities.map((item) => {
                const info = data.data[item.key] as MarketData;

                if (!info || 'error' in info) {
                    return (
                        <div key={item.key} className="glass-card rounded-xl p-5">
                            <p className="text-xs font-medium text-gray-400 dark:text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
                                <span>{item.icon}</span> {item.name}
                            </p>
                            <p className="text-gray-400 mt-2 text-sm">—</p>
                        </div>
                    );
                }

                const isPositive = info.change_percent >= 0;
                const isArs = info.currency === 'ARS';

                return (
                    <div key={item.key} className="glass-card rounded-xl p-5 hover:scale-[1.02] transition-transform duration-200">
                        <p className="text-xs font-medium text-gray-400 dark:text-gray-500 uppercase tracking-wider flex items-center gap-1.5">
                            <span>{item.icon}</span> {item.name}
                        </p>

                        <p className="text-xl font-bold font-mono text-gray-900 dark:text-white mt-2">
                            {isArs ? '$' : 'US$'}
                            {info.price.toLocaleString('es-AR', { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
                        </p>

                        <div className={`mt-1.5 text-xs font-mono font-semibold flex items-center gap-0.5 ${isPositive ? 'text-green-500' : 'text-red-500'}`}>
                            <span>{isPositive ? '▲' : '▼'}</span>
                            <span>{Math.abs(info.change_percent).toFixed(2)}%</span>
                        </div>
                    </div>
                );
            })}
        </div>
    );
}
