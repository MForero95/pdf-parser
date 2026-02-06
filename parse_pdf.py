#!/usr/bin/env python3
"""
PDF to Markdown Converter

Convert PDF files to markdown using marker-pdf with Gemini API for maximum accuracy.
"""

import sys
import time
from pathlib import Path
from typing import List, Optional

import click
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TimeElapsedColumn,
)
from rich.table import Table

from src.config import load_config, Config
from src.converter import convert_pdf_to_markdown, ConversionError
from src.file_picker import select_files, validate_paths
from src.utils import (
    validate_pdf,
    validate_marker_installation,
    ensure_directory,
    get_file_info,
)

console = Console()


@click.command()
@click.argument("pdf_paths", nargs=-1, type=click.Path(exists=True))
@click.option("--output-dir", default=None, help="Output directory for markdown files")
@click.option(
    "--no-llm",
    is_flag=True,
    help="Disable LLM for faster (but less accurate) processing",
)
@click.option("--batch", is_flag=True, help="Enable batch mode for multiple files")
def main(pdf_paths: tuple, output_dir: Optional[str], no_llm: bool, batch: bool):
    """
    Convert PDF files to Markdown using marker-pdf with Gemini API.

    Examples:

        # Interactive mode (GUI file picker)
        python parse_pdf.py

        # Convert single PDF
        python parse_pdf.py document.pdf

        # Convert multiple PDFs
        python parse_pdf.py doc1.pdf doc2.pdf doc3.pdf

        # Custom output directory
        python parse_pdf.py document.pdf --output-dir ./my_outputs

        # Fast mode (no LLM)
        python parse_pdf.py document.pdf --no-llm
    """
    try:
        # Display header
        console.print("\n[bold cyan]📄 PDF to Markdown Converter[/bold cyan]")
        console.print("[dim]Powered by marker-pdf + Gemini API[/dim]\n")

        # Load configuration
        try:
            config = load_config(output_dir=output_dir, use_llm=not no_llm)
        except ValueError as e:
            console.print(f"[bold red]❌ Configuration Error:[/bold red] {e}")
            sys.exit(1)

        # Display configuration
        display_config(config)

        # Validate marker installation
        if not validate_marker_installation():
            console.print(
                "\n[bold red]❌ Error:[/bold red] marker_single command not found."
            )
            console.print("\nPlease install marker-pdf:")
            console.print("  [bold]pip install marker-pdf[full][/bold]\n")
            sys.exit(1)

        # Ensure output directory exists
        ensure_directory(config.output_dir)

        # Get PDF files to process
        files_to_process = []

        if pdf_paths:
            # Use provided paths
            files_to_process = validate_paths(list(pdf_paths))
        else:
            # Launch file picker
            console.print("\n[yellow]Opening file picker...[/yellow]")
            try:
                files_to_process = select_files(multiple=True)
            except ValueError as e:
                console.print(f"\n[bold red]❌ Error:[/bold red] {e}")
                sys.exit(1)
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Cancelled by user.[/yellow]")
                sys.exit(0)

        # Validate all files
        valid_files = []
        for file_path in files_to_process:
            if validate_pdf(file_path):
                valid_files.append(file_path)
            else:
                console.print(f"[yellow]⚠️  Skipping invalid PDF:[/yellow] {file_path}")

        if not valid_files:
            console.print("\n[bold red]❌ No valid PDF files to process.[/bold red]")
            sys.exit(1)

        # Display files to process
        display_files_summary(valid_files)

        # Process files
        results = process_files(valid_files, config)

        # Display summary
        display_results_summary(results)

    except KeyboardInterrupt:
        console.print("\n\n[yellow]⚠️  Interrupted by user.[/yellow]")
        sys.exit(130)
    except Exception as e:
        console.print(f"\n[bold red]❌ Unexpected error:[/bold red] {e}")
        sys.exit(1)


def display_config(config: Config):
    """Display current configuration."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    table.add_row(
        "🔑 API Key", "✓ Configured" if config.gemini_api_key else "✗ Missing"
    )
    table.add_row("📁 Output Dir", config.output_dir)
    table.add_row(
        "🤖 Use LLM", "Yes (Maximum accuracy)" if config.use_llm else "No (Faster)"
    )

    console.print(table)


def display_files_summary(files: List[str]):
    """Display summary of files to process."""
    console.print(f"\n[bold]📋 Files to process:[/bold] {len(files)}\n")

    table = Table(show_header=True, box=None)
    table.add_column("#", style="dim", width=3)
    table.add_column("Filename", style="cyan")
    table.add_column("Size", justify="right", style="yellow")
    table.add_column("Pages", justify="right", style="magenta")

    for idx, file_path in enumerate(files, 1):
        info = get_file_info(file_path)
        pages = str(info["pages"]) if info["pages"] else "?"
        table.add_row(str(idx), info["name"], info["size_formatted"], pages)

    console.print(table)
    console.print()


def process_files(files: List[str], config: Config) -> dict:
    """
    Process all PDF files.

    Args:
        files: List of PDF file paths
        config: Configuration object

    Returns:
        dict: Processing results with success/failure counts
    """
    results = {
        "total": len(files),
        "success": 0,
        "failed": 0,
        "outputs": [],
        "errors": [],
    }

    start_time = time.time()

    for idx, pdf_path in enumerate(files, 1):
        file_name = Path(pdf_path).name

        console.print(
            f"\n[bold cyan]Processing ({idx}/{len(files)}):[/bold cyan] {file_name}"
        )

        try:
            # Convert PDF
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task("Converting...", total=None)

                def update_progress(message: str):
                    progress.update(task, description=message[:50])

                output_file = convert_pdf_to_markdown(
                    pdf_path,
                    config.output_dir,
                    config,
                    progress_callback=update_progress,
                )

            # Success
            console.print(f"[bold green]✅ Success![/bold green] Output: {output_file}")
            results["success"] += 1
            results["outputs"].append(output_file)

        except ConversionError as e:
            console.print(f"[bold red]❌ Failed:[/bold red] {e}")
            results["failed"] += 1
            results["errors"].append({"file": pdf_path, "error": str(e)})

        except Exception as e:
            console.print(f"[bold red]❌ Unexpected error:[/bold red] {e}")
            results["failed"] += 1
            results["errors"].append({"file": pdf_path, "error": str(e)})

    elapsed_time = time.time() - start_time
    results["elapsed_time"] = elapsed_time

    return results


def display_results_summary(results: dict):
    """Display processing results summary."""
    console.print("\n" + "=" * 60)
    console.print("[bold]📊 Processing Summary[/bold]")
    console.print("=" * 60 + "\n")

    # Create summary table
    table = Table(show_header=False, box=None)
    table.add_column("Metric", style="cyan")
    table.add_column("Count", justify="right")

    table.add_row("Total files", str(results["total"]))
    table.add_row("✅ Successful", f"[green]{results['success']}[/green]")
    table.add_row("❌ Failed", f"[red]{results['failed']}[/red]")

    # Format elapsed time
    elapsed = results.get("elapsed_time", 0)
    minutes = int(elapsed // 60)
    seconds = int(elapsed % 60)
    time_str = f"{minutes}m {seconds}s" if minutes > 0 else f"{seconds}s"
    table.add_row("⏱️  Time", time_str)

    console.print(table)

    # Show output files
    if results["outputs"]:
        console.print("\n[bold green]✅ Output files:[/bold green]")
        for output in results["outputs"]:
            console.print(f"   📄 {output}")

    # Show errors
    if results["errors"]:
        console.print("\n[bold red]❌ Failed files:[/bold red]")
        for error in results["errors"]:
            console.print(f"   • {Path(error['file']).name}")
            console.print(f"     [dim]{error['error']}[/dim]")

    console.print()


if __name__ == "__main__":
    main()
