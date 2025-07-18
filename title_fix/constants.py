"""
Constants and configuration data for title_fix package.
"""

CASE_TYPES = {
    "sentence", "upper", "lower", "first", "alt", "toggle"
}

LOWERCASE_WORDS = {
    'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'if', 'in', 'nor',
    'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet', 'into', 'with',
    'within', 'between', 'through', 'after', 'before', 'under', 'over',
    'from', 'until', 'unless', 'upon', 'while', 'via', 'toward', 'towards'
}

ALWAYS_CAPITALIZE = {
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x',
    'us', 'uk', 'uae', 'eu', 'un', 'nato', 'nasa', 'fbi', 'cia'
}

ROMAN_NUMERALS = {
    'i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x'
}

ACRONYMS = {
    'nasa', 'fbi', 'cia', 'un', 'nato', 'us', 'uk', 'uae', 'eu'
}

CITATION_STYLES = {
    "apa": {
        "name": "APA",
        "description": "APA Style - Capitalize first word, all major words, and words with 4+ letters",
        "min_length": 4,
        "exceptions": {'a', 'an', 'and', 'as', 'at', 'but', 'by', 'for', 'in', 'nor', 
                      'of', 'on', 'or', 'so', 'the', 'to', 'up', 'yet'},
        "always_capitalize": ALWAYS_CAPITALIZE | {'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did'}
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