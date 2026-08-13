"""
Stage 5: Evaluate cryptanalysis performance vs. ciphertext length, and plot it.

Idea: the shorter the ciphertext, the less reliable letter-frequency
statistics become (both for key-length detection and for breaking each
column), so the crack pipeline should fail more often on short texts.
This script measures that effect experimentally and produces the plot
required by the project ("success rate vs. ciphertext length").
"""

import random
import matplotlib
matplotlib.use("Agg")  # render to file, no GUI needed
import matplotlib.pyplot as plt

from vigenere_utils import clean_text, get_alphabet
from vigenere_cipher import vigenere_encrypt
from vigenere_crack import crack_vigenere, ENGLISH_LETTER_FREQUENCIES


# ---------------------------------------------------------------------------
# A reasonably long, original sample corpus for sampling test snippets from.
# Needs to be long enough to cut snippets of a few thousand letters.
# ---------------------------------------------------------------------------
SAMPLE_CORPUS = """
Cryptography is the practice of protecting information by transforming it
into a form that only authorized people can read. Long before computers
existed, people used simple substitution and shift methods to hide the
meaning of military and diplomatic messages. The Caesar cipher, named
after the Roman general who reportedly used it, shifts every letter of
the alphabet by a fixed amount. Although easy to break today, it was
effective when few people could read at all, let alone break a code.

As messages grew more important, cryptographers looked for stronger
methods. The Vigenere cipher improved on simple shifts by using a
repeating keyword, so that the same plaintext letter could be encrypted
differently depending on its position. For centuries this method was
considered unbreakable and was nicknamed the indecipherable cipher.
Eventually, statisticians discovered that natural languages have very
distinctive letter frequency patterns, and these patterns could be used
to attack even polyalphabetic ciphers once the key length was known.

The weather that morning was calm and clear, with a light breeze coming
from the west. Farmers in the valley were already out in their fields,
checking on the crops before the heat of the afternoon arrived. Children
walked along the dirt road toward the small schoolhouse, carrying their
books and lunch pails. In the distance, a train whistle echoed across
the hills, announcing the arrival of goods from the city.

Modern computers can search enormous spaces of possibilities in a very
short time, but even they cannot brute force every possible key for a
cipher whose key space grows exponentially or factorially. This is why
statistical methods remain essential: instead of trying every possible
key, an analyst narrows the search using patterns that are extremely
unlikely to occur by chance in random data. The frequency of letters,
pairs of letters, and triples of letters all carry information about the
underlying language, and a careful analyst can exploit that information
to recover a hidden message without ever knowing the original key.

Every language has its own letter frequency fingerprint. In English, the
letter E appears far more often than the letter Z, and this imbalance
does not disappear even after simple encryption, unless the cipher mixes
multiple alphabets together in a clever way. The index of coincidence
measures exactly this kind of imbalance, giving analysts a numerical way
to distinguish single alphabet substitution from mixed alphabet ciphers.
Combined with the Kasiski method of studying repeated fragments, these
tools formed the foundation of classical cryptanalysis for nearly a
century, until machines eventually took over the heaviest calculations.

In the evening, the village gathered near the old stone well to share
news and stories. An elderly woman recalled tales from her childhood,
when messages between distant relatives took weeks to arrive by letter.
The younger listeners found it hard to imagine a world without instant
communication, yet they still enjoyed hearing how clever people once
solved difficult problems using nothing more than pencil, paper, and
patience. Long after the fire had died down, the stars above the village
shone brightly, indifferent to the passage of time and technology alike.
"""


def generate_random_key(min_len=4, max_len=10, language="en"):
    """Generate a random key of random length using letters from the alphabet."""
    alphabet = get_alphabet(language)
    length = random.randint(min_len, max_len)
    return "".join(random.choice(alphabet) for _ in range(length))


def sample_snippet(corpus, length, language="en"):
    """
    Take a random contiguous snippet of the requested `length` (in cleaned
    letters) from the corpus. If the corpus is shorter than needed, it
    wraps around by repeating itself.
    """
    cleaned = clean_text(corpus, language)
    # Repeat the corpus if necessary so we can always cut a snippet of the
    # requested length, then pick a random starting point.
    while len(cleaned) < length:
        cleaned += cleaned
    start = random.randint(0, len(cleaned) - length)
    return cleaned[start:start + length]


def run_single_trial(text_length, language="en"):
    """
    Run one crack attempt:
    - sample a plaintext snippet of the given length
    - encrypt it with a random key
    - attempt to crack it with no knowledge of the key
    - return True if the recovered plaintext exactly matches the original
    """
    plaintext = sample_snippet(SAMPLE_CORPUS, text_length, language)
    key = generate_random_key(language=language)

    ciphertext = vigenere_encrypt(plaintext, key, language)
    result = crack_vigenere(ciphertext, ENGLISH_LETTER_FREQUENCIES, language=language)

    return result["plaintext"] == plaintext


def evaluate_success_rate(text_lengths, trials_per_length=10, language="en"):
    """
    For each ciphertext length in `text_lengths`, run several trials and
    compute the fraction of trials where the full plaintext was recovered
    exactly. Returns a dict mapping length -> success rate (0.0 to 1.0).
    """
    results = {}
    for length in text_lengths:
        successes = 0
        for _ in range(trials_per_length):
            if run_single_trial(length, language):
                successes += 1
        rate = successes / trials_per_length
        results[length] = rate
        print(f"length={length:5d}  success_rate={rate*100:5.1f}%  "
              f"({successes}/{trials_per_length} trials)")
    return results


def plot_success_rate(results, output_path="success_rate_vs_length.png"):
    """Plot success rate (%) vs. ciphertext length and save to a file."""
    lengths = sorted(results.keys())
    rates = [results[L] * 100 for L in lengths]

    plt.figure(figsize=(8, 5))
    plt.plot(lengths, rates, marker="o", linewidth=2)
    plt.xlabel("Ciphertext length (letters)")
    plt.ylabel("Cracking success rate (%)")
    plt.title("Vigenere Cryptanalysis Success Rate vs. Ciphertext Length")
    plt.grid(True, alpha=0.3)
    plt.ylim(-5, 105)
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    print(f"\nPlot saved to: {output_path}")


# ---------------------------------------------------------------------------
# Run the evaluation (only when this file is executed directly)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    random.seed(42)  # reproducible results

    text_lengths = [30, 60, 100, 150, 250, 400, 600, 900, 1300, 1800]
    results = evaluate_success_rate(text_lengths, trials_per_length=15, language="en")
    plot_success_rate(results, output_path="success_rate_vs_length.png")
