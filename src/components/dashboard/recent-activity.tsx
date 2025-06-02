'use client';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  Clock, 
  CheckCircle, 
  AlertCircle, 
  Upload,
  BarChart3,
  FileText
} from 'lucide-react';
import { formatRelativeTime } from '@/lib/utils';

export function RecentActivity() {
  const activities = [
    {
      id: '1',
      type: 'analysis_completed',
      title: 'Analysis completed for Nike',
      description: 'Brand positioning analysis finished',
      timestamp: '2024-01-15T14:30:00Z',
      icon: <CheckCircle className="h-4 w-4 text-green-500" />,
    },
    {
      id: '2',
      type: 'assets_uploaded',
      title: 'Assets uploaded to Adidas project',
      description: '12 new campaign images added',
      timestamp: '2024-01-15T12:15:00Z',
      icon: <Upload className="h-4 w-4 text-blue-500" />,
    },
    {
      id: '3',
      type: 'analysis_started',
      title: 'Started analysis for Puma',
      description: 'Visual identity analysis in progress',
      timestamp: '2024-01-15T10:45:00Z',
      icon: <BarChart3 className="h-4 w-4 text-orange-500" />,
    },
    {
      id: '4',
      type: 'report_generated',
      title: 'Report generated',
      description: 'Q4 Competitor Analysis presentation ready',
      timestamp: '2024-01-14T16:20:00Z',
      icon: <FileText className="h-4 w-4 text-purple-500" />,
    },
    {
      id: '5',
      type: 'error',
      title: 'Scraping failed for Under Armour',
      description: 'Website blocked automated requests',
      timestamp: '2024-01-14T14:10:00Z',
      icon: <AlertCircle className="h-4 w-4 text-red-500" />,
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle className="flex items-center">
          <Clock className="h-5 w-5 mr-2" />
          Recent Activity
        </CardTitle>
        <CardDescription>
          Latest updates from your projects
        </CardDescription>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {activities.map((activity) => (
            <div key={activity.id} className="flex items-start space-x-3">
              <div className="flex-shrink-0 mt-0.5">
                {activity.icon}
              </div>
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-gray-900">
                  {activity.title}
                </p>
                <p className="text-xs text-gray-500">
                  {activity.description}
                </p>
                <p className="text-xs text-gray-400 mt-1">
                  {formatRelativeTime(activity.timestamp)}
                </p>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
