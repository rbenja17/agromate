/**
 * NewsCard component displays a single news article with sentiment analysis.
 */

import { Article } from '@/types';
import SentimentBadge from './SentimentBadge';

interface NewsCardProps {
    article: Article;
}

export default function NewsCard({ article }: NewsCardProps) {
    // Format date
    const formatDate = (dateString: string | null) => {
        if (!dateString) return 'Fecha desconocida';

        const date = new Date(dateString);
        return new Intl.DateTimeFormat('es-AR', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(date);
    };

    return (
        <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 p-6 border border-gray-200 dark:border-gray-700">
            {/* Header with source and date */}
            <div className="flex items-center justify-between mb-3">
                <span className="text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-900/30 px-2 py-1 rounded">
                    {article.source}
                </span>
                <span className="text-xs text-gray-500 dark:text-gray-400">
                    {formatDate(article.published_at)}
                </span>
            </div>

            {/* Title */}
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-3 line-clamp-2 hover:text-blue-600 dark:hover:text-blue-400 cursor-pointer">
                <a href={article.url} target="_blank" rel="noopener noreferrer">
                    {article.title}
                </a>
            </h3>

            {/* Sentiment badge */}
            <div className="flex items-center justify-between">
                <SentimentBadge
                    sentiment={article.sentiment}
                    confidence={article.confidence}
                />

                {/* Link to article */}
                <a
                    href={article.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-sm text-blue-600 hover:text-blue-800 font-medium flex items-center gap-1"
                >
                    Leer más
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                    </svg>
                </a>
            </div>

            {/* Commodity tag (badge visual con emoji) */}
            {article.commodity && article.commodity !== 'GENERAL' && (
                <div className="mt-3 pt-3 border-t border-gray-100">
                    <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium bg-amber-50 dark:bg-amber-900/30 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-700">
                        {article.commodity === 'SOJA' && '🌱'}
                        {article.commodity === 'MAÍZ' && '🌽'}
                        {article.commodity === 'TRIGO' && '🌾'}
                        {article.commodity === 'GIRASOL' && '🌻'}
                        {article.commodity === 'CEBADA' && '🍺'}
                        {article.commodity === 'SORGO' && '🌿'}
                        {article.commodity}
                    </span>
                </div>
            )}
        </div>
    );
}
