'use client';

import { useState } from 'react';

interface BrandInputProps {
  onAnalyze: (brands: string[]) => void;
}

export default function BrandInput({ onAnalyze }: BrandInputProps) {
  const [brands, setBrands] = useState(['', '', '']);
  const [industry, setIndustry] = useState('');

  const updateBrand = (index: number, value: string) => {
    const newBrands = [...brands];
    newBrands[index] = value;
    setBrands(newBrands);
  };

  const addBrand = () => {
    setBrands([...brands, '']);
  };

  const removeBrand = (index: number) => {
    if (brands.length > 1) {
      setBrands(brands.filter((_, i) => i !== index));
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const validBrands = brands.filter(brand => brand.trim());
    if (validBrands.length === 0) {
      alert('Please enter at least one brand');
      return;
    }
    onAnalyze(validBrands);
  };

  const loadMedicalExample = () => {
    setBrands(['wolterskluwer.com', 'elsevier.com', 'openevidence.com']);
    setIndustry('Healthcare & Medical Information');
  };

  const loadTechExample = () => {
    setBrands(['microsoft.com', 'google.com', 'apple.com']);
    setIndustry('Technology');
  };

  return (
    <div className="max-w-4xl mx-auto">
      <form onSubmit={handleSubmit} className="bg-white rounded-xl shadow-lg p-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-6">Brand Analysis Setup</h2>
        
        {/* Quick Examples */}
        <div className="mb-8 p-4 bg-blue-50 rounded-lg">
          <h3 className="font-semibold text-blue-900 mb-3">Quick Examples:</h3>
          <div className="flex flex-wrap gap-3">
            <button
              type="button"
              onClick={loadMedicalExample}
              className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
            >
              📊 Medical Industry (Wolters Kluwer, Elsevier, Open Evidence)
            </button>
            <button
              type="button"
              onClick={loadTechExample}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 text-sm"
            >
              💻 Tech Giants (Microsoft, Google, Apple)
            </button>
          </div>
        </div>

        {/* Industry Context */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Industry Context (Optional)
          </label>
          <input
            type="text"
            value={industry}
            onChange={(e) => setIndustry(e.target.value)}
            placeholder="e.g., Healthcare, Technology, Retail, Finance..."
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <p className="text-sm text-gray-500 mt-1">
            Helps tailor the analysis to industry-specific metrics and insights
          </p>
        </div>

        {/* Brand Inputs */}
        <div className="mb-6">
          <label className="block text-sm font-medium text-gray-700 mb-3">
            Brands to Analyze
          </label>
          <div className="space-y-3">
            {brands.map((brand, index) => (
              <div key={index} className="flex gap-3 items-center">
                <div className="flex-1">
                  <input
                    type="text"
                    value={brand}
                    onChange={(e) => updateBrand(index, e.target.value)}
                    placeholder={`Brand ${index + 1} (e.g., company.com or "Company Name")`}
                    className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent text-lg"
                  />
                </div>
                {brands.length > 1 && (
                  <button
                    type="button"
                    onClick={() => removeBrand(index)}
                    className="p-2 text-red-600 hover:bg-red-50 rounded"
                    title="Remove brand"
                  >
                    🗑️
                  </button>
                )}
              </div>
            ))}
          </div>
          
          {brands.length < 10 && (
            <button
              type="button"
              onClick={addBrand}
              className="mt-3 px-4 py-2 text-blue-600 border border-blue-300 rounded hover:bg-blue-50"
            >
              ➕ Add Another Brand
            </button>
          )}
        </div>

        {/* Analysis Features */}
        <div className="mb-8 p-4 bg-gray-50 rounded-lg">
          <h3 className="font-semibold text-gray-800 mb-3">📊 What We'll Analyze:</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-gray-700">
            <div>
              <h4 className="font-medium text-blue-700 mb-2">🎨 Visual Brand Identity</h4>
              <ul className="space-y-1">
                <li>• Logo extraction and variations</li>
                <li>• Brand color palettes</li>
                <li>• Typography and fonts</li>
                <li>• Visual design patterns</li>
              </ul>
            </div>
            <div>
              <h4 className="font-medium text-green-700 mb-2">🏢 Business Intelligence</h4>
              <ul className="space-y-1">
                <li>• Market positioning</li>
                <li>• Digital presence metrics</li>
                <li>• Content strategy analysis</li>
                <li>• Recent brand work and press</li>
              </ul>
            </div>
          </div>
        </div>

        {/* Submit Button */}
        <button
          type="submit"
          className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-lg font-semibold text-lg hover:from-blue-700 hover:to-purple-700 transition-all duration-200 shadow-lg"
        >
          🚀 Generate Brand Analysis Report
        </button>
        
        <p className="text-sm text-gray-500 text-center mt-4">
          Analysis typically takes 2-5 minutes. We'll extract logos, colors, and generate comprehensive insights.
        </p>
      </form>
    </div>
  );
}