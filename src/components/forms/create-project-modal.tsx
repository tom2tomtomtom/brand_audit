'use client';

import { useState } from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { X, Plus, Trash2, Globe } from 'lucide-react';
import toast from 'react-hot-toast';
import type { CreateProjectForm } from '@/types';

interface CreateProjectModalProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

interface BrandForm {
  name: string;
  websiteUrl: string;
  industry: string;
}

export function CreateProjectModal({ open, onClose, onSuccess }: CreateProjectModalProps) {
  const [loading, setLoading] = useState(false);
  const [projectName, setProjectName] = useState('');
  const [projectDescription, setProjectDescription] = useState('');
  const [brands, setBrands] = useState<BrandForm[]>([
    { name: '', websiteUrl: '', industry: '' }
  ]);

  const handleAddBrand = () => {
    setBrands([...brands, { name: '', websiteUrl: '', industry: '' }]);
  };

  const handleRemoveBrand = (index: number) => {
    if (brands.length > 1) {
      setBrands(brands.filter((_, i) => i !== index));
    }
  };

  const handleBrandChange = (index: number, field: keyof BrandForm, value: string) => {
    const updatedBrands = brands.map((brand, i) => 
      i === index ? { ...brand, [field]: value } : brand
    );
    setBrands(updatedBrands);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!projectName.trim()) {
      toast.error('Project name is required');
      return;
    }

    const validBrands = brands.filter(brand => 
      brand.name.trim() && brand.websiteUrl.trim()
    );

    if (validBrands.length === 0) {
      toast.error('At least one brand with name and URL is required');
      return;
    }

    setLoading(true);

    try {
      const formData: CreateProjectForm = {
        name: projectName.trim(),
        description: projectDescription.trim() || undefined,
        brands: validBrands.map(brand => ({
          name: brand.name.trim(),
          websiteUrl: brand.websiteUrl.trim(),
          industry: brand.industry.trim() || undefined,
        })),
      };

      const response = await fetch('/api/projects', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        toast.success('Project created successfully!');
        resetForm();
        onSuccess();
      } else {
        toast.error(data.error || 'Failed to create project');
      }
    } catch (error) {
      toast.error('Failed to create project');
      console.error('Create project error:', error);
    } finally {
      setLoading(false);
    }
  };

  const resetForm = () => {
    setProjectName('');
    setProjectDescription('');
    setBrands([{ name: '', websiteUrl: '', industry: '' }]);
  };

  const handleClose = () => {
    if (!loading) {
      resetForm();
      onClose();
    }
  };

  if (!open) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        <Card className="border-0 shadow-none">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-4">
            <div>
              <CardTitle>Create New Project</CardTitle>
              <CardDescription>
                Start a new brand analysis project with one or more brands
              </CardDescription>
            </div>
            <Button
              variant="ghost"
              size="sm"
              onClick={handleClose}
              disabled={loading}
            >
              <X className="h-4 w-4" />
            </Button>
          </CardHeader>

          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              {/* Project Details */}
              <div className="space-y-4">
                <h3 className="text-lg font-medium">Project Details</h3>
                
                <div className="space-y-2">
                  <Label htmlFor="projectName">Project Name *</Label>
                  <Input
                    id="projectName"
                    value={projectName}
                    onChange={(e) => setProjectName(e.target.value)}
                    placeholder="e.g., Q4 Competitor Analysis"
                    disabled={loading}
                    required
                  />
                </div>

                <div className="space-y-2">
                  <Label htmlFor="projectDescription">Description</Label>
                  <Input
                    id="projectDescription"
                    value={projectDescription}
                    onChange={(e) => setProjectDescription(e.target.value)}
                    placeholder="Brief description of the project goals"
                    disabled={loading}
                  />
                </div>
              </div>

              {/* Brands Section */}
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <h3 className="text-lg font-medium">Brands to Analyze</h3>
                  <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    onClick={handleAddBrand}
                    disabled={loading}
                  >
                    <Plus className="h-4 w-4 mr-2" />
                    Add Brand
                  </Button>
                </div>

                <div className="space-y-4">
                  {brands.map((brand, index) => (
                    <div key={index} className="border rounded-lg p-4 space-y-3">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-2">
                          <Globe className="h-4 w-4 text-gray-500" />
                          <span className="text-sm font-medium">Brand {index + 1}</span>
                        </div>
                        {brands.length > 1 && (
                          <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            onClick={() => handleRemoveBrand(index)}
                            disabled={loading}
                          >
                            <Trash2 className="h-4 w-4" />
                          </Button>
                        )}
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                        <div className="space-y-2">
                          <Label htmlFor={`brandName-${index}`}>Brand Name *</Label>
                          <Input
                            id={`brandName-${index}`}
                            value={brand.name}
                            onChange={(e) => handleBrandChange(index, 'name', e.target.value)}
                            placeholder="e.g., Nike"
                            disabled={loading}
                            required
                          />
                        </div>

                        <div className="space-y-2">
                          <Label htmlFor={`brandUrl-${index}`}>Website URL *</Label>
                          <Input
                            id={`brandUrl-${index}`}
                            type="url"
                            value={brand.websiteUrl}
                            onChange={(e) => handleBrandChange(index, 'websiteUrl', e.target.value)}
                            placeholder="https://example.com"
                            disabled={loading}
                            required
                          />
                        </div>

                        <div className="space-y-2 md:col-span-2">
                          <Label htmlFor={`brandIndustry-${index}`}>Industry</Label>
                          <Input
                            id={`brandIndustry-${index}`}
                            value={brand.industry}
                            onChange={(e) => handleBrandChange(index, 'industry', e.target.value)}
                            placeholder="e.g., Fashion, Technology, Healthcare"
                            disabled={loading}
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Actions */}
              <div className="flex justify-end space-x-3 pt-4 border-t">
                <Button
                  type="button"
                  variant="outline"
                  onClick={handleClose}
                  disabled={loading}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  disabled={loading}
                >
                  {loading ? 'Creating...' : 'Create Project'}
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
