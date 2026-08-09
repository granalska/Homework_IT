import hashlib

#творюємо клас BloomFilter
class BloomFilter:
    def __init__(self, size=1000, num_hashes=3):

        #перевіряємо введені дані
        if not isinstance(size, int):
            raise TypeError('Розмір повинен бути числом')
        if not isinstance(num_hashes, int):
            raise TypeError('Кількість хешів повинна бути числом')
        if size <= 0:
            raise ValueError('Розмір повинен бути більше 0')
        if num_hashes <= 0:
            raise ValueError('Кількість хешів повинна бути більше 0')
        self.size = size
        self.num_hashes = num_hashes
        self.bits = bytearray(size)
    def _get_hashes(self, value):

        #отримуємо хеші
        hashes = []
        for i in range(self.num_hashes):
            data = (str(i) + value).encode('utf-8')
            hash_value = int(hashlib.md5(data).hexdigest(), 16)
            hashes.append(hash_value % self.size)
        return hashes
    def add(self, value):

        #перевіряємо дані
        if not isinstance(value, str):
            raise TypeError('Пароль повинен бути рядком')
        if len(value) == 0:
            raise ValueError('Пароль не може бути пустим')
        
        #додаємо пароль
        for index in self._get_hashes(value):
            self.bits[index] = 1
    def __contains__(self, value):

        #перевіряємо дані
        if not isinstance(value, str):
            return False
        if len(value) == 0:
            return False
        
        #перевіряємо пароль
        for index in self._get_hashes(value):
            if self.bits[index] == 0:
                return False
        return True
    
# функція для перевірки паролів
def check_password_uniqueness(bloom, passwords):

    # перевіряємо дані
    if not isinstance(bloom, BloomFilter):
        raise TypeError('Потрібно передати BloomFilter')
    if not isinstance(passwords, list):
        raise TypeError('Потрібно передати список паролів')
    results = {}

    # перевіряємо всі паролі
    for password in passwords:
        if not isinstance(password, str):
            results[password] = 'некоректне значення'
        elif len(password) == 0:
            results[password] = 'порожній пароль'
        elif password in bloom:
            results[password] = 'вже використаний'
        else:
            results[password] = 'унікальний'
    return results

if __name__ == '__main__':

    #створюємо фільтр Блума
    bloom = BloomFilter(size=1000, num_hashes=3)

    #додаємо існуючі паролі
    existing_passwords = [
        'password123',
        'admin123',
        'qwerty123']
    for password in existing_passwords:
        bloom.add(password)\
        
    #перевіряємо нові паролі
    new_passwords_to_check = [
        'password123',
        'newpassword',
        'admin123',
        'guest']
    results = check_password_uniqueness(
        bloom,
        new_passwords_to_check)

    #виводимо результати
    for password, status in results.items():
        print(f"Пароль '{password}' - {status}.")
    print('--------------------------\n')

    #перевіряємо правильність результатів
    assert 'password123' in bloom
    assert 'admin123' in bloom
    assert 'newpassword' not in bloom
    assert results['password123'] == 'вже використаний'
    assert results['newpassword'] == 'унікальний'
    
    print('Перевірка пройдена')