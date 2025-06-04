'use client';

import { useState, useMemo } from 'react';
import { VisualBrandCard } from './visual-brand-card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Badge } from '@/components/ui/badge';
import { 
  Search, 
  Filter, 
  Grid3X3, 
  List, 
  Palette, 
  Type, 
  Sparkles,
  SortAsc,
  SortDesc
} from 'lucide-react';
import { VisualBrandData } from '@/services/scraper';

interface Brand {
  id: string;
  name: string;
  websiteUrl: string;
  industry?: string;
  visualData?: VisualBrandData;
}

interface VisualBrandGalleryProps {
  brands: Brand[];
  loading?: boolean;
  onAnalyzeBrand?: (brandId: string) => void;
  onViewBrandDetails?: (brandId: string) => void;
}

type ViewMode = 'grid' | 'list';
type SortBy = 'name' | 'colors' | 'visual-complexity' | 'recent';
type FilterBy = 'all' | 'minimalist' | 'colorful' | 'modern' | 'classic';

export function VisualBrandGallery({ 
  brands, 
  loading = false, 
  onAnalyzeBrand, 
  onViewBrandDetails 
}: VisualBrandGalleryProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [viewMode, setViewMode] = useState<ViewMode>('grid');
  const [sortBy, setSortBy] = useState<SortBy>('name');
  const [filterBy, setFilterBy] = useState<FilterBy>('all');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('asc');

  // Filter and sort brands
  const filteredAndSortedBrands = useMemo(() => {
    let filtered = brands.filter(brand => {
      // Search filter
      const matchesSearch = brand.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           brand.industry?.toLowerCase().includes(searchTerm.toLowerCase());

      if (!matchesSearch) return false;

      // Visual style filter
      if (filterBy === 'all') return true;
      
      const visualStyle = brand.visualData?.visualStyle;
      if (!visualStyle) return filterBy === 'all';

      switch (filterBy) {
        case 'minimalist':
          return visualStyle.personality.includes('minimalist');
        case 'colorful':
          return (brand.visualData?.colorPalette.primary.length || 0) > 3;
        case 'modern':
          return visualStyle.designTrends.includes('gradients') || 
                 visualStyle.designTrends.includes('rounded-design');
        case 'classic':
          return visualStyle.mood === 'sophisticated';
        default:
          return true;
      }
    });

    // Sort brands
    filtered.sort((a, b) => {
      let comparison = 0;

      switch (sortBy) {
        case 'name':
          comparison = a.name.localeCompare(b.name);
          break;
        case 'colors':
          const aColors = (a.visualData?.colorPalette.primary.length || 0) + 
                         (a.visualData?.colorPalette.secondary.length || 0);
          const bColors = (b.visualData?.colorPalette.primary.length || 0) + 
                         (b.visualData?.colorPalette.secondary.length || 0);
          comparison = aColors - bColors;
          break;
        case 'visual-complexity':
          const aComplexity = (a.visualData?.logos.variations.length || 0) + 
                             (a.visualData?.typography.headingFonts.length || 0);
          const bComplexity = (b.visualData?.logos.variations.length || 0) + 
                             (b.visualData?.typography.headingFonts.length || 0);
          comparison = aComplexity - bComplexity;
          break;
        case 'recent':
          // For now, sort by name as we don't have timestamps
          comparison = a.name.localeCompare(b.name);
          break;
      }

      return sortOrder === 'asc' ? comparison : -comparison;
    });

    return filtered;
  }, [brands, searchTerm, filterBy, sortBy, sortOrder]);

  const toggleSortOrder = () => {
    setSortOrder(prev => prev === 'asc' ? 'desc' : 'asc');
  };

  const getFilterStats = () => {
    const stats = {
      all: brands.length,
      minimalist: brands.filter(b => b.visualData?.visualStyle.personality.includes('minimalist')).length,
      colorful: brands.filter(b => (b.visualData?.colorPalette.primary.length || 0) > 3).length,
      modern: brands.filter(b => 
        b.visualData?.visualStyle.designTrends.includes('gradients') || 
        b.visualData?.visualStyle.designTrends.includes('rounded-design')
      ).length,
      classic: brands.filter(b => b.visualData?.visualStyle.mood === 'sophisticated').length,
    };
    return stats;
  };

  const filterStats = getFilterStats();

  if (loading) {
    return (
      <div className="space-y-6">
        {/* Loading skeleton */}
        <div className="flex items-center justify-between">
          <div className="h-8 bg-gray-200 rounded w-48 animate-pulse"></div>
          <div className="flex space-x-2">
            <div className="h-8 bg-gray-200 rounded w-24 animate-pulse"></div>
            <div className="h-8 bg-gray-200 rounded w-24 animate-pulse"></div>
          </div>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {[1, 2, 3, 4, 5, 6].map(i => (
            <div key={i} className="h-80 bg-gray-200 rounded-lg animate-pulse"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900">Visual Brand Gallery</h2>
          <p className="text-gray-600">
            {filteredAndSortedBrands.length} of {brands.length} brands
          </p>
        </div>
        
        {/* View Mode Toggle */}
        <div className="flex items-center space-x-2">
          <Button
            variant={viewMode === 'grid' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('grid')}
          >
            <Grid3X3 className="h-4 w-4" />
          </Button>
          <Button
            variant={viewMode === 'list' ? 'default' : 'outline'}
            size="sm"
            onClick={() => setViewMode('list')}
          >
            <List className="h-4 w-4" />
          </Button>
        </div>
      </div>

      {/* Search and Filters */}
      <div className="flex flex-col lg:flex-row gap-4">
        {/* Search */}
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
          <Input
            placeholder="Search brands by name or industry..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="pl-10"
          />
        </div>

        {/* Sort */}
        <div className="flex items-center space-x-2">
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value as SortBy)}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value="name">Sort by Name</option>
            <option value="colors">Sort by Colors</option>
            <option value="visual-complexity">Sort by Complexity</option>
            <option value="recent">Sort by Recent</option>
          </select>
          <Button
            variant="outline"
            size="sm"
            onClick={toggleSortOrder}
          >
            {sortOrder === 'asc' ? <SortAsc className="h-4 w-4" /> : <SortDesc className="h-4 w-4" />}
          </Button>
        </div>
      </div>

      {/* Visual Style Filters */}
      <div className="flex flex-wrap gap-2">
        {Object.entries(filterStats).map(([filter, count]) => (
          <Badge
            key={filter}
            variant={filterBy === filter ? 'default' : 'outline'}
            className="cursor-pointer hover:bg-blue-50 transition-colors"
            onClick={() => setFilterBy(filter as FilterBy)}
          >
            {filter === 'all' ? 'All' : 
             filter === 'minimalist' ? 'Minimalist' :
             filter === 'colorful' ? 'Colorful' :
             filter === 'modern' ? 'Modern' : 'Classic'} ({count})
          </Badge>
        ))}
      </div>

      {/* Brand Grid/List */}
      {filteredAndSortedBrands.length === 0 ? (
        <div className="text-center py-12">
          <Sparkles className="h-12 w-12 text-gray-400 mx-auto mb-4" />
          <h3 className="text-lg font-medium text-gray-900 mb-2">No brands found</h3>
          <p className="text-gray-600">
            Try adjusting your search or filter criteria
          </p>
        </div>
      ) : (
        <div className={
          viewMode === 'grid' 
            ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6'
            : 'space-y-4'
        }>
          {filteredAndSortedBrands.map((brand) => (
            <VisualBrandCard
              key={brand.id}
              brand={brand}
              onAnalyze={onAnalyzeBrand}
              onViewDetails={onViewBrandDetails}
            />
          ))}
        </div>
      )}
    </div>
  );
}
