
USE mydb;

-- видаляємо таблиці, раніше помилково створені
DROP TABLE IF EXISTS OrderItems;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Clients;

-- створюємо таблицю клієнтів
CREATE TABLE Clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    last_name VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL);

-- створюємо таблицю товарів
CREATE TABLE Products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL);

-- створюємо таблицю замовлень
CREATE TABLE Orders (
    order_id INT PRIMARY KEY,
    order_date DATE NOT NULL,
    client_id INT,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id));

-- створюємо таблицю складу замовлення
CREATE TABLE OrderItems (
    order_id INT,
    product_id INT,
    quantity INT NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id));

-- заповнюємо дані
INSERT INTO Clients (last_name, address) VALUES 
('Мельник', 'Хрещатик 1'),
('Шевченко', 'Басейна 2'),
('Коваленко', 'Комп’ютерна 3');

INSERT INTO Products (product_name) VALUES 
('Лептоп'), 
('Мишка'), 
('Принтер');

INSERT INTO Orders (order_id, order_date, client_id) VALUES 
(101, '2023-03-15', 1),
(102, '2023-03-16', 2),
(103, '2023-03-17', 3);

INSERT INTO OrderItems (order_id, product_id, quantity) VALUES 
(101, 1, 3), 
(101, 2, 2), 
(102, 3, 1), 
(103, 2, 4);

-- перевірка результату
SELECT 
    o.order_id AS 'Замовлення №',
    p.product_name AS 'Товар',
    oi.quantity AS 'Кількість',
    c.last_name AS 'Клієнт',
    o.order_date AS 'Дата'
FROM OrderItems oi
JOIN Orders o ON oi.order_id = o.order_id
JOIN Products p ON oi.product_id = p.product_id
JOIN Clients c ON o.client_id = c.client_id;
