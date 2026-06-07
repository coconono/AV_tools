# Image Transparency Tool (transparency.py)

## Purpose
Create a Python script that processes images to add, remove, or modify transparency/alpha channels.

## Core Features

### 1. Transparency Operations
- **Add Transparency**: Convert images to RGBA format and add alpha channel
- **Remove Transparency**: Flatten transparent images with a background color
- **Adjust Transparency**: Modify existing alpha channel values (increase/decrease opacity)
- **Extract Alpha Channel**: Save the alpha channel as a separate grayscale image

### 2. Input/Output
- Support common image formats: PNG, JPEG, WEBP, GIF, BMP, TIFF
- Handle single files or batch process entire directories
- Preserve original files with configurable output naming
- Support for recursive directory processing

### 3. Processing Options
- Set global opacity level (0-100%)
- Apply transparency based on color threshold (make specific colors transparent)
- Gradient transparency effects
- Preserve/flatten specific channels
- Optional background color for transparency removal (default: white)

## Command-Line Interface

```bash
# Add transparency
python transparency.py add input.jpg --opacity 80 --output output.png

# Remove transparency with custom background
python transparency.py remove input.png --background "#FF0000" --output output.jpg

# Make white pixels transparent
python transparency.py color-to-alpha input.png --color white --tolerance 10

# Batch process directory
python transparency.py add ./images/ --opacity 75 --recursive --output-dir ./processed/
```

## Technical Requirements
- Use Pillow (PIL) for image processing
- Include progress bars for batch operations (tqdm)
- Proper error handling and validation
- Support for command-line arguments (argparse)
- Logging for debugging and operation tracking
- gitignore file to exclude all sensitive or unnecessary files
- venv and requirements.txt for dependency management

## Error Handling
- Validate file formats before processing
- Handle corrupted or unsupported images gracefully
- Clear error messages for user mistakes
- Skip problematic files in batch mode with warnings

## Output
- Maintain original image quality when possible
- Default output format based on operation (PNG for transparency, JPEG for flattened)
- Option to overwrite or create new files with suffix/prefix
- Summary report after batch operations (files processed, errors, time taken)

python script that removes all white from a given image and saves the result as a new image with a transparent background. The script should take the input image path and output image path as arguments.

it should not overwrite the original image, but instead create a new image with the same name as the original image but with "_transparent" appended to the filename before the file extension. For example, if the original image is "image.png", the new image should be saved as "image_transparent.png".


it should use all available tools to accomplish this task, including reading the image, editing it to remove the white background, and saving the new image with a transparent background.

if needed, maintain a venv and requiresments.txt file to manage dependencies for the script.

create a gitignore file that ignores all files except for the python script and the README.md file.