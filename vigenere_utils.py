"""
Stage 1: Utilities and preprocessing for the Vigenere cipher project.

This module defines the alphabet(s) we work with, text cleaning functions,
and letter <-> index mapping functions. These are shared building blocks
used by every later stage (encryption, cryptanalysis, evaluation).
"""

# ---------------------------------------------------------------------------
# Alphabets
# ---------------------------------------------------------------------------

# English alphabet (26 letters, uppercase)
ENGLISH_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# Persian alphabet (simplified, 32 letters commonly used for text processing).
# Note: some visually/phonetically similar letters (e.g. different forms of "ی")
# are intentionally not merged here; merging can be done later in cleaning
# if needed for a specific corpus.
PERSIAN_ALPHABET = "ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"


def get_alphabet(language="en"):
    """
    Return the alphabet string for the requested language.
    language: "en" for English, "fa" for Persian.
    """
    if language == "en":
        return ENGLISH_ALPHABET
    elif language == "fa":
        return PERSIAN_ALPHABET
    else:
        raise ValueError("Unsupported language: choose 'en' or 'fa'")


# ---------------------------------------------------------------------------
# Text cleaning
# ---------------------------------------------------------------------------

def clean_text(text, language="en"):
    """
    Clean raw text so it only contains letters from the target alphabet.

    Steps:
    - Convert English text to uppercase (Persian has no case, so this is skipped).
    - Remove spaces, punctuation, digits, and any character not in the alphabet.

    This keeps letter statistics clean for later frequency analysis.
    """
    alphabet = get_alphabet(language)

    if language == "en":
        text = text.upper()

    # Keep only characters that belong to the chosen alphabet
    cleaned = [ch for ch in text if ch in alphabet]
    return "".join(cleaned)


# ---------------------------------------------------------------------------
# Letter <-> index mapping
# ---------------------------------------------------------------------------

def char_to_index(ch, language="en"):
    """Convert a single letter to its numeric index in the alphabet (0-based)."""
    alphabet = get_alphabet(language)
    return alphabet.index(ch)


def index_to_char(idx, language="en"):
    """Convert a numeric index back to its corresponding letter."""
    alphabet = get_alphabet(language)
    m = len(alphabet)
    return alphabet[idx % m]


def text_to_indices(text, language="en"):
    """Convert a cleaned text string into a list of numeric indices."""
    alphabet = get_alphabet(language)
    return [alphabet.index(ch) for ch in text]


def indices_to_text(indices, language="en"):
    """Convert a list of numeric indices back into a text string."""
    alphabet = get_alphabet(language)
    return "".join(alphabet[i % len(alphabet)] for i in indices)


# ---------------------------------------------------------------------------
# Quick self-test (only runs when this file is executed directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    sample = "Attack at Dawn! 123"
    cleaned = clean_text(sample, language="en")
    print("Original:", sample)
    print("Cleaned :", cleaned)

    indices = text_to_indices(cleaned, language="en")
    print("Indices :", indices)

    back_to_text = indices_to_text(indices, language="en")
    print("Back    :", back_to_text)

    assert back_to_text == cleaned, "Round trip conversion failed!"
    print("Self-test passed.")
