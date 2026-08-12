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

def test_success_rate(text_lengths, num_tests=50):
    success_rates = []
    for L in text_lengths:
        correct = 0
        for _ in range(num_tests):
            plain = ''.join(random.choice(string.ascii_lowercase + ' ') for _ in range(L))
            shift = random.randint(1, 25)
            cipher = caesar_encrypt(plain, shift)
            
            best_shift, _, _ = crack_caesar(cipher)
            
            if best_shift == shift:
                correct += 1
        
        success_rates.append(correct / num_tests)
    
    return success_rates
