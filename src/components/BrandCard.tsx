'use client';

interface BrandCardProps {
  brand: any;
}

export default function BrandCard({ brand }: BrandCardProps) {
  return (
    <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
      {/* Brand Header */}
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          {brand.visual?.logo && (
            <img 
              src={brand.visual.logo} 
              alt={`${brand.name} logo`}
              className="h-12 w-auto object-contain bg-white p-2 rounded border"
            />
          )}
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{brand.name}</h2>
            <p className="text-gray-600">{brand.website}</p>
          </div>
        </div>
        
        {/* Brand Score */}
        <div className="text-center">
          <div className={`text-3xl font-bold ${
            brand.score >= 80 ? 'text-green-600' : 
            brand.score >= 60 ? 'text-yellow-600' : 'text-red-600'
          }`}>
            {brand.score}/100
          </div>
          <p className="text-sm text-gray-500">Overall Score</p>
        </div>
      </div>

      {/* Company Overview */}
      {brand.overview && (
        <div className="mb-6 p-4 bg-white rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-blue-700">🏢 Company Overview</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
            <div>
              <strong>Industry:</strong> {brand.overview.industry || 'Not specified'}
            </div>
            <div>
              <strong>Founded:</strong> {brand.overview.founded || 'Not specified'}
            </div>
            <div>
              <strong>Revenue:</strong> {brand.overview.revenue || 'Not specified'}
            </div>
            <div>
              <strong>Employees:</strong> {brand.overview.employees || 'Not specified'}
            </div>
          </div>
          {brand.overview.description && (
            <p className="mt-3 text-gray-700">{brand.overview.description}</p>
          )}
        </div>
      )}

      {/* Brand Positioning */}
      {brand.positioning && (
        <div className="mb-6 p-4 bg-white rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-purple-700">🎯 Brand Positioning</h3>
          <div className="space-y-2 text-sm">
            <div>
              <strong>Positioning:</strong> {brand.positioning.statement || 'Not analyzed'}
            </div>
            <div>
              <strong>Value Proposition:</strong> {brand.positioning.valueProposition || 'Not analyzed'}
            </div>
            <div>
              <strong>Target Audience:</strong> {brand.positioning.targetAudience || 'Not analyzed'}
            </div>
            <div>
              <strong>Brand Personality:</strong> {brand.positioning.personality || 'Not analyzed'}
            </div>
          </div>
        </div>
      )}

      {/* Digital Presence */}
      {brand.digital && (
        <div className="mb-6 p-4 bg-white rounded-lg">
          <h3 className="text-lg font-semibold mb-3 text-green-700">💻 Digital Presence</h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div className="text-center">
              <div className="font-bold text-lg">{brand.digital.seoScore || 'N/A'}/10</div>
              <div className="text-gray-600">SEO Score</div>
            </div>
            <div className="text-center">
              <div className="font-bold text-lg">{brand.digital.uxScore || 'N/A'}/10</div>
              <div className="text-gray-600">UX Score</div>
            </div>
            <div className="text-center">
              <div className="font-bold text-lg">{brand.digital.socialScore || 'N/A'}/10</div>
              <div className="text-gray-600">Social Score</div>
            </div>
            <div className="text-center">
              <div className="font-bold text-lg">{brand.digital.contentScore || 'N/A'}/10</div>
              <div className="text-gray-600">Content Score</div>
            </div>
          </div>
        </div>
      )}

      {/* SWOT Analysis Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {/* Strengths */}
        <div className="bg-green-50 p-4 rounded-lg">
          <h4 className="font-semibold text-green-800 mb-3">✅ Strengths</h4>
          <ul className="space-y-1 text-sm text-green-700">
            {brand.strengths?.map((strength: string, index: number) => (
              <li key={index}>• {strength}</li>
            )) || <li>No strengths identified</li>}
          </ul>
        </div>

        {/* Weaknesses */}
        <div className="bg-red-50 p-4 rounded-lg">
          <h4 className="font-semibold text-red-800 mb-3">⚠️ Areas for Improvement</h4>
          <ul className="space-y-1 text-sm text-red-700">
            {brand.weaknesses?.map((weakness: string, index: number) => (
              <li key={index}>• {weakness}</li>
            )) || <li>No weaknesses identified</li>}
          </ul>
        </div>

        {/* Opportunities */}
        <div className="bg-blue-50 p-4 rounded-lg">
          <h4 className="font-semibold text-blue-800 mb-3">🌟 Opportunities</h4>
          <ul className="space-y-1 text-sm text-blue-700">
            {brand.opportunities?.map((opportunity: string, index: number) => (
              <li key={index}>• {opportunity}</li>
            )) || <li>No opportunities identified</li>}
          </ul>
        </div>

        {/* Threats */}
        <div className="bg-yellow-50 p-4 rounded-lg">
          <h4 className="font-semibold text-yellow-800 mb-3">⚡ Threats</h4>
          <ul className="space-y-1 text-sm text-yellow-700">
            {brand.threats?.map((threat: string, index: number) => (
              <li key={index}>• {threat}</li>
            )) || <li>No threats identified</li>}
          </ul>
        </div>
      </div>

      {/* Recommendations */}
      {brand.recommendations && (
        <div className="mt-6 p-4 bg-purple-50 rounded-lg">
          <h4 className="font-semibold text-purple-800 mb-3">💡 Strategic Recommendations</h4>
          <ul className="space-y-1 text-sm text-purple-700">
            {brand.recommendations.map((rec: string, index: number) => (
              <li key={index}>• {rec}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}