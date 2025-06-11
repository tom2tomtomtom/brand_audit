'use client';

interface CompetitiveMatrixProps {
  brands: any[];
}

export default function CompetitiveMatrix({ brands }: CompetitiveMatrixProps) {
  const metrics = [
    { key: 'score', label: 'Overall Score', type: 'score' },
    { key: 'digital.seoScore', label: 'SEO', type: 'score' },
    { key: 'digital.uxScore', label: 'UX Design', type: 'score' },
    { key: 'digital.socialScore', label: 'Social Media', type: 'score' },
    { key: 'digital.contentScore', label: 'Content Quality', type: 'score' },
    { key: 'positioning.marketPosition', label: 'Market Position', type: 'text' },
    { key: 'overview.industry', label: 'Industry Focus', type: 'text' },
    { key: 'overview.revenue', label: 'Revenue Scale', type: 'text' },
  ];

  const getNestedValue = (obj: any, path: string) => {
    return path.split('.').reduce((current, key) => current?.[key], obj);
  };

  const getScoreColor = (score: number) => {
    if (score >= 8) return 'bg-green-100 text-green-800';
    if (score >= 6) return 'bg-yellow-100 text-yellow-800';
    if (score >= 4) return 'bg-orange-100 text-orange-800';
    return 'bg-red-100 text-red-800';
  };

  const getOverallScoreColor = (score: number) => {
    if (score >= 80) return 'bg-green-500 text-white';
    if (score >= 60) return 'bg-yellow-500 text-white';
    if (score >= 40) return 'bg-orange-500 text-white';
    return 'bg-red-500 text-white';
  };

  return (
    <div className="space-y-6">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">⚖️ Competitive Comparison Matrix</h2>
      
      {/* Main Comparison Table */}
      <div className="bg-white rounded-lg overflow-hidden shadow-sm border">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-4 text-left text-sm font-medium text-gray-900 border-r">
                  Metric
                </th>
                {brands?.map((brand, index) => (
                  <th key={index} className="px-4 py-4 text-center text-sm font-medium text-gray-900 min-w-[140px]">
                    <div className="flex flex-col items-center gap-2">
                      {brand.visual?.logo && (
                        <img 
                          src={brand.visual.logo} 
                          alt={`${brand.name} logo`}
                          className="h-8 w-auto object-contain"
                        />
                      )}
                      <span className="font-semibold">{brand.name}</span>
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-200">
              {metrics.map((metric, metricIndex) => (
                <tr key={metricIndex} className={metricIndex % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                  <td className="px-6 py-4 text-sm font-medium text-gray-900 border-r">
                    {metric.label}
                  </td>
                  {brands?.map((brand, brandIndex) => {
                    const value = getNestedValue(brand, metric.key);
                    return (
                      <td key={brandIndex} className="px-4 py-4 text-center text-sm">
                        {metric.type === 'score' ? (
                          <span 
                            className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              metric.key === 'score' 
                                ? getOverallScoreColor(value || 0)
                                : getScoreColor(value || 0)
                            }`}
                          >
                            {value || 'N/A'}{metric.key === 'score' ? '' : '/10'}
                          </span>
                        ) : (
                          <span className="text-gray-700">
                            {value || 'Not specified'}
                          </span>
                        )}
                      </td>
                    );
                  })}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Visual Brand Comparison */}
      <div className="bg-white rounded-lg p-6 shadow-sm border">
        <h3 className="text-lg font-semibold mb-4">🎨 Visual Brand Identity Comparison</h3>
        
        {/* Color Palettes */}
        <div className="mb-6">
          <h4 className="font-medium mb-3">Brand Color Palettes</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {brands?.map((brand, index) => (
              <div key={index} className="text-center">
                <h5 className="font-medium mb-2">{brand.name}</h5>
                <div className="flex justify-center gap-1 mb-2">
                  {brand.visual?.colors ? (
                    brand.visual.colors.slice(0, 5).map((color: string, colorIndex: number) => (
                      <div
                        key={colorIndex}
                        className="w-8 h-8 rounded border-2 border-gray-300"
                        style={{ backgroundColor: color }}
                        title={color}
                      />
                    ))
                  ) : (
                    <div className="text-gray-400 text-sm">No colors extracted</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Typography */}
        <div>
          <h4 className="font-medium mb-3">Typography</h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {brands?.map((brand, index) => (
              <div key={index} className="text-center">
                <h5 className="font-medium mb-2">{brand.name}</h5>
                <div className="text-sm space-y-1">
                  {brand.visual?.fonts ? (
                    brand.visual.fonts.slice(0, 3).map((font: string, fontIndex: number) => (
                      <div key={fontIndex} className="p-2 bg-gray-50 rounded">
                        {font}
                      </div>
                    ))
                  ) : (
                    <div className="text-gray-400">No fonts detected</div>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Market Positioning Chart */}
      <div className="bg-white rounded-lg p-6 shadow-sm border">
        <h3 className="text-lg font-semibold mb-4">📍 Market Positioning Analysis</h3>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {/* Performance vs Price Positioning */}
          <div>
            <h4 className="font-medium mb-3">Performance vs Market Position</h4>
            <div className="relative h-64 bg-gray-50 rounded-lg p-4">
              <div className="absolute inset-4 border-l-2 border-b-2 border-gray-300">
                {/* Y-axis label */}
                <div className="absolute -left-8 top-0 -rotate-90 text-xs text-gray-600 origin-left">
                  Performance Score
                </div>
                {/* X-axis label */}
                <div className="absolute bottom-[-20px] right-0 text-xs text-gray-600">
                  Market Maturity
                </div>
                
                {/* Plot brands */}
                {brands?.map((brand, index) => {
                  const x = Math.random() * 80 + 10; // Placeholder positioning
                  const y = ((brand.score || 50) / 100) * 80 + 10;
                  
                  return (
                    <div
                      key={index}
                      className="absolute w-3 h-3 bg-blue-500 rounded-full transform -translate-x-1.5 -translate-y-1.5"
                      style={{ 
                        left: `${x}%`, 
                        bottom: `${y}%` 
                      }}
                      title={`${brand.name}: ${brand.score || 'N/A'}/100`}
                    />
                  );
                })}
              </div>
            </div>
          </div>

          {/* Key Metrics Summary */}
          <div>
            <h4 className="font-medium mb-3">Key Performance Indicators</h4>
            <div className="space-y-3">
              {brands?.map((brand, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                  <div className="flex items-center gap-3">
                    {brand.visual?.logo && (
                      <img 
                        src={brand.visual.logo} 
                        alt={`${brand.name} logo`}
                        className="h-6 w-auto object-contain"
                      />
                    )}
                    <span className="font-medium">{brand.name}</span>
                  </div>
                  <div className="text-sm space-x-4">
                    <span className="text-gray-600">Score: {brand.score || 'N/A'}</span>
                    <span className="text-gray-600">SEO: {brand.digital?.seoScore || 'N/A'}/10</span>
                    <span className="text-gray-600">UX: {brand.digital?.uxScore || 'N/A'}/10</span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}