'use client';

import Link from 'next/link';
import { Card, CardContent } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  MoreHorizontal, 
  Calendar, 
  BarChart3, 
  FileText,
  Users
} from 'lucide-react';
import { formatRelativeTime } from '@/lib/utils';

interface ProjectCardProps {
  project: {
    project_id: string;
    project_name: string;
    project_description: string;
    project_status: 'draft' | 'active' | 'completed' | 'archived';
    organization_id: string;
    organization_name: string;
    brands_count: number;
    completed_analyses_count: number;
    total_assets_count: number;
    created_at: string;
    updated_at: string;
  };
}

export function ProjectCard({ project }: ProjectCardProps) {
  const statusColors = {
    draft: 'bg-gray-100 text-gray-800',
    active: 'bg-blue-100 text-blue-800',
    completed: 'bg-green-100 text-green-800',
    archived: 'bg-yellow-100 text-yellow-800',
  };

  const progressPercentage = project.brands_count > 0
    ? Math.round((project.completed_analyses_count / project.brands_count) * 100)
    : 0;

  return (
    <Card className="hover:shadow-md transition-shadow">
      <CardContent className="p-4">
        <div className="flex items-start justify-between">
          <div className="flex-1">
            <div className="flex items-center space-x-2 mb-2">
              <Link
                href={`/dashboard/projects/${project.project_id}`}
                className="text-lg font-semibold text-gray-900 hover:text-primary transition-colors"
              >
                {project.project_name}
              </Link>
              <Badge className={statusColors[project.project_status]}>
                {project.project_status}
              </Badge>
            </div>

            <p className="text-gray-600 text-sm mb-3">
              {project.project_description || 'No description provided'}
            </p>

            <div className="flex items-center space-x-4 text-sm text-gray-500">
              <div className="flex items-center">
                <Users className="h-4 w-4 mr-1" />
                {project.brands_count} brands
              </div>
              <div className="flex items-center">
                <BarChart3 className="h-4 w-4 mr-1" />
                {project.completed_analyses_count}/{project.brands_count} analyzed
              </div>
              <div className="flex items-center">
                <FileText className="h-4 w-4 mr-1" />
                {project.total_assets_count} assets
              </div>
              <div className="flex items-center">
                <Calendar className="h-4 w-4 mr-1" />
                {formatRelativeTime(project.updated_at)}
              </div>
            </div>

            {/* Progress bar */}
            {project.project_status === 'active' && (
              <div className="mt-3">
                <div className="flex items-center justify-between text-xs text-gray-500 mb-1">
                  <span>Analysis Progress</span>
                  <span>{progressPercentage}%</span>
                </div>
                <div className="w-full bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-primary h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progressPercentage}%` }}
                  />
                </div>
              </div>
            )}
          </div>

          <Button variant="ghost" size="sm">
            <MoreHorizontal className="h-4 w-4" />
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}
