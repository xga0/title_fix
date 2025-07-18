"""
Utility functions for title_fix package.
"""

from typing import List
from .constants import CITATION_STYLES


def get_supported_styles() -> List[str]:
    """Get list of supported citation styles."""
    return list(CITATION_STYLES.keys())


def get_supported_case_types() -> List[str]:
    """Get list of supported case types."""
    return ['title', 'sentence', 'upper', 'lower', 'first', 'alt', 'toggle']


def validate_input(text: str, case_type: str, style: str) -> None:
    """Validate input parameters."""
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    if case_type not in get_supported_case_types():
        raise ValueError(f"Invalid case_type. Must be one of: {get_supported_case_types()}")
    if case_type == 'title' and style not in get_supported_styles():
        raise ValueError(f"Invalid style. Must be one of: {get_supported_styles()}") 