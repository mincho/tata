#!/bin/bash

# Web optimization script for memoir images
# This will create optimized versions in assets/images/

SOURCE_DIR="source/pics"
OUTPUT_DIR="assets/images"

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Maximum width for images (good for memoir site)
MAX_WIDTH=1200

# Quality setting (80 is a good balance)
QUALITY=82

echo "Optimizing images for web..."
echo "Source: $SOURCE_DIR"
echo "Output: $OUTPUT_DIR"
echo "Max width: ${MAX_WIDTH}px"
echo "Quality: ${QUALITY}%"
echo ""

# Counter
count=0

# Process each JPG file
for img in "$SOURCE_DIR"/*.JPG; do
    # Skip if no files found
    [ -e "$img" ] || continue

    # Get filename without path
    filename=$(basename "$img")
    # Convert to lowercase and change extension
    output_name="${filename%.JPG}.jpg"
    output_name="${output_name%.jpg}.jpg"
    output_path="$OUTPUT_DIR/$output_name"

    # Get original dimensions
    original_size=$(magick identify -format "%wx%h" "$img")
    original_filesize=$(ls -lh "$img" | awk '{print $5}')

    echo "Processing: $filename"
    echo "  Original: $original_size, $original_filesize"

    # Resize and optimize with ImageMagick
    magick "$img" \
        -strip \
        -resize "${MAX_WIDTH}x>" \
        -quality $QUALITY \
        -interlace Plane \
        "$output_path"

    # Get new dimensions and size
    new_size=$(magick identify -format "%wx%h" "$output_path")
    new_filesize=$(ls -lh "$output_path" | awk '{print $5}')

    echo "  Optimized: $new_size, $new_filesize"
    echo "  Saved to: $output_path"
    echo ""

    ((count++))
done

echo "✓ Optimization complete!"
echo "✓ Processed $count images"
echo "✓ Images saved to: $OUTPUT_DIR"
