"""
title_fix - A Python package for intelligent title case conversion and text formatting.
"""

from typing import Dict
from .core import TitleFixer
from .utils import get_supported_styles, get_supported_case_types, validate_input

__version__ = "0.0.3"
__all__ = ['title_fix', 'TitleFixer', 'get_supported_styles', 'get_supported_case_types', 'validate_input']

_GLOBAL_FIXER = TitleFixer()


def title_fix(text: str, **kwargs) -> Dict:
    """
    Convenience function to process text.
    
    Args:
        text: Input text to process
        case_type: One of "title", "sentence", "upper", "lower", "first", "alt", "toggle"
        style: Citation style - "apa", "chicago", "ap", "mla", "nyt"
        straight_quotes: Convert curly quotes to straight quotes
        quick_copy: Enable quick copy functionality
        acronyms: Optional iterable of custom acronyms to capitalize (e.g., ["api", "sdk"])
        preserve_uppercase: Preserve words that are already fully uppercase in the input
        **kwargs: Additional arguments to pass to TitleFixer.process()
        
    Returns:
        Dict containing processed text and metadata
    """
    return _GLOBAL_FIXER.process(text, **kwargs) 