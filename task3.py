import timeit
import re
import pandas as pd

# ---------------------------
# Читання текстів з файлів
# ---------------------------
with open('article1.txt', 'r', encoding='utf-8') as f:
    text1 = f.read()

with open('article2.txt', 'r', encoding='utf-8') as f:
    text2 = f.read()

# ---------------------------
# Алгоритм Рабіна-Карпа
# ---------------------------
def rabin_karp(text, pattern):
    d = 256
    q = 101
    n = len(text)
    m = len(pattern)
    h = pow(d, m-1, q)
    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for s in range(n - m + 1):
        if p == t:
            if text[s:s + m] == pattern:
                return s
        if s < n - m:
            t = (d * (t - ord(text[s]) * h) + ord(text[s + m])) % q
            t = (t + q) % q
    return -1

# ---------------------------
# Алгоритм Кнута-Морріса-Пратта
# ---------------------------
def kmp_search(text, pattern):
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            elif length:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
        return lps

    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return i - j
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return -1

# ---------------------------
# Алгоритм Боєра-Мура
# ---------------------------
def boyer_moore(text, pattern):
    match = re.search(re.escape(pattern), text)
    return match.start() if match else -1

# ---------------------------
# Функція для timeit
# ---------------------------
def measure_time(func, text, pattern):
    return timeit.timeit(lambda: func(text, pattern), number=3) / 3  # середній час

# ---------------------------
# Підрядки для пошуку
# ---------------------------
existing_substring_1 = text1[100:130]
fake_substring_1 = "qwertyuiopasdfghjkl"

existing_substring_2 = text2[200:230]
fake_substring_2 = "zxcvbnmlkjhgfdsa"

# ---------------------------
# Збір результатів
# ---------------------------
results = []

for text_id, text, substr_exist, substr_fake in [
    ("Text 1", text1, existing_substring_1, fake_substring_1),
    ("Text 2", text2, existing_substring_2, fake_substring_2)
]:
    for algo_name, algo_func in [
        ("Rabin-Karp", rabin_karp),
        ("KMP", kmp_search),
        ("Boyer-Moore", boyer_moore)
    ]:
        time_exist = measure_time(algo_func, text, substr_exist)
        time_fake = measure_time(algo_func, text, substr_fake)
        results.append((text_id, algo_name, time_exist, time_fake))

# ---------------------------
# Виведення результатів
# ---------------------------
df = pd.DataFrame(results, columns=["Text", "Algorithm", "Time (existing)", "Time (fake)"])

print("\n📊 Таблиця порівняння часу виконання:")
print(df.to_string(index=False))

# Найшвидший для кожного тексту
best_per_text = df.loc[df.groupby("Text")["Time (existing)"].idxmin().values]

print("\n🏆 Найшвидший алгоритм для кожного тексту:")
print(best_per_text[["Text", "Algorithm", "Time (existing)"]].to_string(index=False))

# Найшвидший загалом
overall_best = df.loc[df["Time (existing)"].idxmin()]
print("\n🌐 Найшвидший алгоритм загалом:")
print(overall_best[["Text", "Algorithm", "Time (existing)"]].to_string())