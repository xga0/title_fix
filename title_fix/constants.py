"""
Constants and configuration data for title_fix package - Performance optimized.
"""

# Use frozensets for O(1) lookups instead of sets/lists
CASE_TYPES = frozenset({
    "title", "sentence", "upper", "lower", "first", "alt", "toggle"
})

# Precompute all lowercase words as frozenset for fast lookups
LOWERCASE_WORDS = frozenset({
    'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'if', 'in', 'nor',
    'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet', 'into', 'with',
    'within', 'between', 'through', 'after', 'before', 'under', 'over',
    'from', 'until', 'unless', 'upon', 'while', 'via', 'toward', 'towards'
})

# Optimized with frozenset for fast membership testing
ALWAYS_CAPITALIZE = frozenset({
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
    'us', 'uk', 'uae', 'eu', 'un', 'nato', 'nasa', 'fbi', 'cia'
})

# Roman numerals as frozenset for performance
ROMAN_NUMERALS = frozenset({
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'
})

# Acronyms as frozenset for performance
ACRONYMS = frozenset({
    'nasa', 'fbi', 'cia', 'un', 'nato', 'us', 'uk', 'uae', 'eu'
})

# Optimized citation styles with precomputed frozensets for faster lookups
CITATION_STYLES = {
    "apa": {
        "name": "APA",
        "description": "APA Style - Capitalize first word, all major words, and words with 4+ letters",
        "min_length": 4,
        "exceptions": frozenset({'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'in', 'nor', 
                                'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet'}),
        "always_capitalize": ALWAYS_CAPITALIZE | frozenset({'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did'})
    },
    "chicago": {
        "name": "Chicago",
        "description": "Chicago Manual of Style - Capitalize first word and all major words",
        "min_length": 0,
        "exceptions": LOWERCASE_WORDS,
        "always_capitalize": ALWAYS_CAPITALIZE
    },
    "ap": {
        "name": "AP",
        "description": "Associated Press - Capitalize words with 4+ letters",
        "min_length": 4,
        "exceptions": LOWERCASE_WORDS,
        "always_capitalize": ALWAYS_CAPITALIZE | frozenset({'us', 'uk', 'ap'})
    },
    "mla": {
        "name": "MLA",
        "description": "MLA Style - Capitalize first word and all principal words",
        "min_length": 0,
        "exceptions": LOWERCASE_WORDS - frozenset({'is', 'are', 'was', 'were'}),
        "always_capitalize": ALWAYS_CAPITALIZE
    },
    "nyt": {
        "name": "NYT",
        "description": "New York Times - Capitalize words with 5+ letters",
        "min_length": 5,
        "exceptions": LOWERCASE_WORDS | frozenset({'that', 'than', 'who', 'whom', 'this', 'when'}),
        "always_capitalize": ALWAYS_CAPITALIZE | frozenset({'new', 'york', 'times'})
    }
}

# Precompute style keys as tuple for faster iterations
CITATION_STYLE_KEYS = tuple(CITATION_STYLES.keys()) 