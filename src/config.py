"""Configuration management for PDF converter."""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Config:
    """Configuration for PDF to Markdown conversion."""

    gemini_api_key: str
    output_dir: str = "./output"
    use_llm: bool = True


def validate_api_key(key: Optional[str]) -> bool:
    """
    Validate that the API key is set and not empty.

    Args:
        key: API key to validate

    Returns:
        bool: True if key is valid, False otherwise
    """
    if not key:
        return False

    # Check if it's not the placeholder value
    if key.strip() in ["", "your_api_key_here"]:
        return False

    # Basic format check (Gemini API keys typically start with 'AIza')
    return len(key.strip()) > 10


def ensure_env_file() -> bool:
    """
    Ensure .env file exists. If not, create from .env.example.

    Returns:
        bool: True if .env exists or was created, False if user cancelled
    """
    env_path = Path(".env")
    env_example_path = Path(".env.example")

    if env_path.exists():
        return True

    # Create .env from .env.example
    if env_example_path.exists():
        print("\n📝 First-time setup: Creating .env file...")
        print(
            "\nGet your Gemini API key from: https://aistudio.google.com/app/apikey\n"
        )

        api_key = input("Enter your Gemini API key: ").strip()

        if not api_key or api_key == "your_api_key_here":
            print("❌ Invalid API key provided.")
            return False

        # Read .env.example and replace placeholder
        with open(env_example_path, "r") as f:
            content = f.read()

        content = content.replace("your_api_key_here", api_key)

        with open(env_path, "w") as f:
            f.write(content)

        print("✅ .env file created successfully!\n")
        return True

    return False


def load_config(
    output_dir: Optional[str] = None, use_llm: Optional[bool] = None
) -> Config:
    """
    Load configuration from environment variables.

    Args:
        output_dir: Override default output directory
        use_llm: Override default LLM usage

    Returns:
        Config: Configuration object

    Raises:
        ValueError: If GEMINI_API_KEY is not set or invalid
    """
    # Ensure .env file exists
    if not ensure_env_file():
        raise ValueError("Configuration setup cancelled or failed.")

    # Load environment variables from .env file
    load_dotenv()

    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    if not validate_api_key(api_key):
        raise ValueError(
            "GEMINI_API_KEY is not set or invalid.\n"
            "Please add your API key to the .env file.\n"
            "Get your API key from: https://aistudio.google.com/app/apikey"
        )

    # Get output directory
    if output_dir is None:
        output_dir = os.getenv("DEFAULT_OUTPUT_DIR", "./output")

    # Get use_llm setting
    if use_llm is None:
        use_llm_env = os.getenv("USE_LLM", "true").lower()
        use_llm = use_llm_env in ("true", "1", "yes")

    return Config(gemini_api_key=api_key, output_dir=output_dir, use_llm=use_llm)
