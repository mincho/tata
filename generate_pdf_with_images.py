#!/usr/bin/env python3
"""
Generate PDF versions of the memoir with embedded images
"""
import os
import subprocess
import re
from pathlib import Path

def fix_image_paths(html_content, base_path='/Users/ben/dev/tata'):
    """Convert relative image paths to absolute file:// URLs"""
    # Fix ../assets/images/ paths (from chapter files)
    html_content = re.sub(
        r'src="../assets/images/',
        f'src="file://{base_path}/assets/images/',
        html_content
    )
    # Fix assets/images/ paths (from index file)
    html_content = re.sub(
        r'src="assets/images/',
        f'src="file://{base_path}/assets/images/',
        html_content
    )
    return html_content

def create_all_chapters_html(language='es'):
    """Create a single HTML file with all chapters for PDF generation"""

    base_path = '/Users/ben/dev/tata'
    os.chdir(base_path)

    if language == 'es':
        index_file = 'index.html'
        chapter_pattern = 'chapters/chapter-{}.html'
        output_file = 'all_chapters_es.html'
        title = 'Memorias de Benjamin Vides Deneke'
    else:
        index_file = 'index-en.html'
        chapter_pattern = 'chapters/chapter-{}-en.html'
        output_file = 'all_chapters_en.html'
        title = 'Memoirs of Benjamin Vides Deneke'

    html_content = f'''<!DOCTYPE html>
<html lang="{language}">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        @page {{
            margin: 2cm;
            size: letter;
        }}
        body {{
            font-family: Georgia, serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            color: #333;
        }}
        h1 {{
            font-size: 2em;
            margin-top: 1em;
            page-break-after: avoid;
        }}
        h2 {{
            font-size: 1.5em;
            margin-top: 1.5em;
            page-break-after: avoid;
        }}
        h3 {{
            font-size: 1.2em;
            margin-top: 1.2em;
            page-break-after: avoid;
        }}
        p {{
            margin: 1em 0;
            text-align: justify;
        }}
        figure {{
            page-break-inside: avoid;
            margin: 2em 0;
            text-align: center;
        }}
        img {{
            max-width: 100%;
            height: auto;
        }}
        figcaption {{
            font-style: italic;
            font-size: 0.9em;
            margin-top: 0.5em;
            color: #666;
        }}
        .chapter-break {{
            page-break-before: always;
        }}
        .signature {{
            text-align: right;
            font-style: italic;
            margin-top: 2em;
        }}
        .intro-section {{
            margin-bottom: 3em;
        }}
        .chapter-header {{
            margin-top: 2em;
            margin-bottom: 2em;
        }}
        .chapter-number {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}
        .chapter-period {{
            font-size: 0.9em;
            color: #999;
            font-style: italic;
        }}
        .image-grid {{
            display: flex;
            gap: 1em;
            justify-content: center;
            flex-wrap: wrap;
        }}
        .image-grid figure {{
            flex: 1;
            min-width: 300px;
            max-width: 45%;
        }}
        .memoir-image {{
            margin: 2em 0;
        }}
        .memoir-image.medium {{
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
        }}
        .image-caption {{
            font-style: italic;
            color: #666;
            margin-top: 0.5em;
        }}
    </style>
</head>
<body>
'''

    # Add index introduction
    with open(index_file, 'r', encoding='utf-8') as f:
        index_html = f.read()
        # Extract the intro section
        intro_match = re.search(r'<section class="intro-section">(.*?)</section>', index_html, re.DOTALL)
        if intro_match:
            intro_content = intro_match.group(1)
            intro_content = fix_image_paths(intro_content, base_path)
            html_content += '<div class="intro-section">' + intro_content + '</div>\n'

    # Add each chapter
    for i in range(1, 11):
        chapter_file = chapter_pattern.format(i)
        if os.path.exists(chapter_file):
            with open(chapter_file, 'r', encoding='utf-8') as f:
                chapter_html = f.read()

                # Extract chapter content
                chapter_match = re.search(
                    r'<article class="chapter-header">(.*?)</article>\s*<div class="chapter-content">(.*?)</div>\s*<nav class="chapter-nav-buttons">',
                    chapter_html,
                    re.DOTALL
                )

                if chapter_match:
                    header_content = chapter_match.group(1)
                    body_content = chapter_match.group(2)

                    # Fix image paths
                    header_content = fix_image_paths(header_content, base_path)
                    body_content = fix_image_paths(body_content, base_path)

                    html_content += f'\n<div class="chapter-break"></div>\n'
                    html_content += '<article class="chapter-header">' + header_content + '</article>\n'
                    html_content += '<div class="chapter-content">' + body_content + '</div>\n'

    html_content += '''
</body>
</html>
'''

    # Write the combined HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"  ✓ Created {output_file}")
    return output_file

def generate_pdf_from_html(html_file, output_file, language='es'):
    """Generate PDF from HTML file using weasyprint"""

    if language == 'es':
        title = 'Memorias de Benjamin Vides Deneke'
    else:
        title = 'Memoirs of Benjamin Vides Deneke'

    print(f"\nGenerating {title}...")

    # Use weasyprint with base URL set to handle relative paths
    base_path = '/Users/ben/dev/tata'
    result = subprocess.run(
        [
            'weasyprint',
            '--base-url', f'file://{base_path}/',
            '--presentational-hints',
            html_file,
            output_file
        ],
        capture_output=True,
        text=True,
        cwd=base_path
    )

    if result.returncode == 0:
        size = os.path.getsize(output_file) / (1024 * 1024)
        print(f"  ✓ Successfully generated {output_file} ({size:.1f} MB)")
        return True
    else:
        print(f"  ✗ Error generating {output_file}")
        if result.stderr:
            # Filter out common warnings
            errors = []
            for line in result.stderr.split('\n'):
                if 'WARNING' not in line and line.strip():
                    errors.append(line)
            if errors:
                print('\n'.join(errors[:10]))  # Show first 10 real errors
        return False

def main():
    base_path = '/Users/ben/dev/tata'
    os.chdir(base_path)

    print("Creating PDF versions of the memoir (with images)...")
    print("=" * 60)

    # Create combined HTML files
    print("\n1. Creating combined HTML for Spanish version...")
    spanish_html = create_all_chapters_html('es')

    print("\n2. Creating combined HTML for English version...")
    english_html = create_all_chapters_html('en')

    # Generate PDFs
    print("\n3. Generating Spanish PDF with images...")
    spanish_success = generate_pdf_from_html(spanish_html, 'Memorias_Benjamin_Vides_Deneke.pdf', 'es')

    print("\n4. Generating English PDF with images...")
    english_success = generate_pdf_from_html(english_html, 'Memoirs_Benjamin_Vides_Deneke.pdf', 'en')

    # Clean up temporary files
    print("\n5. Cleaning up temporary files...")
    if os.path.exists(spanish_html):
        os.remove(spanish_html)
        print(f"  ✓ Removed {spanish_html}")
    if os.path.exists(english_html):
        os.remove(english_html)
        print(f"  ✓ Removed {english_html}")

    print("\n" + "=" * 60)

    if spanish_success and english_success:
        print("✓ PDF generation complete!")
        print("\nGenerated files:")
        if os.path.exists('Memorias_Benjamin_Vides_Deneke.pdf'):
            size = os.path.getsize('Memorias_Benjamin_Vides_Deneke.pdf') / (1024 * 1024)
            print(f"  - Memorias_Benjamin_Vides_Deneke.pdf ({size:.1f} MB)")
        if os.path.exists('Memoirs_Benjamin_Vides_Deneke.pdf'):
            size = os.path.getsize('Memoirs_Benjamin_Vides_Deneke.pdf') / (1024 * 1024)
            print(f"  - Memoirs_Benjamin_Vides_Deneke.pdf ({size:.1f} MB)")
    else:
        print("⚠ PDF generation completed with some errors")

if __name__ == '__main__':
    main()
