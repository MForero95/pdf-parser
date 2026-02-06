# PDF to Markdown Converter

A frictionless PDF to markdown converter using [marker-pdf](https://github.com/VikParuchuri/marker) with Gemini API for maximum accuracy. Features GUI file picker, batch processing, and automatic configuration.

## Features

- 🎯 **Maximum Accuracy**: Uses Gemini API with LLM enhancement for best results
- 🖱️ **Easy to Use**: GUI file picker for effortless PDF selection
- 📦 **Batch Processing**: Convert multiple PDFs in one go
- ⚡ **Smart Defaults**: Automatic device detection (MPS for Apple Silicon)
- 🔧 **Zero Configuration**: Interactive setup wizard handles everything
- 📊 **Rich Feedback**: Beautiful terminal progress indicators and summaries

## Requirements

- Python 3.12 or 3.13 (required for dependency compatibility)
- macOS, Linux, or Windows
- Gemini API key (free from [Google AI Studio](https://aistudio.google.com/app/apikey))

> **Note**: Python 3.14+ is not yet supported due to marker-pdf dependencies requiring Pydantic V1.

## Quick Start

### 1. Install System Dependencies (macOS)

```bash
brew install python@3.12
brew install jpeg zlib libtiff freetype little-cms2 webp
```

### 2. Set Up the Project

```bash
# Create virtual environment with Python 3.12
/opt/homebrew/bin/python3.12 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install Python dependencies
export LDFLAGS="-L/opt/homebrew/opt/jpeg/lib -L/opt/homebrew/opt/zlib/lib"
export CPPFLAGS="-I/opt/homebrew/opt/jpeg/include -I/opt/homebrew/opt/zlib/include"
pip install -r requirements.txt
```

### 3. Configure API Key

```bash
# Copy example config
cp .env.example .env

# Edit .env and add your Gemini API key
# Get a free key at: https://aistudio.google.com/app/apikey
```

Your `.env` file should look like:
```env
GEMINI_API_KEY=your_api_key_here
DEFAULT_OUTPUT_DIR=./output
USE_LLM=true
AUTO_DETECT_DEVICE=true
```

### 4. Start Converting

```bash
# Easy mode: GUI file picker
./run.sh

# Or convert a specific PDF
./run.sh document.pdf
```

## Usage

### Using the run script (Recommended)

The `run.sh` script automatically activates the virtual environment:

```bash
# Interactive mode with GUI file picker
./run.sh

# Convert a single PDF
./run.sh document.pdf

# Convert multiple PDFs
./run.sh doc1.pdf doc2.pdf doc3.pdf

# Batch convert all PDFs in a folder
./run.sh *.pdf

# Custom output directory
./run.sh document.pdf --output-dir ./my_outputs

# Fast mode (disable LLM for speed)
./run.sh document.pdf --no-llm
```

### Manual usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run the parser
python parse_pdf.py document.pdf
```

### Command-line options

```bash
python parse_pdf.py --help

Options:
  --output-dir TEXT  Output directory for markdown files
  --no-llm          Disable LLM for faster (but less accurate) processing
  --batch           Enable batch mode for multiple files
  --help            Show this message and exit
```

## Project Structure

```
pdf_parser/
├── parse_pdf.py          # Main CLI entry point
├── setup.py              # Installation wizard (legacy)
├── run.sh               # Convenience script to run with venv
├── test_installation.py  # Validation script
├── requirements.txt      # Python dependencies
├── .env.example          # Configuration template
├── .env                  # Your API keys (git-ignored)
├── .gitignore            # Git ignore rules
├── src/
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Configuration management
│   ├── converter.py      # PDF conversion logic
│   ├── file_picker.py    # GUI/CLI file selection
│   └── utils.py          # Utility functions
└── output/               # Converted markdown files
```

### File Descriptions

**parse_pdf.py**
- Main entry point using Click framework
- Handles command-line arguments
- Orchestrates the conversion workflow
- Provides rich terminal feedback with progress bars

**src/config.py**
- Loads configuration from `.env` file
- Validates Gemini API key
- Auto-detects best device (MPS/CUDA/CPU)
- Manages environment variables

**src/converter.py**
- Wraps marker-pdf's `marker_single` command
- Sets up Gemini API environment
- Handles subprocess execution
- Parses and reports errors

**src/file_picker.py**
- GUI file picker using tkinter
- Falls back to CLI input if GUI unavailable
- Supports multiple file selection
- Validates selected PDFs

**src/utils.py**
- PDF file validation
- Output filename generation with timestamps
- Directory management
- File metadata extraction

**run.sh**
- Activates virtual environment automatically
- Passes all arguments to parse_pdf.py
- Simplifies daily usage

## How It Works

1. **Configuration**: Loads settings from `.env` file, including Gemini API key
2. **File Selection**: GUI file picker (or CLI input) for easy PDF selection
3. **Device Detection**: Automatically uses MPS on Apple Silicon for GPU acceleration
4. **Conversion**: Calls `marker_single` with LLM flags for accuracy
5. **Output**: Saves markdown files with timestamps to avoid overwrites

The tool wraps marker-pdf and enhances it with:
- Easy configuration via `.env` files
- User-friendly GUI/CLI interface
- Automatic Gemini API integration
- Beautiful progress feedback
- Robust error handling

## Output Format

Converted files are saved in the `output/` directory with the original PDF name:

```
output/
└── Document Name/
    └── Document Name.md
```

Images and other assets are extracted alongside the markdown file.

## Configuration

Edit `.env` to customize behavior:

```env
# Required: Your Gemini API key
GEMINI_API_KEY=your_api_key_here

# Output directory (default: ./output)
DEFAULT_OUTPUT_DIR=./output

# Use LLM for maximum accuracy (default: true)
USE_LLM=true

# Auto-detect best device (default: true)
AUTO_DETECT_DEVICE=true
```

## Troubleshooting

### "Core Pydantic V1 functionality isn't compatible with Python 3.14+"

You're using Python 3.14 or higher. marker-pdf requires Python 3.12 or 3.13:

```bash
# Create new venv with Python 3.12
/opt/homebrew/bin/python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "marker_single command not found"

The marker-pdf package wasn't installed correctly:

```bash
source venv/bin/activate
pip install --upgrade marker-pdf[full]
```

### "API key is not set or invalid"

Check your `.env` file has a valid Gemini API key:

1. Get a free key at [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Add it to `.env`: `GEMINI_API_KEY=your_key_here`

### "Building Pillow fails with jpeg not found"

Install system-level image libraries:

```bash
brew install jpeg zlib libtiff freetype little-cms2 webp

# Then reinstall with environment variables
source venv/bin/activate
export LDFLAGS="-L/opt/homebrew/opt/jpeg/lib -L/opt/homebrew/opt/zlib/lib"
export CPPFLAGS="-I/opt/homebrew/opt/jpeg/include -I/opt/homebrew/opt/zlib/include"
pip install --force-reinstall --no-cache-dir Pillow
```

### "Out of memory" errors

The PDF may be too large. Try:

1. Use fast mode: `./run.sh document.pdf --no-llm`
2. Process smaller PDFs
3. Close other applications

### GUI file picker doesn't open

If tkinter is unavailable, the tool automatically falls back to CLI input. You can:

1. Enter file paths manually when prompted
2. Use command-line arguments: `./run.sh document.pdf`

## Dependencies

- **marker-pdf[full]** - PDF to markdown conversion engine
- **python-dotenv** - Environment variable management
- **rich** - Beautiful terminal formatting
- **click** - Command-line interface framework
- **pypdf** - PDF metadata extraction

## Performance

### Device Performance (Approximate)
- **MPS (Apple Silicon)**: 10-20 pages/minute with LLM
- **CUDA (NVIDIA GPU)**: 15-25 pages/minute with LLM
- **CPU**: 3-8 pages/minute with LLM
- **Fast Mode (--no-llm)**: 2-3x faster, lower accuracy

### Memory Usage
- **Typical**: 2-4 GB
- **Large PDFs with LLM**: 8+ GB

## Supported File Types

While optimized for PDFs, marker-pdf also supports:
- PDF documents
- Microsoft PowerPoint (PPTX)
- Microsoft Word (DOCX)
- Microsoft Excel (XLSX)
- EPUB ebooks

## License

This project uses marker-pdf, which is licensed under GPL-3.0. See the [marker-pdf repository](https://github.com/VikParuchuri/marker) for details.

## Credits

- [marker-pdf](https://github.com/VikParuchuri/marker) by Vik Paruchuri
- [Gemini API](https://ai.google.dev/) by Google

## Contributing

This is a personal project, but suggestions are welcome! Feel free to:
- Report issues
- Suggest improvements
- Share your use cases

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section above
2. Review [marker-pdf documentation](https://github.com/VikParuchuri/marker)
3. Check [Gemini API documentation](https://ai.google.dev/docs)
