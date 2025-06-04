'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { 
  Palette, 
  Copy, 
  Download, 
  Eye, 
  Zap,
  TrendingUp,
  BarChart3,
  CheckCircle
} from 'lucide-react';
import { VisualBrandData } from '@/services/scraper';
import toast from 'react-hot-toast';

interface ColorPaletteAnalysisProps {
  brands: Array<{
    id: string;
    name: string;
    visualData?: VisualBrandData;
  }>;
}

interface ColorInfo {
  hex: string;
  name: string;
  usage: number;
  brands: string[];
  category: 'primary' | 'secondary' | 'accent';
}

export function ColorPaletteAnalysis({ brands }: ColorPaletteAnalysisProps) {
  const [selectedColor, setSelectedColor] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'palette' | 'comparison' | 'trends'>('palette');

  // Analyze color usage across all brands
  const analyzeColors = (): ColorInfo[] => {
    const colorMap = new Map<string, ColorInfo>();

    brands.forEach(brand => {
      if (!brand.visualData) return;

      const processColors = (colors: string[], category: 'primary' | 'secondary' | 'accent') => {
        colors.forEach(color => {
          if (colorMap.has(color)) {
            const existing = colorMap.get(color)!;
            existing.usage += 1;
            existing.brands.push(brand.name);
          } else {
            colorMap.set(color, {
              hex: color,
              name: getColorName(color),
              usage: 1,
              brands: [brand.name],
              category,
            });
          }
        });
      };

      processColors(brand.visualData.colorPalette.primary, 'primary');
      processColors(brand.visualData.colorPalette.secondary, 'secondary');
      processColors(brand.visualData.colorPalette.accent, 'accent');
    });

    return Array.from(colorMap.values()).sort((a, b) => b.usage - a.usage);
  };

  const getColorName = (hex: string): string => {
    // Simple color name mapping - in a real app, you'd use a color name library
    const colorNames: Record<string, string> = {
      '#000000': 'Black',
      '#ffffff': 'White',
      '#ff0000': 'Red',
      '#00ff00': 'Green',
      '#0000ff': 'Blue',
      '#ffff00': 'Yellow',
      '#ff00ff': 'Magenta',
      '#00ffff': 'Cyan',
    };

    return colorNames[hex.toLowerCase()] || hex.toUpperCase();
  };

  const getColorBrightness = (hex: string): number => {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);
    return (r * 299 + g * 587 + b * 114) / 1000;
  };

  const getContrastColor = (hex: string): string => {
    return getColorBrightness(hex) > 128 ? '#000000' : '#ffffff';
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard!');
  };

  const colorAnalysis = analyzeColors();
  const totalColors = colorAnalysis.length;
  const mostUsedColor = colorAnalysis[0];
  const colorTrends = colorAnalysis.slice(0, 10);

  const ColorSwatch = ({ color, size = 'md', showInfo = true }: { 
    color: ColorInfo; 
    size?: 'sm' | 'md' | 'lg';
    showInfo?: boolean;
  }) => {
    const sizeClasses = {
      sm: 'w-8 h-8',
      md: 'w-12 h-12',
      lg: 'w-16 h-16'
    };

    return (
      <div 
        className={`group relative cursor-pointer transition-all duration-200 hover:scale-110 ${
          selectedColor === color.hex ? 'ring-4 ring-blue-500 ring-offset-2' : ''
        }`}
        onClick={() => setSelectedColor(selectedColor === color.hex ? null : color.hex)}
      >
        <div
          className={`${sizeClasses[size]} rounded-lg border-2 border-white shadow-lg`}
          style={{ backgroundColor: color.hex }}
        />
        {showInfo && (
          <div className="absolute -bottom-8 left-1/2 transform -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity bg-black text-white text-xs px-2 py-1 rounded whitespace-nowrap z-10">
            {color.name}
          </div>
        )}
        {color.usage > 1 && (
          <Badge className="absolute -top-2 -right-2 text-xs min-w-[20px] h-5 flex items-center justify-center">
            {color.usage}
          </Badge>
        )}
      </div>
    );
  };

  const ColorDetails = ({ color }: { color: ColorInfo }) => (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <div
            className="w-6 h-6 rounded border"
            style={{ backgroundColor: color.hex }}
          />
          <span>{color.name}</span>
        </CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-sm font-medium text-gray-700">Hex Code</span>
            <div className="flex items-center space-x-2">
              <code className="bg-gray-100 px-2 py-1 rounded text-sm">{color.hex}</code>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => copyToClipboard(color.hex)}
              >
                <Copy className="h-4 w-4" />
              </Button>
            </div>
          </div>
          <div>
            <span className="text-sm font-medium text-gray-700">Usage</span>
            <p className="text-sm text-gray-600">{color.usage} brand{color.usage > 1 ? 's' : ''}</p>
          </div>
        </div>

        <div>
          <span className="text-sm font-medium text-gray-700">Used by</span>
          <div className="flex flex-wrap gap-1 mt-1">
            {color.brands.map((brand, index) => (
              <Badge key={index} variant="outline" className="text-xs">
                {brand}
              </Badge>
            ))}
          </div>
        </div>

        <div>
          <span className="text-sm font-medium text-gray-700">Category</span>
          <Badge className={`ml-2 ${
            color.category === 'primary' ? 'bg-blue-100 text-blue-800' :
            color.category === 'secondary' ? 'bg-green-100 text-green-800' :
            'bg-purple-100 text-purple-800'
          }`}>
            {color.category}
          </Badge>
        </div>
      </CardContent>
    </Card>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 flex items-center">
            <Palette className="h-6 w-6 mr-2" />
            Color Palette Analysis
          </h2>
          <p className="text-gray-600">
            Analyzing {totalColors} unique colors across {brands.length} brands
          </p>
        </div>

        {/* View Mode Toggle */}
        <div className="flex space-x-2">
          <Button
            variant={viewMode === 'palette' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('palette')}
          >
            <Palette className="h-4 w-4 mr-2" />
            Palette
          </Button>
          <Button
            variant={viewMode === 'comparison' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('comparison')}
          >
            <BarChart3 className="h-4 w-4 mr-2" />
            Compare
          </Button>
          <Button
            variant={viewMode === 'trends' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('trends')}
          >
            <TrendingUp className="h-4 w-4 mr-2" />
            Trends
          </Button>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Palette className="h-5 w-5 text-blue-500" />
              <div>
                <p className="text-sm font-medium text-gray-700">Total Colors</p>
                <p className="text-2xl font-bold">{totalColors}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <TrendingUp className="h-5 w-5 text-green-500" />
              <div>
                <p className="text-sm font-medium text-gray-700">Most Popular</p>
                <div className="flex items-center space-x-2">
                  {mostUsedColor && (
                    <>
                      <div
                        className="w-4 h-4 rounded border"
                        style={{ backgroundColor: mostUsedColor.hex }}
                      />
                      <span className="text-sm font-bold">{mostUsedColor.usage} uses</span>
                    </>
                  )}
                </div>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Eye className="h-5 w-5 text-purple-500" />
              <div>
                <p className="text-sm font-medium text-gray-700">Primary Colors</p>
                <p className="text-2xl font-bold">
                  {colorAnalysis.filter(c => c.category === 'primary').length}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="p-4">
            <div className="flex items-center space-x-2">
              <Zap className="h-5 w-5 text-orange-500" />
              <div>
                <p className="text-sm font-medium text-gray-700">Unique Brands</p>
                <p className="text-2xl font-bold">{brands.length}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Color Palette */}
        <div className="lg:col-span-2">
          <Card>
            <CardHeader>
              <CardTitle>Color Palette</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-8 md:grid-cols-12 gap-3">
                {colorTrends.map((color, index) => (
                  <ColorSwatch key={index} color={color} />
                ))}
              </div>
              {colorAnalysis.length > 10 && (
                <p className="text-sm text-gray-500 mt-4">
                  Showing top 10 colors. {colorAnalysis.length - 10} more available.
                </p>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Color Details */}
        <div>
          {selectedColor ? (
            <ColorDetails color={colorAnalysis.find(c => c.hex === selectedColor)!} />
          ) : (
            <Card>
              <CardContent className="p-6 text-center">
                <Palette className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                <h3 className="font-medium text-gray-900 mb-2">Select a Color</h3>
                <p className="text-sm text-gray-600">
                  Click on any color swatch to see detailed information
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
