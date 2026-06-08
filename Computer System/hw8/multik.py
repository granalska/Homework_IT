import multiprocessing
from multiprocessing import Process
from time import sleep
import re

#ф-ція пошуку ключових слів
def search_keywords(keywords_data):
    keywords_index, lines, target_word = keywords_data
    coincidences = []

#перебираємо рядки, зводимо до нижнього регістру і повертаємо усе знайдене
    for line_num, line in enumerate(lines, 1):
        line_lower = line.lower()

        #перевіряємо кожне слово зі списку ключових слів
        for word in target_word:
            if word.lower() in line_lower:
                pattern = r'[а-яєіїґ]*' + re.escape(word.lower()) + r'[а-яєіїґ]*'
                match = re.search(pattern, line_lower)
                
                if match:
                    full_word = match.group() #повне слово з тексту
                else:
                    full_word = word
                coincidences.append((keywords_index, line_num, full_word))
                break
    return coincidences
        
#прописуємо шлях до тексту, ключові слова, розділення рядків та порожній список куди все закинемо
if __name__ == '__main__':

    file_path = '/Users/admin/Developer/Computer System/hw8/Аналітика контернаступу на Запоріжжі 23р.txt'
    target_word = ['засоб', 'контрнаступ', 'ЗСУ', 'бронетех', 'оборон', 'артилер', 'фронт']

    keyword_size = 200
    empty_list = []

#відкриваємо файл для читання та індексуємо
    with open(file_path, 'r', encoding= 'utf-8') as file:
        data_collection = []
        keywords_index = 0

#перебираємо частини тексту і складаємо в пустий список. а потім беремо нову частину
        for line in file:
            data_collection.append(line)
            if len(data_collection) == keyword_size:
                empty_list.append((keywords_index, data_collection, target_word))
                keywords_index += 1
                data_collection = []

#обробка залишку по тексту
        if data_collection:
            empty_list.append((keywords_index, data_collection, target_word))
        
    print(f'Обробка тексту. Розбиття на частини...')

#запуск завдань на ядрах
    with multiprocessing.Pool() as pool:
        results = pool.map(search_keywords, empty_list)

    print(f'Результати пошуку ключових слів:\n', target_word)
    total_coincidence = 0

#результат
    for match_list in results:
        for keywords_index, line_num, text in match_list:
            real_line_num = (keywords_index * keyword_size) + line_num
            print(f"Рядок {real_line_num}: {text}")
            total_coincidence += 1
            
    print(f"Всього знайдено збігів по ключових словах: {total_coincidence}")

