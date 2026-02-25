"use client";

import React, { useEffect, useRef } from 'react';

interface AdSlotProps {
    variant: 'banner' | 'sponsored';
}

declare global {
    interface Window {
        adsbygoogle: any[];
    }
}

function AdUnit({ format, layout, style }: { format: string; layout?: string; style: React.CSSProperties }) {
    const adRef = useRef<HTMLModElement>(null);
    const pushed = useRef(false);

    useEffect(() => {
        if (adRef.current && !pushed.current) {
            try {
                (window.adsbygoogle = window.adsbygoogle || []).push({});
                pushed.current = true;
            } catch (e) {
                // AdSense not loaded yet or ad blocker active
            }
        }
    }, []);

    return (
        <ins
            ref={adRef}
            className="adsbygoogle"
            style={style}
            data-ad-client="ca-pub-1706326824835689"
            data-ad-format={format}
            {...(layout ? { 'data-ad-layout': layout } : {})}
            data-full-width-responsive="true"
        />
    );
}

export default function ResponsiveAd({ variant }: AdSlotProps) {
    if (variant === 'banner') {
        return (
            <div className="glass-card rounded-lg overflow-hidden my-4 min-h-[90px] flex items-center justify-center">
                <AdUnit
                    format="horizontal"
                    style={{ display: 'block', width: '100%', height: '90px' }}
                />
            </div>
        );
    }

    // Sponsored card — in-feed ad mimicking NewsCard style
    return (
        <div className="glass-card rounded-xl overflow-hidden relative min-h-[200px]">
            <div className="absolute top-3 right-3 z-10">
                <span className="text-[10px] font-medium text-gray-400 dark:text-gray-500 uppercase tracking-wider px-2 py-0.5 rounded bg-gray-100 dark:bg-white/5 border border-gray-200 dark:border-white/10">
                    Anuncio
                </span>
            </div>
            <AdUnit
                format="fluid"
                layout="in-article"
                style={{ display: 'block', textAlign: 'center' }}
            />
        </div>
    );
}
