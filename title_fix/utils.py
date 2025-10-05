"""
Utility functions for title_fix package.
"""

from typing import List
from functools import lru_cache
from .constants import CITATION_STYLE_KEYS, CASE_TYPES

_CASE_TYPES_LIST = ['title', 'sentence', 'upper', 'lower', 'first', 'alt', 'toggle']
_CITATION_STYLES_LIST = list(CITATION_STYLE_KEYS)


@lru_cache(maxsize=1)
def get_supported_styles() -> List[str]:
    """Get list of supported citation styles."""
    return _CITATION_STYLES_LIST.copy()


@lru_cache(maxsize=1)
def get_supported_case_types() -> List[str]:
    """Get list of supported case types."""
    return _CASE_TYPES_LIST.copy()


def validate_input(text: str, case_type: str, style: str) -> None:
    """
    Validate input parameters.
    
    Args:
        text: Input text to validate
        case_type: Case type to validate
        style: Citation style to validate
        
    Raises:
        ValueError: If any parameter is invalid
    """
    if not isinstance(text, str):
        raise ValueError("Text must be a string")
    
    if case_type not in CASE_TYPES:
        raise ValueError(f"Invalid case_type. Must be one of: {_CASE_TYPES_LIST}")
    
    if case_type == 'title' and style not in CITATION_STYLE_KEYS:
        raise ValueError(f"Invalid style. Must be one of: {_CITATION_STYLES_LIST}") 