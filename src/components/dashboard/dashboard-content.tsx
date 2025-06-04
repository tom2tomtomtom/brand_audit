'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/components/providers';
import { DashboardLayout } from '@/components/layout/dashboard-layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import {
  BarChart3,
  Plus,
  Search,
  Filter,
  TrendingUp,
  Users,
  FileText,
  Clock
} from 'lucide-react';
import { ProjectCard } from './project-card';
import { StatsCard } from './stats-card';
import { RecentActivity } from './recent-activity';
import { QuickActions } from './quick-actions';
import { CreateProjectModal } from '@/components/forms/create-project-modal';
import { NoOrganization } from '@/components/onboarding/no-organization';
import type { Project } from '@/types';

export function DashboardContent() {
  const { user, currentOrganization, organizations } = useAuth();
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showCreateModal, setShowCreateModal] = useState(false);

  useEffect(() => {
    fetchProjects();
  }, [currentOrganization]);

  // Show no organization screen if user has no organizations
  if (!loading && organizations.length === 0) {
    return <NoOrganization />;
  }

  const fetchProjects = async () => {
    try {
      const response = await fetch('/api/projects');
      const data = await response.json();

      if (response.ok) {
        setProjects(data.projects || []);
      } else {
        console.error('Failed to fetch projects:', data.error);
      }
    } catch (error) {
      console.error('Error fetching projects:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStats = () => {
    const totalProjects = projects.length;
    const totalBrands = projects.reduce((sum, p) => sum + ((p as any).brands_count || 0), 0);
    const activeProjects = projects.filter(p => (p as any).project_status === 'active').length;
    const completedProjects = projects.filter(p => (p as any).project_status === 'completed').length;

    return [
      {
        title: 'Total Projects',
        value: totalProjects.toString(),
        change: `${activeProjects} active`,
        trend: 'up' as const,
        icon: <FileText className="h-4 w-4" />,
      },
      {
        title: 'Brands Analyzed',
        value: totalBrands.toString(),
        change: `${completedProjects} completed`,
        trend: 'up' as const,
        icon: <BarChart3 className="h-4 w-4" />,
      },
      {
        title: 'Team Members',
        value: '1',
        change: 'You',
        trend: 'up' as const,
        icon: <Users className="h-4 w-4" />,
      },
      {
        title: 'Success Rate',
        value: totalProjects > 0 ? `${Math.round((completedProjects / totalProjects) * 100)}%` : '0%',
        change: 'Project completion',
        trend: 'up' as const,
        icon: <Clock className="h-4 w-4" />,
      },
    ];
  };

  const stats = getStats();

  // Show recent projects (limit to 3 for dashboard)
  const recentProjects = projects.slice(0, 3);

  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">
              Welcome back, {user?.user_metadata?.full_name || user?.email}
            </h1>
            <p className="text-gray-600 mt-1">
              Here&apos;s what&apos;s happening with your brand analysis projects
            </p>
          </div>
          <div className="flex items-center space-x-3">
            <Button variant="outline" size="sm">
              <Filter className="h-4 w-4 mr-2" />
              Filter
            </Button>
            <Button onClick={() => setShowCreateModal(true)}>
              <Plus className="h-4 w-4 mr-2" />
              New Project
            </Button>
          </div>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <StatsCard key={index} {...stat} />
          ))}
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Recent Projects */}
          <div className="lg:col-span-2">
            <Card>
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle>Recent Projects</CardTitle>
                    <CardDescription>
                      Your latest brand analysis projects
                    </CardDescription>
                  </div>
                  <Button variant="ghost" size="sm">
                    View All
                  </Button>
                </div>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="space-y-4">
                    {[1, 2, 3].map((i) => (
                      <div key={i} className="animate-pulse">
                        <div className="h-20 bg-gray-200 rounded"></div>
                      </div>
                    ))}
                  </div>
                ) : recentProjects.length > 0 ? (
                  <div className="space-y-4">
                    {recentProjects.map((project) => (
                      <ProjectCard key={project.id} project={project as any} />
                    ))}
                  </div>
                ) : (
                  <div className="text-center py-8">
                    <FileText className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                    <h3 className="text-lg font-medium text-gray-900 mb-2">No projects yet</h3>
                    <p className="text-gray-600 mb-4">
                      Create your first project to start analyzing brands
                    </p>
                    <Button onClick={() => setShowCreateModal(true)}>
                      <Plus className="h-4 w-4 mr-2" />
                      Create Project
                    </Button>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Sidebar */}
          <div className="space-y-6">
            {/* Quick Actions */}
            <QuickActions />
            
            {/* Recent Activity */}
            <RecentActivity />
          </div>
        </div>

        {/* Performance Chart */}
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center">
              <TrendingUp className="h-5 w-5 mr-2" />
              Analysis Performance
            </CardTitle>
            <CardDescription>
              Track your team&apos;s analysis efficiency over time
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-64 flex items-center justify-center text-gray-500">
              {/* TODO: Add chart component */}
              <div className="text-center">
                <BarChart3 className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                <p>Performance chart will be displayed here</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Create Project Modal */}
      <CreateProjectModal
        open={showCreateModal}
        onClose={() => setShowCreateModal(false)}
        onSuccess={() => {
          setShowCreateModal(false);
          fetchProjects();
        }}
      />
    </DashboardLayout>
  );
}
