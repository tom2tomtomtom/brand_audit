'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Brain, 
  Eye, 
  Users, 
  TrendingUp, 
  ArrowLeft,
  Download,
  RefreshCw
} from 'lucide-react';
import { formatRelativeTime } from '@/lib/utils';
import toast from 'react-hot-toast';

interface AnalysisResultsProps {
  brandId: string;
  onBack?: () => void;
}

interface AnalysisData {
  brand: {
    id: string;
    name: string;
    websiteUrl: string;
    industry?: string;
    project: {
      id: string;
      name: string;
    };
  };
  analyses: Record<string, any>;
  history: any[];
}

export function AnalysisResults({ brandId, onBack }: AnalysisResultsProps) {
  const [data, setData] = useState<AnalysisData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAnalyses();
  }, [brandId]);

  const fetchAnalyses = async () => {
    try {
      setLoading(true);
      const response = await fetch(`/api/brands/${brandId}/analyses`);
      
      if (!response.ok) {
        throw new Error('Failed to fetch analyses');
      }

      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load analyses');
    } finally {
      setLoading(false);
    }
  };

  const getAnalysisIcon = (type: string) => {
    switch (type) {
      case 'positioning':
        return <Brain className="h-5 w-5" />;
      case 'visual':
        return <Eye className="h-5 w-5" />;
      case 'competitive':
        return <TrendingUp className="h-5 w-5" />;
      case 'sentiment':
        return <Users className="h-5 w-5" />;
      default:
        return <Brain className="h-5 w-5" />;
    }
  };

  const getAnalysisTitle = (type: string) => {
    switch (type) {
      case 'positioning':
        return 'Brand Positioning';
      case 'visual':
        return 'Visual Identity';
      case 'competitive':
        return 'Competitive Analysis';
      case 'sentiment':
        return 'Sentiment Analysis';
      default:
        return type.charAt(0).toUpperCase() + type.slice(1);
    }
  };

  const renderAnalysisContent = (type: string, analysis: any) => {
    if (!analysis.results) return <p className="text-gray-500">No results available</p>;

    const results = analysis.results;

    switch (type) {
      case 'positioning':
        return (
          <div className="space-y-4">
            <div>
              <h4 className="font-medium mb-2">Brand Voice</h4>
              <p className="text-sm text-gray-600">{results.brandVoice}</p>
            </div>
            <div>
              <h4 className="font-medium mb-2">Value Proposition</h4>
              <p className="text-sm text-gray-600">{results.valueProposition}</p>
            </div>
            <div>
              <h4 className="font-medium mb-2">Target Audience</h4>
              <div className="flex flex-wrap gap-2">
                {results.targetAudience?.map((audience: string, index: number) => (
                  <Badge key={index} variant="outline">{audience}</Badge>
                ))}
              </div>
            </div>
            <div>
              <h4 className="font-medium mb-2">Key Messages</h4>
              <ul className="text-sm text-gray-600 space-y-1">
                {results.keyMessages?.map((message: string, index: number) => (
                  <li key={index}>• {message}</li>
                ))}
              </ul>
            </div>
          </div>
        );

      case 'visual':
        return (
          <div className="space-y-4">
            <div>
              <h4 className="font-medium mb-2">Visual Style</h4>
              <p className="text-sm text-gray-600">{results.visualStyle}</p>
            </div>
            <div>
              <h4 className="font-medium mb-2">Color Palette</h4>
              <div className="flex flex-wrap gap-2">
                {results.colorPalette?.map((color: string, index: number) => (
                  <div key={index} className="flex items-center space-x-2">
                    <div 
                      className="w-4 h-4 rounded border"
                      style={{ backgroundColor: color }}
                    />
                    <span className="text-xs text-gray-600">{color}</span>
                  </div>
                ))}
              </div>
            </div>
            <div>
              <h4 className="font-medium mb-2">Typography</h4>
              <div className="flex flex-wrap gap-2">
                {results.typography?.map((font: string, index: number) => (
                  <Badge key={index} variant="outline">{font}</Badge>
                ))}
              </div>
            </div>
            {results.consistencyScore && (
              <div>
                <h4 className="font-medium mb-2">Consistency Score</h4>
                <div className="flex items-center space-x-2">
                  <div className="flex-1 bg-gray-200 rounded-full h-2">
                    <div 
                      className="bg-primary h-2 rounded-full"
                      style={{ width: `${results.consistencyScore}%` }}
                    />
                  </div>
                  <span className="text-sm font-medium">{results.consistencyScore}%</span>
                </div>
              </div>
            )}
          </div>
        );

      case 'competitive':
        return (
          <div className="space-y-4">
            <div>
              <h4 className="font-medium mb-2">Market Position</h4>
              <p className="text-sm text-gray-600">{results.marketPosition}</p>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-medium mb-2 text-green-700">Strengths</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {results.strengths?.map((strength: string, index: number) => (
                    <li key={index}>• {strength}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-medium mb-2 text-red-700">Weaknesses</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {results.weaknesses?.map((weakness: string, index: number) => (
                    <li key={index}>• {weakness}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-medium mb-2 text-blue-700">Opportunities</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {results.opportunities?.map((opportunity: string, index: number) => (
                    <li key={index}>• {opportunity}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h4 className="font-medium mb-2 text-orange-700">Threats</h4>
                <ul className="text-sm text-gray-600 space-y-1">
                  {results.threats?.map((threat: string, index: number) => (
                    <li key={index}>• {threat}</li>
                  ))}
                </ul>
              </div>
            </div>
          </div>
        );

      case 'sentiment':
        return (
          <div className="space-y-4">
            <div>
              <h4 className="font-medium mb-2">Overall Sentiment</h4>
              <Badge 
                className={
                  results.overallSentiment === 'positive' ? 'bg-green-100 text-green-800' :
                  results.overallSentiment === 'negative' ? 'bg-red-100 text-red-800' :
                  'bg-gray-100 text-gray-800'
                }
              >
                {results.overallSentiment}
              </Badge>
            </div>
            <div>
              <h4 className="font-medium mb-2">Brand Perception</h4>
              <p className="text-sm text-gray-600">{results.brandPerception}</p>
            </div>
            <div>
              <h4 className="font-medium mb-2">Emotional Tone</h4>
              <div className="flex flex-wrap gap-2">
                {results.emotionalTone?.map((tone: string, index: number) => (
                  <Badge key={index} variant="outline">{tone}</Badge>
                ))}
              </div>
            </div>
          </div>
        );

      default:
        return (
          <div className="text-sm text-gray-600">
            <pre className="whitespace-pre-wrap">{JSON.stringify(results, null, 2)}</pre>
          </div>
        );
    }
  };

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {[1, 2, 3, 4].map((i) => (
              <div key={i} className="h-64 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600 mb-4">{error}</p>
        <Button onClick={fetchAnalyses}>
          <RefreshCw className="h-4 w-4 mr-2" />
          Retry
        </Button>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-600">No analysis data available</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          {onBack && (
            <Button variant="ghost" size="sm" onClick={onBack}>
              <ArrowLeft className="h-4 w-4" />
            </Button>
          )}
          <div>
            <h1 className="text-2xl font-bold">{data.brand.name} Analysis</h1>
            <p className="text-gray-600">
              {data.brand.project.name} • {data.brand.websiteUrl}
            </p>
          </div>
        </div>
        <div className="flex space-x-2">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export
          </Button>
          <Button variant="outline" size="sm" onClick={fetchAnalyses}>
            <RefreshCw className="h-4 w-4 mr-2" />
            Refresh
          </Button>
        </div>
      </div>

      {/* Analysis Results */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {Object.entries(data.analyses).map(([type, analysis]) => (
          <Card key={type}>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-2">
                  {getAnalysisIcon(type)}
                  <CardTitle className="text-lg">{getAnalysisTitle(type)}</CardTitle>
                </div>
                <div className="flex items-center space-x-2">
                  <Badge 
                    className={
                      analysis.status === 'completed' ? 'bg-green-100 text-green-800' :
                      analysis.status === 'failed' ? 'bg-red-100 text-red-800' :
                      'bg-blue-100 text-blue-800'
                    }
                  >
                    {analysis.status}
                  </Badge>
                  {analysis.confidence_score && (
                    <Badge variant="outline">
                      {Math.round(analysis.confidence_score * 100)}% confidence
                    </Badge>
                  )}
                </div>
              </div>
              <CardDescription>
                Analyzed {formatRelativeTime(analysis.created_at)}
              </CardDescription>
            </CardHeader>
            <CardContent>
              {renderAnalysisContent(type, analysis)}
            </CardContent>
          </Card>
        ))}
      </div>

      {Object.keys(data.analyses).length === 0 && (
        <div className="text-center py-12">
          <Brain className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No analyses yet</h3>
          <p className="text-gray-600">
            Run an analysis on this brand to see insights here
          </p>
        </div>
      )}
    </div>
  );
}
