"""
main.py - Entry point that ties together all Vigenere cipher stages.

This file does NOT redefine any logic - it only imports and uses the
functions built in Stages 1-5:
    vigenere_utils.py       -> alphabets, cleaning, char/index conversion
    vigenere_cipher.py      -> encrypt / decrypt with a known key
    vigenere_keylength.py   -> detect key length (IC + Kasiski)
    vigenere_crack.py       -> full no-key cryptanalysis pipeline
    vigenere_evaluation.py  -> success-rate experiment + plot (optional, slow)

HOW TO USE THIS FILE
---------------------
Everything you need to change is in the "USER SETTINGS" section below.
There are two independent modes; run either or both.

MODE A - Encrypt/Decrypt with a known key
    -> Put your own plaintext in PLAINTEXT
    -> Put your own key in KEY
    -> Run the file: it will show the ciphertext and confirm decryption

MODE B - Crack a ciphertext with NO known key
    -> Put a ciphertext in CIPHERTEXT_TO_CRACK
       (or leave it as None to auto-generate one from PLAINTEXT + KEY,
       which is useful for testing that the whole pipeline works)
    -> Run the file: it will print the estimated key length, the
       recovered key, and the recovered plaintext

OUTPUT
------
Everything is printed directly to the terminal/console - there is no
separate output file for Modes A and B (only vigenere_evaluation.py
saves a file, the plot success_rate_vs_length.png, if you run it).
"""

from vigenere_cipher import vigenere_encrypt, vigenere_decrypt
from vigenere_keylength import find_key_length_ic, find_key_length_kasiski
from vigenere_crack import crack_vigenere, ENGLISH_LETTER_FREQUENCIES


# ===========================================================================
# USER SETTINGS - edit these values
# ===========================================================================

LANGUAGE = "en"  # "en" for English, "fa" for Persian (needs its own frequency table)

# ---- Mode A: known-key encryption/decryption ----
PLAINTEXT = (
    "This is a secret message that we want to protect using the "
    "Vigenere cipher. The longer the message, the more reliable the "
    "frequency statistics become, which is important for Mode B below, "
    "where we try to crack a ciphertext without knowing the key at all."
)
KEY = "SECURITY"

# ---- Mode B: cryptanalysis without a key ----
# Leave this as None to auto-generate a ciphertext from PLAINTEXT + KEY above
# (useful to confirm the pipeline works). Otherwise, paste your own
# ciphertext string here, e.g. CIPHERTEXT_TO_CRACK = "LXFOPVEFRNHR..."
CIPHERTEXT_TO_CRACK = None

# Reference frequency table used for cracking. For English, the built-in
# table from vigenere_crack.py is used automatically. For Persian, you
# must first build your own table with build_frequency_table() from a
# large Persian corpus (see vigenere_crack.py) and pass it in here instead.
REFERENCE_FREQ = ENGLISH_LETTER_FREQUENCIES


# ===========================================================================
# MODE A: Encrypt and decrypt with a known key
# ===========================================================================

def run_mode_a():
    print("=" * 70)
    print("MODE A: Encrypt / Decrypt with a known key")
    print("=" * 70)

    print(f"Plaintext : {PLAINTEXT}")
    print(f"Key       : {KEY}")

    ciphertext = vigenere_encrypt(PLAINTEXT, KEY, language=LANGUAGE)
    print(f"Encrypted : {ciphertext}")

    decrypted = vigenere_decrypt(ciphertext, KEY, language=LANGUAGE)
    print(f"Decrypted : {decrypted}")

    return ciphertext


# ===========================================================================
# MODE B: Crack a ciphertext with no known key
# ===========================================================================

def run_mode_b(ciphertext):
    print("\n" + "=" * 70)
    print("MODE B: Crack ciphertext WITHOUT knowing the key")
    print("=" * 70)

    print(f"Ciphertext: {ciphertext}")

    # Step 1: estimate key length with both methods (just for inspection)
    ic_result = find_key_length_ic(ciphertext, language=LANGUAGE)
    kasiski_result = find_key_length_kasiski(ciphertext, language=LANGUAGE)
    print(f"\nKey length guess (Index of Coincidence): {ic_result['best_length']}")
    print(f"Key length guess (Kasiski examination)  : {kasiski_result['best_length']}")

    # Step 2: run the full pipeline (uses IC internally to pick the length,
    # then recovers the key with frequency analysis, then decrypts)
    result = crack_vigenere(ciphertext, REFERENCE_FREQ, language=LANGUAGE)

    print(f"\nFinal estimated key length: {result['key_length']}")
    print(f"Recovered key             : {result['recovered_key']}")
    print(f"Recovered plaintext       : {result['plaintext']}")

    return result


# ===========================================================================
# Program entry point
# ===========================================================================

if __name__ == "__main__":
    # --- Mode A always runs, so you always see a working encrypt/decrypt demo ---
    generated_ciphertext = run_mode_a()

    # --- Mode B runs on either your own ciphertext or the one just generated ---
    ciphertext_for_cracking = CIPHERTEXT_TO_CRACK or generated_ciphertext
    run_mode_b(ciphertext_for_cracking)

    print("\n" + "=" * 70)
    print("Done. To run the length-vs-success-rate experiment and generate")
    print("the plot, run: python3 vigenere_evaluation.py")
    print("=" * 70)
