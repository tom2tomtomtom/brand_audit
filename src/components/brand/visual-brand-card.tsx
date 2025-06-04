'use client';

import { useState } from 'react';
import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import {
  Eye,
  Palette,
  Type,
  Image as ImageIcon,
  Monitor,
  Smartphone,
  ExternalLink,
  Heart,
  Share2
} from 'lucide-react';
import { VisualBrandData } from '@/services/scraper';

interface VisualBrandCardProps {
  brand: {
    id: string;
    name: string;
    websiteUrl: string;
    industry?: string;
    visualData?: VisualBrandData;
  };
  onAnalyze?: ((brandId: string) => void) | undefined;
  onViewDetails?: ((brandId: string) => void) | undefined;
}

export function VisualBrandCard({ brand, onAnalyze, onViewDetails }: VisualBrandCardProps) {
  const [imageError, setImageError] = useState(false);
  const [isLiked, setIsLiked] = useState(false);

  const handleImageError = () => {
    setImageError(true);
  };

  const ColorPalette = ({ colors }: { colors: string[] }) => (
    <div className="flex space-x-1">
      {colors.slice(0, 5).map((color, index) => (
        <div
          key={index}
          className="w-6 h-6 rounded-full border-2 border-white shadow-sm"
          style={{ backgroundColor: color }}
          title={color}
        />
      ))}
      {colors.length > 5 && (
        <div className="w-6 h-6 rounded-full bg-gray-200 border-2 border-white shadow-sm flex items-center justify-center text-xs text-gray-600">
          +{colors.length - 5}
        </div>
      )}
    </div>
  );

  const VisualMetrics = () => {
    if (!brand.visualData) return null;

    const metrics = [
      {
        label: 'Colors',
        value: brand.visualData.colorPalette.primary.length + brand.visualData.colorPalette.secondary.length,
        icon: Palette,
        color: 'bg-purple-100 text-purple-700'
      },
      {
        label: 'Fonts',
        value: brand.visualData.typography.headingFonts.length + brand.visualData.typography.bodyFonts.length,
        icon: Type,
        color: 'bg-blue-100 text-blue-700'
      },
      {
        label: 'Logos',
        value: brand.visualData.logos.variations.length,
        icon: ImageIcon,
        color: 'bg-green-100 text-green-700'
      }
    ];

    return (
      <div className="flex space-x-2">
        {metrics.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <div key={index} className={`px-2 py-1 rounded-full ${metric.color} flex items-center space-x-1`}>
              <Icon className="h-3 w-3" />
              <span className="text-xs font-medium">{metric.value}</span>
            </div>
          );
        })}
      </div>
    );
  };

  return (
    <Card className="group hover:shadow-lg transition-all duration-300 overflow-hidden">
      {/* Header with Logo and Actions */}
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex items-center space-x-3">
            {/* Brand Logo */}
            <div className="relative">
              {brand.visualData?.logos.primary && !imageError ? (
                <img
                  src={brand.visualData.logos.primary}
                  alt={`${brand.name} logo`}
                  className="w-12 h-12 object-contain rounded-lg border border-gray-200"
                  onError={handleImageError}
                />
              ) : (
                <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center text-white font-bold text-lg">
                  {brand.name.charAt(0).toUpperCase()}
                </div>
              )}
            </div>

            {/* Brand Info */}
            <div>
              <h3 className="font-semibold text-lg text-gray-900 group-hover:text-blue-600 transition-colors">
                {brand.name}
              </h3>
              {brand.industry && (
                <Badge variant="secondary" className="text-xs">
                  {brand.industry}
                </Badge>
              )}
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setIsLiked(!isLiked)}
              className={isLiked ? 'text-red-500' : 'text-gray-400'}
            >
              <Heart className={`h-4 w-4 ${isLiked ? 'fill-current' : ''}`} />
            </Button>
            <Button variant="ghost" size="sm">
              <Share2 className="h-4 w-4" />
            </Button>
            <Button variant="ghost" size="sm">
              <ExternalLink className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>

      <CardContent className="space-y-4">
        {/* Visual Metrics */}
        <VisualMetrics />

        {/* Color Palette */}
        {brand.visualData?.colorPalette && (
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Brand Colors</span>
              <span className="text-xs text-gray-500">
                {brand.visualData.colorPalette.primary.length + brand.visualData.colorPalette.secondary.length} colors
              </span>
            </div>
            <ColorPalette colors={[...brand.visualData.colorPalette.primary, ...brand.visualData.colorPalette.secondary]} />
          </div>
        )}

        {/* Screenshots Preview */}
        {brand.visualData?.screenshots && (
          <div>
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">Screenshots</span>
              <div className="flex space-x-1">
                <Monitor className="h-4 w-4 text-gray-400" />
                <Smartphone className="h-4 w-4 text-gray-400" />
              </div>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {brand.visualData.screenshots.homepage && (
                <div className="relative group/screenshot">
                  <img
                    src={brand.visualData.screenshots.homepage}
                    alt="Homepage screenshot"
                    className="w-full h-20 object-cover rounded border border-gray-200 hover:border-blue-300 transition-colors"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover/screenshot:bg-opacity-20 transition-all rounded flex items-center justify-center">
                    <Eye className="h-5 w-5 text-white opacity-0 group-hover/screenshot:opacity-100 transition-opacity" />
                  </div>
                </div>
              )}
              {brand.visualData.screenshots.mobile?.[0] && (
                <div className="relative group/screenshot">
                  <img
                    src={brand.visualData.screenshots.mobile[0]}
                    alt="Mobile screenshot"
                    className="w-full h-20 object-cover rounded border border-gray-200 hover:border-blue-300 transition-colors"
                  />
                  <div className="absolute inset-0 bg-black bg-opacity-0 group-hover/screenshot:bg-opacity-20 transition-all rounded flex items-center justify-center">
                    <Eye className="h-5 w-5 text-white opacity-0 group-hover/screenshot:opacity-100 transition-opacity" />
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Visual Style Tags */}
        {brand.visualData?.visualStyle && (
          <div>
            <span className="text-sm font-medium text-gray-700 block mb-2">Visual Style</span>
            <div className="flex flex-wrap gap-1">
              {brand.visualData.visualStyle.mood && (
                <Badge variant="outline" className="text-xs">
                  {brand.visualData.visualStyle.mood}
                </Badge>
              )}
              {brand.visualData.visualStyle.personality.slice(0, 3).map((trait, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {trait}
                </Badge>
              ))}
              {brand.visualData.visualStyle.designTrends.slice(0, 2).map((trend, index) => (
                <Badge key={index} variant="outline" className="text-xs">
                  {trend}
                </Badge>
              ))}
            </div>
          </div>
        )}

        {/* Action Buttons */}
        <div className="flex space-x-2 pt-2">
          <Button
            variant="outline"
            size="sm"
            className="flex-1"
            onClick={() => onViewDetails?.(brand.id)}
          >
            <Eye className="h-4 w-4 mr-2" />
            View Details
          </Button>
          <Button
            size="sm"
            className="flex-1"
            onClick={() => onAnalyze?.(brand.id)}
          >
            <Palette className="h-4 w-4 mr-2" />
            Analyze
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
