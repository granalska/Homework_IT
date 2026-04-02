-- вибираємо всі стовпчики
SELECT * FROM products2;
-- вибираємо тільки стовпчики name, phone
SELECT name, phone FROM shippers;

-- знаходимо середнє, максимальне та мінімальне значення стовпчика price
SELECT avg(price) as 'Середнє значення', min(price) as 'Мінімальне', max(price) as 'Максимальне' from products2;

-- вибираємо унікальні значення колонок category_id та price
select distinct category_id, price from products2 
-- тільки 10 рядків
WHERE price <= 10
-- виведення на екран за спаданням
order by price DESC;

-- цінова межа від 20 до 100
select count(*) as 'Кількість продуктів' from products2
where price between 20 and 100;

-- кількість продуктів та середня ціна у кожного постачальника
select supplier_id, count(*) as 'Кількість продуктів', avg(price) as 'Середня ціна' from products2
group by supplier_id;


