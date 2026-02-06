"""File picker for PDF selection with GUI and CLI fallback."""

import sys
from pathlib import Path
from typing import List, Optional


def select_files(multiple: bool = False) -> List[str]:
    """
    Open file picker dialog to select PDF files.

    Falls back to CLI input if GUI is unavailable.

    Args:
        multiple: Allow multiple file selection

    Returns:
        List of selected PDF file paths

    Raises:
        ValueError: If no files selected or invalid files
    """
    # Try GUI file picker first
    try:
        return _select_via_gui(multiple)
    except Exception as e:
        print(f"⚠️  GUI file picker unavailable: {e}")
        print("Falling back to CLI input...\n")
        return _select_via_cli(multiple)


def _select_via_gui(multiple: bool) -> List[str]:
    """
    Select files using tkinter GUI dialog.

    Args:
        multiple: Allow multiple file selection

    Returns:
        List of selected file paths

    Raises:
        ImportError: If tkinter is not available
        ValueError: If no files selected
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        raise ImportError("tkinter not available")

    # Create root window (hidden)
    root = tk.Tk()
    root.withdraw()

    # Bring dialog to front on macOS
    root.lift()
    root.attributes('-topmost', True)
    root.after_idle(root.attributes, '-topmost', False)

    # Open file dialog
    if multiple:
        file_paths = filedialog.askopenfilenames(
            title="Select PDF files",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )
    else:
        file_path = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[
                ("PDF files", "*.pdf"),
                ("All files", "*.*")
            ]
        )
        file_paths = [file_path] if file_path else []

    # Clean up
    root.destroy()

    # Validate selection
    if not file_paths or (isinstance(file_paths, tuple) and not file_paths):
        raise ValueError("No files selected")

    # Convert to list and validate paths
    selected = list(file_paths)
    if not selected:
        raise ValueError("No files selected")

    return selected


def _select_via_cli(multiple: bool = False) -> List[str]:
    """
    Select files via command-line input.

    Supports:
    - Single file path
    - Multiple file paths (comma or newline separated)
    - Drag and drop (paste path directly)

    Args:
        multiple: Allow multiple file selection

    Returns:
        List of selected file paths

    Raises:
        ValueError: If no valid files provided
    """
    print("=" * 60)
    print("📄 PDF File Selection")
    print("=" * 60)

    if multiple:
        print("\nEnter PDF file paths (one per line, or comma-separated).")
        print("You can also drag and drop files into the terminal.")
        print("Press Ctrl+D (Unix) or Ctrl+Z (Windows) when done.\n")
    else:
        print("\nEnter PDF file path (or drag and drop):\n")

    file_paths = []

    try:
        if multiple:
            # Read multiple lines
            lines = []
            while True:
                try:
                    line = input()
                    if line.strip():
                        lines.append(line.strip())
                except EOFError:
                    break

            # Parse input (handle comma-separated or newline-separated)
            for line in lines:
                if ',' in line:
                    # Comma-separated
                    paths = [p.strip() for p in line.split(',')]
                    file_paths.extend(paths)
                else:
                    # Single path per line
                    file_paths.append(line)
        else:
            # Single file input
            path = input().strip()
            if path:
                file_paths.append(path)

    except KeyboardInterrupt:
        print("\n\n❌ Selection cancelled.")
        sys.exit(0)

    # Clean up paths (remove quotes that might come from drag-and-drop)
    cleaned_paths = []
    for path in file_paths:
        # Remove surrounding quotes
        path = path.strip().strip('"').strip("'")
        if path:
            cleaned_paths.append(path)

    # Validate paths
    valid_paths = []
    invalid_paths = []

    for path in cleaned_paths:
        path_obj = Path(path)
        if path_obj.exists() and path_obj.is_file() and path_obj.suffix.lower() == '.pdf':
            valid_paths.append(str(path_obj.resolve()))
        else:
            invalid_paths.append(path)

    # Report invalid paths
    if invalid_paths:
        print("\n⚠️  Invalid or non-PDF files (skipped):")
        for path in invalid_paths:
            print(f"   - {path}")

    # Check if any valid files
    if not valid_paths:
        raise ValueError("No valid PDF files provided")

    print(f"\n✅ Selected {len(valid_paths)} PDF file(s)\n")
    return valid_paths


def validate_paths(paths: List[str]) -> List[str]:
    """
    Validate that all paths are readable PDF files.

    Args:
        paths: List of file paths to validate

    Returns:
        List of valid paths

    Raises:
        ValueError: If no valid paths found
    """
    valid = []
    invalid = []

    for path in paths:
        path_obj = Path(path)
        if path_obj.exists() and path_obj.is_file() and path_obj.suffix.lower() == '.pdf':
            valid.append(str(path_obj.resolve()))
        else:
            invalid.append(path)

    if invalid:
        print(f"\n⚠️  Skipping {len(invalid)} invalid file(s):")
        for path in invalid:
            print(f"   - {path}")

    if not valid:
        raise ValueError("No valid PDF files found")

    return valid
