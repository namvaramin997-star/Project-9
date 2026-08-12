import math

def key_space_size(alphabet_size):
    return math.factorial(alphabet_size)

eng_space = key_space_size(26)
fa_space = key_space_size(32)

print(f"فضای کلید انگلیسی (26!): {eng_space:.3e}")
print(f"فضای کلید فارسی (32!): {fa_space:.3e}")

# تخمین زمان brute-force
def estimate_bruteforce_time(key_space, keys_per_second=1e9):
    seconds = key_space / keys_per_second
    years = seconds / (60*60*24*365)
    return seconds, years

sec, years = estimate_bruteforce_time(eng_space)
print(f"با فرض اینکه {1e9:.0e} کلید در ثانیه، زمان لازم: {years:.3e} سال")
