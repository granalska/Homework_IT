-- створення схеми 'LibraryManagement'
-- CREATE SCHEMA LibraryManagement;
USE LibraryManagement;

-- створення таблиць
-- create table Authors(author_id int primary key, author_name varchar(255));
-- create table Genres(genre_id int primary key, genre_name varchar(255));
-- create table Books(book_id int primary key, title varchar(255), publication_year int, author_id int, genre_id int, FOREIGN KEY(author_id) REFERENCES Authors(author_id), FOREIGN KEY(genre_id) REFERENCES Genres(genre_id));
-- create table LibraryUsers(user_id int primary key, username varchar(255), email varchar(255));
-- create table Borrowed_books(borrow_id int primary key, book_id int, user_id int, FOREIGN KEY(book_id) REFERENCES Books(book_id), FOREIGN KEY(user_id) REFERENCES LibraryUsers(user_id), borrow_date date, return_date date);

set foreign_key_checks = 0;
TRUNCATE TABLE Borrowed_books;
TRUNCATE TABLE Books;
TRUNCATE TABLE Authors;
TRUNCATE TABLE Genres;
TRUNCATE TABLE LibraryUsers;
SET FOREIGN_KEY_CHECKS = 1;

-- Заповнення Authors
INSERT INTO Authors(author_id, author_name) VALUES
(1, 'Сунь Цзи'),
(2, 'Роберт Грін'),
(3, 'Вальтер'); 

-- Заповнення Genres
INSERT INTO Genres(genre_id, genre_name) VALUES
(1, 'Військова стратегія'),
(2, 'Саморозвиток'),
(3, 'Філософія');

-- Заповнення Books
INSERT INTO Books(book_id, title, publication_year, author_id, genre_id) VALUES
(1, 'Мистецтво війни', -500, 1, 1),
(2, '48 законів влади', 1998, 2, 2),
(3, 'Філософські повісті', 1750, 3, 3); 

-- Заповнення Users 
INSERT INTO LibraryUsers(user_id, username, email) VALUES
(1, 'Михайлюк Діана', 'mihailyuk.diana@example.com'),
(2, 'Федорова Тетяна', 'fedorova.tetiana@example.com'),
(3, 'Пальчик Андрій', 'palchyk.andrii@example.com');

-- Заповнення Borrowed_books
INSERT INTO Borrowed_books(borrow_id, book_id, user_id, borrow_date, return_date) VALUES
(1, 1, 1, '2024-05-10', '2024-05-20'), -- Михайлюк взяла "Мистецтво війни"
(2, 2, 2, '2025-06-15', '2025-06-25'), -- Федорова взяла "48 законів влади"
(3, 3, 3, '2026-07-01', '2026-07-10'); -- Пальчик взяв "Філософські повісті"

-- обʼєднання баз даних теми 3
select orders2.id as order_id, orders2.date as order_date, customers.name as customer_name, employees.first_name, employees.last_name, shippers.name as shipper_name, products2.name as product_name, order_details.quantity, products2.price, categories.name as category_name, suppliers.name as supplier_name from mydb.orders2
inner join mydb.customers on orders2.customer_id = customers.id
inner join mydb.employees on orders2.employee_id = employees.employee_id
inner join mydb.shippers on orders2.shipper_id = shippers.id
inner join mydb.order_details on orders2.id = order_details.order_id
inner join mydb.products2 on order_details.product_id = products2.id
inner join mydb.categories on products2.category_id = categories.id
inner join mydb.suppliers on products2.supplier_id = suppliers.id;

-- кількість рядків отримані після зливання
 select count(*) as 'кількість рядків' from mydb.orders2;

-- заміна операторів
-- select orders2.id as order_id, orders2.date as order_date, customers.name as customer_name, employees.first_name, employees.last_name, shippers.name as shipper_name, products2.name as product_name, order_details.quantity, products2.price, categories.name as category_name, suppliers.name as supplier_name from mydb.orders2
-- inner join mydb.customers on orders2.customer_id = customers.id
-- inner join mydb.employees on orders2.employee_id = employees.employee_id
-- inner join mydb.shippers on orders2.shipper_id = shippers.id
-- left join mydb.order_details on orders2.id = order_details.order_id
-- left join mydb.products2 on order_details.product_id = products2.id
-- right join mydb.categories on products2.category_id = categories.id
-- right join mydb.suppliers on products2.supplier_id = suppliers.id
-- limit 50;

-- к-сть рядків після зміни операторів 
-- select count(*) as 'кількість рядків після зміни операторів' from mydb.orders2;

/* Протестувавши обидва варіанти операторів можна зробити висновок, 
що inner зменшує кількість рядків бо фільтрує дані по яким немає збігів
тобто показує тільки ті де є збіги в обох таблицях. В той час як left і right 
збільшують обсяг на стільки, що workbench вибиває, цк відбувається через 
те що крім усіх даних у пусті рядки додаються також відсутні значення (null)*/

-- рядки, де employee_id > 3 та ≤ 10
select employee_id from mydb.orders2
where employee_id > 3 and employee_id <= 10;

/* Групуємо за іменем категорії, рахуємо к-сть рядків у групі та 
середню к-сть товару. Тут же фільтруємо рядки сер. к-сті тов. > 21.
Сортуємо за спаданням та обираємо 4 рядки з пропущеним 1 рядком.*/
select categories.name as 'Kатегорія', count(*) as 'Kількість рядків', avg(order_details.quantity) as 'Cередня кількість товару' from mydb.orders2
inner join mydb.order_details on orders2.id = order_details.order_id
inner join mydb.products2 on order_details.product_id = products2.id
inner join mydb.categories on products2.category_id = categories.id
group by categories.name
having avg(order_details.quantity) > 21
order by avg(order_details.quantity) desc
limit 4
offset 1;


