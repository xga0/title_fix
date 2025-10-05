# Title Fix

[![PyPI version](https://img.shields.io/pypi/v/title-fix.svg)](https://pypi.org/project/title-fix/)
[![Python Versions](https://img.shields.io/badge/python-3.7%20%7C%203.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](https://pypi.org/project/title-fix/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python package for intelligent title case conversion and text formatting. This package provides a comprehensive solution for converting text between different case styles while maintaining proper capitalization rules and offering additional text analysis features.

## 🌐 Live Demo

Try the web interface powered by this package: **[https://title-fix-app.onrender.com/](https://title-fix-app.onrender.com/)**

Experience all the features through a modern, responsive web application built with React and FastAPI. The web app provides:
- Real-time text conversion as you type
- All citation styles and case types
- Copy-to-clipboard functionality  
- Text statistics and headline scoring
- Beautiful, user-friendly interface

## Features

- Multiple case conversion options:
  - Title Case (follows standard style guidelines)
  - Sentence case
  - UPPERCASE
  - lowercase
  - First Letter Case
  - AlTeRnAtInG cAsE
  - tOGGLE cAsE

- Citation Style Support:
  - APA (American Psychological Association)
  - Chicago Manual of Style
  - AP (Associated Press)
  - MLA (Modern Language Association)
  - NYT (New York Times)

- Additional features:
  - **Custom acronyms** - Add your own acronyms (API, SDK, REST, etc.)
  - **Preserve uppercase** - Keep words that are already fully uppercase
  - Word and character count
  - Straight quotes conversion
  - Quick copy functionality
  - Headline scoring
  - Input validation and error handling

## Installation

```bash
pip install title-fix
```

## Usage

### Basic Usage

```python
from title_fix import title_fix

# Simple title case conversion (using default APA style)
result = title_fix("this is a test title")
print(result["text"])  # Output: "This Is a Test Title"

# Get word and character count
print(result["word_count"])  # Output: 5
print(result["char_count"])  # Output: 20
```

### Citation Styles

```python
# APA Style (default) - capitalizes words with 4+ letters
result = title_fix("the theory of relativity in physics", style="apa")
print(result["text"])  # Output: "The Theory of Relativity in Physics"

# Chicago Style - capitalizes all major words
result = title_fix("the theory of relativity in physics", style="chicago")
print(result["text"])  # Output: "The Theory of Relativity in Physics"

# AP Style - capitalizes words with 4+ letters
result = title_fix("the theory of relativity in physics", style="ap")
print(result["text"])  # Output: "The Theory of Relativity in Physics"

# MLA Style - capitalizes all principal words
result = title_fix("the theory of relativity in physics", style="mla")
print(result["text"])  # Output: "The Theory of Relativity in Physics"

# NYT Style - capitalizes words with 5+ letters
result = title_fix("the theory of relativity in physics", style="nyt")
print(result["text"])  # Output: "The Theory of Relativity in Physics"
```

### Different Case Styles

```python
# Sentence case
result = title_fix("THIS IS A TEST.", case_type="sentence")
print(result["text"])  # Output: "This is a test."

# UPPERCASE
result = title_fix("test text", case_type="upper")
print(result["text"])  # Output: "TEST TEXT"

# lowercase
result = title_fix("TEST TEXT", case_type="lower")
print(result["text"])  # Output: "test text"

# First Letter Case
result = title_fix("test text", case_type="first")
print(result["text"])  # Output: "Test Text"

# AlTeRnAtInG cAsE
result = title_fix("test text", case_type="alt")
print(result["text"])  # Output: "TeSt TeXt"

# tOGGLE cAsE
result = title_fix("Test Text", case_type="toggle")
print(result["text"])  # Output: "tEST tEXT"
```

### Additional Features

```python
# Convert curly quotes to straight quotes
result = title_fix("test with quotes", straight_quotes=True)
print(result["text"])  # Converts any curly quotes to straight quotes

# Get headline score (0-100 based on best practices)
result = title_fix("How to Write the Perfect Headline in 7 Steps")
print(result["headline_score"])  # Output: 75

# Get available options
from title_fix import get_supported_styles, get_supported_case_types
print(get_supported_styles())     # ['apa', 'chicago', 'ap', 'mla', 'nyt']
print(get_supported_case_types()) # ['title', 'sentence', 'upper', 'lower', 'first', 'alt', 'toggle']
```

### Special Handling

The package intelligently handles various text elements:

```python
# Roman numerals
result = title_fix("world war ii and chapter iv")
print(result["text"])  # Output: "World war II and Chapter IV"

# Acronyms
result = title_fix("nasa, fbi, and cia collaboration")
print(result["text"])  # Output: "NASA, FBI, and CIA Collaboration"

# Hyphenated words
result = title_fix("well-known state-of-the-art solution")
print(result["text"])  # Output: "Well-Known State-of-the-art Solution"

# Subtitles after colons
result = title_fix("main title: a subtitle here")
print(result["text"])  # Output: "Main Title: A Subtitle Here"
```

### Custom Acronyms

You can now provide your own acronyms to be capitalized:

```python
# Add custom acronyms like API, SDK, REST, etc.
result = title_fix("the api and sdk documentation", acronyms=["api", "sdk"])
print(result["text"])  # Output: "The API and SDK Documentation"

# Works with default acronyms too
result = title_fix("nasa api and fbi database", acronyms=["api", "database"])
print(result["text"])  # Output: "NASA API and FBI DATABASE"

# Handles acronyms with numbers
result = title_fix("using oauth2 authentication", acronyms=["oauth2"])
print(result["text"])  # Output: "Using OAUTH2 Authentication"

# Works with hyphenated acronyms
result = title_fix("jwt-based authentication", acronyms=["jwt"])
print(result["text"])  # Output: "JWT-Based Authentication"
```

### Preserve Uppercase Words

Keep words that are already fully uppercase in your input:

```python
# Preserve all-uppercase words from the input
result = title_fix("REST API with GRAPHQL backend", preserve_uppercase=True)
print(result["text"])  # Output: "REST API With GRAPHQL Backend"

# Works with mixed content
result = title_fix("Using JWT tokens with OAUTH2", preserve_uppercase=True)
print(result["text"])  # Output: "Using JWT Tokens With OAUTH2"

# Combine with custom acronyms for maximum flexibility
result = title_fix(
    "REST api and SDK integration",
    acronyms=["api", "sdk"],
    preserve_uppercase=True
)
print(result["text"])  # Output: "REST API and SDK Integration"
```

## Citation Style Rules

Each citation style follows specific rules for capitalization:

### APA Style
- Capitalize first word and first word after colons
- Capitalize all major words with 4+ letters
- Capitalize both parts of hyphenated major words
- Always capitalize: proper nouns, acronyms, and verbs

### Chicago Style
- Capitalize first and last words
- Capitalize all major words regardless of length
- Lowercase articles (a, an, the), coordinating conjunctions, and prepositions
- Capitalize both parts of hyphenated words

### AP Style
- Capitalize words with 4+ letters
- Capitalize first and last words
- Always capitalize: proper nouns, acronyms
- Special handling for AP-specific terms

### MLA Style
- Capitalize first word and all principal words
- Capitalize verbs (including is, are, was, were)
- Lowercase articles, prepositions, and coordinating conjunctions
- Capitalize both parts of hyphenated major words

### NYT Style
- Capitalize words with 5+ letters
- Always capitalize proper nouns and acronyms
- More conservative with capitalization of short words
- Capitalize first and last words

## Headline Score

The headline score is calculated based on several factors:

- Optimal length (40-60 characters scores highest)
- Word count (6-10 words ideal)
- Use of power words (how, why, what, when, top, best, new, ultimate, complete, guide)
- Use of emotional words (amazing, incredible, shocking, secret, proven)
- Presence of numbers
- Overall structure and readability

A score of 100 indicates an optimal headline according to common best practices. Scores above 70 are generally considered good.

## Error Handling

The package includes comprehensive input validation:

```python
from title_fix import validate_input

# Validate parameters before processing
try:
    validate_input("test text", "title", "apa")  # Valid
    validate_input("test text", "invalid", "apa")  # Raises ValueError
except ValueError as e:
    print(f"Validation error: {e}")
```

## API Reference

### Main Function

```python
title_fix(text, case_type="title", style="apa", straight_quotes=False, quick_copy=True, 
          acronyms=None, preserve_uppercase=False)
```

**Parameters:**
- `text` (str): Input text to process
- `case_type` (str): One of "title", "sentence", "upper", "lower", "first", "alt", "toggle"
- `style` (str): Citation style for title case - "apa", "chicago", "ap", "mla", "nyt"
- `straight_quotes` (bool): Convert curly quotes to straight quotes
- `quick_copy` (bool): Enable quick copy functionality
- `acronyms` (Iterable[str], optional): Custom acronyms to capitalize (e.g., ["api", "sdk", "rest"])
- `preserve_uppercase` (bool): Keep words that are already fully uppercase in the input

**Returns:**
- Dictionary with keys: `text`, `word_count`, `char_count`, `headline_score`, `quick_copy`, `case_type`, `style`

### Utility Functions

- `get_supported_styles()`: Returns list of supported citation styles
- `get_supported_case_types()`: Returns list of supported case types
- `validate_input(text, case_type, style)`: Validates input parameters

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 