"""
Core functionality for title case conversion.
"""

import regex as re
from typing import Dict, Iterable, Optional
from .constants import CITATION_STYLES, ROMAN_NUMERALS, ACRONYMS

_SENTENCE_SPLIT_PATTERN = re.compile(r'([.!?]+\s*)')
_ALPHA_ONLY_PATTERN = re.compile(r'[^a-zA-Z]')

_POWER_WORDS = frozenset(['how', 'why', 'what', 'when', 'top', 'best', 'new', 'ultimate', 'complete', 'guide'])
_EMOTIONAL_WORDS = frozenset(['amazing', 'incredible', 'shocking', 'unbelievable', 'secret', 'proven'])

_QUOTE_REPLACEMENTS = {
    '"': '"',
    '"': '"',
    ''': "'",
    ''': "'",
}


class TitleFixer:
    """Main class for processing text with various case conversion options."""
    
    __slots__ = ('text', 'word_count', 'char_count', '_words_cache', '_text_lower_cache', 
                 'acronyms', 'preserve_uppercase', '_uppercase_words')
    
    def __init__(self):
        self.text = ""
        self.word_count = 0
        self.char_count = 0
        self._words_cache = None
        self._text_lower_cache = None
        self.acronyms = ACRONYMS
        self.preserve_uppercase = False
        self._uppercase_words = None
        
    def process(self, text: str, case_type: str = "title", style: str = "apa", 
                straight_quotes: bool = False, 
                quick_copy: bool = True,
                acronyms: Optional[Iterable[str]] = None,
                preserve_uppercase: bool = False) -> Dict:
        """
        Process text with specified formatting options.
        
        Args:
            text: Input text to process
            case_type: One of "title", "sentence", "upper", "lower", "first", "alt", "toggle"
            style: Citation style to use when case_type is "title". One of "apa", "chicago", "ap", "mla", "nyt"
            straight_quotes: Whether to convert curly quotes to straight quotes
            quick_copy: Whether to enable quick copy functionality
            acronyms: Optional iterable of custom acronyms to capitalize (e.g., ["api", "sdk"])
            preserve_uppercase: Whether to preserve words that are already fully uppercase in the input
            
        Returns:
            Dict containing processed text and metadata
            
        Raises:
            ValueError: If text is not a string or case_type/style are invalid
        """
        if not isinstance(text, str):
            raise ValueError("Text must be a string")
        if not isinstance(case_type, str):
            raise ValueError("Case type must be a string")
        if not isinstance(style, str):
            raise ValueError("Style must be a string")
            
        self.text = text
        self.char_count = len(text)
        self._words_cache = None
        self._text_lower_cache = None
        
        if acronyms:
            custom_acronyms = frozenset(a.lower() for a in acronyms if isinstance(a, str))
            self.acronyms = ACRONYMS | custom_acronyms
        else:
            self.acronyms = ACRONYMS
        
        self.preserve_uppercase = preserve_uppercase
        if preserve_uppercase:
            words = text.split()
            uppercase_words = set()
            for w in words:
                if any(c.isalpha() for c in w) and all(c.isupper() or not c.isalpha() for c in w):
                    uppercase_words.add(w.lower())
                    if '-' in w:
                        for part in w.split('-'):
                            if any(c.isalpha() for c in part):
                                uppercase_words.add(part.lower())
            self._uppercase_words = frozenset(uppercase_words)
        else:
            self._uppercase_words = frozenset()
        
        stripped_text = text.strip()
        self.word_count = len(stripped_text.split()) if stripped_text else 0
        
        case_type_lower = case_type.lower()
        style_lower = style.lower()
        
        if case_type_lower == "title":
            if style_lower not in CITATION_STYLES:
                style_lower = "apa"
            processed = self._title_case(style_lower)
        elif case_type_lower == "sentence":
            processed = self._sentence_case()
        elif case_type_lower == "upper":
            processed = text.upper()
        elif case_type_lower == "lower":
            processed = text.lower()
        elif case_type_lower == "first":
            processed = self._first_letter_case()
        elif case_type_lower == "alt":
            processed = self._alternating_case()
        elif case_type_lower == "toggle":
            processed = self._toggle_case()
        else:
            processed = self._title_case("apa")
            case_type_lower = "title"
            style_lower = "apa"
            
        if straight_quotes:
            for curly, straight in _QUOTE_REPLACEMENTS.items():
                processed = processed.replace(curly, straight)
            
        return {
            "text": processed,
            "word_count": self.word_count,
            "char_count": self.char_count,
            "headline_score": self._calculate_headline_score(processed),
            "quick_copy": quick_copy,
            "case_type": case_type_lower.upper(),
            "style": style_lower.upper() if case_type_lower == "title" else None
        }

    def _get_words_cached(self):
        """Get words with caching."""
        if self._words_cache is None:
            self._words_cache = self.text.split()
        return self._words_cache

    def _get_text_lower_cached(self):
        """Get lowercase text with caching."""
        if self._text_lower_cache is None:
            self._text_lower_cache = self.text.lower()
        return self._text_lower_cache

    def _should_capitalize(self, word_lower: str, style_key: str, 
                          is_first_or_last: bool, is_after_colon: bool) -> bool:
        """Determine if a word should be capitalized based on style rules."""
        style_rules = CITATION_STYLES[style_key]
        
        if is_first_or_last or is_after_colon:
            return True
        
        # Check if word should be preserved as uppercase
        if self.preserve_uppercase and word_lower in self._uppercase_words:
            return True
            
        if word_lower in style_rules["always_capitalize"]:
            return True
        
        if word_lower in self.acronyms:
            return True
            
        word_alpha = _ALPHA_ONLY_PATTERN.sub('', word_lower)
        if word_alpha and word_alpha in self.acronyms:
            return True
            
        if word_lower in style_rules["exceptions"]:
            return False
            
        return len(word_lower) >= style_rules["min_length"] or style_rules["min_length"] == 0

    def _title_case(self, citation_style: str = "apa") -> str:
        """Convert text to title case."""
        words = self._get_words_cached()
        if not words:
            return ""
            
        result = []
        last_word_ended_with_colon = False
        
        for i, word in enumerate(words):
            is_first_or_last = (i == 0 or i == len(words) - 1)
            is_after_colon = last_word_ended_with_colon
            
            if '-' in word:
                parts = word.split('-')
                processed_parts = []
                for j, part in enumerate(parts):
                    part_lower = part.lower()
                    should_cap = self._should_capitalize(
                        part_lower, citation_style, is_first_or_last or j == 0, is_after_colon)
                    
                    if should_cap:
                        processed_parts.append(self._capitalize_word(part, part_lower))
                    else:
                        processed_parts.append(part_lower)
                result.append('-'.join(processed_parts))
            else:
                word_lower = word.lower()
                should_cap = self._should_capitalize(
                    word_lower, citation_style, is_first_or_last, is_after_colon)
                
                if should_cap:
                    result.append(self._capitalize_word(word, word_lower))
                else:
                    result.append(word_lower)
            
            last_word_ended_with_colon = word.endswith(':')
                    
        return " ".join(result)

    def _capitalize_word(self, word: str, word_lower: str) -> str:
        """Capitalize a word based on its type."""
        word_alpha = _ALPHA_ONLY_PATTERN.sub('', word_lower)
        
        if self.preserve_uppercase and word_lower in self._uppercase_words:
            return word.upper()
        
        if word_alpha in ROMAN_NUMERALS or word_lower in self.acronyms or (word_alpha and word_alpha in self.acronyms):
            return ''.join(c.upper() if c.isalpha() else c for c in word)
        else:
            return word.capitalize()
        
    def _sentence_case(self) -> str:
        """Convert text to sentence case."""
        if not self.text:
            return ""
            
        sentences = _SENTENCE_SPLIT_PATTERN.split(self.text)
        result = []
        
        for i, part in enumerate(sentences):
            if i % 2 == 0 and part:
                result.append(part[0].upper() + part[1:].lower())
            else:
                result.append(part)
                
        return "".join(result)
        
    def _first_letter_case(self) -> str:
        """Capitalize first letter of each word."""
        words = self._get_words_cached()
        return " ".join(word.capitalize() for word in words)
        
    def _alternating_case(self) -> str:
        """Convert to alternating case."""
        result = []
        capitalize = True
        
        for char in self.text:
            if char.isalpha():
                result.append(char.upper() if capitalize else char.lower())
                capitalize = not capitalize
            else:
                result.append(char)
                
        return "".join(result)
        
    def _toggle_case(self) -> str:
        """Toggle case of all characters."""
        return "".join(c.lower() if c.isupper() else c.upper() for c in self.text)
        
    def _calculate_headline_score(self, text: str) -> int:
        """Calculate headline score."""
        if not text.strip():
            return 0
            
        score = 0
        length = len(text)
        
        if 40 <= length <= 60:
            score += 30
        elif 30 <= length <= 70:
            score += 20
        elif 20 <= length <= 80:
            score += 10
            
        if 6 <= self.word_count <= 10:
            score += 30
        elif 4 <= self.word_count <= 12:
            score += 20
        elif 3 <= self.word_count <= 15:
            score += 10
            
        text_lower = self._get_text_lower_cached()
        text_words = set(text_lower.split())
        power_word_count = len(_POWER_WORDS & text_words)
        score += min(20, power_word_count * 5)
        
        if any(c.isdigit() for c in text):
            score += 10
            
        emotional_count = len(_EMOTIONAL_WORDS & text_words)
        score += min(10, emotional_count * 3)
            
        return min(100, score) 