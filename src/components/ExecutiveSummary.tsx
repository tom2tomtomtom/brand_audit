'use client';

interface ExecutiveSummaryProps {
  data: any;
}

export default function ExecutiveSummary({ data }: ExecutiveSummaryProps) {
  const brands = data.brands || [];
  const averageScore = brands.length > 0 
    ? Math.round(brands.reduce((sum: number, brand: any) => sum + (brand.score || 0), 0) / brands.length)
    : 0;

  const topPerformer = brands.length > 0 
    ? brands.reduce((top: any, current: any) => 
        (current.score || 0) > (top.score || 0) ? current : top
      )
    : null;

  const industryFocus = data.industry || 'Multi-industry';

  return (
    <div className="space-y-8">
      <div className="text-center">
        <h2 className="text-3xl font-bold text-gray-900 mb-4">📊 Executive Summary</h2>
        <p className="text-lg text-gray-600 max-w-3xl mx-auto">
          Comprehensive competitive analysis of {brands.length} brands in the {industryFocus.toLowerCase()} sector. 
          This report provides strategic insights into market positioning, digital presence, and competitive advantages.
        </p>
      </div>

      {/* Key Metrics Dashboard */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-gradient-to-r from-blue-500 to-blue-600 rounded-xl p-6 text-white text-center">
          <div className="text-3xl font-bold mb-2">{brands.length}</div>
          <div className="text-blue-100">Brands Analyzed</div>
        </div>
        
        <div className="bg-gradient-to-r from-green-500 to-green-600 rounded-xl p-6 text-white text-center">
          <div className="text-3xl font-bold mb-2">{averageScore}/100</div>
          <div className="text-green-100">Average Score</div>
        </div>
        
        <div className="bg-gradient-to-r from-purple-500 to-purple-600 rounded-xl p-6 text-white text-center">
          <div className="text-3xl font-bold mb-2">{industryFocus}</div>
          <div className="text-purple-100">Industry Focus</div>
        </div>
        
        <div className="bg-gradient-to-r from-orange-500 to-orange-600 rounded-xl p-6 text-white text-center">
          <div className="text-3xl font-bold mb-2">{new Date().toLocaleDateString()}</div>
          <div className="text-orange-100">Analysis Date</div>
        </div>
      </div>

      {/* Top Performer Highlight */}
      {topPerformer && (
        <div className="bg-gradient-to-r from-yellow-50 to-yellow-100 border border-yellow-200 rounded-xl p-6">
          <div className="flex items-center gap-4 mb-4">
            <div className="text-4xl">🏆</div>
            <div>
              <h3 className="text-xl font-bold text-yellow-800">Market Leader</h3>
              <p className="text-yellow-700">Highest performing brand in this analysis</p>
            </div>
          </div>
          
          <div className="flex items-center gap-6">
            {topPerformer.visual?.logo && (
              <img 
                src={topPerformer.visual.logo} 
                alt={`${topPerformer.name} logo`}
                className="h-16 w-auto object-contain bg-white p-2 rounded border"
              />
            )}
            <div>
              <h4 className="text-2xl font-bold text-yellow-900">{topPerformer.name}</h4>
              <p className="text-yellow-800">Score: {topPerformer.score}/100</p>
              <p className="text-yellow-700 mt-2">
                {topPerformer.positioning?.statement || 'Leading market position with strong digital presence and brand recognition.'}
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Strategic Insights */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Market Landscape */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <h3 className="text-xl font-semibold mb-4 text-blue-700">🌍 Market Landscape</h3>
          <div className="space-y-4">
            <div>
              <h4 className="font-medium text-gray-900">Competitive Intensity</h4>
              <div className="flex items-center gap-3 mt-1">
                <div className="flex-1 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-blue-500 h-2 rounded-full" 
                    style={{ width: `${Math.min(100, (brands.length / 5) * 100)}%` }}
                  ></div>
                </div>
                <span className="text-sm text-gray-600">
                  {brands.length <= 2 ? 'Low' : brands.length <= 4 ? 'Medium' : 'High'}
                </span>
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900">Digital Maturity</h4>
              <div className="flex items-center gap-3 mt-1">
                <div className="flex-1 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full" 
                    style={{ width: `${averageScore}%` }}
                  ></div>
                </div>
                <span className="text-sm text-gray-600">{averageScore}%</span>
              </div>
            </div>

            <div className="pt-2 border-t">
              <p className="text-sm text-gray-700">
                The {industryFocus.toLowerCase()} market shows {averageScore >= 70 ? 'high' : averageScore >= 50 ? 'moderate' : 'emerging'} digital 
                maturity with {brands.length > 3 ? 'intense' : 'moderate'} competition among key players.
              </p>
            </div>
          </div>
        </div>

        {/* Key Opportunities */}
        <div className="bg-white border border-gray-200 rounded-xl p-6">
          <h3 className="text-xl font-semibold mb-4 text-green-700">🚀 Strategic Opportunities</h3>
          <div className="space-y-3">
            <div className="flex items-start gap-3">
              <div className="text-green-600 mt-1">📱</div>
              <div>
                <h4 className="font-medium text-gray-900">Digital Experience Enhancement</h4>
                <p className="text-sm text-gray-600">
                  Average UX scores suggest room for mobile optimization and user experience improvements.
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="text-green-600 mt-1">🎯</div>
              <div>
                <h4 className="font-medium text-gray-900">Content Strategy Differentiation</h4>
                <p className="text-sm text-gray-600">
                  Opportunity to establish unique content positioning in the {industryFocus.toLowerCase()} space.
                </p>
              </div>
            </div>
            
            <div className="flex items-start gap-3">
              <div className="text-green-600 mt-1">🤝</div>
              <div>
                <h4 className="font-medium text-gray-900">Partnership & Integration</h4>
                <p className="text-sm text-gray-600">
                  Strategic partnerships could enhance market reach and service integration.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Brand Performance Overview */}
      <div className="bg-white border border-gray-200 rounded-xl p-6">
        <h3 className="text-xl font-semibold mb-4 text-gray-900">📈 Brand Performance Overview</h3>
        
        <div className="space-y-4">
          {brands.map((brand: any, index: number) => (
            <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center gap-4">
                {brand.visual?.logo && (
                  <img 
                    src={brand.visual.logo} 
                    alt={`${brand.name} logo`}
                    className="h-10 w-auto object-contain bg-white p-1 rounded border"
                  />
                )}
                <div>
                  <h4 className="font-semibold text-gray-900">{brand.name}</h4>
                  <p className="text-sm text-gray-600">{brand.website}</p>
                </div>
              </div>
              
              <div className="flex items-center gap-6 text-sm">
                <div className="text-center">
                  <div className={`font-bold text-lg ${
                    brand.score >= 80 ? 'text-green-600' : 
                    brand.score >= 60 ? 'text-yellow-600' : 'text-red-600'
                  }`}>
                    {brand.score || 'N/A'}
                  </div>
                  <div className="text-gray-500">Overall</div>
                </div>
                
                <div className="text-center">
                  <div className="font-bold text-lg text-blue-600">{brand.digital?.seoScore || 'N/A'}</div>
                  <div className="text-gray-500">SEO</div>
                </div>
                
                <div className="text-center">
                  <div className="font-bold text-lg text-purple-600">{brand.digital?.uxScore || 'N/A'}</div>
                  <div className="text-gray-500">UX</div>
                </div>
                
                <div className="text-center">
                  <div className="font-bold text-lg text-green-600">{brand.digital?.socialScore || 'N/A'}</div>
                  <div className="text-gray-500">Social</div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Action Items */}
      <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-xl p-6">
        <h3 className="text-xl font-semibold mb-4 text-purple-800">🎯 Strategic Action Items</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-medium text-purple-700 mb-2">Immediate Priorities (0-3 months)</h4>
            <ul className="space-y-1 text-sm text-purple-600">
              <li>• Audit and optimize website user experience</li>
              <li>• Enhance mobile responsiveness and speed</li>
              <li>• Strengthen SEO and content strategy</li>
              <li>• Analyze competitor visual identity gaps</li>
            </ul>
          </div>
          
          <div>
            <h4 className="font-medium text-purple-700 mb-2">Strategic Initiatives (3-12 months)</h4>
            <ul className="space-y-1 text-sm text-purple-600">
              <li>• Develop differentiated brand positioning</li>
              <li>• Invest in digital marketing capabilities</li>
              <li>• Explore strategic partnerships</li>
              <li>• Implement customer experience improvements</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}