"""
title_fix - A Python package for intelligent title case conversion and text formatting.
"""

from typing import Dict
from .core import TitleFixer
from .utils import get_supported_styles, get_supported_case_types, validate_input

__version__ = "0.0.1"
__all__ = ['title_fix', 'TitleFixer', 'get_supported_styles', 'get_supported_case_types', 'validate_input']


def title_fix(text: str, **kwargs) -> Dict:
    """
    Convenience function to create a TitleFixer instance and process text.
    
    Args:
        text: Input text to process
        **kwargs: Additional arguments to pass to TitleFixer.process()
        
    Returns:
        Dict containing processed text and metadata
    """
    fixer = TitleFixer()
    return fixer.process(text, **kwargs) 