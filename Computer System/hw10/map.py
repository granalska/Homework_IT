import requests
import matplotlib.pyplot as plt
import re
from concurrent.futures import ThreadPoolExecutor

#прибираємо зайве
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+", " ", text)
    text = re.sub(r"\d+", " ", text)

    #залишаємо англійські літери
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text)

    return text

#отримуємо текст
def get_text_from_url(url):
    response = requests.get(url)
    return response.text

#map
def map_words(text_part):
    result = []
    for word in text_part.split():
        result.append((word, 1))

    return result

#reduce
def reduce_words(mapped_words):
    word_count = {}

    for word, count in mapped_words:
        if word in word_count:
            word_count[word] += count
        else:
            word_count[word] = count

    return word_count

#видалення коротких слів
def remove_short_words(mapped_words):
    result = []

    for word, count in mapped_words:
        if len(word) > 2:
            result.append((word, count))

    return result

#візуалізація
def visualize_top_words(word_count):
    sorted_words = sorted(word_count.items(), key=lambda item: item[1], reverse=True)
    top_words = sorted_words[:10]
    words = []
    counts = []

    for word, count in top_words:
        words.append(word)
        counts.append(count)

    plt.bar(words, counts)
    plt.xticks(rotation=45)
    plt.title("Найчастіше використовуються слова:")
    plt.show()

#опрацювання тексту
url = "https://www.gutenberg.org/cache/epub/11/pg11.txt"
print("Завантаження тексту...")
text = get_text_from_url(url)
text = clean_text(text)
words = text.split()
parts = []
part_size = (len(words) // 4) + 1
for i in range(0, len(words), part_size):
    parts.append(' '.join(words[i:i + part_size]))
with ThreadPoolExecutor(max_workers = 4) as executor:
    result = executor.map(map_words, parts)

mapped_words = []
for part in result:
    mapped_words.extend(part)

filter_word = remove_short_words(mapped_words)
word_count = reduce_words(filter_word)
 
print(sorted(word_count.items(), key=lambda item: item[1], reverse=True)[:10])

print("Візуалізація...")
visualize_top_words(word_count)