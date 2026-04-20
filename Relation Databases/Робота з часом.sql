use mydb;
-- запит який витягує рік, місяць, день та виводить поряд ориг id та date
select id, `date`, year(`date`) as Year, month(`date`) as Month, day(`date`) as Day from orders2;

-- запит який додає один день та виводить поряд ориг id та date
select id, `date`, date_add(`date`, interval 1 day) as date_plus_one_day from orders2;
 
-- запит який відображає кількість секунд з початку відліку (показує його значення timestamp) та виводить поряд ориг id та date
 select id, `date`, timestamp(`date`) from orders2;
 
 -- запит, який рахує, скільки таблиця orders містить рядків з атрибутом date у межах між 1996-07-10 00:00:00 та 1996-10-08 00:00:00
 select `date` from orders2 where `date` between '1996-07-10 00:00:00' and '1996-10-08 00:00:00';
 
 -- запит, який який для таблиці orders виводить на екран атрибут id, атрибут date та JSON-об’єкт {"id": <атрибут id рядка>, "date": <атрибут date рядка>}
 select id, date, json_object('id', `id`, 'date', `date`) as json_obj from orders2;