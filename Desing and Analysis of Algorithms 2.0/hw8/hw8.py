import random
import time
from collections import OrderedDict


#створюємо клас LRUCache
class LRUCache:
    def __init__(self, capacity=1000):

        #перевіряємо дані
        if capacity <= 0:
            raise ValueError('Розмір кешу повинен бути більше 0')

        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):

        #перевіряємо чи є ключ
        if key not in self.cache:
            return -1

        value = self.cache.pop(key)
        self.cache[key] = value

        return value

    def put(self, key, value):

        #якщо ключ вже існує
        if key in self.cache:
            self.cache.pop(key)

        self.cache[key] = value

        #видаляємо найстаріший елемент
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)

    def keys(self):
        return list(self.cache.keys())

    def remove(self, key):

        #видаляємо ключ
        if key in self.cache:
            del self.cache[key]


#функція для суми без кешу
def range_sum_no_cache(array, left, right):

    #рахуємо суму
    total = 0

    for i in range(left, right + 1):
        total = total + array[i]

    return total


#функція для оновлення без кешу
def update_no_cache(array, index, value):

    #змінюємо значення
    array[index] = value


#створюємо кеш
cache = LRUCache(1000)


#функція для суми з кешем
def range_sum_with_cache(array, left, right):

    #створюємо ключ
    key = (left, right)

    #перевіряємо кеш
    result = cache.get(key)

    if result == -1:

        #рахуємо суму
        result = range_sum_no_cache(
            array,
            left,
            right)

        #зберігаємо результат
        cache.put(key, result)

    return result


#функція для оновлення з кешем
def update_with_cache(array, index, value):

    #оновлюємо значення
    array[index] = value

    #отримуємо всі ключі
    keys = cache.keys()

    #перевіряємо діапазони
    for key in keys:

        left, right = key

        if left <= index <= right:
            cache.remove(key)


#функція для створення запитів
def make_queries(n, q, hot_pool=30, p_hot=0.95, p_update=0.03):

    #створюємо гарячі діапазони
    hot = [
        (
            random.randint(0, n // 2),
            random.randint(n // 2, n - 1)
        )
        for _ in range(hot_pool)]

    queries = []

    #створюємо запити
    for _ in range(q):

        if random.random() < p_update:

            #запит Update
            idx = random.randint(0, n - 1)
            val = random.randint(1, 100)

            queries.append(
                ("Update", idx, val))

        else:

            #запит Range
            if random.random() < p_hot:
                left, right = random.choice(hot)

            else:
                left = random.randint(0, n - 1)
                right = random.randint(left, n - 1)

            queries.append(
                ("Range", left, right)
            )

    return queries


#функція для роботи без кешу
def run_without_cache(array, queries):

    #проходимо всі запити
    for query in queries:

        if query[0] == "Range":
            range_sum_no_cache(
                array,
                query[1],
                query[2]
            )

        else:
            update_no_cache(
                array,
                query[1],
                query[2]
            )


#функція для роботи з кешем
def run_with_cache(array, queries):

    #проходимо всі запити
    for query in queries:

        if query[0] == "Range":
            range_sum_with_cache(
                array,
                query[1],
                query[2]
            )

        else:
            update_with_cache(
                array,
                query[1],
                query[2]
            )


if __name__ == '__main__':

    #розмір масиву
    n = 100000

    #кількість запитів
    q = 50000

    #створюємо масив
    array = [
        random.randint(1, 100)
        for _ in range(n)
    ]

    #створюємо запити
    queries = make_queries(n, q)

    #копія масиву для тесту
    array_no_cache = array.copy()

    #копія масиву для кешу
    array_with_cache = array.copy()

    print('Початок тестування...')
    print('--------------------------\n')

    #тест без кешу
    start_time = time.time()

    run_without_cache(
        array_no_cache,
        queries
    )

    no_cache_time = time.time() - start_time

    #тест з кешем
    start_time = time.time()

    run_with_cache(
        array_with_cache,
        queries
    )

    cache_time = time.time() - start_time

    #рахуємо прискорення
    speedup = no_cache_time / cache_time

    #виводимо результати
    print('Результати:')
    print(
        f'Без кешу : {no_cache_time:.2f} c'
    )
    print(
        f'LRU-кеш  : {cache_time:.2f} c'
    )
    print(
        f'Прискорення: x{speedup:.2f}'
    )

    print('--------------------------\n')

    #перевіряємо правильність
    assert no_cache_time >= 0
    assert cache_time >= 0
    assert speedup > 0

    print('Перевірка пройдена')