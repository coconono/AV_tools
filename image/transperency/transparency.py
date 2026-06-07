#!/usr/bin/env python3
"""
Image Transparency Tool
Processes images to add, remove, or modify transparency/alpha channels.
"""

import argparse
import logging
import os
import sys
from pathlib import Path
from typing import Tuple, Optional, List
from PIL import Image, ImageColor
from tqdm import tqdm


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TransparencyProcessor:
    """Handles image transparency operations."""
    
    SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tiff', '.tif'}
    
    def __init__(self):
        self.processed_count = 0
        self.error_count = 0
        self.errors = []
    
    def validate_image_file(self, file_path: Path) -> bool:
        """Validate if the file is a supported image format."""
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return False
        
        if file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            logger.error(f"Unsupported format: {file_path.suffix}")
            return False
        
        return True
    
    def add_transparency(self, image: Image.Image, opacity: float = 100.0) -> Image.Image:
        """
        Add or adjust transparency to an image.
        
        Args:
            image: PIL Image object
            opacity: Opacity level (0-100%)
        
        Returns:
            Image with transparency applied
        """
        # Convert to RGBA if not already
        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        
        # Adjust opacity if needed
        if opacity < 100:
            alpha = image.getchannel('A')
            # Scale alpha channel by opacity factor
            alpha = alpha.point(lambda x: int(x * (opacity / 100.0)))
            image.putalpha(alpha)
        
        return image
    
    def remove_transparency(self, image: Image.Image, background_color: str = 'white') -> Image.Image:
        """
        Remove transparency by flattening with a background color.
        
        Args:
            image: PIL Image object
            background_color: Background color name or hex code
        
        Returns:
            Flattened image without transparency
        """
        if image.mode == 'RGBA' or image.mode == 'LA':
            # Create background with specified color
            try:
                bg_color = ImageColor.getrgb(background_color)
            except ValueError:
                logger.warning(f"Invalid color '{background_color}', using white")
                bg_color = (255, 255, 255)
            
            background = Image.new('RGB', image.size, bg_color)
            
            # Paste image on background using alpha channel as mask
            if image.mode == 'RGBA':
                background.paste(image, mask=image.split()[3])
            else:
                background.paste(image, mask=image.split()[1])
            
            return background
        
        return image.convert('RGB')
    
    def color_to_alpha(self, image: Image.Image, color: str = 'white', tolerance: int = 10) -> Image.Image:
        """
        Make a specific color transparent.
        
        Args:
            image: PIL Image object
            color: Color to make transparent (name or hex)
            tolerance: Color matching tolerance (0-255)
        
        Returns:
            Image with specified color made transparent
        """
        # Convert to RGBA
        image = image.convert('RGBA')
        
        # Parse target color
        try:
            target_rgb = ImageColor.getrgb(color)
        except ValueError:
            logger.error(f"Invalid color: {color}")
            return image
        
        # Get pixel data
        pixels = image.load()
        width, height = image.size
        
        # Process each pixel
        for y in range(height):
            for x in range(width):
                r, g, b, a = pixels[x, y]
                
                # Check if pixel color matches target within tolerance
                if (abs(r - target_rgb[0]) <= tolerance and
                    abs(g - target_rgb[1]) <= tolerance and
                    abs(b - target_rgb[2]) <= tolerance):
                    # Make pixel transparent
                    pixels[x, y] = (r, g, b, 0)
        
        return image
    
    def extract_alpha(self, image: Image.Image) -> Optional[Image.Image]:
        """
        Extract alpha channel as a grayscale image.
        
        Args:
            image: PIL Image object
        
        Returns:
            Grayscale image of alpha channel or None if no alpha
        """
        if image.mode in ('RGBA', 'LA'):
            return image.getchannel('A')
        else:
            logger.warning("Image has no alpha channel to extract")
            return None
    
    def generate_output_path(self, input_path: Path, output_path: Optional[str], 
                           suffix: str = '_transparent', output_dir: Optional[Path] = None,
                           default_ext: str = '.png') -> Path:
        """
        Generate output file path.
        
        Args:
            input_path: Input file path
            output_path: Explicit output path (if provided)
            suffix: Suffix to add to filename
            output_dir: Output directory (if provided)
            default_ext: Default extension for output file
        
        Returns:
            Output file path
        """
        if output_path:
            return Path(output_path)
        
        # Generate automatic output path
        stem = input_path.stem
        ext = default_ext if default_ext else input_path.suffix
        
        if output_dir:
            output_dir.mkdir(parents=True, exist_ok=True)
            return output_dir / f"{stem}{suffix}{ext}"
        else:
            return input_path.parent / f"{stem}{suffix}{ext}"
    
    def process_file(self, input_path: Path, operation: str, **kwargs) -> bool:
        """
        Process a single image file.
        
        Args:
            input_path: Input file path
            operation: Operation to perform (add, remove, color-to-alpha, extract-alpha)
            **kwargs: Additional operation-specific arguments
        
        Returns:
            True if successful, False otherwise
        """
        if not self.validate_image_file(input_path):
            self.error_count += 1
            self.errors.append(f"{input_path}: Invalid file")
            return False
        
        try:
            # Open image
            image = Image.open(input_path)
            
            # Perform operation
            if operation == 'add':
                opacity = kwargs.get('opacity', 100.0)
                result = self.add_transparency(image, opacity)
                default_ext = '.png'
            
            elif operation == 'remove':
                background = kwargs.get('background', 'white')
                result = self.remove_transparency(image, background)
                default_ext = '.jpg'
            
            elif operation == 'color-to-alpha':
                color = kwargs.get('color', 'white')
                tolerance = kwargs.get('tolerance', 10)
                result = self.color_to_alpha(image, color, tolerance)
                default_ext = '.png'
            
            elif operation == 'extract-alpha':
                result = self.extract_alpha(image)
                if result is None:
                    self.error_count += 1
                    self.errors.append(f"{input_path}: No alpha channel")
                    return False
                default_ext = '.png'
            
            else:
                logger.error(f"Unknown operation: {operation}")
                self.error_count += 1
                return False
            
            # Generate output path
            output_path = self.generate_output_path(
                input_path,
                kwargs.get('output'),
                kwargs.get('suffix', '_transparent'),
                kwargs.get('output_dir'),
                default_ext
            )
            
            # Save result
            if default_ext == '.jpg' or output_path.suffix.lower() in ('.jpg', '.jpeg'):
                # Convert to RGB for JPEG
                if result.mode in ('RGBA', 'LA'):
                    result = result.convert('RGB')
                result.save(output_path, quality=95)
            else:
                result.save(output_path)
            
            logger.info(f"Processed: {input_path} -> {output_path}")
            self.processed_count += 1
            return True
        
        except Exception as e:
            logger.error(f"Error processing {input_path}: {e}")
            self.error_count += 1
            self.errors.append(f"{input_path}: {e}")
            return False
    
    def process_directory(self, input_dir: Path, operation: str, recursive: bool = False, **kwargs) -> None:
        """
        Process all images in a directory.
        
        Args:
            input_dir: Input directory path
            operation: Operation to perform
            recursive: Process subdirectories recursively
            **kwargs: Additional operation-specific arguments
        """
        # Collect all image files
        if recursive:
            files = []
            for ext in self.SUPPORTED_FORMATS:
                files.extend(input_dir.rglob(f"*{ext}"))
        else:
            files = []
            for ext in self.SUPPORTED_FORMATS:
                files.extend(input_dir.glob(f"*{ext}"))
        
        if not files:
            logger.warning(f"No supported image files found in {input_dir}")
            return
        
        # Process files with progress bar
        for file_path in tqdm(files, desc="Processing images"):
            self.process_file(file_path, operation, **kwargs)
    
    def print_summary(self) -> None:
        """Print processing summary."""
        print("\n" + "="*50)
        print("PROCESSING SUMMARY")
        print("="*50)
        print(f"Files processed: {self.processed_count}")
        print(f"Errors: {self.error_count}")
        
        if self.errors and len(self.errors) <= 10:
            print("\nErrors:")
            for error in self.errors:
                print(f"  - {error}")
        elif self.errors:
            print(f"\nShowing first 10 of {len(self.errors)} errors:")
            for error in self.errors[:10]:
                print(f"  - {error}")


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Image Transparency Tool - Process images to add, remove, or modify transparency',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Add transparency with 80% opacity
  %(prog)s add input.jpg --opacity 80 --output output.png
  
  # Remove transparency with red background
  %(prog)s remove input.png --background "#FF0000" --output output.jpg
  
  # Make white pixels transparent
  %(prog)s color-to-alpha input.png --color white --tolerance 10
  
  # Extract alpha channel
  %(prog)s extract-alpha input.png --output alpha.png
  
  # Batch process directory
  %(prog)s add ./images/ --opacity 75 --recursive --output-dir ./processed/
        """
    )
    
    parser.add_argument('operation', 
                       choices=['add', 'remove', 'color-to-alpha', 'extract-alpha'],
                       help='Operation to perform')
    
    parser.add_argument('input', 
                       help='Input file or directory path')
    
    parser.add_argument('-o', '--output',
                       help='Output file path (for single file processing)')
    
    parser.add_argument('--output-dir',
                       help='Output directory (for batch processing)')
    
    parser.add_argument('--opacity', type=float, default=100.0,
                       help='Opacity level (0-100%%, default: 100)')
    
    parser.add_argument('--background', default='white',
                       help='Background color for transparency removal (default: white)')
    
    parser.add_argument('--color', default='white',
                       help='Color to make transparent (default: white)')
    
    parser.add_argument('--tolerance', type=int, default=10,
                       help='Color matching tolerance (0-255, default: 10)')
    
    parser.add_argument('--suffix', default='_transparent',
                       help='Suffix for output filenames (default: _transparent)')
    
    parser.add_argument('-r', '--recursive', action='store_true',
                       help='Process directories recursively')
    
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose logging')
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_arguments()
    
    # Set logging level
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Validate inputs
    input_path = Path(args.input)
    if not input_path.exists():
        logger.error(f"Input path does not exist: {input_path}")
        sys.exit(1)
    
    # Validate opacity
    if not 0 <= args.opacity <= 100:
        logger.error("Opacity must be between 0 and 100")
        sys.exit(1)
    
    # Validate tolerance
    if not 0 <= args.tolerance <= 255:
        logger.error("Tolerance must be between 0 and 255")
        sys.exit(1)
    
    # Create processor
    processor = TransparencyProcessor()
    
    # Prepare kwargs
    kwargs = {
        'output': args.output,
        'output_dir': Path(args.output_dir) if args.output_dir else None,
        'opacity': args.opacity,
        'background': args.background,
        'color': args.color,
        'tolerance': args.tolerance,
        'suffix': args.suffix
    }
    
    # Process
    if input_path.is_file():
        processor.process_file(input_path, args.operation, **kwargs)
    elif input_path.is_dir():
        processor.process_directory(input_path, args.operation, args.recursive, **kwargs)
    else:
        logger.error(f"Invalid input path: {input_path}")
        sys.exit(1)
    
    # Print summary
    processor.print_summary()
    
    # Exit with appropriate code
    sys.exit(0 if processor.error_count == 0 else 1)


if __name__ == '__main__':
    main()
