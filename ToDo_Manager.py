import json
import task
from pathlib import Path
from datetime import datetime


STORE = Path("todos.json")

def load_todos():
    if not STORE.exists():
        return []
    try:
        data = json.loads(STORE.read_text(encoding="utf-8"))
        return [task.Task.from_dict(d) for d in data]
    except:
        return []


def save_todos(todos):
    data = [t.to_dict() for t in todos]
    STORE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Speichere in:", STORE.resolve())


def next_id(todos):
    if not todos:
        return 1
    return max(t.id for t in todos) + 1

def add_todo(todos):
    title = input("Title: ").strip()
    if not title:
        print("Cancelled: Title is empty.")
        return
    desc = input("Description (optional): ").strip()
    cat = input("Category (optional): ").strip()
    prio = input("Priority (low, medium, high) [medium]: ").strip().lower()
    if prio not in ["low", "medium", "high", ""]:
        print("Invalid priority. Please enter low, medium, or high.")
        prio = input("Priority (low, medium, high) [medium]: ").strip().lower()
    elif prio == "":
        prio = "medium"

    new_task = task.Task(
        id=next_id(todos),
        title=title,
        desc=desc,
        cat = cat,
        prio=prio,
        done=False
    )

    todos.append(new_task)
    save_todos(todos)
    print(f"Todo added (ID {new_task.id}).")

def format_todo(t: task.Task):
    status = "✔" if t.done else " "
    return f"[{status}] {t.id:3} | {t.title} {t.cat} {t.prio}"

def list_todos(todos, filter_mode="all", query=None):
    filtered = todos

    if filter_mode == "open":
        filtered = [t for t in todos if not t.done]
    elif filter_mode == "done":
        filtered = [t for t in todos if t.done]

    if query:
        q = query.lower()
        filtered = [
            t for t in filtered
            if q in t.title.lower() or q in t.desc.lower()
        ]

    if not filtered:
        print("Keine Todos gefunden.")
        return

    print("-" * 60)
    for t in filtered:
        print(format_todo(t))
    print("-" * 60)

# not looping when exception is thrown 
# if not todos 
def delete_todo(todos):
    notValid = True
    if todos == []:
        print("The list is empty, there is nothing to delete")
        return 
    while notValid:
        try:
            notValid = False
            todo_id = int(input("Enter the ID of the todo to delete: "))
        except ValueError:
            notValid = True
            print("Please enter a valid number.")

    for t in todos:
        if t.id == todo_id:
            confirm = input(f"Are you sure you want to delete todo '{t.title}'? (y/n): ").strip().lower()
            if confirm == 'y':
                todos.remove(t)
                save_todos(todos)
                print(f"Todo ID {todo_id} deleted.")
                return
            else:
                print("Deletion cancelled.")
                return

    print("Todo ID not found.")

def change_todo_status(todos):
    try:
        todo_id = int(input("Enter the ID of the todo to change status: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for t in todos:
        if t.id == todo_id:
            t.done = not t.done
            save_todos(todos)
            print(f"Todo ID {todo_id} marked as {'done' if t.done else 'not done'}.")
            return

    print("Todo ID not found.")

#anpassen an verwendung von klassen
def show_details(todos):
    try:
        todo_id = int(input("Enter the ID of the todo to view details: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    for t in todos:
        if t.id == todo_id:
            print(f"Details for Todo ID {todo_id}:")
            print(f"Title: {t.title}")
            print(f"Description: {t.desc}")
            print(f"Priority: {t.prio}")
            print(f"Category: {t.cat}")
            print(f"Status: {'Done' if t.done else 'Not Done'}")
            print(f"Created: {t.created}")
            return
    print("Todo ID not found.")

def filter_prios(todos):
    try:
        todo_prio = str(input("Enter the priority of the todo to filter (low, medium, high): "))
    except ValueError:
        print("Please enter a valid priority.")
        return
    for t in todos:
        if t.prio == todo_prio:
            print(format_todo(t))
            return
        else:
            print("No task with this priority found.")
            return
        
def filter_todos(todos):
    print("Filter options:")
    print("1. Filter by todo-status")
    print("2. Filter by Priority")
    choice = input("Choose a filter option (1-3): ").strip()

    if choice == '1':
        status = input("Enter status to filter by (open/done): ").strip().lower()
        if status == "open":
            list_todos(todos, filter_mode="open")
        elif status == "done":
            list_todos(todos, filter_mode="done")
        else:
            print("Invalid status option.")
    elif choice == '2':
        filter_prios(todos)
    else:
        print("Invalid filter option.")

    



def help_menu():
    print("""Available commands:
        1. View All Todos - List all todos with their status.
        2. Add Todo - Create a new todo item.
        3. Filter Todos - Filter todos by status (open/done) or priority.
        4. Search Todos - Search todos by keyword in title or description.
        5. Change Todo Status - Mark a todo as done or not done by ID.
        6. Show Todo Details - View detailed information of a todo by ID.
        7. Delete Todo - Remove a todo item by ID.
        H. Help - Show this help menu.
        X. Exit - Close the application.""")

def main():
    print("*" * 40)
    print("Todo Manager Application".center(40))
    print("*" * 40)
    while True:
        todos = load_todos()
        print("\nOptions:")
        print("1. View All Todos")
        print("2. Add Todo")
        print("3. Filter Todos")
        print("4. Search Todos")
        print("5. Change Todo Status")
        print("6. Show Todo Details")
        print("7. Delete Todo")
        print("H. Help")
        print("X. Exit")
        choice = input("Choose an option (1-9 or H or X): ").strip().upper()

        if choice == '1':
            list_todos(todos, filter_mode="all")
        elif choice == '2':
            add_todo(todos)
        elif choice == '3':
            filter_todos(todos)
        elif choice == '4':
            query = input("Enter search query: ").strip()
            list_todos(todos, query=query)
        elif choice == '5':
            change_todo_status(todos)
        elif choice == '6':
            show_details(todos)
        elif choice == '7':
            delete_todo(todos)
        elif choice == 'H':
            help_menu()
        elif choice == 'X':
            print("Exiting Todo Manager. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()