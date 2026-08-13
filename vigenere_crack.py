"""
Stage 4: Full Vigenere cryptanalysis (no key known).

Once we know the key length L (from Stage 3), the ciphertext splits into
L columns, and each column was encrypted with a single, fixed Caesar
shift. So each column can be cracked independently using letter
frequency analysis - the exact same idea used to break a simple Caesar
cipher.

This stage combines the per-column shifts into the full key and
decrypts the entire message.
"""

from collections import Counter

from vigenere_utils import get_alphabet, clean_text, indices_to_text
from vigenere_cipher import vigenere_decrypt
from vigenere_keylength import find_key_length_ic, split_into_columns


# ---------------------------------------------------------------------------
# Reference letter frequencies (English)
# ---------------------------------------------------------------------------
# Standard English letter frequency table (in percent), commonly used for
# frequency analysis. For Persian, this same dictionary structure should be
# filled in using frequencies extracted from a large Persian corpus, as
# required by the project (see build_frequency_table() below).
ENGLISH_LETTER_FREQUENCIES = {
    "A": 8.17, "B": 1.49, "C": 2.78, "D": 4.25, "E": 12.70, "F": 2.23,
    "G": 2.02, "H": 6.09, "I": 6.97, "J": 0.15, "K": 0.77, "L": 4.03,
    "M": 2.41, "N": 6.75, "O": 7.51, "P": 1.93, "Q": 0.10, "R": 5.99,
    "S": 6.33, "T": 9.06, "U": 2.76, "V": 0.98, "W": 2.36, "X": 0.15,
    "Y": 1.97, "Z": 0.07,
}


def build_frequency_table(corpus_text, language="en"):
    """
    Build a letter frequency table (in percent) from a large reference
    corpus. This is what the project asks for: extracting the Persian
    letter frequency table yourself from a large text, instead of relying
    on a pre-made table.

    Usage for Persian:
        with open("persian_corpus.txt", encoding="utf-8") as f:
            corpus = f.read()
        fa_freq_table = build_frequency_table(corpus, language="fa")
    """
    cleaned = clean_text(corpus_text, language)
    counts = Counter(cleaned)
    total = sum(counts.values())

    if total == 0:
        raise ValueError("Corpus produced no valid letters - check the language/alphabet")

    alphabet = get_alphabet(language)
    # Every letter of the alphabet gets an entry, even if it never appeared
    # (frequency 0.0), so the table always has a consistent shape.
    freq_table = {ch: (counts.get(ch, 0) / total) * 100 for ch in alphabet}
    return freq_table


# ---------------------------------------------------------------------------
# Chi-squared statistic: measures how "close" a shifted column's letter
# distribution is to the reference language distribution.
# ---------------------------------------------------------------------------

def chi_squared_stat(text, reference_freq, language="en"):
    """
    Compute the chi-squared statistic comparing the observed letter
    distribution of `text` against the expected `reference_freq` table.

    A LOWER chi-squared value means the text's letter distribution looks
    MORE like natural language - i.e. it's a better decryption candidate.
    """
    alphabet = get_alphabet(language)
    n = len(text)
    if n == 0:
        return float("inf")

    observed_counts = Counter(text)
    chi_sq = 0.0
    for ch in alphabet:
        observed = observed_counts.get(ch, 0)
        expected = reference_freq.get(ch, 0.0) / 100.0 * n
        if expected > 0:
            chi_sq += ((observed - expected) ** 2) / expected
    return chi_sq


def break_caesar_shift(column_text, reference_freq, language="en"):
    """
    Break a single Caesar-shifted column using frequency analysis.

    Try every possible shift (0..m-1), decrypt the column with it, score
    the result with the chi-squared statistic against the reference
    frequency table, and return the shift with the lowest (best) score.

    This is brute-force over the shift (only m possibilities - cheap),
    combined with a statistical scoring function - this is the same
    principle used to crack a plain Caesar cipher.
    """
    alphabet = get_alphabet(language)
    m = len(alphabet)

    best_shift = 0
    best_score = float("inf")

    for shift in range(m):
        # Decrypt column assuming this shift: P_i = (C_i - shift) mod m
        decrypted_indices = [(alphabet.index(ch) - shift) % m for ch in column_text]
        decrypted_text = indices_to_text(decrypted_indices, language)

        score = chi_squared_stat(decrypted_text, reference_freq, language)
        if score < best_score:
            best_score = score
            best_shift = shift

    return best_shift, best_score


# ---------------------------------------------------------------------------
# Full Vigenere cracking pipeline
# ---------------------------------------------------------------------------

def recover_key(ciphertext, key_length, reference_freq, language="en"):
    """
    Recover the full Vigenere key given the ciphertext and a known key
    length, by breaking each column independently with frequency analysis.
    """
    cleaned = clean_text(ciphertext, language)
    columns = split_into_columns(cleaned, key_length)

    alphabet = get_alphabet(language)
    key_chars = []
    for column in columns:
        shift, _score = break_caesar_shift(column, reference_freq, language)
        key_chars.append(alphabet[shift])

    return "".join(key_chars)


def crack_vigenere(ciphertext, reference_freq, language="en", max_key_length=20):
    """
    Full no-key cryptanalysis pipeline:
    1. Estimate the key length using the Index of Coincidence (Stage 3).
    2. Recover the key by breaking each column with frequency analysis.
    3. Decrypt the ciphertext with the recovered key.

    Returns a dictionary with the estimated key length, recovered key,
    and the decrypted plaintext, so the caller can inspect every step.
    """
    ic_result = find_key_length_ic(ciphertext, language, max_key_length)
    key_length = ic_result["best_length"]

    recovered_key = recover_key(ciphertext, key_length, reference_freq, language)
    plaintext = vigenere_decrypt(ciphertext, recovered_key, language)

    return {
        "key_length": key_length,
        "recovered_key": recovered_key,
        "plaintext": plaintext,
    }


# ---------------------------------------------------------------------------
# Quick self-test (only runs when this file is executed directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from vigenere_cipher import vigenere_encrypt

    plaintext = (
        "THISISASAMPLEPLAINTEXTUSEDFORTESTINGTHEVIGENERECIPHERCRACKING"
        "PIPELINEWEFIRSTESTIMATETHEKEYLENGTHTHENBREAKEACHCOLUMNWITHFR"
        "EQUENCYANALYSISJUSTLIKEBREAKINGASIMPLECAESARCIPHERANDFINALLY"
        "WERECONSTRUCTTHEFULLKEYANDDECRYPTTHEWHOLEMESSAGECORRECTLYIFA"
        "LLSTEPSWORKEDASEXPECTEDTHENTHERECOVEREDPLAINTEXTSHOULDMATCH"
        "THEORIGINALMESSAGEEXACTLYWITHOUTANYERRORSORTYPOSINTHERESULT"
    )
    key = "SECRET"
    cipher = vigenere_encrypt(plaintext, key, language="en")

    result = crack_vigenere(cipher, ENGLISH_LETTER_FREQUENCIES, language="en", max_key_length=15)

    print("True key       :", key)
    print("Estimated length:", result["key_length"])
    print("Recovered key   :", result["recovered_key"])
    print("Plaintext match :", result["plaintext"] == plaintext)

    assert result["recovered_key"] == key, (
        f"Key recovery failed: expected {key}, got {result['recovered_key']}"
    )
    assert result["plaintext"] == plaintext, "Decrypted plaintext does not match the original"

    print("\nSelf-test passed: full crack pipeline recovered the exact key and plaintext.")
