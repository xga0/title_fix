"""
title_fix - A Python package for intelligent title case conversion and text formatting.
"""

import regex as re
from typing import Tuple, Optional, Dict, List, Set

__all__ = ['title_fix', 'TitleFixer', 'get_supported_styles', 'get_supported_case_types', 'validate_input']

# Case types that don't use citation styles
CASE_TYPES = {
    "sentence", "upper", "lower", "first", "alt", "toggle"
}

# Common words that should remain lowercase in title case
LOWERCASE_WORDS = {
    'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'if', 'in', 'nor',
    'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet', 'into', 'with',
    'within', 'between', 'through', 'after', 'before', 'under', 'over',
    'from', 'until', 'unless', 'upon', 'while', 'via', 'toward', 'towards'
}

# Words that should always be capitalized
ALWAYS_CAPITALIZE = {
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
    'us', 'uk', 'uae', 'eu', 'un', 'nato', 'nasa', 'fbi', 'cia'
}

# Roman numerals that should be uppercase
ROMAN_NUMERALS = {
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'
}

# Acronyms that should be all uppercase
ACRONYMS = {
    'nasa', 'fbi', 'cia', 'un', 'nato', 'us', 'uk', 'uae', 'eu'
}

# Citation style rules
CITATION_STYLES = {
    "apa": {
        "name": "APA",
        "description": "APA Style - Capitalize first word, all major words, and words with 4+ letters",
        "min_length": 4,  # Words with 4+ letters are capitalized
        "exceptions": {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'in', 'nor', 
                      'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet'},  # Only basic articles/conjunctions/prepositions
        "always_capitalize": ALWAYS_CAPITALIZE | {'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did'}
    },
    "chicago": {
        "name": "Chicago",
        "description": "Chicago Manual of Style - Capitalize first word and all major words",
        "min_length": 0,  # All major words are capitalized regardless of length
        "exceptions": LOWERCASE_WORDS,
        "always_capitalize": ALWAYS_CAPITALIZE
    },
    "ap": {
        "name": "AP",
        "description": "Associated Press - Capitalize words with 4+ letters",
        "min_length": 4,
        "exceptions": LOWERCASE_WORDS,
        "always_capitalize": ALWAYS_CAPITALIZE | {'us', 'uk', 'ap'}
    },
    "mla": {
        "name": "MLA",
        "description": "MLA Style - Capitalize first word and all principal words",
        "min_length": 0,
        "exceptions": LOWERCASE_WORDS - {'is', 'are', 'was', 'were'},
        "always_capitalize": ALWAYS_CAPITALIZE
    },
    "nyt": {
        "name": "NYT",
        "description": "New York Times - Capitalize words with 5+ letters",
        "min_length": 5,
        "exceptions": LOWERCASE_WORDS | {'that', 'than', 'who', 'whom', 'this', 'when'},
        "always_capitalize": ALWAYS_CAPITALIZE | {'new', 'york', 'times'}
    }
}

class TitleFixer:
    def __init__(self):
        self.text = ""
        self.word_count = 0
        self.char_count = 0
        self._style_cache = {}  # Cache for style rules
        
    def process(self, text: str, case_type: str = "title", style: str = "apa", 
                straight_quotes: bool = False, 
                quick_copy: bool = True) -> Dict:
        """
        Process text with specified formatting options.
        
        Args:
            text: Input text to process
            case_type: One of "title", "sentence", "upper", "lower", "first", "alt", "toggle"
            style: Citation style to use when case_type is "title". One of "apa", "chicago", "ap", "mla", "nyt"
            straight_quotes: Whether to convert curly quotes to straight quotes
            quick_copy: Whether to enable quick copy functionality
            
        Returns:
            Dict containing processed text and metadata
            
        Raises:
            ValueError: If text is not a string or case_type/style are invalid
        """
        # Input validation
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        if not isinstance(case_type, str):
            raise ValueError("Case type must be a string")
        if not isinstance(style, str):
            raise ValueError("Style must be a string")
            
        self.text = text
        self.word_count = len(text.split()) if text.strip() else 0
        self.char_count = len(text)
        
        # Normalize inputs
        case_type = case_type.lower()
        style = style.lower()
        
        # Process based on case type
        if case_type == "title":
            # For title case, use citation style
            if style not in CITATION_STYLES:
                style = "apa"  # Default to APA if invalid style
            processed = self._title_case(style)
        elif case_type == "sentence":
            processed = self._sentence_case()
        elif case_type == "upper":
            processed = text.upper()
        elif case_type == "lower":
            processed = text.lower()
        elif case_type == "first":
            processed = self._first_letter_case()
        elif case_type == "alt":
            processed = self._alternating_case()
        elif case_type == "toggle":
            processed = self._toggle_case()
        else:
            # Default to title case with APA style
            processed = self._title_case("apa")
            case_type = "title"
            style = "apa"
            
        # Handle quotes if requested
        if straight_quotes:
            processed = self._convert_to_straight_quotes(processed)
            
        return {
            "text": processed,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "headline_score": self._calculate_headline_score(processed),
            "quick_copy": quick_copy,
            "case_type": case_type.upper(),
            "style": style.upper() if case_type == "title" else None
        }
        
    def _should_capitalize(self, word: str, style_rules: Dict, 
                          is_first_or_last: bool = False) -> bool:
        """Determine if a word should be capitalized based on style rules."""
        # Always capitalize first/last word
        if is_first_or_last:
            return True
            
        # Always capitalize certain words
        if word.lower() in style_rules["always_capitalize"]:
            return True
            
        # Always capitalize acronyms regardless of other rules (strip punctuation first)
        word_alpha = ''.join(c for c in word if c.isalpha())
        if word_alpha.lower() in ACRONYMS:
            return True
            
        # Check exceptions first (these should NOT be capitalized)
        if word.lower() in style_rules["exceptions"]:
            return False
            
        # Check word length rule
        if len(word) >= style_rules["min_length"]:
            return True
            
        # For styles with min_length=0, capitalize all non-exception words
        if style_rules["min_length"] == 0:
            return True
            
        return False
        
    def _title_case(self, citation_style: str = "apa") -> str:
        """Convert text to title case following the specified citation style."""
        words = self.text.split()
        if not words:
            return ""
            
        # Get style rules
        style_rules = CITATION_STYLES.get(citation_style.lower(), CITATION_STYLES["apa"])
        
        # Process each word
        result = []
        for i, word in enumerate(words):
            is_first_or_last = (i == 0 or i == len(words) - 1)
            
            # Check if this word comes after a colon (subtitle)
            is_after_colon = i > 0 and result[i-1].endswith(':')
            should_capitalize_as_first = is_first_or_last or is_after_colon
            
            # Handle hyphenated words
            if '-' in word:
                parts = word.split('-')
                processed_parts = []
                for j, part in enumerate(parts):
                    if self._should_capitalize(part, style_rules, should_capitalize_as_first or j == 0):
                        # Strip punctuation for checking against special word sets
                        part_alpha = ''.join(c for c in part if c.isalpha())
                        
                        # Handle Roman numerals specially
                        if part_alpha.lower() in ROMAN_NUMERALS:
                            # Preserve punctuation but make letters uppercase
                            processed_parts.append(''.join(c.upper() if c.isalpha() else c for c in part))
                        # Handle acronyms specially
                        elif part_alpha.lower() in ACRONYMS:
                            # Preserve punctuation but make letters uppercase
                            processed_parts.append(''.join(c.upper() if c.isalpha() else c for c in part))
                        else:
                            processed_parts.append(part.capitalize())
                    else:
                        processed_parts.append(part.lower())
                result.append('-'.join(processed_parts))
            else:
                if self._should_capitalize(word, style_rules, should_capitalize_as_first):
                    # Strip punctuation for checking against special word sets
                    word_alpha = ''.join(c for c in word if c.isalpha())
                    
                    # Handle Roman numerals specially
                    if word_alpha.lower() in ROMAN_NUMERALS:
                        # Preserve punctuation but make letters uppercase
                        result.append(''.join(c.upper() if c.isalpha() else c for c in word))
                    # Handle acronyms specially
                    elif word_alpha.lower() in ACRONYMS:
                        # Preserve punctuation but make letters uppercase
                        result.append(''.join(c.upper() if c.isalpha() else c for c in word))
                    else:
                        result.append(word.capitalize())
                else:
                    result.append(word.lower())
                    
        return " ".join(result)
        
    def _sentence_case(self) -> str:
        """Convert text to sentence case."""
        if not self.text:
            return ""
            
        # Split into sentences and capitalize first letter of each
        sentences = re.split(r'([.!?]+\s*)', self.text)
        result = []
        for i, part in enumerate(sentences):
            if i % 2 == 0:  # This is a sentence
                if part:
                    result.append(part[0].upper() + part[1:].lower())
                else:
                    result.append(part)
            else:  # This is a separator
                result.append(part)
        return "".join(result)
        
    def _first_letter_case(self) -> str:
        """Capitalize the first letter of each word."""
        return " ".join(word.capitalize() for word in self.text.split())
        
    def _alternating_case(self) -> str:
        """Convert to alternating case (e.g., AlTeRnAtInG)."""
        result = ""
        capitalize = True
        for char in self.text:
            if char.isalpha():
                result += char.upper() if capitalize else char.lower()
                capitalize = not capitalize
            else:
                result += char
        return result
        
    def _toggle_case(self) -> str:
        """Toggle the case of each character."""
        return "".join(
            c.lower() if c.isupper() else c.upper()
            for c in self.text
        )
        
    def _convert_to_straight_quotes(self, text: str) -> str:
        """Convert curly quotes to straight quotes."""
        replacements = {
            '"': '"',
            '"': '"',
            ''': "'",
            ''': "'",
        }
        for curly, straight in replacements.items():
            text = text.replace(curly, straight)
        return text
        
    def _calculate_headline_score(self, text: str) -> int:
        """Calculate a headline score based on various factors."""
        if not text.strip():
            return 0
            
        score = 0
        length = len(text)
        
        # Length factor (ideal length 40-60 chars) - optimized conditions
        if 40 <= length <= 60:
            score += 30
        elif 30 <= length <= 70:
            score += 20
        elif 20 <= length <= 80:
            score += 10
            
        # Word count factor (ideal 6-10 words) - use cached word count
        if 6 <= self.word_count <= 10:
            score += 30
        elif 4 <= self.word_count <= 12:
            score += 20
        elif 3 <= self.word_count <= 15:
            score += 10
            
        # Power words bonus - optimized with frozenset
        power_words = frozenset(['how', 'why', 'what', 'when', 'top', 'best', 'new', 'ultimate', 'complete', 'guide'])
        text_lower = text.lower()
        power_word_count = sum(1 for word in power_words if word in text_lower)
        score += min(20, power_word_count * 5)
        
        # Numbers bonus - optimized check
        has_numbers = any(c.isdigit() for c in text)
        if has_numbers:
            score += 10
            
        # Emotional words bonus
        emotional_words = frozenset(['amazing', 'incredible', 'shocking', 'unbelievable', 'secret', 'proven'])
        emotional_count = sum(1 for word in emotional_words if word in text_lower)
        score += min(10, emotional_count * 3)
            
        return min(100, score)

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