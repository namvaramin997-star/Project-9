"""
Stage 3: Key length detection for the Vigenere cipher, without knowing the key.

Two independent methods are implemented:
1. Index of Coincidence (IC)   - a statistical method
2. Kasiski examination         - a combinatorial method based on repeated substrings

Both methods only need the ciphertext as input.
"""

import math
from collections import Counter
from vigenere_utils import get_alphabet, clean_text


# ---------------------------------------------------------------------------
# Method 1: Index of Coincidence (IC)
# ---------------------------------------------------------------------------

def index_of_coincidence(text):
    """
    Compute the Index of Coincidence (IC) of a text.

    IC = sum(n_i * (n_i - 1)) / (N * (N - 1))

    where n_i is the count of letter i, and N is the total text length.
    A high IC (close to natural language) means the text behaves like
    single-alphabet text. A low IC (close to 1/m) means the letters
    look closer to uniformly random, which happens when several
    different Caesar shifts are mixed together.
    """
    n = len(text)
    if n < 2:
        return 0.0

    counts = Counter(text)
    numerator = sum(c * (c - 1) for c in counts.values())
    denominator = n * (n - 1)
    return numerator / denominator


def split_into_columns(text, key_length):
    """
    Split text into `key_length` columns.

    Column j contains every letter whose position i satisfies i % key_length == j.
    Under the correct key length, every column was encrypted with a single
    fixed Caesar shift, so each column behaves like single-alphabet text.
    """
    columns = ["" for _ in range(key_length)]
    for i, ch in enumerate(text):
        columns[i % key_length] += ch
    return columns


def find_key_length_ic(ciphertext, language="en", max_key_length=20):
    """
    Estimate the Vigenere key length using the Index of Coincidence.

    For each candidate key length L (1 to max_key_length):
        - split the ciphertext into L columns
        - compute the IC of each column
        - average the column ICs

    The candidate length whose average IC is closest to natural-language
    IC is the most likely key length. We return the full score table so
    the caller can inspect and plot it, plus the best guess.
    """
    cleaned = clean_text(ciphertext, language)

    scores = {}
    for key_length in range(1, max_key_length + 1):
        columns = split_into_columns(cleaned, key_length)
        column_ics = [index_of_coincidence(col) for col in columns if len(col) > 1]
        if column_ics:
            scores[key_length] = sum(column_ics) / len(column_ics)
        else:
            scores[key_length] = 0.0

    # Natural language IC reference values (used only for reporting/comparison)
    natural_ic_reference = {"en": 0.0667, "fa": None}  # fa should be computed from a corpus

    # IMPORTANT: raw argmax is not enough. Any multiple of the true key length
    # (e.g. 12 when the true length is 6) also produces a high IC, because
    # splitting into 12 columns still groups letters encrypted with the same
    # shift together. So instead of blindly taking the highest score, we scan
    # candidate lengths from smallest to largest and pick the first one whose
    # score is "close enough" to the best score found. This favors the
    # fundamental (smallest) period instead of one of its multiples.
    best_score = max(scores.values())
    threshold = best_score * 0.92  # accept lengths within 8% of the peak score
    best_length = next(L for L in sorted(scores) if scores[L] >= threshold)

    return {
        "scores": scores,
        "best_length": best_length,
        "natural_ic_reference": natural_ic_reference.get(language),
    }


# ---------------------------------------------------------------------------
# Method 2: Kasiski Examination
# ---------------------------------------------------------------------------

def find_repeated_sequences(text, seq_length=3):
    """
    Find all repeated substrings of a fixed length in the text.

    Returns a dictionary mapping each repeated substring to the list of
    starting positions where it occurs (only substrings that occur 2+ times
    are kept).
    """
    positions = {}
    for i in range(len(text) - seq_length + 1):
        seq = text[i:i + seq_length]
        positions.setdefault(seq, []).append(i)

    # Keep only sequences that repeat
    repeated = {seq: pos_list for seq, pos_list in positions.items() if len(pos_list) > 1}
    return repeated


def gcd_of_list(numbers):
    """Compute the GCD of a list of integers."""
    result = numbers[0]
    for n in numbers[1:]:
        result = math.gcd(result, n)
    return result


def find_key_length_kasiski(ciphertext, language="en", seq_length=3, max_key_length=20):
    """
    Estimate the Vigenere key length using Kasiski examination.

    Steps:
    1. Find repeated substrings of length `seq_length` in the ciphertext.
    2. For each repeated substring, compute the distances between
       consecutive occurrences.
    3. Collect all these distances. The key length is likely a common
       divisor of most distances (in practice we count how often each
       small divisor appears across all distances, since real-world
       noise means not every distance is a clean multiple of the key length).
    """
    cleaned = clean_text(ciphertext, language)
    repeated = find_repeated_sequences(cleaned, seq_length)

    distances = []
    for seq, pos_list in repeated.items():
        for i in range(1, len(pos_list)):
            distances.append(pos_list[i] - pos_list[i - 1])

    if not distances:
        return {"distances": [], "divisor_votes": {}, "best_length": None}

    # Vote for each candidate key length: count how many distances it evenly divides.
    # Note: small candidates (like 2 or 3) get "free" votes just by chance, since
    # a random distance has a 1/candidate probability of being divisible by it.
    # To correct for this bias we compute an "enrichment" score: how many more
    # votes a candidate got compared to what pure chance would predict.
    total = len(distances)
    divisor_votes = {}
    enrichment = {}
    for candidate in range(2, max_key_length + 1):
        votes = sum(1 for d in distances if d % candidate == 0)
        expected_by_chance = total / candidate
        divisor_votes[candidate] = votes
        enrichment[candidate] = votes / expected_by_chance if expected_by_chance > 0 else 0

    # Multiples of the true key length (e.g. 12 when the truth is 6) are also
    # enriched, since any distance divisible by 6 is automatically divisible
    # by 12 as well for a good fraction of cases. So among the candidates
    # with strong enrichment, we pick the SMALLEST one - the fundamental
    # period - rather than the single highest-scoring candidate.
    best_enrichment = max(enrichment.values())
    threshold = best_enrichment * 0.8
    strong_candidates = [L for L in sorted(enrichment) if enrichment[L] >= threshold]
    best_length = min(strong_candidates)

    return {
        "distances": distances,
        "divisor_votes": divisor_votes,
        "enrichment": enrichment,
        "best_length": best_length,
    }


# ---------------------------------------------------------------------------
# Quick self-test (only runs when this file is executed directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    from vigenere_cipher import vigenere_encrypt

    # Use a longer, natural-language plaintext so statistics have enough
    # data to work with (short texts make both methods unreliable - this
    # exact effect is measured in Stage 5).
    plaintext = (
        "THISISASAMPLEPLAINTEXTUSEDFORTESTINGTHEVIGENERECIPHERKEYLENGTH"
        "DETECTIONMETHODSTHEINDEXOFCOINCIDENCEANDTHEKASISKIEXAMINATION"
        "SHOULDBOTHBEABLETOESTIMATETHECORRECTKEYLENGTHWHENGIVENENOUGH"
        "CIPHERTEXTTOANALYZESTATISTICALLYANDCOMBINATORIALLYTHEQUICKBROWN"
        "FOXJUMPSOVERTHELAZYDOGWHILETHECRYPTOGRAPHERSTUDIESTHEPATTERNS"
        "OFLETTERFREQUENCYINBOTHTHEPLAINTEXTANDTHERESULTINGCIPHERTEXTTO"
        "RECOVERTHESECRETKEYWITHOUTEVERKNOWINGITINADVANCEWHICHISTHEWHOLE"
        "POINTOFCLASSICALCRYPTANALYSISUSINGSTATISTICSANDCOMBINATORICS"
    )
    key = "CIPHER"  # length 6
    cipher = vigenere_encrypt(plaintext, key, language="en")

    print("True key length:", len(key))

    ic_result = find_key_length_ic(cipher, language="en", max_key_length=15)
    print("\n[IC method] scores per candidate length:")
    for length, score in ic_result["scores"].items():
        marker = "  <-- best" if length == ic_result["best_length"] else ""
        print(f"  L={length:2d}: IC={score:.4f}{marker}")
    print("IC best guess:", ic_result["best_length"])

    kasiski_result = find_key_length_kasiski(cipher, language="en", seq_length=3, max_key_length=15)
    print("\n[Kasiski method] divisor votes and enrichment scores:")
    for length in kasiski_result["divisor_votes"]:
        votes = kasiski_result["divisor_votes"][length]
        enr = kasiski_result["enrichment"][length]
        marker = "  <-- best" if length == kasiski_result["best_length"] else ""
        print(f"  L={length:2d}: votes={votes:3d}  enrichment={enr:.2f}{marker}")
    print("Kasiski best guess:", kasiski_result["best_length"])

    assert ic_result["best_length"] == len(key), "IC method failed to find correct key length"
    assert kasiski_result["best_length"] == len(key), "Kasiski method failed to find correct key length"
    print("\nSelf-test passed: both methods correctly recovered the key length.")
