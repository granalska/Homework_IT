use mydb;
/** запит, який відображає таблицю order_details та поле customer_id з таблиці 
orders відповідно для кожного поля запису з таблиці order_details **/
select order_details.*,(select orders2.customer_id from orders2
where orders2.id = order_details.order_id) as customer_id from order_details;

/** запит, який буде відображати таблицю order_details. 
результат відфільтрований так, щоб відповідний запис із таблиці orders 
виконував умову shipper_id=3 **/
select order_details.* from order_details
where order_id in(select orders2.id from orders2 where orders2.shipper_id = 3);

/** вкладений в операторі FROM, який буде обирати рядки з умовою quantity>10
з таблиці order_details. Для отриманих даних знайдіть середнє значення поля
quantity — групувати слід за order_id **/
select order_id, avg(quantity) as avg_quantity from (select order_id,
quantity from order_details
where quantity > 10) as filtr_orders 
group by order_id;

/** розвʼязок 3 задачі використовуючи оператор WITH для створення
тимчасової таблиці temp **/
with temp as( select order_id, avg(quantity) as avg_quantity from order_details
where quantity > 10
group by order_id)
select order_id, avg_quantity from temp;

/** функція з двома параметрами, яка ділить перший на другий.
 Обидва параметри та значення, що повертається, повинні мати тип FLOAT. 
Використовуємо конструкцію DROP FUNCTION IF EXISTS та застосовуємо
функцію до атрибута quantity таблиці order_details **/
delimiter //
drop function if exists separation //
create function separation(input_number float, divider float)
returns float
deterministic
begin
    if divider = 0.0 then
        return null;
    end if;

    return input_number / divider;
end //
delimiter ;


