import json
import os
from colorama import Fore, Style, init
from datetime import datetime, date
import time
from plyer import notification

DATA_BASE = "data_base.json"
init(autoreset=True)  # Сбрасываем автоматически цвет после каждого print.


def load_tasks():
    """Загружает задания и автоматически обновляет статусы по дедлайнам"""
    if not os.path.exists(DATA_BASE):
        return {"tasks": []}

    try:
        with open(DATA_BASE, "r", encoding="utf-8") as f:
            tasks_data = json.load(f)

        today = date.today()
        status_changed = False

        for task in tasks_data['tasks']:
            if task.get('Deadline'):
                deadline_date = datetime.strptime(task['Deadline'], "%d.%m.%Y").date()

                if "В процессе" in task['Status']:
                    if deadline_date < today:
                        task['Status'] = "😰 Прогорело!"
                        status_changed = True
                    elif deadline_date == today:
                        task['Status'] = "‼️ Поспешите выполнить!"
                        status_changed = True

                if deadline_date == today and "Сделано" not in task['Status']:
                    try:
                        notification.notify(
                            title="⏰ Дедлайн сегодня!",
                            message=f"Задача №{task['id']}: {task['Title']}\nНе забудьте её выполнить!",
                            app_name="To-Do List",
                            timeout=5
                        )
                    except Exception as e:
                        print(f"Не удалось показать уведомление: {e}")

        if status_changed:
            save_tasks(tasks_data)

        return tasks_data

    except (json.JSONDecodeError, ValueError):
        return {"tasks": []}


def save_tasks(tasks):
    """Сохраняет Ваши задания"""

    with open(DATA_BASE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def show_tasks(tasks):
    """Красиво выводит Ваши задания на экран"""

    print("\n" + "=" * 33)
    if len(tasks['tasks']) == 0:
        print("🗨️ Список пуст. Добавьте задачу!")
    else:
        for i in range(len(tasks['tasks'])):
            print(f"• {Fore.LIGHTWHITE_EX}Задача №{tasks['tasks'][i]['id']}")
            print(f"• {Fore.LIGHTGREEN_EX}Название:{Style.RESET_ALL} {tasks['tasks'][i]['Title']}")
            print(f"• {Fore.GREEN}Описание{Style.RESET_ALL}: {tasks['tasks'][i]['Bio']}")
            print(f"• {Fore.CYAN}Дедлайн (срок){Style.RESET_ALL}: {tasks['tasks'][i]['Deadline']}")
            print(f"• {Fore.BLUE}Статус:{Style.RESET_ALL} {tasks['tasks'][i]['Status']}\n")
    print("=" * 33 + "\n")

    while True:
        value = input('\n❕ Для продолжения нажмите Enter: ')
        if plug_func(value) == True:
            print()
            info()


def info():
    """Вывод панели управления на экран"""

    print()
    print(f"{Fore.RED}To Do{Style.RESET_ALL} - {Fore.CYAN}Ваш помощник для ведения списка задач!\n")
    print("=" * 37)
    print(f"‖       {Fore.LIGHTBLUE_EX}--Панель управления--       {Style.RESET_ALL}‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Показать задачи ({Fore.LIGHTRED_EX}1{Style.RESET_ALL})             ‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Добавить задачу ({Fore.LIGHTRED_EX}2{Style.RESET_ALL})             ‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Отметить выполненную задачу ({Fore.LIGHTRED_EX}3{Style.RESET_ALL}) ‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Удалить задачу ({Fore.LIGHTRED_EX}4{Style.RESET_ALL})              ‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Выход ({Fore.LIGHTRED_EX}5{Style.RESET_ALL})                       ‖")
    print("=" * 37)
    while True:
        try:
            option = int(input("\n💠 Выберите число (от 1 до 5): "))
            if option <= 0 or option > 5:
                print("\n❌ Число должно быть в диапазоне от 1 до 5!")
            else:
                break
        except ValueError:
            print("\n❌ Введите числовое значение!")

    tasks = load_tasks()

    match option:
        case 1:
            show_tasks(tasks)  # Показать задачи
        case 2:
            add_task()  # Добавить задачу
        case 3:
            completed_task()  # Отметить выполненную задачу
        case 4:
            delete_task()  # Удалить задачу
        case 5:
            program_exit()  # Выход


def plug_func(value):
    """Функция-заглушка"""

    if value != '':
        print('\n❌ Для перехода на панель управления нажмите Enter!')
    else:
        return True


def confirmation():
    """Подтверждение выбора"""

    print("\nВы уверены❓\n")
    while True:
        choice = input("✋ Оставить (или 1) / ✏️ Изменить (или 2): ")
        if choice.lower() != "оставить" and choice.lower() != "изменить" and choice != "1" and choice != "2":
            print("\n❌ Вы ввели некорректное значение!\n")
        else:
            return choice


def delete_confirmation(choice):
    """Подтверждение удаления задачи"""

    tasks = load_tasks()

    print(f"\nВы точно хотите удалить задачу №{tasks['tasks'][choice - 1]['id']}⁉️\n")
    while True:
        choice2 = input("✅ Да / ❌ Нет: ")
        if choice2.lower() != "да" and choice2.lower() != "нет":
            print("\n❌ Некорректное значение!\n")
        else:
            return choice2


def add_task():
    """Добавление задачи (название, описание, дедлайн)"""

    tasks = load_tasks()

    while True:
        option = input("\n📅 Введите название задачи: ")
        choice = confirmation()
        if choice.lower() == "оставить" or choice == "1":
            break

    while True:
        option2 = input("\n\n📝 Введите описание задачи, (что нужно сделать): ")
        choice2 = confirmation()
        if choice2.lower() == "оставить" or choice2 == "1":
            break

    while True:
        option3 = input(
            f"\n\n🏁 Введите дедлайн (сроки выполнения), формат - {Fore.LIGHTYELLOW_EX}01.01.2026{Style.RESET_ALL}: ")
        try:
            parsed_date = datetime.strptime(option3, "%d.%m.%Y").date()
            if parsed_date < date.today():
                print("\n❌ Дата не может быть в прошлом! Введите сегодняшнюю или будущую дату.")
                continue
        except ValueError:
            print("\n❌ Некорректное значение!")
            continue
        choice3 = confirmation()
        if choice3.lower() == "оставить" or choice3 == "1":
            break

    tasks['tasks'].append({'id': f'{len(tasks['tasks']) + 1}', 'Title': option, 'Bio': option2,
                           'Deadline': parsed_date.strftime("%d.%m.%Y"),
                           'Status': '⚙️ В процессе'})

    save_tasks(tasks)

    while True:
        value = input('\n❕ Для продолжения нажмите Enter: ')
        if plug_func(value) == True:
            print()
            info()


def completed_task():
    """Отмечает сделанную задачу"""

    tasks = load_tasks()
    in_progress_count = len([task for task in tasks['tasks'] if task['Status'] == "⚙️ В процессе" or task['Status'] == "‼️ Поспешите выполнить!"])

    while True:
        choice = int(input(f"\n🖲️ Введите задачу, которую Вы сделали (У вас их: {in_progress_count}): "))
        if type(choice) != int:
            print("\n❌ Неверный тип данных!")
        elif choice < len(tasks['tasks']) or choice > len(tasks['tasks']):
            print("\n❌ Данной задачи не существует")
        else:
            break

    deadline_str = tasks['tasks'][choice - 1]['Deadline']
    deadline_date = datetime.strptime(deadline_str, "%d.%m.%Y").date()

    today = date.today()

    allowed_statuses = ["⚙️ В процессе", "‼️ Поспешите выполнить!"]

    if tasks['tasks'][choice - 1]['Status'] not in allowed_statuses:
        print(f"\n⚠️ Эту задачу нельзя изменить. Она уже имеет статус: {tasks['tasks'][choice - 1]['Status']}")

    else:
        if today <= deadline_date:
            print(
                "\n✅ Всё в порядке, срок еще не вышел (или истекает сегодня). Вы отметили эту задачу, как сделанной!\n")
            tasks['tasks'][choice - 1]['Status'] = "✅ Сделано вовремя"
        else:
            print("\n🔥 Дедлайн просрочен! Вы отметили эту задачу, как просроченную, но сделанную!\n")
            tasks['tasks'][choice - 1]['Status'] = "🔥 Сделано, но просрочено"

    save_tasks(tasks)

    while True:
        value = input('\n❕ Для продолжения нажмите Enter: ')
        if plug_func(value) == True:
            print()
            info()


def delete_task():
    """Удаляет выбранную задачу"""

    tasks = load_tasks()

    while True:
        try:
            choice = int(input("\n⛔ Выберите какую задачу Вы хотите удалить: "))
            if choice < 1 or choice > len(tasks['tasks']):
                print("\n❌ Некорректное значение!")
                continue
        except ValueError:
            print("\n❌ Неверный тип данных!")
            continue
        else:
            choice2 = delete_confirmation(choice)
            if choice2.lower() == "да":
                print('\n♦️ Начало удаления...\n')
                del tasks['tasks'][choice - 1]
                save_tasks(tasks)
                time.sleep(2)
                print("\n✅ Успешно!\n")
                break

    while True:
        value = input('\n❕ Для продолжения нажмите Enter: ')
        if plug_func(value) == True:
            print()
            info()


def program_exit():
    """Выход из программы"""

    print("\nВы точно хотите выйти❓\n")
    while True:
        choice = input("✅ Да / ❎ Нет: ")
        if choice.lower() != "да" and choice.lower() != "нет":
            print("\n❌ Некорректное значение!\n")
        else:
            break
    if choice.lower() == "да":
        exit("\n‼️ Следите за своими дедлайнами!")
    else:
        print('\n')
        info()


info()
