'use client';

import { useState } from 'react';
import BrandCard from './BrandCard';
import CompetitiveMatrix from './CompetitiveMatrix';
import ExecutiveSummary from './ExecutiveSummary';

interface AnalysisReportProps {
  data: any;
  onNewAnalysis: () => void;
}

export default function AnalysisReport({ data, onNewAnalysis }: AnalysisReportProps) {
  const [activeTab, setActiveTab] = useState('overview');
  const [downloading, setDownloading] = useState(false);

  const handleDownload = async (format: 'pdf' | 'html' | 'json') => {
    setDownloading(true);
    try {
      const response = await fetch(`/api/download/${format}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `brand-analysis-${new Date().toISOString().split('T')[0]}.${format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      setDownloading(false);
    }
  };

  const tabs = [
    { id: 'overview', label: '📊 Executive Overview', icon: '📊' },
    { id: 'brands', label: '🏢 Brand Profiles', icon: '🏢' },
    { id: 'matrix', label: '⚖️ Competitive Matrix', icon: '⚖️' },
    { id: 'visuals', label: '🎨 Visual Analysis', icon: '🎨' },
  ];

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header with Download Options */}
      <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-4">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              📈 Brand Analysis Report
            </h1>
            <p className="text-gray-600">
              Comprehensive analysis of {data.brands?.length || 0} brands • Generated {new Date().toLocaleDateString()}
            </p>
          </div>
          
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => handleDownload('pdf')}
              disabled={downloading}
              className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:opacity-50 flex items-center gap-2"
            >
              📄 Download PDF
            </button>
            <button
              onClick={() => handleDownload('html')}
              disabled={downloading}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 flex items-center gap-2"
            >
              🌐 Download HTML
            </button>
            <button
              onClick={() => handleDownload('json')}
              disabled={downloading}
              className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 flex items-center gap-2"
            >
              📊 Download Data
            </button>
            <button
              onClick={onNewAnalysis}
              className="px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 flex items-center gap-2"
            >
              🔄 New Analysis
            </button>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white rounded-xl shadow-lg mb-6">
        <div className="border-b border-gray-200">
          <nav className="flex space-x-8 px-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-2 border-b-2 font-medium text-sm ${
                  activeTab === tab.id
                    ? 'border-blue-500 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                }`}
              >
                {tab.label}
              </button>
            ))}
          </nav>
        </div>

        {/* Tab Content */}
        <div className="p-6">
          {activeTab === 'overview' && (
            <ExecutiveSummary data={data} />
          )}
          
          {activeTab === 'brands' && (
            <div className="space-y-8">
              {data.brands?.map((brand: any, index: number) => (
                <BrandCard key={index} brand={brand} />
              ))}
            </div>
          )}
          
          {activeTab === 'matrix' && (
            <CompetitiveMatrix brands={data.brands} />
          )}
          
          {activeTab === 'visuals' && (
            <div className="space-y-8">
              <h2 className="text-2xl font-bold text-gray-900 mb-6">🎨 Visual Brand Analysis</h2>
              
              {/* Visual comparison content */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {data.brands?.map((brand: any, index: number) => (
                  <div key={index} className="bg-gray-50 rounded-lg p-6">
                    <h3 className="text-xl font-semibold mb-4">{brand.name}</h3>
                    
                    {/* Logo Display */}
                    {brand.visual?.logo && (
                      <div className="mb-4">
                        <h4 className="font-medium mb-2">Logo</h4>
                        <img 
                          src={brand.visual.logo} 
                          alt={`${brand.name} logo`}
                          className="max-h-20 object-contain bg-white p-2 rounded border"
                        />
                      </div>
                    )}
                    
                    {/* Color Palette */}
                    {brand.visual?.colors && (
                      <div className="mb-4">
                        <h4 className="font-medium mb-2">Brand Colors</h4>
                        <div className="flex gap-2">
                          {brand.visual.colors.map((color: string, colorIndex: number) => (
                            <div key={colorIndex} className="text-center">
                              <div 
                                className="w-12 h-12 rounded border-2 border-gray-300"
                                style={{ backgroundColor: color }}
                              ></div>
                              <span className="text-xs mt-1 block">{color}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                    
                    {/* Typography */}
                    {brand.visual?.fonts && (
                      <div>
                        <h4 className="font-medium mb-2">Typography</h4>
                        <div className="space-y-1 text-sm">
                          {brand.visual.fonts.map((font: string, fontIndex: number) => (
                            <div key={fontIndex} className="font-medium">
                              {font}
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}