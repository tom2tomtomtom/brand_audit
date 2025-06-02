'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { 
  Plus, 
  Upload, 
  FileText, 
  BarChart3,
  Zap
} from 'lucide-react';

export function QuickActions() {
  const actions = [
    {
      title: 'New Project',
      description: 'Start a new brand analysis project',
      icon: <Plus className="h-5 w-5" />,
      action: () => {
        // TODO: Open new project modal
      },
    },
    {
      title: 'Upload Assets',
      description: 'Add brand assets to existing project',
      icon: <Upload className="h-5 w-5" />,
      action: () => {
        // TODO: Open upload modal
      },
    },
    {
      title: 'Generate Report',
      description: 'Create presentation from analysis',
      icon: <FileText className="h-5 w-5" />,
      action: () => {
        // TODO: Open report generator
      },
    },
    {
      title: 'Run Analysis',
      description: 'Start AI analysis on pending brands',
      icon: <BarChart3 className="h-5 w-5" />,
      action: () => {
        // TODO: Start analysis
      },
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <Zap className="h-5 w-5 mr-2" />
          Quick Actions
        </CardTitle>
        <CardDescription>
          Common tasks to get you started
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-3">
          {actions.map((action, index) => (
            <Button
              key={index}
              variant="ghost"
              className="w-full justify-start h-auto p-3"
              onClick={action.action}
            >
              <div className="flex items-start space-x-3">
                <div className="p-1 bg-primary/10 rounded">
                  {action.icon}
                </div>
                <div className="text-left">
                  <div className="font-medium text-sm">{action.title}</div>
                  <div className="text-xs text-gray-500">{action.description}</div>
                </div>
              </div>
            </Button>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
