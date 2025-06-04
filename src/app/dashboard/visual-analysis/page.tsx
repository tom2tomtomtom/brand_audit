'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/components/providers';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { VisualBrandGallery } from '@/components/brand/visual-brand-gallery';
import { ColorPaletteAnalysis } from '@/components/brand/color-palette-analysis';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { 
  Palette, 
  Eye, 
  BarChart3, 
  TrendingUp, 
  Sparkles,
  Image as ImageIcon,
  Type,
  Monitor
} from 'lucide-react';
import { VisualBrandData } from '@/services/scraper';

interface Brand {
  id: string;
  name: string;
  websiteUrl: string;
  industry?: string;
  visualData?: VisualBrandData;
}

export default function VisualAnalysisPage() {
  const { currentOrganization } = useAuth();
  const [brands, setBrands] = useState<Brand[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('gallery');

  useEffect(() => {
    fetchBrands();
  }, [currentOrganization]);

  const fetchBrands = async () => {
    try {
      const response = await fetch('/api/brands');
      const data = await response.json();

      if (response.ok) {
        setBrands(data.brands || []);
      } else {
        console.error('Failed to fetch brands:', data.error);
      }
    } catch (error) {
      console.error('Error fetching brands:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAnalyzeBrand = (brandId: string) => {
    // TODO: Trigger brand analysis
    console.log('Analyzing brand:', brandId);
  };

  const handleViewBrandDetails = (brandId: string) => {
    // TODO: Navigate to brand details
    console.log('Viewing brand details:', brandId);
  };

  // Calculate visual analytics
  const getVisualStats = () => {
    const brandsWithVisualData = brands.filter(b => b.visualData);
    const totalColors = brandsWithVisualData.reduce((sum, b) => 
      sum + (b.visualData?.colorPalette.primary.length || 0) + 
            (b.visualData?.colorPalette.secondary.length || 0), 0
    );
    const totalLogos = brandsWithVisualData.reduce((sum, b) => 
      sum + (b.visualData?.logos.variations.length || 0), 0
    );
    const totalFonts = brandsWithVisualData.reduce((sum, b) => 
      sum + (b.visualData?.typography.headingFonts.length || 0) + 
            (b.visualData?.typography.bodyFonts.length || 0), 0
    );

    return {
      totalBrands: brands.length,
      analyzedBrands: brandsWithVisualData.length,
      totalColors,
      totalLogos,
      totalFonts,
      analysisRate: brands.length > 0 ? Math.round((brandsWithVisualData.length / brands.length) * 100) : 0
    };
  };

  const stats = getVisualStats();

  if (loading) {
    return (
      <DashboardLayout>
        <div className="space-y-6">
          <div className="h-8 bg-gray-200 rounded w-64 animate-pulse"></div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="h-24 bg-gray-200 rounded animate-pulse"></div>
            ))}
          </div>
          <div className="h-96 bg-gray-200 rounded animate-pulse"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 flex items-center">
              <Eye className="h-8 w-8 mr-3 text-blue-600" />
              Visual Brand Analysis
            </h1>
            <p className="text-gray-600 mt-1">
              Explore visual elements, colors, and design patterns across your brand portfolio
            </p>
          </div>
          <Button>
            <Sparkles className="h-4 w-4 mr-2" />
            Generate Report
          </Button>
        </div>

        {/* Visual Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-blue-100 rounded-lg">
                  <Eye className="h-6 w-6 text-blue-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700">Brands Analyzed</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stats.analyzedBrands}/{stats.totalBrands}
                  </p>
                  <p className="text-xs text-gray-500">{stats.analysisRate}% complete</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-purple-100 rounded-lg">
                  <Palette className="h-6 w-6 text-purple-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700">Colors Extracted</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalColors}</p>
                  <p className="text-xs text-gray-500">Unique color palette</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-green-100 rounded-lg">
                  <ImageIcon className="h-6 w-6 text-green-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700">Logo Variations</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalLogos}</p>
                  <p className="text-xs text-gray-500">Brand assets found</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-orange-100 rounded-lg">
                  <Type className="h-6 w-6 text-orange-600" />
                </div>
                <div>
                  <p className="text-sm font-medium text-gray-700">Typography</p>
                  <p className="text-2xl font-bold text-gray-900">{stats.totalFonts}</p>
                  <p className="text-xs text-gray-500">Font families detected</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs value={activeTab} onValueChange={setActiveTab} className="space-y-6">
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="gallery" className="flex items-center space-x-2">
              <Monitor className="h-4 w-4" />
              <span>Brand Gallery</span>
            </TabsTrigger>
            <TabsTrigger value="colors" className="flex items-center space-x-2">
              <Palette className="h-4 w-4" />
              <span>Color Analysis</span>
            </TabsTrigger>
            <TabsTrigger value="comparison" className="flex items-center space-x-2">
              <BarChart3 className="h-4 w-4" />
              <span>Comparison</span>
            </TabsTrigger>
            <TabsTrigger value="trends" className="flex items-center space-x-2">
              <TrendingUp className="h-4 w-4" />
              <span>Trends</span>
            </TabsTrigger>
          </TabsList>

          <TabsContent value="gallery" className="space-y-6">
            <VisualBrandGallery
              brands={brands}
              loading={loading}
              onAnalyzeBrand={handleAnalyzeBrand}
              onViewBrandDetails={handleViewBrandDetails}
            />
          </TabsContent>

          <TabsContent value="colors" className="space-y-6">
            <ColorPaletteAnalysis brands={brands} />
          </TabsContent>

          <TabsContent value="comparison" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <BarChart3 className="h-5 w-5 mr-2" />
                  Brand Comparison
                </CardTitle>
                <CardDescription>
                  Compare visual elements across different brands
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center text-gray-500">
                  <div className="text-center">
                    <BarChart3 className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                    <p>Brand comparison tool coming soon</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="trends" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle className="flex items-center">
                  <TrendingUp className="h-5 w-5 mr-2" />
                  Visual Trends
                </CardTitle>
                <CardDescription>
                  Discover emerging design trends in your industry
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="h-64 flex items-center justify-center text-gray-500">
                  <div className="text-center">
                    <TrendingUp className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                    <p>Trend analysis coming soon</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  );
}
