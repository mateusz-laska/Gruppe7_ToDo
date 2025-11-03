import json
from pathlib import Path
from datetime import datetime

STORE = Path("todos.json")
print(f"Datei wird gespeichert unter: {STORE.resolve()}")




def load_todos():
    if not STORE.exists():
        return []
    try:
        return json.loads(STORE.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_todos(todos):
    STORE.write_text(json.dumps(todos, ensure_ascii=False, indent=2), encoding="utf-8")

def next_id(todos):
    if not todos:
        return 1
    return max(t["id"] for t in todos) + 1

def add_todo(todos):
    title = input("Title: ").strip()
    if not title:
        print("Cancelled: Title is empty.")
        return
    desc = input("Description (optional): ").strip()
    prio = input("Priority (low, medium, high) [medium]: ").strip().lower()
    if prio not in ["low", "medium", "high", ""]:
        print("Invalid priority. Please enter low, medium, or high.")
        prio = input("Priority (low, medium, high) [medium]: ").strip().lower()
    elif prio == "":
        prio = "medium"
    todo = {
        "id": next_id(todos),
        "title": title,
        "description": desc,
        "priority": prio,
        "done": False,
        "created": datetime.now().isoformat(),
    }
    todos.append(todo)
    save_todos(todos)
    print(f"Todo added (ID {todo['id']}).")

def format_todo(t):
    status = "✔" if t["done"] else " "
    title = t["title"]
    prio = t.get("priority", "medium")
    return f"[{status}] {t['id']:3} | {title} (Priority: {prio})"

def list_todos(todos, filter_mode="all", query=None):
    filtered = todos
    if filter_mode == "open":
        filtered = [t for t in todos if not t["done"]]
    elif filter_mode == "done":
        filtered = [t for t in todos if t["done"]]
    if query:
        q = query.lower()
        filtered = [t for t in filtered if q in t["title"].lower() or q in (t.get("description") or "").lower()]
    if not filtered:
        print("Keine Todos gefunden.")
        return
    print("-" * 60)
    for t in sorted(filtered, key=lambda x: (x["done"], x["id"])):
        print(format_todo(t))
    print("-" * 60)
    print(f"{len(filtered)} Einträge (Filter: {filter_mode}{', Suche: '+query if query else ''})")

def delete_todo(todos):
    try:
        todo_id = int(input("Enter the ID of the todo to delete: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    for t in todos:
        if t["id"] == todo_id:
           confirm = input(f"Are you sure you want to delete todo '{t['title']}'? (y/n): ").strip().lower()
           if confirm == 'y':
               todos.remove(t)
               save_todos(todos)
               print(f"Todo ID {todo_id} deleted.")
               return
           else:
               print("Deletion cancelled.")
               return

def change_todo_status(todos):
    try:
        todo_id = int(input("Enter the ID of the todo to change status: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    for t in todos:
        if t["id"] == todo_id:
            t["done"] = not t["done"]
            save_todos(todos)
            status = "done" if t["done"] else "not done"
            print(f"Todo ID {todo_id} marked as {status}.")
            return
    print("Todo ID not found.")


def show_details(todos):
    try:
        todo_id = int(input("Enter the ID of the todo to view details: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    for t in todos:
        if t["id"] == todo_id:
            print(f"Details for Todo ID {todo_id}:")
            print(f"Title: {t['title']}")
            print(f"Description: {t.get('description', 'No description')}")
            print(f"Priority: {t['priority']}")
            print(f"Status: {'Done' if t['done'] else 'Not Done'}")
            print(f"Created: {t['created']}")
            return
    print("Todo ID not found.")

def change_priority(todos):
    try:
        todo_id = int(input("Enter the ID of the todo to change priority: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    for t in todos:
        if t["id"] == todo_id:
            new_prio = input("Enter new priority (low, medium, high): ").strip().lower()
            if new_prio in ["low", "medium", "high"]:
                t["priority"] = new_prio
                save_todos(todos)
                print(f"Todo ID {todo_id} priority changed to {new_prio}.")
            else:
                print("Invalid priority. Please enter low, medium, or high.")
            return
    print("Todo ID not found.")

def help_menu():
    print("""Available commands:
        1. View All Todos - List all todos with their status.
        2. Add Todo - Create a new todo item.
        3. Show Open Todos - List only the todos that are not done.
        4. Show Done Todos - List only the todos that are marked as done.
        5. Search Todos - Search todos by keyword in title or description.
        6. Change Todo Status - Mark a todo as done or not done by ID.
        7. Show Todo Details - View detailed information of a todo by ID.
        8. Delete Todo - Remove a todo item by ID.
        9. Change Todo Priority - Update the priority of a todo by ID.
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
        print("3. Show Open Todos")
        print("4. Show Done Todos")
        print("5. Search Todos")
        print("6. Change Todo Status")
        print("7. Show Todo Details")
        print("8. Delete Todo")
        print("9. Change Todo Priority")
        print("H. Help")
        print("X. Exit")
        choice = input("Choose an option (1-9 or H or X):").strip()
        if choice == '1':
            list_todos(todos, filter_mode="all")
        elif choice == '2':
            add_todo(todos)
        elif choice == '3':
            list_todos(todos, filter_mode="open")
        elif choice == '4':
            list_todos(todos, filter_mode="done")
        elif choice == '5':
            query = input("Enter search query: ").strip()
            list_todos(todos, query=query)
        elif choice == '6':
            change_todo_status(todos)
        elif choice == '7':
            show_details(todos)
        elif choice == '8':
            delete_todo(todos)
        elif choice == '9':
            change_priority(todos)
        elif choice.upper() == 'H':
            help_menu()
        elif choice.upper() == 'X':
            print("Exiting Todo Manager. Goodbye!")
            break
        else:
            print(f"DEBUG: Eingabe war '{choice}', upper: '{choice.upper()}'")
            print("Invalid option. Please try again.")
if __name__ == "__main__":
    main()




