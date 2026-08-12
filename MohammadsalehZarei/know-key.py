import random
import string

# الفبای انگلیسی
ENGLISH_ALPHABET = string.ascii_lowercase  # 26 حرف

# الفبای فارسی (۳۲ حرف رایج، بدون همزه و اشکال خاص)
PERSIAN_ALPHABET = "ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی"

def generate_key(alphabet):
    """تولید یک کلید تصادفی (جایگشت الفبا)"""
    shuffled = list(alphabet)
    random.shuffle(shuffled)
    return dict(zip(alphabet, shuffled))

def encrypt_substitution(plaintext, key):
    """رمزنگاری با کلید جانشینی مشخص"""
    result = []
    for ch in plaintext:
        result.append(key.get(ch, ch))  # کاراکترهای خارج الفبا بدون تغییر
    return ''.join(result)

def decrypt_substitution(ciphertext, key):
    """رمزگشایی با معکوس‌کردن کلید"""
    inverse_key = {v: k for k, v in key.items()}
    result = []
    for ch in ciphertext:
        result.append(inverse_key.get(ch, ch))
    return ''.join(result)


# --- تست ---
key = generate_key(ENGLISH_ALPHABET)
plaintext = "this is a secret message"
ciphertext = encrypt_substitution(plaintext, key)
decrypted = decrypt_substitution(ciphertext, key)

print("کلید:", key)
print("متن اصلی:", plaintext)
print("متن رمز شده:", ciphertext)
print("متن بازیابی شده:", decrypted)
