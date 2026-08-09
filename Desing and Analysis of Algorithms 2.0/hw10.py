#створюємо клас Teacher
class Teacher:
    def __init__(
        self,
        first_name,
        last_name,
        age,
        email,
        can_teach_subjects):

        #зберігаємо дані викладача
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.can_teach_subjects = can_teach_subjects
        self.assigned_subjects = set()


#функція для створення розкладу
def create_schedule(subjects, teachers):

    #перевіряємо дані
    if not isinstance(subjects, set):
        raise TypeError('Предмети повинні бути множиною')

    if not isinstance(teachers, list):
        raise TypeError('Викладачі повинні бути списком')

    #предмети які ще не покриті
    not_covered = set(subjects)

    #результат
    schedule = []

    #поки залишилися предмети
    while not_covered:

        best_teacher = None
        best_subjects = set()

        #шукаємо найкращого викладача
        for teacher in teachers:

            #предмети які він може викладати
            possible_subjects = (
                teacher.can_teach_subjects
                & not_covered)

            #якщо викладач може покрити більше
            if len(possible_subjects) > len(best_subjects):
                best_teacher = teacher
                best_subjects = possible_subjects

            #якщо однакова кількість
            elif len(possible_subjects) == len(best_subjects):

                if len(possible_subjects) > 0:

                    if best_teacher is None:
                        best_teacher = teacher
                        best_subjects = possible_subjects

                    elif teacher.age < best_teacher.age:
                        best_teacher = teacher
                        best_subjects = possible_subjects

        #якщо не знайшли викладача
        if best_teacher is None or len(best_subjects) == 0:
            return []

        #запам'ятовуємо предмети
        best_teacher.assigned_subjects = best_subjects

        #додаємо викладача
        schedule.append(best_teacher)

        #видаляємо покриті предмети
        not_covered -= best_subjects

    return schedule


if __name__ == '__main__':

    #множина предметів
    subjects = {
        'Математика',
        'Фізика',
        'Хімія',
        'Інформатика',
        'Біологія'}

    #створюємо список викладачів
    teachers = [
        Teacher(
            'Олександр',
            'Іваненко',
            45,
            'o.ivanenko@example.com',
            {'Математика', 'Фізика'}),

        Teacher(
            'Марія',
            'Петренко',
            38,
            'm.petrenko@example.com',
            {'Хімія'}),

        Teacher(
            'Сергій',
            'Коваленко',
            50,
            's.kovalenko@example.com',
            {'Інформатика', 'Математика'}),

        Teacher(
            'Наталія',
            'Шевченко',
            29,
            'n.shechenko@example.com',
            {'Біологія', 'Хімія'}),

        Teacher(
            'Дмитро',
            'Бондаренко',
            35,
            'd.bondarenko@example.com',
            {'Фізика', 'Інформатика'}),

        Teacher(
            'Олена',
            'Гриценко',
            42,
            'o.grytsenko@example.com',
            {'Біологія'})]

    #створюємо розклад
    schedule = create_schedule(
        subjects,
        teachers)

    #виводимо результат
    if schedule:

        print('Розклад занять:')
        print('--------------------------\n')

        for teacher in schedule:

            print(
                f'{teacher.first_name} '
                f'{teacher.last_name}, '
                f'{teacher.age} років, '
                f'email: {teacher.email}')

            print(
                f'   Викладає предмети: '
                f'{", ".join(teacher.assigned_subjects)}\n')

    else:
        print(
            'Неможливо покрити всі предмети '
            'наявними викладачами.')
    print('--------------------------\n')

    #перевіряємо правильність
    assert len(schedule) > 0

    all_subjects = set()

    for teacher in schedule:
        all_subjects.update(
            teacher.assigned_subjects)

    assert all_subjects == subjects

    print('Перевірка пройдена')