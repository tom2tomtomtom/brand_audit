'use client';

import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import { BrandActions } from './brand-actions';
import { AddBrandModal } from './add-brand-modal';
import {
  FileText,
  Download,
  Plus,
  BarChart3,
  Users,
  Globe,
  TrendingUp
} from 'lucide-react';
import { Project, Brand } from '@/types';
import toast from 'react-hot-toast';

interface ProjectDashboardProps {
  project: Project;
}

export function ProjectDashboard({ project }: ProjectDashboardProps) {
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loading, setLoading] = useState(true);
  const [generatingPresentation, setGeneratingPresentation] = useState(false);
  const [showAddBrandModal, setShowAddBrandModal] = useState(false);

  useEffect(() => {
    fetchBrands();
  }, [project.id]);

  const fetchBrands = async () => {
    try {
      const response = await fetch(`/api/projects/${project.id}/brands`);
      const data = await response.json();
      
      if (response.ok) {
        setBrands(data.brands || []);
      } else {
        toast.error('Failed to fetch brands');
      }
    } catch (error) {
      toast.error('Failed to fetch brands');
      console.error('Fetch brands error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePresentation = async () => {
    setGeneratingPresentation(true);
    
    try {
      const response = await fetch('/api/presentations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          projectId: project.id,
          templateId: 'competitive-analysis',
        }),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success('Presentation generated successfully!');
        // Open presentation in new tab
        window.open(`/dashboard/presentations/${data.presentationId}`, '_blank');
      } else {
        toast.error(data.error || 'Failed to generate presentation');
      }
    } catch (error) {
      toast.error('Failed to generate presentation');
      console.error('Presentation generation error:', error);
    } finally {
      setGeneratingPresentation(false);
    }
  };

  const handleBulkScraping = async () => {
    try {
      const response = await fetch(`/api/projects/${project.id}/bulk-scrape`, {
        method: 'POST',
      });

      const data = await response.json();

      if (response.ok) {
        toast.success(`Started scraping ${data.brands} brands. This may take several minutes.`);
        // Refresh brands every 30 seconds to show progress
        const interval = setInterval(() => {
          fetchBrands();
        }, 30000);

        // Clear interval after 10 minutes
        setTimeout(() => clearInterval(interval), 600000);
      } else {
        toast.error(data.error || 'Failed to start bulk scraping');
      }
    } catch (error) {
      toast.error('Failed to start bulk scraping');
      console.error('Bulk scraping error:', error);
    }
  };

  const handleBulkAnalysis = async () => {
    try {
      const response = await fetch(`/api/projects/${project.id}/bulk-analyze`, {
        method: 'POST',
      });

      const data = await response.json();

      if (response.ok) {
        toast.success(`Started analyzing ${data.brands} brands. This may take several minutes.`);
        // Refresh brands every 30 seconds to show progress
        const interval = setInterval(() => {
          fetchBrands();
        }, 30000);

        // Clear interval after 15 minutes
        setTimeout(() => clearInterval(interval), 900000);
      } else {
        toast.error(data.error || 'Failed to start bulk analysis');
      }
    } catch (error) {
      toast.error('Failed to start bulk analysis');
      console.error('Bulk analysis error:', error);
    }
  };

  const handleExportData = async () => {
    try {
      // Create download link for JSON export
      const link = document.createElement('a');
      link.href = `/api/projects/${project.id}/export?format=json`;
      link.download = `${project.name}_export.json`;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      toast.success('Export started');
    } catch (error) {
      toast.error('Failed to export data');
      console.error('Export error:', error);
    }
  };

  const getProjectStats = () => {
    const totalBrands = brands.length;
    const completedScraping = brands.filter(b => b.scrapingStatus === 'completed').length;
    const completedAnalysis = brands.filter(b => b.analysisStatus === 'completed').length;
    const totalAssets = brands.reduce((sum, b) => sum + (b.assets?.length || 0), 0);

    return {
      totalBrands,
      completedScraping,
      completedAnalysis,
      totalAssets,
      scrapingProgress: totalBrands > 0 ? (completedScraping / totalBrands) * 100 : 0,
      analysisProgress: totalBrands > 0 ? (completedAnalysis / totalBrands) * 100 : 0,
    };
  };

  const stats = getProjectStats();

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-64 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Project Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">{project.name}</h1>
          {project.description && (
            <p className="text-gray-600 mt-2">{project.description}</p>
          )}
        </div>
        <div className="flex space-x-2">
          <Button
            onClick={handleGeneratePresentation}
            disabled={generatingPresentation || stats.completedAnalysis === 0}
          >
            <FileText className="h-4 w-4 mr-2" />
            Generate Report
          </Button>
          <Button variant="outline" onClick={() => setShowAddBrandModal(true)}>
            <Plus className="h-4 w-4 mr-2" />
            Add Brand
          </Button>
        </div>
      </div>

      {/* Project Stats */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Total Brands</CardTitle>
            <Globe className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalBrands}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Assets Collected</CardTitle>
            <BarChart3 className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.totalAssets}</div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Scraping Progress</CardTitle>
            <TrendingUp className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completedScraping}/{stats.totalBrands}</div>
            <Progress value={stats.scrapingProgress} className="mt-2" />
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Analysis Progress</CardTitle>
            <Users className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{stats.completedAnalysis}/{stats.totalBrands}</div>
            <Progress value={stats.analysisProgress} className="mt-2" />
          </CardContent>
        </Card>
      </div>

      {/* Brands Grid */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Brands</h2>
        {brands.length === 0 ? (
          <Card>
            <CardContent className="flex flex-col items-center justify-center py-12">
              <Globe className="h-12 w-12 text-gray-400 mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">No brands yet</h3>
              <p className="text-gray-600 text-center mb-4">
                Add brands to start analyzing their digital presence and competitive positioning.
              </p>
              <Button onClick={() => setShowAddBrandModal(true)}>
                <Plus className="h-4 w-4 mr-2" />
                Add Your First Brand
              </Button>
            </CardContent>
          </Card>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {brands.map((brand) => (
              <BrandActions
                key={brand.id}
                brand={brand}
                onUpdate={fetchBrands}
              />
            ))}
          </div>
        )}
      </div>

      {/* Quick Actions */}
      {brands.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>
              Perform bulk operations on all brands in this project
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex space-x-2">
              <Button
                variant="outline"
                onClick={handleBulkScraping}
                disabled={brands.every(b => b.scrapingStatus === 'in_progress') || brands.length === 0}
              >
                Scrape All Brands
              </Button>
              <Button
                variant="outline"
                onClick={handleBulkAnalysis}
                disabled={
                  brands.every(b => b.analysisStatus === 'in_progress') ||
                  brands.filter(b => b.scrapingStatus === 'completed').length === 0
                }
              >
                Analyze All Brands
              </Button>
              <Button
                variant="outline"
                onClick={handleExportData}
              >
                <Download className="h-4 w-4 mr-2" />
                Export Data
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Add Brand Modal */}
      <AddBrandModal
        open={showAddBrandModal}
        onClose={() => setShowAddBrandModal(false)}
        projectId={project.id}
        onSuccess={() => {
          setShowAddBrandModal(false);
          fetchBrands();
        }}
      />
    </div>
  );
}
