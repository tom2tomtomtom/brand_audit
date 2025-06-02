'use client';

import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  Download, 
  ExternalLink, 
  ArrowLeft,
  FileText,
  Calendar,
  User
} from 'lucide-react';
import { formatRelativeTime } from '@/lib/utils';
import toast from 'react-hot-toast';

interface PresentationViewerProps {
  presentation: {
    id: string;
    name: string;
    template: string;
    status: string;
    export_url?: string;
    slides_data?: any;
    created_at: string;
    updated_at: string;
    projects: {
      id: string;
      name: string;
    };
  };
}

export function PresentationViewer({ presentation }: PresentationViewerProps) {
  const [downloading, setDownloading] = useState(false);
  const [generatingPDF, setGeneratingPDF] = useState(false);

  const handleDownload = async () => {
    if (!presentation.export_url) {
      toast.error('Presentation file not available');
      return;
    }

    setDownloading(true);
    try {
      // Create download link
      const link = document.createElement('a');
      link.href = `/api/presentations/${presentation.id}/download`;
      link.download = `${presentation.name}.html`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      
      toast.success('Download started');
    } catch (error) {
      toast.error('Failed to download presentation');
      console.error('Download error:', error);
    } finally {
      setDownloading(false);
    }
  };

  const handleViewFullscreen = () => {
    if (presentation.export_url) {
      window.open(`/api/presentations/${presentation.id}/view`, '_blank');
    } else {
      toast.error('Presentation not ready for viewing');
    }
  };

  const handleGeneratePDF = async () => {
    setGeneratingPDF(true);
    try {
      const response = await fetch(`/api/presentations/${presentation.id}/pdf`, {
        method: 'POST',
      });

      if (response.ok) {
        toast.success('PDF generated successfully!');
        // Download the PDF
        const downloadLink = document.createElement('a');
        downloadLink.href = `/api/presentations/${presentation.id}/pdf`;
        downloadLink.download = `${presentation.name}.pdf`;
        document.body.appendChild(downloadLink);
        downloadLink.click();
        document.body.removeChild(downloadLink);
      } else {
        const data = await response.json();
        toast.error(data.error || 'Failed to generate PDF');
      }
    } catch (error) {
      toast.error('Failed to generate PDF');
      console.error('PDF generation error:', error);
    } finally {
      setGeneratingPDF(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800';
      case 'generating':
        return 'bg-blue-100 text-blue-800';
      case 'failed':
        return 'bg-red-100 text-red-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getTemplateDisplayName = (template: string) => {
    switch (template) {
      case 'competitive-analysis':
        return 'Competitive Analysis Report';
      case 'brand-audit':
        return 'Brand Audit Report';
      default:
        return template.replace('-', ' ').replace(/\b\w/g, l => l.toUpperCase());
    }
  };

  return (
    <div className="container mx-auto py-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={() => window.history.back()}
          >
            <ArrowLeft className="h-4 w-4" />
          </Button>
          <div>
            <h1 className="text-2xl font-bold">{presentation.name}</h1>
            <p className="text-gray-600">
              {presentation.projects.name} • {getTemplateDisplayName(presentation.template)}
            </p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <Badge className={getStatusColor(presentation.status)}>
            {presentation.status}
          </Badge>
        </div>
      </div>

      {/* Presentation Info */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center space-x-2">
            <FileText className="h-5 w-5" />
            <span>Presentation Details</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="flex items-center space-x-3">
              <Calendar className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-sm font-medium">Created</p>
                <p className="text-sm text-gray-600">
                  {formatRelativeTime(presentation.created_at)}
                </p>
              </div>
            </div>
            
            <div className="flex items-center space-x-3">
              <User className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-sm font-medium">Template</p>
                <p className="text-sm text-gray-600">
                  {getTemplateDisplayName(presentation.template)}
                </p>
              </div>
            </div>

            <div className="flex items-center space-x-3">
              <FileText className="h-4 w-4 text-gray-500" />
              <div>
                <p className="text-sm font-medium">Slides</p>
                <p className="text-sm text-gray-600">
                  {presentation.slides_data?.slides?.length || 'Unknown'} slides
                </p>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Actions */}
      <Card>
        <CardHeader>
          <CardTitle>Actions</CardTitle>
          <CardDescription>
            View, download, or share your presentation
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="flex flex-wrap gap-3">
            <Button
              onClick={handleViewFullscreen}
              disabled={presentation.status !== 'completed'}
            >
              <ExternalLink className="h-4 w-4 mr-2" />
              View Fullscreen
            </Button>
            
            <Button
              variant="outline"
              onClick={handleDownload}
              disabled={presentation.status !== 'completed' || downloading}
            >
              <Download className="h-4 w-4 mr-2" />
              {downloading ? 'Downloading...' : 'Download HTML'}
            </Button>

            <Button
              variant="outline"
              onClick={handleGeneratePDF}
              disabled={presentation.status !== 'completed' || generatingPDF}
            >
              <Download className="h-4 w-4 mr-2" />
              {generatingPDF ? 'Generating...' : 'Download PDF'}
            </Button>

            <Button
              variant="outline"
              onClick={() => {
                const url = `${window.location.origin}/dashboard/presentations/${presentation.id}`;
                navigator.clipboard.writeText(url);
                toast.success('Link copied to clipboard');
              }}
            >
              Share Link
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Slides Preview */}
      {presentation.slides_data?.slides && (
        <Card>
          <CardHeader>
            <CardTitle>Slides Overview</CardTitle>
            <CardDescription>
              Preview of slides in this presentation
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {presentation.slides_data.slides.map((slide: any, index: number) => (
                <div key={slide.id} className="border rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium">Slide {index + 1}</span>
                    <Badge variant="outline">{slide.type}</Badge>
                  </div>
                  <h4 className="font-medium text-sm mb-2">{slide.title}</h4>
                  <p className="text-xs text-gray-600">
                    Layout: {slide.layout}
                  </p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Status Messages */}
      {presentation.status === 'generating' && (
        <Card className="border-blue-200 bg-blue-50">
          <CardContent className="pt-6">
            <div className="flex items-center space-x-3">
              <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div>
              <p className="text-blue-800">
                Your presentation is being generated. This may take a few minutes.
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {presentation.status === 'failed' && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <p className="text-red-800">
              Presentation generation failed. Please try generating a new presentation.
            </p>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
