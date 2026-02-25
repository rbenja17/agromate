"use client";

import React from 'react';

interface AdSlotProps {
    variant: 'banner' | 'sponsored';
}

export default function ResponsiveAd({ variant }: AdSlotProps) {
    if (variant === 'banner') {
        return (
            <div className="glass-card rounded-lg p-3 flex items-center justify-center text-center my-4">
                <div className="flex items-center gap-3">
                    <span className="text-[10px] font-medium text-gray-400 dark:text-gray-500 uppercase tracking-wider px-2 py-0.5 rounded bg-gray-100 dark:bg-gray-800">
                        Ad
                    </span>
                    <div className="h-[50px] flex items-center justify-center">
                        <p className="text-sm text-gray-500 dark:text-gray-400">
                            📢 Espacio publicitario — <a href="mailto:contacto@agromate.com.ar" className="text-blue-500 hover:text-blue-400 underline">Anunciar aquí</a>
                        </p>
                    </div>
                </div>
            </div>
        );
    }

    // Sponsored card variant — mimics NewsCard style
    return (
        <div className="glass-card rounded-xl p-5 flex flex-col justify-between relative overflow-hidden group hover:border-blue-500/30 transition-all duration-300">
            {/* Anuncio tag */}
            <div className="absolute top-3 right-3">
                <span className="text-[10px] font-medium text-gray-400 dark:text-gray-500 uppercase tracking-wider px-2 py-0.5 rounded bg-gray-100 dark:bg-white/5 border border-gray-200 dark:border-white/10">
                    Anuncio
                </span>
            </div>

            <div>
                <div className="flex items-center gap-2 mb-3">
                    <span className="text-xs font-medium text-blue-500 dark:text-blue-400 bg-blue-50 dark:bg-blue-500/10 px-2 py-0.5 rounded">
                        Sponsor
                    </span>
                </div>
                <h3 className="text-base font-semibold text-gray-900 dark:text-white leading-snug mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                    Potenciá tu campo con tecnología de precisión
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
                    Soluciones inteligentes para maximizar tu rendimiento por hectárea. Conocé más.
                </p>
            </div>
            <div className="mt-4 pt-3 border-t border-gray-100 dark:border-white/5">
                <a href="#" className="text-sm font-medium text-blue-600 dark:text-blue-400 hover:underline">
                    Saber más →
                </a>
            </div>
        </div>
    );
}
