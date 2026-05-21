-- create schema Pandemic;
use Pandemic;
-- створюємо таблицю статистики пандемій(країна, код країни, перелік хвороб та частота випадків) 
-- create table pandemic_stats(entity varchar(225), code varchar(255), disease varchar(20), cases int);

-- переносимо дані у таблицю статистики
-- insert into pandemic_stats(entity, code, disease, cases)
-- select entity, code, 'yaws', nullif(number_yaws, '') from infectious_cases
-- union all
-- select entity, code, 'polio', nullif(polio_cases,'') from infectious_cases
-- union all
-- select entity, code, 'guinea_worm', nullif(cases_guinea_worm, '') from infectious_cases
-- union all
-- select entity, code, 'rabies', nullif(number_rabies,'') from infectious_cases
-- union all
-- select entity, code, 'malaria', nullif(number_malaria,'') from infectious_cases
-- union all
-- select entity, code, 'hiv', nullif(number_hiv,'') from infectious_cases
-- union all
-- select entity, code, 'tuberculosis', nullif(number_tuberculosis,'') from infectious_cases
-- union all
-- select entity, code, 'smallpox', nullif(number_smallpox,'') from infectious_cases
-- union all
-- select entity, code, 'cholera', nullif(number_cholera_cases,'') from infectious_cases;

-- створюємо таблицю країн(айді, імʼя, код)
-- create table countries(id int primary key auto_increment, name varchar(255), code varchar(255));

-- переносимо дані у табл країн
-- insert into countries(name, code)
-- select distinct entity, code from infectious_cases;

-- створюємо таблицю захворювань(айді, імʼя)
-- create table disease(id int primary key auto_increment, name varchar(255));

-- переносимо дані у табл захворювань 
-- insert into disease(name)
-- select 'yaws' union
-- select 'polio' union
-- select 'guinea_worm' union
-- select 'rabies' union
-- select 'malaria' union
-- select 'hiv' union
-- select 'tuberculosis' union
-- select 'smallpox' union
-- select 'cholera';

-- створюємо табл статистичних даних
-- create table statistics(id int primary key auto_increment, country_id int, disease_id int , cases double, foreign key(country_id) references countries(id), foreign key(disease_id) references disease(id));

-- переносимо дані у табл статистичних даних 
-- insert into statistics (country_id, disease_id, year, cases)
-- select countries.id, disease.id, infectious_cases.year, nullif(infectious_cases.number_yaws,'') from infectious_cases
-- join countries on infectious_cases.entity = countries.name
-- join disease on disease.name = 'yaws'
-- union all
-- select countries.id, disease.id, infectious_cases.year, nullif(infectious_cases.polio_cases,'') from infectious_cases
-- join countries on infectious_cases.entity = countries.name
-- join disease on disease.name = 'polio'
-- union all
-- select countries.id, disease.id, infectious_cases.year, nullif(infectious_cases.cases_guinea_worm,'') from infectious_cases
-- join countries on infectious_cases.entity = countries.name
-- join disease on disease.name = 'guinea_worm'
-- union all
-- select countries.id, disease.id, infectious_cases.year, nullif(infectious_cases.number_rabies,'') from infectious_cases
-- join countries on infectious_cases.entity = countries.name
-- join disease on disease.name = 'rabies'
-- union all
-- select countries.id, disease.id, infectious_cases.year, nullif(infectious_cases.number_malaria,'') from infectious_cases
-- join countries on infectious_cases.entity = countries.name
-- join disease on disease.name = 'malaria'
-- union all
-- select countries.id, disease.id, infectious_cases.year, nullif(infectious_cases.number_hiv,'') from infectious_cases
-- join countries on infectious_cases.entity = countries.name
-- join disease on disease.name = 'hiv'
-- union all
-- select countries.id, disease.id, infectious_cases.year, nullif(infectious_cases.number_tuberculosis,'') from infectious_cases
-- join countries on infectious_cases.entity = countries.name
-- join disease on disease.name = 'tuberculosis'
-- union all
-- select countries.id, disease.id, infectious_cases.year, nullif(infectious_cases.number_smallpox,'') from infectious_cases
-- join countries on infectious_cases.entity = countries.name
-- join disease on disease.name = 'smallpox'
-- union all
-- select countries.id, disease.id, infectious_cases.year, nullif(infectious_cases.number_cholera_cases,'') from infectious_cases
-- join countries on infectious_cases.entity = countries.name
-- join disease on disease.name = 'cholera';

-- кількість завантажених даних
select count(*) as number_of_downloaded from infectious_cases;

-- рахуємо середнє, мінімальне, максимальне значення унікальних entity, code та суму для атрибута number_radies
select country_id, disease_id, avg(cases) as average_rabies, min(cases) as min_rabies, max(cases) as max_rabies, sum(cases) as total_rabies from statistics
where disease_id = (select id from disease where name = 'rabies')
group by country_id, disease_id
order by total_rabies desc
limit 10;

-- побудова колонки різниці в роках, поточної дати та різниці в роках
-- alter table statistics 
-- add column first_january_date date,
-- add column current_date_col date,
-- add column year_diff int;

-- set sql_safe_updates = 0;
-- update statistics
-- set 
-- -- дата першого січня
-- first_january_date = str_to_date(concat(year, '-01-01'), '%Y-%m-%d'),
-- -- поточна дата
-- current_date_col = curdate(),
-- -- різниця між ними в роках
-- year_diff = timestampdiff(year, str_to_date(concat(year, '-01-01'), '%Y-%m-%d'), curdate());
-- set sql_safe_updates = 1;
-- перевірка
select year, first_january_date, current_date_col, year_diff from statistics;

-- створення ф-кції, яка рахує к-сть захворювань на місяць
-- delimiter //
-- create function period_avg(cases_val double, divisor int) returns double deterministic begin return cases_val / divisor; end //
-- delimiter ;
select year, cases, period_avg(cases, 12) as number_of_diseases from statistics where cases is not null and cases != '';

