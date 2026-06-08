-- користувачі
--create table users(id serial primary key, fullname varchar(100), email varchar(100) unique);
--insert into users (fullname, email)
--values ('mykhailiuk diana', 'diana.mykhailiuk@gmail.com'), ('andriy palchyk', 'andriy.palchyk@gmail.com'), ('tetiana volodymyrivna', 'tetiana.volodymyrivna@gmail.com'), ('vadym kolesnikov', 'vadym.kolesnikov@gmail.com'), ('olha nekrassova', 'olha.nekrassova@gmail.com');

-- таблиця статусів 
--create table status(id serial primary key, name varchar(50) unique)
--insert into status (name) values ('new'), ('in progress'), ('completed');

-- таблиця завдань
--create table tasks(id serial primary key, title varchar(100), description text, status_id integer references status(id), user_id integer references users(id) on delete cascade);
select * from users;
-- отримати завдання для користув
select * from tasks
where user_id = 27;

-- завдання з певним статусом
select * from tasks
where status_id = (select id from status where name = 'new');

-- оновлення статусу 
update tasks
set status_id = (select id from status where name = 'in progress')
where id = 29;

-- список тих, хто немає жодного завдання
select * from users
where id not in (select distinct user_id from tasks where user_id is not null);

-- нова задача користувачу
insert into tasks(title, description, status_id, user_id)
values('new task', 'task description',(select id from status where name = 'new'), 28);

--завдакння, які не завершено
select * from tasks
where status_id <> (select id from status where name = 'completed');

-- видаляємо завдан
delete from tasks
where id = 28;

-- користувач з певною електронкою
select * from users
where email like '%@gmail.com';

-- оновлення імені
update users
set fullname = 'Михайлюк Ді'
where id = 27;

-- кільк завдань для кожного статусу
select status.name, count(tasks.id) from status
left join tasks on tasks.status_id = status.id
group by status.name;

-- корист з певною електронкою
select tasks.* from tasks
join users on users.id = tasks.user_id
where users.email like 'olga%';

-- завдання без опису
select * from tasks
where description is null or description = '';

--корист і задачі з стакьтусом 'in progress'
select users.fullname, tasks.title from users
inner join tasks on users.id = tasks.user_id
inner join status on status.id = tasks.status_id
where status.name = 'in progress';

-- корист та к-сть завдань
select users.fullname, count(tasks.id) as task_count from users
left join tasks on users.id = tasks.user_id
group by users.fullname;

