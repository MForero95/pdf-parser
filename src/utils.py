"""Utility functions for PDF converter."""

import os
import shutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

try:
    import pypdf
    PYPDF_AVAILABLE = True
except ImportError:
    PYPDF_AVAILABLE = False


def validate_pdf(path: str) -> bool:
    """
    Validate that the file exists and is a readable PDF.

    Args:
        path: Path to PDF file

    Returns:
        bool: True if valid PDF, False otherwise
    """
    pdf_path = Path(path)

    # Check if file exists
    if not pdf_path.exists():
        return False

    # Check if it's a file (not directory)
    if not pdf_path.is_file():
        return False

    # Check file extension
    if pdf_path.suffix.lower() != '.pdf':
        return False

    # Check if readable
    if not os.access(pdf_path, os.R_OK):
        return False

    return True


def generate_output_filename(pdf_path: str, output_dir: str) -> str:
    """
    Generate output filename for converted markdown.

    Format: {original_name}_converted_{timestamp}.md

    Args:
        pdf_path: Path to source PDF
        output_dir: Output directory

    Returns:
        str: Full path to output markdown file
    """
    pdf_file = Path(pdf_path)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    base_name = pdf_file.stem

    # Clean filename (remove special characters)
    base_name = "".join(c for c in base_name if c.isalnum() or c in (' ', '-', '_'))
    base_name = base_name.replace(' ', '_')

    output_filename = f"{base_name}_converted_{timestamp}.md"
    return str(Path(output_dir) / output_filename)


def ensure_directory(path: str) -> None:
    """
    Create directory if it doesn't exist.

    Args:
        path: Directory path to create
    """
    Path(path).mkdir(parents=True, exist_ok=True)


def validate_marker_installation() -> bool:
    """
    Check if marker_single command is available.

    Returns:
        bool: True if marker is installed, False otherwise
    """
    return shutil.which('marker_single') is not None


def get_pdf_page_count(path: str) -> Optional[int]:
    """
    Get the number of pages in a PDF file.

    Args:
        path: Path to PDF file

    Returns:
        int: Number of pages, or None if unable to determine
    """
    if not PYPDF_AVAILABLE:
        return None

    try:
        with open(path, 'rb') as f:
            pdf_reader = pypdf.PdfReader(f)
            return len(pdf_reader.pages)
    except Exception:
        return None


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human-readable format.

    Args:
        size_bytes: File size in bytes

    Returns:
        str: Formatted file size (e.g., "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"


def get_file_info(path: str) -> dict:
    """
    Get information about a PDF file.

    Args:
        path: Path to PDF file

    Returns:
        dict: File information (size, pages, etc.)
    """
    pdf_path = Path(path)
    info = {
        'name': pdf_path.name,
        'size': pdf_path.stat().st_size,
        'size_formatted': format_file_size(pdf_path.stat().st_size),
        'pages': get_pdf_page_count(str(pdf_path))
    }
    return info


def check_python_version() -> bool:
    """
    Check if Python version is 3.10 or higher.

    Returns:
        bool: True if version is sufficient
    """
    import sys
    return sys.version_info >= (3, 10)
