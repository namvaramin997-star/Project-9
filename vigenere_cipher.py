"""
Stage 2: Vigenere encryption and decryption with a known key.

Formula:
    Encryption: C_i = (P_i + K_(i mod L)) mod m
    Decryption: P_i = (C_i - K_(i mod L)) mod m

Where:
    P = plaintext index, C = ciphertext index, K = key index,
    L = key length, m = alphabet size

This stage builds directly on the utilities from Stage 1
(vigenere_utils.py) for text cleaning and char/index conversion.
"""

from vigenere_utils import (
    get_alphabet,
    clean_text,
    text_to_indices,
    indices_to_text,
)


def vigenere_encrypt(plaintext, key, language="en"):
    """
    Encrypt plaintext using the Vigenere cipher with the given key.

    Steps:
    1. Clean both plaintext and key (same alphabet, same casing rules).
    2. Convert plaintext and key letters to numeric indices.
    3. Shift each plaintext letter by the corresponding key letter,
       cycling through the key with the modulo operator.
    4. Convert the resulting indices back to letters.
    """
    m = len(get_alphabet(language))

    plain_clean = clean_text(plaintext, language)
    key_clean = clean_text(key, language)

    if len(key_clean) == 0:
        raise ValueError("Key must contain at least one valid letter")

    plain_indices = text_to_indices(plain_clean, language)
    key_indices = text_to_indices(key_clean, language)
    key_len = len(key_indices)

    cipher_indices = []
    for i, p in enumerate(plain_indices):
        k = key_indices[i % key_len]  # cycle the key over the plaintext
        c = (p + k) % m
        cipher_indices.append(c)

    return indices_to_text(cipher_indices, language)


def vigenere_decrypt(ciphertext, key, language="en"):
    """
    Decrypt ciphertext using the Vigenere cipher with the given key.

    Same idea as encryption, but we subtract the key index instead
    of adding it (the inverse operation under modulo m).
    """
    m = len(get_alphabet(language))

    cipher_clean = clean_text(ciphertext, language)
    key_clean = clean_text(key, language)

    if len(key_clean) == 0:
        raise ValueError("Key must contain at least one valid letter")

    cipher_indices = text_to_indices(cipher_clean, language)
    key_indices = text_to_indices(key_clean, language)
    key_len = len(key_indices)

    plain_indices = []
    for i, c in enumerate(cipher_indices):
        k = key_indices[i % key_len]  # cycle the key over the ciphertext
        p = (c - k) % m
        plain_indices.append(p)

    return indices_to_text(plain_indices, language)


# ---------------------------------------------------------------------------
# Quick self-test (only runs when this file is executed directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Well-known textbook example: ATTACKATDAWN / LEMON -> LXFOPVEFRNHR
    plaintext = "ATTACKATDAWN"
    key = "LEMON"
    expected_cipher = "LXFOPVEFRNHR"

    cipher = vigenere_encrypt(plaintext, key, language="en")
    print("Plaintext :", plaintext)
    print("Key       :", key)
    print("Encrypted :", cipher)
    assert cipher == expected_cipher, f"Encryption mismatch! Got {cipher}"

    decrypted = vigenere_decrypt(cipher, key, language="en")
    print("Decrypted :", decrypted)
    assert decrypted == plaintext, "Decryption did not recover the original plaintext!"

    print("Self-test passed: encryption matches the known example and decryption is correct.")

    # A second round-trip test with a longer, messier input (spaces/punctuation/case)
    sample = "Meet me at the old bridge, tonight!"
    key2 = "SECRET"
    c2 = vigenere_encrypt(sample, key2, language="en")
    p2 = vigenere_decrypt(c2, key2, language="en")
    assert p2 == clean_text(sample, language="en")
    print("Round-trip test on a messy sentence passed.")
