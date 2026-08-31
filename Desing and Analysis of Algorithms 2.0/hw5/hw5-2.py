import hashlib
import math
import re
import time

#клас HyperLogLog 
class HyperLogLog:
    def __init__(self, b=10):
        self.b = b
        self.m = 1 << b  #2^b регістрів
        self.registers = [0] * self.m

    def _hash(self, val):
        #отримуємо число з хешу
        h = hashlib.md5(val.encode('utf-8')).hexdigest()
        return int(h, 16) & 0xFFFFFFFF

    def add(self, val):
        x = self._hash(val)
        #перші b бітів індекс регістра
        j = x >> (32 - self.b)
        #решта бітів для підрахунку нулів
        w = x & ((1 << (32 - self.b)) - 1)
        
        #позиція першої одиниці
        if w == 0:
            zeros = 32 - self.b + 1
        else:
            zeros = (w & -w).bit_length()

        if zeros > self.registers[j]:
            self.registers[j] = zeros

    def count(self):
        #розрахунок
        alpha = 0.7213 / (1 + 1.079 / self.m)
        z = sum(2.0 ** -reg for reg in self.registers)
        e = alpha * (self.m ** 2) / z

        #корекція для малої кількості значень
        if e <= 2.5 * self.m:
            zeros = self.registers.count(0)
            if zeros != 0:
                e = self.m * math.log(self.m / zeros)

        return round(e)


#ф-ція витягування IP з рядка
def get_ip(line):
    #шукає комбінацію X.X.X.X у рядку
    match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
    return match.group(0) if match else None


#основна частина
filename = '/Users/admin/Developer/Desing and Analysis of Algorithms 2.0/hw5/d.log'

#точний підрахунок через set
start_time = time.time()
unique_ips = set()

with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        ip = get_ip(line)
        if ip:
            unique_ips.add(ip)

exact_count = len(unique_ips)
exact_time = time.time() - start_time

#підрахунок через HyperLogLog
start_time = time.time()
hll = HyperLogLog(b=14)

with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        ip = get_ip(line)
        if ip:
            hll.add(ip)

hll_count = hll.count()
hll_time = time.time() - start_time

#результати
print("Результати порівняння:")
print(f"{'':25} {'Точний підрахунок':<20} {'HyperLogLog':<15}")
print(f"{'Унікальні елементи':25} {exact_count:<20} {hll_count:<15}")
print(f"{'Час виконання (сек.)':25} {exact_time:<20.4f} {hll_time:<15.4f}")
