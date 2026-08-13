# Vigenère Cipher — Implementation & Cryptanalysis

پیاده‌سازی رمز ویژنر (رمزنگاری با کلید معلوم) و رمزشکنی بدون کلید با استفاده از شاخص تطابق (IC)، روش کاسیسکی، و تحلیل فراوانی حروف.
 
## نحوه استفاده

```bash
pip install matplotlib
python3 main.py                 # رمزنگاری/رمزگشایی + رمزشکنی نمونه
python3 vigenere_evaluation.py  # آزمایش نرخ موفقیت + رسم نمودار
```

تنظیمات (متن، کلید، زبان) در بخش `USER SETTINGS` ابتدای `main.py` قابل ویرایش است.

### استفاده برنامه‌نویسی (API)

```python
from vigenere_cipher import vigenere_encrypt, vigenere_decrypt
from vigenere_crack import crack_vigenere, ENGLISH_LETTER_FREQUENCIES

cipher = vigenere_encrypt("ATTACK AT DAWN", "LEMON")
result = crack_vigenere(cipher, ENGLISH_LETTER_FREQUENCIES)
print(result["recovered_key"], result["plaintext"])
```

## ساختار و منطق ریاضی هر بخش

| فایل | وظیفه | منطق ریاضی |
|---|---|---|
| `vigenere_utils.py` | پاکسازی متن و تبدیل حرف↔عدد | نگاشت الفبا به $\mathbb{Z}_m$ |
| `vigenere_cipher.py` | رمزنگاری/رمزگشایی با کلید معلوم | جمع/تفریق پیمانه‌ای: $C_i=(P_i+K_{i \bmod L}) \bmod m$ |
| `vigenere_keylength.py` | تشخیص طول کلید بدون داشتن آن | **IC**: میزان یکسانی آماری حروف؛ متن تک‌الفبایی IC بالا دارد. **Kasiski**: gcd فاصله‌ی رشته‌های تکراری = مضربی از طول کلید |
| `vigenere_crack.py` | بازیابی کلید کامل | هر ستون = یک رمز سزار مستقل؛ با آزمون chi-squared نسبت به جدول فراوانی زبان، بهترین شیفت هر ستون انتخاب می‌شود |
| `vigenere_evaluation.py` | سنجش تجربی عملکرد | تکرار رمزشکنی روی طول‌های مختلف متن و رسم نرخ موفقیت |
| `main.py` | نقطه ورود؛ اجرای هر دو حالت (کلید معلوم / رمزشکنی) | — |

**نکته کلیدی:** فضای کلید ویژنر برابر $m^L$ است (نمایی)؛ اما با شناخت طول کلید $L$، مسئله به $L$ زیرمسئله‌ی مستقل با فضای کلید $m$ (خطی) تبدیل می‌شود — همین کاهش پیچیدگی اساس رمزشکنی آماری است، نه brute-force.
