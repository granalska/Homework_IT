import random
from typing import Dict
import time
from collections import deque


#створюємо клас SlidingWindowRateLimiter
class SlidingWindowRateLimiter:
    def __init__(self, window_size: int = 10, max_requests: int = 1):

        #перевіряємо дані
        if window_size <= 0:
            raise ValueError('Розмір вікна повинен бути більше 0')

        if max_requests <= 0:
            raise ValueError('Кількість запитів повинна бути більше 0')

        self.window_size = window_size
        self.max_requests = max_requests

        #історія повідомлень користувачів
        self.user_requests: Dict[str, deque] = {}

    def _cleanup_window(self, user_id: str, current_time: float) -> None:

        #якщо користувача ще немає
        if user_id not in self.user_requests:
            self.user_requests[user_id] = deque()
            return

        requests = self.user_requests[user_id]

        #видаляємо старі повідомлення
        while requests:
            if current_time - requests[0] >= self.window_size:
                requests.popleft()
            else:
                break

    def can_send_message(self, user_id: str) -> bool:

        #перевіряємо користувача
        if not isinstance(user_id, str):
            return False

        current_time = time.time()

        #очищаємо старі запити
        self._cleanup_window(
            user_id,
            current_time)

        #перевіряємо кількість повідомлень
        if len(self.user_requests[user_id]) < self.max_requests:
            return True

        return False

    def record_message(self, user_id: str) -> bool:

        #перевіряємо чи можна відправити
        if not self.can_send_message(user_id):
            return False

        current_time = time.time()

        #додаємо повідомлення
        self.user_requests[user_id].append(
            current_time)

        return True

    def time_until_next_allowed(self, user_id: str) -> float:

        #якщо користувача немає
        if user_id not in self.user_requests:
            return 0.0

        current_time = time.time()

        #очищаємо старі повідомлення
        self._cleanup_window(
            user_id,
            current_time)

        #якщо місце вже є
        if len(self.user_requests[user_id]) < self.max_requests:
            return 0.0

        #час першого повідомлення
        first_request = self.user_requests[user_id][0]

        #рахуємо час очікування
        wait_time = (
            first_request +
            self.window_size -
            current_time)

        if wait_time < 0:
            return 0.0

        return wait_time


#функція для тестування
def test_rate_limiter():

    #створюємо rate limiter
    limiter = SlidingWindowRateLimiter(
        window_size=10,
        max_requests=1)

    #симулюємо повідомлення
    print('\n=== Симуляція потоку повідомлень ===')

    for message_id in range(1, 11):

        #визначаємо користувача
        user_id = message_id % 5 + 1

        result = limiter.record_message(str(user_id))

        wait_time = limiter.time_until_next_allowed(str(user_id))

        if result:
            status = '✓'
        else:
            status = f'× (очікування {wait_time:.1f}с)'

        print(f'Повідомлення {message_id:2d} | 'f'Користувач {user_id} | {status}')

        #невелика затримка
        time.sleep(
            random.uniform(0.1, 1.0))

    #чекаємо
    print('\nОчікуємо 4 секунди...')
    time.sleep(4)

    print('\n=== Нова серія повідомлень після очікування ===')

    for message_id in range(11, 21):

        #визначаємо користувача
        user_id = message_id % 5 + 1

        result = limiter.record_message(
            str(user_id))

        wait_time = limiter.time_until_next_allowed(str(user_id))

        if result:
            status = '✓'
        else:
            status = f'× (очікування {wait_time:.1f}с)'

        print(f'Повідомлення {message_id:2d} | 'f'Користувач {user_id} | {status}')

        #затримка
        time.sleep(
            random.uniform(0.1, 1.0))


if __name__ == '__main__':

    #запускаємо тест
    test_rate_limiter()
    print('\n--------------------------')

    #перевірка
    limiter = SlidingWindowRateLimiter(10, 1)

    assert limiter.record_message('test') is True
    assert limiter.can_send_message('test') is False
    assert limiter.time_until_next_allowed('test') > 0

    print('Перевірка пройдена')