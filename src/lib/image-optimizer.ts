import sharp from 'sharp';

/**
 * Image optimization utilities for the Brand Audit Tool
 * 
 * Provides image processing capabilities including resizing, format conversion,
 * quality optimization, and metadata extraction.
 * 
 * @module ImageOptimization
 */

/**
 * Image processing options
 */
export interface ImageOptimizationOptions {
  /** Maximum width in pixels */
  maxWidth?: number;
  /** Maximum height in pixels */
  maxHeight?: number;
  /** JPEG/WebP quality (1-100) */
  quality?: number;
  /** Output format */
  format?: 'jpeg' | 'png' | 'webp' | 'avif';
  /** Preserve aspect ratio */
  preserveAspectRatio?: boolean;
  /** Add progressive encoding for JPEG */
  progressive?: boolean;
  /** Strip metadata */
  stripMetadata?: boolean;
}

/**
 * Image metadata information
 */
export interface ImageMetadata {
  width: number;
  height: number;
  format: string;
  size: number;
  hasAlpha: boolean;
  density?: number;
  colorSpace?: string;
  orientation?: number;
}

/**
 * Optimization result
 */
export interface OptimizationResult {
  buffer: Buffer;
  metadata: ImageMetadata;
  savedBytes: number;
  compressionRatio: number;
}

/**
 * Default optimization presets
 */
export const OptimizationPresets = {
  /** High quality for logos and brand marks */
  logo: {
    maxWidth: 800,
    maxHeight: 800,
    quality: 95,
    format: 'png' as const,
    preserveAspectRatio: true,
    stripMetadata: false,
  },
  
  /** Web-optimized images for general use */
  web: {
    maxWidth: 1920,
    maxHeight: 1080,
    quality: 85,
    format: 'jpeg' as const,
    progressive: true,
    stripMetadata: true,
  },
  
  /** Thumbnail generation */
  thumbnail: {
    maxWidth: 300,
    maxHeight: 300,
    quality: 80,
    format: 'jpeg' as const,
    progressive: true,
    stripMetadata: true,
  },
  
  /** Hero/banner images */
  hero: {
    maxWidth: 2400,
    maxHeight: 1200,
    quality: 90,
    format: 'webp' as const,
    stripMetadata: true,
  },
  
  /** Mobile-optimized images */
  mobile: {
    maxWidth: 768,
    maxHeight: 1024,
    quality: 80,
    format: 'webp' as const,
    stripMetadata: true,
  },
} as const;

/**
 * Optimize image buffer with specified options
 * 
 * @param {Buffer} inputBuffer - Input image buffer
 * @param {ImageOptimizationOptions} options - Optimization options
 * @returns {Promise<OptimizationResult>} Optimized image and metadata
 * 
 * @example
 * ```typescript
 * const result = await optimizeImage(imageBuffer, {
 *   maxWidth: 1200,
 *   quality: 85,
 *   format: 'webp'
 * });
 * ```
 */
export async function optimizeImage(
  inputBuffer: Buffer,
  options: ImageOptimizationOptions = {}
): Promise<OptimizationResult> {
  const originalSize = inputBuffer.length;
  
  // Get original metadata
  const originalMetadata = await sharp(inputBuffer).metadata();
  
  // Start processing pipeline
  let pipeline = sharp(inputBuffer);
  
  // Resize if needed
  if (options.maxWidth || options.maxHeight) {
    const resizeOptions: sharp.ResizeOptions = {
      width: options.maxWidth,
      height: options.maxHeight,
      fit: options.preserveAspectRatio !== false ? 'inside' : 'cover',
      withoutEnlargement: true,
    };
    
    pipeline = pipeline.resize(resizeOptions);
  }
  
  // Strip metadata if requested
  if (options.stripMetadata) {
    pipeline = pipeline.rotate(); // Auto-rotate based on EXIF then strip metadata
  }
  
  // Convert format and apply quality settings
  const format = options.format || detectOptimalFormat(originalMetadata);
  
  switch (format) {
    case 'jpeg':
      pipeline = pipeline.jpeg({
        quality: options.quality || 85,
        progressive: options.progressive !== false,
        mozjpeg: true, // Use mozjpeg encoder for better compression
      });
      break;
      
    case 'png':
      pipeline = pipeline.png({
        quality: options.quality || 95,
        compressionLevel: 9,
        adaptiveFiltering: true,
        palette: true,
      });
      break;
      
    case 'webp':
      pipeline = pipeline.webp({
        quality: options.quality || 85,
        lossless: false,
        nearLossless: true,
        smartSubsample: true,
        effort: 6,
      });
      break;
      
    case 'avif':
      pipeline = pipeline.avif({
        quality: options.quality || 80,
      });
      break;
  }
  
  // Process the image
  const { data: outputBuffer, info } = await pipeline.toBuffer({ resolveWithObject: true });
  
  // Calculate savings
  const savedBytes = originalSize - outputBuffer.length;
  const compressionRatio = outputBuffer.length / originalSize;
  
  return {
    buffer: outputBuffer,
    metadata: {
      width: info.width,
      height: info.height,
      format: info.format,
      size: outputBuffer.length,
      hasAlpha: info.channels === 4,
    },
    savedBytes,
    compressionRatio,
  };
}

/**
 * Optimize image for specific use case using presets
 * 
 * @param {Buffer} inputBuffer - Input image buffer
 * @param {keyof typeof OptimizationPresets} preset - Preset name
 * @returns {Promise<OptimizationResult>} Optimized image
 * 
 * @example
 * ```typescript
 * const result = await optimizeImageWithPreset(buffer, 'logo');
 * ```
 */
export async function optimizeImageWithPreset(
  inputBuffer: Buffer,
  preset: keyof typeof OptimizationPresets
): Promise<OptimizationResult> {
  return optimizeImage(inputBuffer, OptimizationPresets[preset]);
}

/**
 * Generate multiple image variants for responsive design
 * 
 * @param {Buffer} inputBuffer - Input image buffer
 * @param {number[]} widths - Array of target widths
 * @param {Partial<ImageOptimizationOptions>} baseOptions - Base options for all variants
 * @returns {Promise<Map<number, OptimizationResult>>} Map of width to optimization result
 * 
 * @example
 * ```typescript
 * const variants = await generateResponsiveImages(buffer, [320, 768, 1024, 1920]);
 * ```
 */
export async function generateResponsiveImages(
  inputBuffer: Buffer,
  widths: number[],
  baseOptions: Partial<ImageOptimizationOptions> = {}
): Promise<Map<number, OptimizationResult>> {
  const results = new Map<number, OptimizationResult>();
  
  await Promise.all(
    widths.map(async (width) => {
      const options: ImageOptimizationOptions = {
        ...baseOptions,
        maxWidth: width,
        format: baseOptions.format || 'webp',
        quality: baseOptions.quality || getQualityForWidth(width),
      };
      
      const result = await optimizeImage(inputBuffer, options);
      results.set(width, result);
    })
  );
  
  return results;
}

/**
 * Extract dominant colors from image
 * 
 * @param {Buffer} inputBuffer - Input image buffer
 * @param {number} colorCount - Number of colors to extract
 * @returns {Promise<string[]>} Array of hex color strings
 */
export async function extractDominantColors(
  inputBuffer: Buffer,
  colorCount = 5
): Promise<string[]> {
  // Resize to small size for faster processing
  const { data, info } = await sharp(inputBuffer)
    .resize(100, 100, { fit: 'cover' })
    .raw()
    .toBuffer({ resolveWithObject: true });
  
  // Simple color quantization
  const colorMap = new Map<string, number>();
  // const pixelCount = info.width * info.height; // Unused for now
  const channels = info.channels;

  if (!data || data.length === 0) {
    return ['#000000']; // Return black as fallback
  }

  for (let i = 0; i < data.length; i += channels) {
    const r = Math.floor((data[i] || 0) / 16) * 16;
    const g = Math.floor((data[i + 1] || 0) / 16) * 16;
    const b = Math.floor((data[i + 2] || 0) / 16) * 16;
    const hex = `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;

    colorMap.set(hex, (colorMap.get(hex) || 0) + 1);
  }
  
  // Sort by frequency and return top colors
  return Array.from(colorMap.entries())
    .sort((a, b) => b[1] - a[1])
    .slice(0, colorCount)
    .map(([color]) => color);
}

/**
 * Generate blur hash for lazy loading
 * 
 * @param {Buffer} inputBuffer - Input image buffer
 * @returns {Promise<string>} Base64 encoded blur hash
 */
export async function generateBlurHash(inputBuffer: Buffer): Promise<string> {
  const data = await sharp(inputBuffer)
    .resize(20, 20, { fit: 'cover' })
    .blur(5)
    .jpeg({ quality: 50 })
    .toBuffer();

  return `data:image/jpeg;base64,${data.toString('base64')}`;
}

/**
 * Validate image and get metadata
 * 
 * @param {Buffer} inputBuffer - Input image buffer
 * @returns {Promise<ImageMetadata>} Image metadata
 * @throws {Error} If image is invalid
 */
export async function validateImage(inputBuffer: Buffer): Promise<ImageMetadata> {
  try {
    const metadata = await sharp(inputBuffer).metadata();
    
    if (!metadata.width || !metadata.height) {
      throw new Error('Invalid image dimensions');
    }
    
    return {
      width: metadata.width,
      height: metadata.height,
      format: metadata.format || 'unknown',
      size: inputBuffer.length,
      hasAlpha: metadata.channels === 4,
      density: metadata.density || 72,
      colorSpace: metadata.space || 'srgb',
      orientation: metadata.orientation || 1,
    };
  } catch (error) {
    throw new Error(`Invalid image: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Convert image to different format
 * 
 * @param {Buffer} inputBuffer - Input image buffer
 * @param {string} targetFormat - Target format
 * @returns {Promise<Buffer>} Converted image buffer
 */
export async function convertImageFormat(
  inputBuffer: Buffer,
  targetFormat: 'jpeg' | 'png' | 'webp' | 'avif'
): Promise<Buffer> {
  const pipeline = sharp(inputBuffer);
  
  switch (targetFormat) {
    case 'jpeg':
      return pipeline.jpeg({ quality: 90, progressive: true }).toBuffer();
    case 'png':
      return pipeline.png({ compressionLevel: 9 }).toBuffer();
    case 'webp':
      return pipeline.webp({ quality: 90 }).toBuffer();
    case 'avif':
      return pipeline.avif({ quality: 85 }).toBuffer();
    default:
      throw new Error(`Unsupported format: ${targetFormat}`);
  }
}

/**
 * Create composite image (e.g., for brand collages)
 * 
 * @param {Buffer[]} images - Array of image buffers
 * @param {Object} options - Composite options
 * @returns {Promise<Buffer>} Composite image buffer
 */
export async function createComposite(
  images: Buffer[],
  options: {
    width: number;
    height: number;
    columns: number;
    gap?: number;
    backgroundColor?: string;
  }
): Promise<Buffer> {
  const { width, height, columns, gap = 0, backgroundColor = '#ffffff' } = options;
  const rows = Math.ceil(images.length / columns);
  const cellWidth = Math.floor((width - gap * (columns - 1)) / columns);
  const cellHeight = Math.floor((height - gap * (rows - 1)) / rows);
  
  const composites = await Promise.all(
    images.map(async (image, index) => {
      const row = Math.floor(index / columns);
      const col = index % columns;
      const x = col * (cellWidth + gap);
      const y = row * (cellHeight + gap);
      
      const resized = await sharp(image)
        .resize(cellWidth, cellHeight, { fit: 'cover' })
        .toBuffer();
      
      return { input: resized, left: x, top: y };
    })
  );
  
  return sharp({
    create: {
      width,
      height,
      channels: 4,
      background: backgroundColor,
    },
  })
    .composite(composites)
    .jpeg({ quality: 90 })
    .toBuffer();
}

/**
 * Helper to detect optimal format based on image characteristics
 */
function detectOptimalFormat(metadata: sharp.Metadata): 'jpeg' | 'png' | 'webp' {
  // Use PNG for images with transparency
  if (metadata.channels === 4 && metadata.density && metadata.density < 300) {
    return 'png';
  }
  
  // Use WebP for modern browsers (with fallback handling in frontend)
  if (metadata.width && metadata.width > 1000) {
    return 'webp';
  }
  
  // Default to JPEG for photographs
  return 'jpeg';
}

/**
 * Get quality setting based on image width
 */
function getQualityForWidth(width: number): number {
  if (width <= 400) return 75;
  if (width <= 800) return 80;
  if (width <= 1200) return 85;
  return 90;
}
