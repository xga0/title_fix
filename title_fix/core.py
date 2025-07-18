"""
Core functionality for title case conversion - Optimized for performance.
"""

import regex as re
from typing import Dict
from functools import lru_cache
from .constants import CITATION_STYLES, ROMAN_NUMERALS, ACRONYMS

# Precompiled regex patterns for performance
_SENTENCE_SPLIT_PATTERN = re.compile(r'([.!?]+\s*)')
_ALPHA_ONLY_PATTERN = re.compile(r'[^a-zA-Z]')

# Precomputed sets for fast lookups
_POWER_WORDS = frozenset(['how', 'why', 'what', 'when', 'top', 'best', 'new', 'ultimate', 'complete', 'guide'])
_EMOTIONAL_WORDS = frozenset(['amazing', 'incredible', 'shocking', 'unbelievable', 'secret', 'proven'])

# Quote replacement mapping for fast conversion
_QUOTE_REPLACEMENTS = {
    '"': '"',
    '"': '"',
    ''': "'",
    ''': "'",
}


class TitleFixer:
    """Main class for processing text with various case conversion options - Performance optimized."""
    
    __slots__ = ('text', 'word_count', 'char_count', '_words_cache', '_text_lower_cache')
    
    def __init__(self):
        self.text = ""
        self.word_count = 0
        self.char_count = 0
        self._words_cache = None
        self._text_lower_cache = None
        
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
        # Input validation - optimized to check types first
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        if not isinstance(case_type, str):
            raise ValueError("Case type must be a string")
        if not isinstance(style, str):
            raise ValueError("Style must be a string")
            
        # Set instance variables and clear caches
        self.text = text
        self.char_count = len(text)
        self._words_cache = None
        self._text_lower_cache = None
        
        # Optimized word count calculation
        stripped_text = text.strip()
        self.word_count = len(stripped_text.split()) if stripped_text else 0
        
        case_type_lower = case_type.lower()
        style_lower = style.lower()
        
        # Fast case processing with direct method calls
        if case_type_lower == "title":
            if style_lower not in CITATION_STYLES:
                style_lower = "apa"
            processed = self._title_case_optimized(style_lower)
        elif case_type_lower == "sentence":
            processed = self._sentence_case_optimized()
        elif case_type_lower == "upper":
            processed = text.upper()
        elif case_type_lower == "lower":
            processed = text.lower()
        elif case_type_lower == "first":
            processed = self._first_letter_case_optimized()
        elif case_type_lower == "alt":
            processed = self._alternating_case_optimized()
        elif case_type_lower == "toggle":
            processed = self._toggle_case_optimized()
        else:
            processed = self._title_case_optimized("apa")
            case_type_lower = "title"
            style_lower = "apa"
            
        # Optimized quote conversion
        if straight_quotes:
            for curly, straight in _QUOTE_REPLACEMENTS.items():
                processed = processed.replace(curly, straight)
            
        return {
            "text": processed,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "headline_score": self._calculate_headline_score_optimized(processed),
            "quick_copy": quick_copy,
            "case_type": case_type_lower.upper(),
            "style": style_lower.upper() if case_type_lower == "title" else None
        }

    def _get_words_cached(self):
        """Get words with caching for performance."""
        if self._words_cache is None:
            self._words_cache = self.text.split()
        return self._words_cache

    def _get_text_lower_cached(self):
        """Get lowercase text with caching for performance."""
        if self._text_lower_cache is None:
            self._text_lower_cache = self.text.lower()
        return self._text_lower_cache

    @lru_cache(maxsize=128)
    def _should_capitalize_cached(self, word_lower: str, style_key: str, 
                                 is_first_or_last: bool, is_after_colon: bool) -> bool:
        """Cached version of capitalization logic for frequently used words."""
        style_rules = CITATION_STYLES[style_key]
        
        if is_first_or_last or is_after_colon:
            return True
            
        if word_lower in style_rules["always_capitalize"]:
            return True
            
        # Fast alpha extraction
        word_alpha = _ALPHA_ONLY_PATTERN.sub('', word_lower)
        if word_alpha in ACRONYMS:
            return True
            
        if word_lower in style_rules["exceptions"]:
            return False
            
        return len(word_lower) >= style_rules["min_length"] or style_rules["min_length"] == 0

    def _title_case_optimized(self, citation_style: str = "apa") -> str:
        """Optimized title case conversion."""
        words = self._get_words_cached()
        if not words:
            return ""
            
        style_rules = CITATION_STYLES[citation_style]
        result = []
        last_word_ended_with_colon = False
        
        for i, word in enumerate(words):
            is_first_or_last = (i == 0 or i == len(words) - 1)
            is_after_colon = last_word_ended_with_colon
            
            # Process hyphenated words efficiently
            if '-' in word:
                parts = word.split('-')
                processed_parts = []
                for j, part in enumerate(parts):
                    part_lower = part.lower()
                    should_cap = self._should_capitalize_cached(
                        part_lower, citation_style, is_first_or_last or j == 0, is_after_colon)
                    
                    if should_cap:
                        processed_parts.append(self._capitalize_word_optimized(part, part_lower))
                    else:
                        processed_parts.append(part_lower)
                result.append('-'.join(processed_parts))
            else:
                word_lower = word.lower()
                should_cap = self._should_capitalize_cached(
                    word_lower, citation_style, is_first_or_last, is_after_colon)
                
                if should_cap:
                    result.append(self._capitalize_word_optimized(word, word_lower))
                else:
                    result.append(word_lower)
            
            # Check if this word ends with colon for next iteration
            last_word_ended_with_colon = word.endswith(':')
                    
        return " ".join(result)

    @lru_cache(maxsize=256)
    def _capitalize_word_optimized(self, word: str, word_lower: str) -> str:
        """Optimized word capitalization with caching."""
        word_alpha = _ALPHA_ONLY_PATTERN.sub('', word_lower)
        
        if word_alpha in ROMAN_NUMERALS or word_alpha in ACRONYMS:
            # Fast character-by-character processing for special cases
            return ''.join(c.upper() if c.isalpha() else c for c in word)
        else:
            return word.capitalize()
        
    def _sentence_case_optimized(self) -> str:
        """Optimized sentence case conversion."""
        if not self.text:
            return ""
            
        # Use precompiled regex for better performance
        sentences = _SENTENCE_SPLIT_PATTERN.split(self.text)
        result = []
        
        for i, part in enumerate(sentences):
            if i % 2 == 0 and part:  # Even indices are sentence content
                result.append(part[0].upper() + part[1:].lower())
            else:
                result.append(part)
                
        return "".join(result)
        
    def _first_letter_case_optimized(self) -> str:
        """Optimized first letter capitalization."""
        # More efficient than split/join for simple capitalization
        words = self._get_words_cached()
        return " ".join(word.capitalize() for word in words)
        
    def _alternating_case_optimized(self) -> str:
        """Optimized alternating case conversion."""
        result = []
        capitalize = True
        
        for char in self.text:
            if char.isalpha():
                result.append(char.upper() if capitalize else char.lower())
                capitalize = not capitalize
            else:
                result.append(char)
                
        return "".join(result)
        
    def _toggle_case_optimized(self) -> str:
        """Optimized toggle case using str methods."""
        return "".join(c.lower() if c.isupper() else c.upper() for c in self.text)
        
    def _calculate_headline_score_optimized(self, text: str) -> int:
        """Optimized headline score calculation."""
        if not text.strip():
            return 0
            
        score = 0
        length = len(text)
        
        # Optimized length scoring with single comparison chains
        if 40 <= length <= 60:
            score += 30
        elif 30 <= length <= 70:
            score += 20
        elif 20 <= length <= 80:
            score += 10
            
        # Optimized word count scoring
        if 6 <= self.word_count <= 10:
            score += 30
        elif 4 <= self.word_count <= 12:
            score += 20
        elif 3 <= self.word_count <= 15:
            score += 10
            
        # Fast power word detection using set intersection
        text_lower = self._get_text_lower_cached()
        text_words = set(text_lower.split())
        power_word_count = len(_POWER_WORDS & text_words)
        score += min(20, power_word_count * 5)
        
        # Fast number detection
        if any(c.isdigit() for c in text):
            score += 10
            
        # Fast emotional word detection
        emotional_count = len(_EMOTIONAL_WORDS & text_words)
        score += min(10, emotional_count * 3)
            
        return min(100, score) 