/**
 * SentimentBadge component displays a colored badge based on sentiment type.
 */

import { SentimentType } from '@/types';

interface SentimentBadgeProps {
    sentiment: SentimentType | null;
    confidence?: number | null;
}

export default function SentimentBadge({ sentiment, confidence }: SentimentBadgeProps) {
    if (!sentiment) {
        return (
            <span className="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600">
                Sin análisis
            </span>
        );
    }

    const getStyles = () => {
        switch (sentiment) {
            case 'ALCISTA':
                return {
                    bg: 'bg-green-100',
                    text: 'text-green-800',
                    icon: '↑',
                    label: 'Alcista'
                };
            case 'BAJISTA':
                return {
                    bg: 'bg-red-100',
                    text: 'text-red-800',
                    icon: '↓',
                    label: 'Bajista'
                };
            case 'NEUTRAL':
                return {
                    bg: 'bg-gray-100',
                    text: 'text-gray-800',
                    icon: '→',
                    label: 'Neutral'
                };
            default:
                return {
                    bg: 'bg-gray-100',
                    text: 'text-gray-600',
                    icon: '?',
                    label: 'Desconocido'
                };
        }
    };

    const styles = getStyles();

    return (
        <span className={`inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-semibold ${styles.bg} ${styles.text}`}>
            <span className="text-sm">{styles.icon}</span>
            {styles.label}
            {confidence !== null && confidence !== undefined && (
                <span className="ml-1 opacity-75">
                    ({(confidence * 100).toFixed(0)}%)
                </span>
            )}
        </span>
    );
}
