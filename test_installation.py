#!/usr/bin/env python3
"""
Test script to verify installation and configuration.

Run this after setup to ensure everything is working correctly.
"""

import sys
from importlib.util import find_spec
from pathlib import Path


def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")

    # Test click
    if find_spec("click") is None:
        print("  ❌ click: Module not found")
        return False
    print("  ✅ click")

    # Test python-dotenv
    if find_spec("dotenv") is None:
        print("  ❌ python-dotenv: Module not found")
        return False
    print("  ✅ python-dotenv")

    # Test rich
    if find_spec("rich") is None:
        print("  ❌ rich: Module not found")
        return False
    print("  ✅ rich")

    # Test project modules
    modules = ["src.config", "src.converter", "src.file_picker", "src.utils"]
    for module in modules:
        if find_spec(module) is None:
            print(f"  ❌ Project modules: {module} not found")
            return False
    print("  ✅ All project modules")

    return True


def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")

    env_file = Path(".env")
    if not env_file.exists():
        print("  ⚠️  .env file not found (run setup.py first)")
        return False

    try:
        from src.config import load_config

        config = load_config()
        print("  ✅ Configuration loaded")
        print(f"     - API Key: {'✓ Set' if config.gemini_api_key else '✗ Missing'}")
        print(f"     - Output Dir: {config.output_dir}")
        print(f"     - Use LLM: {config.use_llm}")
        print(f"     - Device: {config.device}")
        return True
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False


def test_marker_installation():
    """Test marker-pdf installation."""
    print("\nTesting marker-pdf installation...")

    try:
        from src.utils import validate_marker_installation

        if validate_marker_installation():
            print("  ✅ marker_single command available")
            return True
        else:
            print("  ❌ marker_single command not found")
            print("     Install with: pip install marker-pdf[full]")
            return False
    except Exception as e:
        print(f"  ❌ Error checking marker: {e}")
        return False


def test_output_directory():
    """Test output directory."""
    print("\nTesting output directory...")

    output_dir = Path("./output")
    if output_dir.exists() and output_dir.is_dir():
        print(f"  ✅ Output directory exists: {output_dir.resolve()}")
        return True
    else:
        print("  ❌ Output directory not found")
        return False


def test_python_version():
    """Test Python version."""
    print("Testing Python version...")

    if sys.version_info >= (3, 10):
        print(
            f"  ✅ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
        return True
    else:
        print(
            f"  ❌ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        )
        print("     Python 3.10+ required")
        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🧪 PDF to Markdown Converter - Installation Test")
    print("=" * 60 + "\n")

    results = []

    # Run tests
    results.append(("Python Version", test_python_version()))
    results.append(("Imports", test_imports()))
    results.append(("Configuration", test_configuration()))
    results.append(("Output Directory", test_output_directory()))
    results.append(("Marker Installation", test_marker_installation()))

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60 + "\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")

    print(f"\n  Total: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed! You're ready to convert PDFs.")
        print("\nTry: python3 parse_pdf.py\n")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nIf you haven't run setup yet, run: python3 setup.py\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
