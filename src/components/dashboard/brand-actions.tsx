'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { 
  Play, 
  Brain, 
  FileText, 
  Download,
  MoreHorizontal,
  AlertCircle,
  CheckCircle,
  Clock,
  Loader2
} from 'lucide-react';
import { Brand } from '@/types';
import toast from 'react-hot-toast';

interface BrandActionsProps {
  brand: Brand;
  onUpdate?: () => void;
}

export function BrandActions({ brand, onUpdate }: BrandActionsProps) {
  const [scrapingLoading, setScrapingLoading] = useState(false);
  const [analysisLoading, setAnalysisLoading] = useState(false);

  const handleStartScraping = async () => {
    setScrapingLoading(true);
    
    try {
      const response = await fetch('/api/scraper', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          brandId: brand.id,
          config: {
            maxPages: 10,
            includeImages: true,
            includeDocuments: true,
            respectRobots: true,
            delayBetweenRequests: 2000,
          },
        }),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success('Scraping started successfully!');
        onUpdate?.();
      } else {
        toast.error(data.error || 'Failed to start scraping');
      }
    } catch (error) {
      toast.error('Failed to start scraping');
      console.error('Scraping error:', error);
    } finally {
      setScrapingLoading(false);
    }
  };

  const handleStartAnalysis = async () => {
    setAnalysisLoading(true);
    
    try {
      const response = await fetch('/api/analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          brandId: brand.id,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success('Analysis started successfully!');
        onUpdate?.();
      } else {
        toast.error(data.error || 'Failed to start analysis');
      }
    } catch (error) {
      toast.error('Failed to start analysis');
      console.error('Analysis error:', error);
    } finally {
      setAnalysisLoading(false);
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />;
      case 'in_progress':
        return <Loader2 className="h-4 w-4 text-blue-500 animate-spin" />;
      case 'failed':
        return <AlertCircle className="h-4 w-4 text-red-500" />;
      default:
        return <Clock className="h-4 w-4 text-gray-400" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'in_progress':
        return 'bg-blue-100 text-blue-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-lg">{brand.name}</CardTitle>
            <CardDescription>
              <a 
                href={brand.websiteUrl} 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-primary hover:underline"
              >
                {brand.websiteUrl}
              </a>
            </CardDescription>
          </div>
          <Button variant="ghost" size="sm">
            <MoreHorizontal className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Status Overview */}
          <div className="grid grid-cols-2 gap-4">
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                {getStatusIcon(brand.scrapingStatus)}
                <span className="text-sm font-medium">Scraping</span>
              </div>
              <Badge className={getStatusColor(brand.scrapingStatus)}>
                {brand.scrapingStatus.replace('_', ' ')}
              </Badge>
            </div>
            <div className="space-y-2">
              <div className="flex items-center space-x-2">
                {getStatusIcon(brand.analysisStatus)}
                <span className="text-sm font-medium">Analysis</span>
              </div>
              <Badge className={getStatusColor(brand.analysisStatus)}>
                {brand.analysisStatus.replace('_', ' ')}
              </Badge>
            </div>
          </div>

          {/* Actions */}
          <div className="space-y-2">
            <Button
              onClick={handleStartScraping}
              disabled={scrapingLoading || brand.scrapingStatus === 'in_progress'}
              className="w-full"
              variant={brand.scrapingStatus === 'completed' ? 'outline' : 'default'}
            >
              {scrapingLoading ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Play className="h-4 w-4 mr-2" />
              )}
              {brand.scrapingStatus === 'completed' ? 'Re-scrape Assets' : 'Start Scraping'}
            </Button>

            <Button
              onClick={handleStartAnalysis}
              disabled={
                analysisLoading || 
                brand.analysisStatus === 'in_progress' ||
                brand.scrapingStatus !== 'completed'
              }
              className="w-full"
              variant={brand.analysisStatus === 'completed' ? 'outline' : 'default'}
            >
              {analysisLoading ? (
                <Loader2 className="h-4 w-4 mr-2 animate-spin" />
              ) : (
                <Brain className="h-4 w-4 mr-2" />
              )}
              {brand.analysisStatus === 'completed' ? 'Re-run Analysis' : 'Start Analysis'}
            </Button>

            {brand.analysisStatus === 'completed' && (
              <Button
                variant="outline"
                className="w-full"
                onClick={() => {
                  window.open(`/dashboard/brands/${brand.id}/analysis`, '_blank');
                }}
              >
                <FileText className="h-4 w-4 mr-2" />
                View Results
              </Button>
            )}
          </div>

          {/* Asset Count */}
          {brand.assets && brand.assets.length > 0 && (
            <div className="text-sm text-gray-600">
              <span className="font-medium">{brand.assets.length}</span> assets collected
            </div>
          )}

          {/* Industry Tag */}
          {brand.industry && (
            <Badge variant="outline" className="w-fit">
              {brand.industry}
            </Badge>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
