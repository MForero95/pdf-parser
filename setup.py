#!/usr/bin/env python3
"""
Setup script for PDF to Markdown converter.

Handles:
- Python version check
- Dependency installation
- First-time configuration
- Marker installation validation
"""

import os
import subprocess
import sys
from pathlib import Path


def print_header():
    """Print setup header."""
    print("\n" + "=" * 60)
    print("📄 PDF to Markdown Converter - Setup")
    print("=" * 60 + "\n")


def check_python_version():
    """Check if Python version is compatible (3.10 to 3.13)."""
    print("Checking Python version...")

    if sys.version_info < (3, 10):
        print(f"❌ Error: Python 3.10 or higher is required.")
        print(f"   Current version: {sys.version}")
        print(f"\n   Please upgrade Python and try again.")
        sys.exit(1)

    if sys.version_info >= (3, 14):
        print(f"❌ Error: Python 3.14+ is not yet supported.")
        print(f"   Current version: {sys.version}")
        print(f"\n   Please use Python 3.12 or 3.13.")
        print(f"   You can install it with: brew install python@3.12")
        print(f"   Then create a virtual environment: python3.12 -m venv venv")
        sys.exit(1)

    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")


def install_dependencies():
    """Install required dependencies."""
    print("\n" + "-" * 60)
    print("📦 Installing dependencies...")
    print("-" * 60 + "\n")

    requirements_file = Path(__file__).parent / "requirements.txt"

    if not requirements_file.exists():
        print("❌ Error: requirements.txt not found")
        sys.exit(1)

    try:
        subprocess.check_call([
            sys.executable,
            "-m",
            "pip",
            "install",
            "-r",
            str(requirements_file)
        ])
        print("\n✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to install dependencies: {e}")
        sys.exit(1)


def setup_configuration():
    """Setup configuration (.env file)."""
    print("\n" + "-" * 60)
    print("⚙️  Configuration Setup")
    print("-" * 60 + "\n")

    env_path = Path(".env")
    env_example_path = Path(".env.example")

    if env_path.exists():
        print("✅ .env file already exists")
        return

    if not env_example_path.exists():
        print("❌ Error: .env.example not found")
        sys.exit(1)

    print("Creating .env file from template...\n")
    print("You need a Gemini API key to use this tool.")
    print("Get your free API key at: https://aistudio.google.com/app/apikey\n")

    # Prompt for API key
    while True:
        api_key = input("Enter your Gemini API key: ").strip()

        if not api_key:
            print("❌ API key cannot be empty")
            continue

        if api_key == "your_api_key_here":
            print("❌ Please enter a valid API key")
            continue

        break

    # Create .env file
    with open(env_example_path, 'r') as f:
        content = f.read()

    content = content.replace('your_api_key_here', api_key)

    with open(env_path, 'w') as f:
        f.write(content)

    print("\n✅ .env file created successfully")


def validate_marker_installation():
    """Check if marker_single is available."""
    print("\n" + "-" * 60)
    print("🔍 Validating marker-pdf installation...")
    print("-" * 60 + "\n")

    try:
        result = subprocess.run(
            ['marker_single', '--help'],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            print("✅ marker_single command is available")
            return True
        else:
            print("⚠️  marker_single command found but returned error")
            return False

    except FileNotFoundError:
        print("❌ marker_single command not found")
        print("\nThis usually means marker-pdf is not properly installed.")
        print("The dependencies should have been installed in the previous step.")
        print("\nIf you continue to have issues, try:")
        print("  pip install --upgrade marker-pdf[full]")
        return False

    except Exception as e:
        print(f"⚠️  Could not validate marker installation: {e}")
        return False


def create_output_directory():
    """Create output directory if it doesn't exist."""
    print("\n" + "-" * 60)
    print("📁 Creating output directory...")
    print("-" * 60 + "\n")

    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    gitkeep = output_dir / ".gitkeep"
    if not gitkeep.exists():
        gitkeep.touch()

    print("✅ Output directory created: ./output")


def display_usage_instructions():
    """Display usage instructions."""
    print("\n" + "=" * 60)
    print("🎉 Setup Complete!")
    print("=" * 60 + "\n")

    print("You can now use the PDF to Markdown converter:\n")

    print("📖 Usage Examples:\n")
    print("  1. Interactive mode (GUI file picker):")
    print("     python parse_pdf.py\n")

    print("  2. Convert a single PDF:")
    print("     python parse_pdf.py document.pdf\n")

    print("  3. Convert multiple PDFs:")
    print("     python parse_pdf.py doc1.pdf doc2.pdf doc3.pdf\n")

    print("  4. Custom output directory:")
    print("     python parse_pdf.py document.pdf --output-dir ./my_outputs\n")

    print("  5. Fast mode (no LLM):")
    print("     python parse_pdf.py document.pdf --no-llm\n")

    print("  6. Force CPU usage:")
    print("     python parse_pdf.py document.pdf --device cpu\n")

    print("📚 For more help:")
    print("   python parse_pdf.py --help\n")


def main():
    """Run setup process."""
    print_header()

    try:
        # Step 1: Check Python version
        check_python_version()

        # Step 2: Install dependencies
        install_dependencies()

        # Step 3: Setup configuration
        setup_configuration()

        # Step 4: Validate marker installation
        marker_ok = validate_marker_installation()
        if not marker_ok:
            print("\n⚠️  Warning: marker-pdf installation could not be validated.")
            print("The tool may not work correctly until this is resolved.\n")

        # Step 5: Create output directory
        create_output_directory()

        # Step 6: Display usage instructions
        display_usage_instructions()

    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled by user.")
        sys.exit(130)

    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
