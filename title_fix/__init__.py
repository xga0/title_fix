"""
title_fix - A Python package for intelligent title case conversion and text formatting.
Performance optimized version.
"""

from typing import Dict
from .core import TitleFixer
from .utils import get_supported_styles, get_supported_case_types, validate_input

__version__ = "0.0.2"
__all__ = ['title_fix', 'TitleFixer', 'get_supported_styles', 'get_supported_case_types', 'validate_input']

# Singleton instance for better performance - avoids repeated object creation
_GLOBAL_FIXER = TitleFixer()


def title_fix(text: str, **kwargs) -> Dict:
    """
    Convenience function to process text with optimized performance.
    
    Uses a singleton TitleFixer instance to avoid object creation overhead
    while maintaining thread safety through stateless processing.
    
    Args:
        text: Input text to process
        **kwargs: Additional arguments to pass to TitleFixer.process()
        
    Returns:
        Dict containing processed text and metadata
    """
    return _GLOBAL_FIXER.process(text, **kwargs) 