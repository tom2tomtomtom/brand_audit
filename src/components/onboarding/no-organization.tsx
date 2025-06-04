'use client';

import { useState } from 'react';
import { useAuth } from '@/components/providers';
import { CreateOrganizationModal } from './create-organization-modal';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Building, Plus, Users, Zap } from 'lucide-react';

export function NoOrganization() {
  const [showCreateModal, setShowCreateModal] = useState(false);
  const { refreshUser } = useAuth();

  const handleOrganizationCreated = async () => {
    setShowCreateModal(false);
    await refreshUser();
  };

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center p-4">
      <div className="max-w-2xl w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="mx-auto w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mb-6">
            <Building className="h-8 w-8 text-blue-600" />
          </div>
          <h1 className="text-3xl font-bold text-gray-900 mb-4">
            Welcome to Brand Audit Tool
          </h1>
          <p className="text-lg text-gray-600">
            To get started, you&apos;ll need to create an organization for your team.
          </p>
        </div>

        {/* Features */}
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto w-12 h-12 bg-green-100 rounded-full flex items-center justify-center mb-4">
                <Zap className="h-6 w-6 text-green-600" />
              </div>
              <CardTitle className="text-lg">AI-Powered Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 text-center">
                Get comprehensive brand insights powered by advanced AI technology.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto w-12 h-12 bg-purple-100 rounded-full flex items-center justify-center mb-4">
                <Users className="h-6 w-6 text-purple-600" />
              </div>
              <CardTitle className="text-lg">Team Collaboration</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 text-center">
                Work together with your team on brand analysis projects.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="text-center">
              <div className="mx-auto w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center mb-4">
                <Building className="h-6 w-6 text-orange-600" />
              </div>
              <CardTitle className="text-lg">Automated Reports</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-gray-600 text-center">
                Generate professional presentations and reports automatically.
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Call to Action */}
        <Card>
          <CardHeader className="text-center">
            <CardTitle>Create Your Organization</CardTitle>
            <CardDescription>
              Set up your organization to start analyzing brands and collaborating with your team.
            </CardDescription>
          </CardHeader>
          <CardContent className="text-center">
            <Button
              onClick={() => setShowCreateModal(true)}
              size="lg"
              className="px-8"
            >
              <Plus className="h-5 w-5 mr-2" />
              Create Organization
            </Button>
          </CardContent>
        </Card>

        {/* Additional Info */}
        <div className="text-center text-sm text-gray-500">
          <p>
            Need help? Contact our support team at{' '}
            <a href="mailto:support@brandaudit.com" className="text-blue-600 hover:underline">
              support@brandaudit.com
            </a>
          </p>
        </div>
      </div>

      {/* Create Organization Modal */}
      {showCreateModal && (
        <CreateOrganizationModal onSuccess={handleOrganizationCreated} />
      )}
    </div>
  );
}
