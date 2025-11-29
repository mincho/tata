# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a memoir website project hosting the personal memoirs of Benjamin Vides Deneke (Tata). The site is designed to be deployed on GitHub Pages and presents a multi-chapter memoir initially written in Spanish.

## Repository Structure

- `index.html` - Main landing page with chapter navigation and audio player
- `source/tata_memoir_spanish.txt` - Complete Spanish-language memoir text (10 chapters covering 1935-2000s)
- `assets/style.css` - Stylesheet for the site (currently empty)
- `.nojekyll` - Ensures GitHub Pages serves the site correctly

## Deployment

This site is configured for GitHub Pages deployment:
- The `.nojekyll` file prevents Jekyll processing
- Content is served directly from the `main` branch
- No build process is required; changes to HTML/CSS are immediately deployable

## Source Content Organization

The memoir (`source/tata_memoir_spanish.txt`) is structured as follows:
- Introduction
- Chapter 1: Santa Ana origins (1935-1941)
- Chapter 2: San Salvador and La Pandilla Atómica (1941-1950)
- Chapter 3: El Club de los Pingüinos (1950s)
- Chapter 4: La Libertad and tunnel construction (late 1950s)
- Chapter 5: Philadelphia, Lookup & Wharton (1957-1967)
- Chapter 6: Europe and the Beetle (1965)
- Chapter 7: Return to San Salvador - Aída, Citibank (1967-1970)
- Chapter 8: Citibank and the internal war (1970s)
- Chapter 9: Washington, IDB and life between two worlds (1980s-1990s)
- Chapter 10: Final return - memory, roots and starting over (2000s onward)

## Current Site Structure

The `index.html` references:
- Three chapter pages (`/memoir/chapter-1.html`, `chapter-2.html`, `chapter-3.html`) - **not yet created**
- Audio file (`/audio/story-intro.mp3`) - **not yet created**
- Stylesheet at `/assets/style.css` - **currently empty**

## Development Workflow

When working on this site:
1. Edit HTML files directly - no build step required
2. Update `assets/style.css` for styling changes
3. Test locally by opening `index.html` in a browser
4. Commit and push to `main` branch to deploy to GitHub Pages

## Content Notes

- The memoir is written in a personal, reflective tone
- Chapters mix Spanish and English titles organically
- Content spans multiple countries: El Salvador, United States (Philadelphia, Washington DC), Europe
- Key themes: family, education, banking career, cultural identity, migration
- The text is meant for family members and descendants
