# Python Static Site Generator (SSG)

A robust and lightweight static site generator (SSG) designed for converting Markdown content into professional, template-based websites.

## Description

This SSG is a full-featured tool that provides a seamless workflow for developers and content creators to manage static websites. It transforms a directory of Markdown files (`content/`) into a structured HTML website (`docs/`) using a flexible HTML template (`template.html`). The project features recursive page generation, automatic static asset management, and a custom Markdown-to-HTML conversion engine.

## Motivation

Static site generation is often overcomplicated by heavy frameworks. This project was developed to provide a minimalist yet powerful alternative by:
- **Ensuring Simplicity:** Leveraging only the Python standard library for maximum portability and zero external dependencies.
- **Streamlining Workflow:** Automating the transition from raw Markdown content to a deployable static site with a single command.
- **Improving Accuracy:** Implementing a custom parsing engine that ensures precise control over HTML output and title extraction.
- **Enhancing Flexibility:** Supporting basepath configurations for easy deployment to GitHub Pages or custom subdirectories.

## Quick Start

### Prerequisites
- Python 3.10+
- A terminal (Bash/Zsh recommended for shell scripts)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/joseflores1/ssg
   cd ssg
   ```

2. **Ensure execution permissions for scripts:**
   ```bash
   chmod +x build.sh main.sh test.sh
   ```

3. **Run the build and development server:**
   ```bash
   ./main.sh
   ```
   The application will be built into the `docs/` directory and served at `http://localhost:8888`.

## Usage

### Project Structure
- `content/`: Place your Markdown files here. The generator mirrors this directory structure in the output.
- `static/`: All files here (images, CSS, etc.) are copied directly to the output directory.
- `template.html`: The base HTML structure. Use `{{ Title }}` and `{{ Content }}` placeholders.
- `docs/`: The destination directory for the generated site (ideal for GitHub Pages).

### Commands
- `./build.sh`: Generates the site into the `docs/` directory.
- `./main.sh`: Cleans `docs/`, builds the site, and starts a local Python HTTP server.
- `./test.sh`: Runs the unit test suite to ensure generation logic is correct.
- `python3 src/main.py [basepath]`: Manual build with an optional basepath (e.g., `/my-project/`).

## Key Features

- **Recursive Generation:** Automatically handles deeply nested directory structures in the `content/` folder.
- **Custom Markdown Engine:** Supports various Markdown blocks (headings, code, quotes, lists) and inline styles (bold, italic, links, images).
- **Title Extraction:** Dynamically extracts the H1 (`# `) from Markdown files to populate the page `<title>`.
- **Static Asset Sync:** Efficiently copies images and stylesheets from `static/` to `docs/` before each build.
- **Link Normalization:** Automatically adjusts internal links and image sources based on a configurable `basepath`.

## Architecture

The generator is organized into modular Python components:

- **`src/main.py`**: The orchestration layer that coordinates file cleanup, static copying, and page generation.
- **`src/gencontent.py`**: Contains the logic for reading Markdown, applying templates, and writing HTML files.
- **`src/markdown_blocks.py`**: The core parser that breaks Markdown into logical blocks.
- **`src/htmlnode.py`**: An abstraction layer for representing and rendering HTML elements.
- **`src/inline_markdown.py`**: Handles inline elements like bold text, italics, and URLs.
- **`src/copystatic.py`**: Manages the recursive copying of non-Markdown assets.
