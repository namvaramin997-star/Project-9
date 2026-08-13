import matplotlib.pyplot as plt
import random
import string

REAL_TEXT = """
the quick brown fox jumps over the lazy dog and the lazy dog sleeps all day
python is a powerful programming language that is used for web development
data science artificial intelligence and machine learning are popular fields
computer science students learn algorithms data structures and cryptography
the caesar cipher is one of the simplest and most widely known encryption techniques
it is a type of substitution cipher in which each letter in the plaintext is shifted
a fixed number of places down the alphabet for example with a shift of three
the letter a would be replaced by d the letter b would become e and so on
this method is named after julius caesar who used it to communicate with his generals
although the caesar cipher is easy to implement it is also easy to break
modern cryptanalysis techniques can crack this cipher in milliseconds
the main weakness of the caesar cipher is its very small key space of only twenty six
possible keys which makes it vulnerable to brute force attacks
frequency analysis is another effective method for breaking substitution ciphers
by analyzing the frequency of letters in the ciphertext we can determine the shift
used in the encryption process this technique works well for longer texts
encryption and decryption are fundamental concepts in computer security
understanding classical ciphers helps students learn modern cryptography
the history of cryptography spans thousands of years from ancient egypt to today
"""
CLEAN_TEXT = REAL_TEXT.replace('\n', ' ').lower()
CLEAN_TEXT = ''.join([c for c in CLEAN_TEXT if c.isalpha() or c == ' '])

def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
        else:
            result += char
    return result

def brute_force_caesar(cipher_text):
    candidates = []
    for shift in range(26):
        plain = caesar_decrypt(cipher_text, shift)
        candidates.append((shift, plain))
    return candidates


ENGLISH_FREQ = {
    'a': 0.0817, 'b': 0.0149, 'c': 0.0278, 'd': 0.0425,
    'e': 0.1270, 'f': 0.0223, 'g': 0.0202, 'h': 0.0609,
    'i': 0.0697, 'j': 0.0015, 'k': 0.0077, 'l': 0.0403,
    'm': 0.0241, 'n': 0.0675, 'o': 0.0751, 'p': 0.0193,
    'q': 0.0010, 'r': 0.0599, 's': 0.0633, 't': 0.0906,
    'u': 0.0276, 'v': 0.0098, 'w': 0.0236, 'x': 0.0015,
    'y': 0.0197, 'z': 0.0007
}

def score_text(text, freq_table):
    score = 0
    count = 0
    for char in text.lower():
        if char in freq_table:
            score += freq_table[char]
            count += 1
    return score / count if count > 0 else 0

def crack_caesar(cipher_text):
    best_shift = 0
    best_score = -1
    best_plain = ""
    
    for shift in range(26):
        plain = caesar_decrypt(cipher_text, shift)
        score = score_text(plain, ENGLISH_FREQ)
        
        if score > best_score:
            best_score = score
            best_shift = shift
            best_plain = plain
    
    return best_shift, best_plain, best_score

def test_success_rate(text_lengths, num_tests=100):
    success_rates = []
    for L in text_lengths:
        correct = 0
        for _ in range(num_tests):
            max_start = len(CLEAN_TEXT) - L
            if max_start <= 0:
                continue
            
            start = random.randint(0, max_start)
            plain = CLEAN_TEXT[start:start + L]
            while len(plain) < L or len([c for c in plain if c.isalpha()]) < L // 2:
                start = random.randint(0, max_start)
                plain = CLEAN_TEXT[start:start + L]


            shift = random.randint(1, 25)
            cipher = caesar_encrypt(plain, shift)
            
            best_shift, _, _ = crack_caesar(cipher)
            
            if best_shift == shift:
                correct += 1
        
        success_rates.append(correct / num_tests)
    
    return success_rates

def plot_success_rate():
    lengths = range(5, 100, 5)
    rates = test_success_rate(lengths, num_tests=100)
    plt.figure(figsize=(10, 6))
    plt.plot(lengths, rates, marker='o', linewidth=2, color='blue')
    plt.xlabel('Cipher Text Length (characters)', fontsize=12)
    plt.ylabel('Success Rate', fontsize=12)
    plt.title('Caesar Cipher Cryptanalysis Success Rate vs Text Length', fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.ylim(0, 1.1)
    plt.axhline(y=1.0, color='red', linestyle='--', alpha=0.5, label='100% Success')
    plt.legend()
    plt.show()


if __name__ == "__main__":
    print("Loading... (this may take 10-15 seconds)")
    plot_success_rate()