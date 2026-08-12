# -*- coding: utf-8 -*-
"""
پروژه رمزنگاری کلاسیک - رمز جانشینی تک حرفی
"""

from collections import Counter
import matplotlib.pyplot as plt

ENGLISH = "abcdefghijklmnopqrstuvwxyz"
PERSIAN = "ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"
EN_FREQ = "etaoinshrdlucmfwypvbgkjqxz"
FA_FREQ = "انریدمتبوهلکگسشف قعزخجپچصضطظثذحغژ".replace(" ", "")


def make_mapping(key, alphabet):
    key = key.lower()
    if len(key) != len(alphabet):
        raise ValueError("طول کلید باید برابر طول الفبا باشد.")
    if set(key) != set(alphabet):
        raise ValueError("کلید باید یک جایگشت کامل و بدون تکرار از الفبا باشد.")
    return dict(zip(alphabet, key))


def encrypt(text, key, alphabet=ENGLISH):
    mapping = make_mapping(key, alphabet)
    result = []
    for ch in text:
        c = ch.lower()
        if c in mapping:
            new = mapping[c]
            result.append(new.upper() if ch.isupper() else new)
        else:
            result.append(ch)
    return "".join(result)


def decrypt(text, key, alphabet=ENGLISH):
    mapping = make_mapping(key, alphabet)
    reverse = {v: k for k, v in mapping.items()}
    result = []
    for ch in text:
        c = ch.lower()
        if c in reverse:
            new = reverse[c]
            result.append(new.upper() if ch.isupper() else new)
        else:
            result.append(ch)
    return "".join(result)


def frequency_table(text, alphabet):
    letters = [c.lower() for c in text if c.lower() in alphabet]
    counts = Counter(letters)
    total = len(letters)
    rows = []
    for c in alphabet:
        n = counts[c]
        p = 100 * n / total if total else 0
        rows.append((c, n, p))
    return sorted(rows, key=lambda x: (-x[1], x[0]))


def index_of_coincidence(text, alphabet):
    letters = [c.lower() for c in text if c.lower() in alphabet]
    n = len(letters)
    if n < 2:
        return 0.0
    counts = Counter(letters)
    return sum(v * (v - 1) for v in counts.values()) / (n * (n - 1))


def ngram_frequency(text, alphabet, n):
    letters = [c.lower() for c in text if c.lower() in alphabet]
    grams = ["".join(letters[i:i+n]) for i in range(len(letters)-n+1)]
    return Counter(grams)


def plot_frequency(text, alphabet, filename="frequency.png"):
    rows = frequency_table(text, alphabet)
    chars = [r[0] for r in rows]
    values = [r[2] for r in rows]
    plt.figure(figsize=(12, 5))
    plt.bar(chars, values)
    plt.xlabel("Letters")
    plt.ylabel("Frequency (%)")
    plt.title("Letter Frequency Analysis")
    plt.tight_layout()
    plt.savefig(filename, dpi=180)
    plt.close()


def frequency_attack(text, alphabet):
    rows = frequency_table(text, alphabet)
    cipher_order = [r[0] for r in rows if r[1] > 0]
    target = EN_FREQ if alphabet == ENGLISH else FA_FREQ
    return dict(zip(cipher_order, target))


def partial_decrypt(text, guess, alphabet):
    return "".join(
        guess.get(ch.lower(), "_") if ch.lower() in alphabet else ch
        for ch in text
    )





def main():
    print("=" * 55)
    print("Monoalphabetic Substitution Cipher")
    print("=" * 55)

    while True:
        print("\n1) Encrypt")
        print("2) Decrypt")
        print("3) Frequency analysis")
        print("4) Frequency attack without key")
        print("5) Exit")

        choice = input("Choose: ").strip()
        if choice == "5":
            break

        language = input("Language (en/fa): ").strip().lower()
        alphabet = PERSIAN if language == "fa" else ENGLISH

        if choice in ("1", "2"):
            text = input("Text: ")
            print("Alphabet:", alphabet)
            key = input("Key: ").strip().lower()
            if choice == "1":
                print("\nEncrypted:", encrypt(text, key, alphabet))
            else:
                print("\nDecrypted:", decrypt(text, key, alphabet))

        elif choice == "3":
            text = input("Text: ")
            print_analysis(text, alphabet)
            plot_frequency(text, alphabet)
            print("frequency.png created.")

        elif choice == "4":
            text = input("Ciphertext: ")
            print_analysis(text, alphabet)
            guess = frequency_attack(text, alphabet)
            print("\nSuggested mapping:")
            for c, p in guess.items():
                print(c, "->", p)
            print("\nInitial guessed plaintext:")
            print(partial_decrypt(text, guess, alphabet))

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
