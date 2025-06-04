/**
 * Worker Thread Manager
 * Offloads heavy processing to Web Workers for better performance
 */

import { useCallback } from 'react';

interface WorkerTask {
  id: string;
  type: string;
  data: any;
  priority: number;
  timestamp: number;
}

interface WorkerResult {
  id: string;
  success: boolean;
  data?: any;
  error?: string;
  duration: number;
}

export class WorkerManager {
  private workers: Worker[] = [];
  private taskQueue: WorkerTask[] = [];
  private activeJobs: Map<string, { worker: Worker; startTime: number }> = new Map();
  private callbacks: Map<string, (result: WorkerResult) => void> = new Map();
  private maxWorkers: number;
  private workerScript: string;

  constructor(maxWorkers = navigator.hardwareConcurrency || 4) {
    this.maxWorkers = maxWorkers;
    this.workerScript = this.createWorkerScript();
    this.initializeWorkers();
  }

  /**
   * Process a task using worker threads
   */
  async process<T>(type: string, data: any, priority = 0): Promise<T> {
    return new Promise((resolve, reject) => {
      const id = this.generateId();
      const task: WorkerTask = {
        id,
        type,
        data,
        priority,
        timestamp: Date.now(),
      };

      this.callbacks.set(id, (result: WorkerResult) => {
        if (result.success) {
          resolve(result.data as T);
        } else {
          reject(new Error(result.error));
        }
      });

      this.enqueueTask(task);
    });
  }

  /**
   * Process multiple tasks in parallel
   */
  async processBatch<T>(
    tasks: Array<{ type: string; data: any; priority?: number }>
  ): Promise<T[]> {
    const promises = tasks.map(task =>
      this.process<T>(task.type, task.data, task.priority)
    );
    return Promise.all(promises);
  }

  /**
   * Get worker pool statistics
   */
  getStats() {
    return {
      totalWorkers: this.workers.length,
      activeJobs: this.activeJobs.size,
      queuedTasks: this.taskQueue.length,
      averageProcessingTime: this.calculateAverageProcessingTime(),
    };
  }

  /**
   * Terminate all workers
   */
  terminate() {
    this.workers.forEach(worker => worker.terminate());
    this.workers = [];
    this.activeJobs.clear();
    this.taskQueue = [];
    this.callbacks.clear();
  }

  // Private methods

  private initializeWorkers() {
    for (let i = 0; i < this.maxWorkers; i++) {
      this.createWorker();
    }
  }

  private createWorker() {
    const blob = new Blob([this.workerScript], { type: 'application/javascript' });
    const workerUrl = URL.createObjectURL(blob);
    const worker = new Worker(workerUrl);

    worker.onmessage = (event: MessageEvent<WorkerResult>) => {
      this.handleWorkerResult(event.data, worker);
    };

    worker.onerror = (error) => {
      console.error('Worker error:', error);
      this.handleWorkerError(worker);
    };

    this.workers.push(worker);
    this.processNextTask(worker);
  }

  private enqueueTask(task: WorkerTask) {
    // Insert task based on priority
    const insertIndex = this.taskQueue.findIndex(t => t.priority < task.priority);
    if (insertIndex === -1) {
      this.taskQueue.push(task);
    } else {
      this.taskQueue.splice(insertIndex, 0, task);
    }

    // Try to process immediately if workers available
    this.tryProcessTasks();
  }

  private tryProcessTasks() {
    const availableWorkers = this.workers.filter(
      worker => !Array.from(this.activeJobs.values()).some(job => job.worker === worker)
    );

    availableWorkers.forEach(worker => this.processNextTask(worker));
  }

  private processNextTask(worker: Worker) {
    if (this.taskQueue.length === 0) return;

    const task = this.taskQueue.shift()!;
    this.activeJobs.set(task.id, { worker, startTime: Date.now() });
    worker.postMessage(task);
  }

  private handleWorkerResult(result: WorkerResult, worker: Worker) {
    const job = this.activeJobs.get(result.id);
    if (job) {
      result.duration = Date.now() - job.startTime;
      this.activeJobs.delete(result.id);
    }

    const callback = this.callbacks.get(result.id);
    if (callback) {
      callback(result);
      this.callbacks.delete(result.id);
    }

    // Process next task
    this.processNextTask(worker);
  }

  private handleWorkerError(worker: Worker) {
    // Find and reject all tasks assigned to this worker
    this.activeJobs.forEach((job, taskId) => {
      if (job.worker === worker) {
        const callback = this.callbacks.get(taskId);
        if (callback) {
          callback({
            id: taskId,
            success: false,
            error: 'Worker crashed',
            duration: Date.now() - job.startTime,
          });
          this.callbacks.delete(taskId);
        }
        this.activeJobs.delete(taskId);
      }
    });

    // Replace the crashed worker
    const index = this.workers.indexOf(worker);
    if (index !== -1) {
      this.workers.splice(index, 1);
      this.createWorker();
    }
  }

  private generateId(): string {
    return `task-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private calculateAverageProcessingTime(): number {
    // This would be implemented with actual metrics tracking
    return 0;
  }

  private createWorkerScript(): string {
    return `
      // Worker script for processing tasks
      self.onmessage = async function(event) {
        const task = event.data;
        const startTime = performance.now();
        
        try {
          let result;
          
          switch (task.type) {
            case 'analyze-text':
              result = await analyzeText(task.data);
              break;
              
            case 'process-image':
              result = await processImage(task.data);
              break;
              
            case 'generate-report':
              result = await generateReport(task.data);
              break;
              
            case 'optimize-data':
              result = await optimizeData(task.data);
              break;
              
            case 'calculate-metrics':
              result = await calculateMetrics(task.data);
              break;
              
            default:
              throw new Error('Unknown task type: ' + task.type);
          }
          
          self.postMessage({
            id: task.id,
            success: true,
            data: result,
            duration: performance.now() - startTime
          });
        } catch (error) {
          self.postMessage({
            id: task.id,
            success: false,
            error: error.message,
            duration: performance.now() - startTime
          });
        }
      };
      
      // Task processing functions
      
      async function analyzeText(data) {
        // Text analysis logic
        const { text, options } = data;
        const words = text.split(/\\s+/);
        const sentences = text.split(/[.!?]+/);
        
        return {
          wordCount: words.length,
          sentenceCount: sentences.length,
          averageWordLength: words.reduce((sum, word) => sum + word.length, 0) / words.length,
          // Add more complex analysis as needed
        };
      }
      
      async function processImage(data) {
        // Image processing logic (simplified)
        const { imageData, operation } = data;
        
        switch (operation) {
          case 'resize':
            return resizeImage(imageData, data.width, data.height);
          case 'compress':
            return compressImage(imageData, data.quality);
          case 'analyze':
            return analyzeImage(imageData);
          default:
            return imageData;
        }
      }
      
      async function generateReport(data) {
        // Report generation logic
        const { type, content, format } = data;
        
        // Process report data
        const processed = {
          title: content.title,
          sections: content.sections?.map(section => ({
            ...section,
            processed: true,
            timestamp: new Date().toISOString()
          })),
          metadata: {
            generated: new Date().toISOString(),
            version: '1.0',
            format
          }
        };
        
        return processed;
      }
      
      async function optimizeData(data) {
        // Data optimization logic
        const { dataset, optimization } = data;
        
        if (optimization === 'dedupe') {
          const seen = new Set();
          return dataset.filter(item => {
            const key = JSON.stringify(item);
            if (seen.has(key)) return false;
            seen.add(key);
            return true;
          });
        }
        
        if (optimization === 'sort') {
          return dataset.sort((a, b) => {
            if (data.sortKey) {
              return a[data.sortKey] > b[data.sortKey] ? 1 : -1;
            }
            return 0;
          });
        }
        
        return dataset;
      }
      
      async function calculateMetrics(data) {
        // Metrics calculation logic
        const { values, metrics } = data;
        const results = {};
        
        if (metrics.includes('mean')) {
          results.mean = values.reduce((sum, val) => sum + val, 0) / values.length;
        }
        
        if (metrics.includes('median')) {
          const sorted = [...values].sort((a, b) => a - b);
          results.median = sorted[Math.floor(sorted.length / 2)];
        }
        
        if (metrics.includes('stdDev')) {
          const mean = results.mean || values.reduce((sum, val) => sum + val, 0) / values.length;
          const variance = values.reduce((sum, val) => sum + Math.pow(val - mean, 2), 0) / values.length;
          results.stdDev = Math.sqrt(variance);
        }
        
        return results;
      }
      
      // Helper functions
      
      function resizeImage(imageData, width, height) {
        // Simplified image resize
        return { ...imageData, width, height, resized: true };
      }
      
      function compressImage(imageData, quality) {
        // Simplified image compression
        return { ...imageData, quality, compressed: true };
      }
      
      function analyzeImage(imageData) {
        // Simplified image analysis
        return {
          width: imageData.width,
          height: imageData.height,
          aspectRatio: imageData.width / imageData.height,
          pixels: imageData.width * imageData.height
        };
      }
    `;
  }
}

// Singleton instance
export const workerManager = new WorkerManager();

// React hook for using workers
export function useWorker() {
  const process = useCallback(async <T>(type: string, data: any, priority?: number): Promise<T> => {
    return workerManager.process<T>(type, data, priority);
  }, []);

  const processBatch = useCallback(async <T>(
    tasks: Array<{ type: string; data: any; priority?: number }>
  ): Promise<T[]> => {
    return workerManager.processBatch<T>(tasks);
  }, []);

  const stats = useCallback(() => {
    return workerManager.getStats();
  }, []);

  return { process, processBatch, stats };
}
