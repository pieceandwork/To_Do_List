import json
import os
from colorama import Fore, Style, init
from datetime import datetime, date
import time
from plyer import notification

DATA_BASE = "data_base_eng.json"  # <--- Изменено на новый файл
init(autoreset=True)  # Automatically resets color after each print.


def load_tasks():
    """Loads tasks and automatically updates statuses based on deadlines"""
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

                if "In progress" in task['Status']:
                    if deadline_date < today:
                        task['Status'] = "😰 Overdue!"
                        status_changed = True
                    elif deadline_date == today:
                        task['Status'] = "‼️ Hurry up!"
                        status_changed = True

                if deadline_date == today and "Done" not in task['Status']:
                    try:
                        notification.notify(
                            title="⏰ Deadline is today!",
                            message=f"Task #{task['id']}: {task['Title']}\nDon't forget to complete it!",
                            app_name="To-Do List",
                            timeout=5
                        )
                    except Exception as e:
                        print(f"Failed to show notification: {e}")

        if status_changed:
            save_tasks(tasks_data)

        return tasks_data

    except (json.JSONDecodeError, ValueError):
        return {"tasks": []}


def save_tasks(tasks):
    """Saves Your tasks"""

    with open(DATA_BASE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def show_tasks(tasks):
    """Beautifully displays Your tasks on the screen"""

    print("\n" + "=" * 33)
    if len(tasks['tasks']) == 0:
        print("🗨️ The list is empty. Add a task!")
    else:
        for i in range(len(tasks['tasks'])):
            print(f"• {Fore.LIGHTWHITE_EX}Task №{tasks['tasks'][i]['id']}")
            print(f"• {Fore.LIGHTGREEN_EX}Title:{Style.RESET_ALL} {tasks['tasks'][i]['Title']}")
            print(f"• {Fore.GREEN}Description{Style.RESET_ALL}: {tasks['tasks'][i]['Bio']}")
            print(f"• {Fore.CYAN}Deadline (due date){Style.RESET_ALL}: {tasks['tasks'][i]['Deadline']}")
            print(f"• {Fore.BLUE}Status:{Style.RESET_ALL} {tasks['tasks'][i]['Status']}\n")
    print("=" * 33 + "\n")

    while True:
        value = input('\n❕ Press Enter to continue: ')
        if plug_func(value) == True:
            print()
            info()


def info():
    """Displays the control panel on the screen"""

    print()
    print(f"{Fore.RED}To Do{Style.RESET_ALL} - {Fore.CYAN}Your assistant for keeping a task list!\n")
    print("=" * 37)
    print(f"‖       {Fore.LIGHTBLUE_EX}  --Control Panel--       {Style.RESET_ALL}  ‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Show tasks ({Fore.LIGHTRED_EX}1{Style.RESET_ALL})                  ‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Add task ({Fore.LIGHTRED_EX}2{Style.RESET_ALL})                    ‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Mark task as completed ({Fore.LIGHTRED_EX}3{Style.RESET_ALL})      ‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Delete task ({Fore.LIGHTRED_EX}4{Style.RESET_ALL})                 ‖\n")
    print(
        f"‖ {Fore.LIGHTYELLOW_EX}•{Style.RESET_ALL} Exit ({Fore.LIGHTRED_EX}5{Style.RESET_ALL})                        ‖")
    print("=" * 37)
    while True:
        try:
            option = int(input("\n💠 Choose a number (from 1 to 5): "))
            if option <= 0 or option > 5:
                print("\n❌ The number must be in the range from 1 to 5!")
            else:
                break
        except ValueError:
            print("\n❌ Please enter a numeric value!")

    tasks = load_tasks()

    match option:
        case 1:
            show_tasks(tasks)  # Show tasks
        case 2:
            add_task()  # Add task
        case 3:
            completed_task()  # Mark task as completed
        case 4:
            delete_task()  # Delete task
        case 5:
            program_exit()  # Exit


def plug_func(value):
    """Stub function"""

    if value != '':
        print('\n❌ Press Enter to return to the control panel!')
    else:
        return True


def confirmation():
    """Confirmation of choice"""

    print("\nAre you sure❓\n")
    while True:
        choice = input("✋ Keep (or 1) / ✏️ Change (or 2): ")
        if choice.lower() != "keep" and choice.lower() != "change" and choice != "1" and choice != "2":
            print("\n❌ You entered an incorrect value!\n")
        else:
            return choice


def delete_confirmation(choice):
    """Deletion confirmation"""

    tasks = load_tasks()

    print(f"\nAre you sure you want to delete task #{tasks['tasks'][choice - 1]['id']}⁉️\n")
    while True:
        choice2 = input("✅ Yes / ❌ No: ")
        if choice2.lower() != "yes" and choice2.lower() != "no":
            print("\n❌ Incorrect value!\n")
        else:
            return choice2


def add_task():
    """Adding a task (title, description, deadline)"""

    tasks = load_tasks()

    while True:
        option = input("\n📅 Enter the task title: ")
        choice = confirmation()
        if choice.lower() == "keep" or choice == "1":
            break

    while True:
        option2 = input("\n\n📝 Enter the task description, (what needs to be done): ")
        choice2 = confirmation()
        if choice2.lower() == "keep" or choice2 == "1":
            break

    while True:
        option3 = input(
            f"\n\n🏁 Enter the deadline (due dates), format - {Fore.LIGHTYELLOW_EX}01.01.2026{Style.RESET_ALL}: ")
        try:
            parsed_date = datetime.strptime(option3, "%d.%m.%Y").date()
            if parsed_date < date.today():
                print("\n❌ The date cannot be in the past! Enter today's or a future date.")
                continue
        except ValueError:
            print("\n❌ Incorrect value!")
            continue
        choice3 = confirmation()
        if choice3.lower() == "keep" or choice3 == "1":
            break

    tasks['tasks'].append({'id': f'{len(tasks['tasks']) + 1}', 'Title': option, 'Bio': option2,
                           'Deadline': parsed_date.strftime("%d.%m.%Y"),
                           'Status': '⚙️ In progress'})

    save_tasks(tasks)

    while True:
        value = input('\n❕ Press Enter to continue: ')
        if plug_func(value) == True:
            print()
            info()


def completed_task():
    """Marks a task as completed"""

    tasks = load_tasks()
    in_progress_count = len([task for task in tasks['tasks'] if task['Status'] == "⚙️ In progress" or task['Status'] == "‼️ Hurry up!"])

    while True:
        choice = int(input(f"\n🖲️ Enter the task you completed (You have: {in_progress_count}): "))
        if type(choice) != int:
            print("\n❌ Invalid data type!")
        elif choice < 1 or choice > len(tasks['tasks']):
            print("\n❌ This task does not exist")
        else:
            break

    deadline_str = tasks['tasks'][choice - 1]['Deadline']
    deadline_date = datetime.strptime(deadline_str, "%d.%m.%Y").date()

    today = date.today()

    allowed_statuses = ["⚙️ In progress", "‼️ Hurry up!"]

    if tasks['tasks'][choice - 1]['Status'] not in allowed_statuses:
        print(f"\n⚠️ This task cannot be changed. It already has the status: {tasks['tasks'][choice - 1]['Status']}")

    else:
        if today <= deadline_date:
            print(
                "\n✅ All good, the deadline has not passed yet (or expires today). You marked this task as completed!\n")
            tasks['tasks'][choice - 1]['Status'] = "✅ Done on time"
        else:
            print("\n🔥 Deadline is overdue! You marked this task as overdue, but completed!\n")
            tasks['tasks'][choice - 1]['Status'] = "🔥 Done, but overdue"

    save_tasks(tasks)

    while True:
        value = input('\n❕ Press Enter to continue: ')
        if plug_func(value) == True:
            print()
            info()


def delete_task():
    """Deletes the selected task"""

    tasks = load_tasks()

    while True:
        try:
            choice = int(input("\n⛔ Select which task you want to delete: "))
            if choice < 1 or choice > len(tasks['tasks']):
                print("\n❌ Incorrect value!")
                continue
        except ValueError:
            print("\n❌ Invalid data type!")
            continue
        else:
            choice2 = delete_confirmation(choice)
            if choice2.lower() == "yes":
                print('\n♦️ Starting deletion...\n')
                del tasks['tasks'][choice - 1]
                save_tasks(tasks)
                time.sleep(2)
                print("\n✅ Success!\n")
                break

    while True:
        value = input('\n❕ Press Enter to continue: ')
        if plug_func(value) == True:
            print()
            info()


def program_exit():
    """Exit the program"""

    print("\nAre you sure you want to exit❓\n")
    while True:
        choice = input("✅ Yes / ❎ No: ")
        if choice.lower() != "yes" and choice.lower() != "no":
            print("\n❌ Incorrect value!\n")
        else:
            break
    if choice.lower() == "yes":
        exit("\n‼️ Keep an eye on your deadlines!")
    else:
        print('\n')
        info()


info()
