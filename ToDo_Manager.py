import json
import task
import os
from pathlib import Path


STORE = Path("todos.json")

# Returns tasks as objects of class Task if todo.json is not empty
def load_task():
    if not STORE.exists():
        return []
    try:
        data = json.loads(STORE.read_text(encoding="utf-8"))
        return [task.Task.from_dict(d) for d in data]
    except:
        return []

# Saves all tasks in todos into data dictionary and writes them into todos.json
def save_data(todos):
    data = [t.to_dict() for t in todos]
    STORE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print("Speichere in:", STORE.resolve())

# Check for the highest id and return id + 1
def next_id(todos):
    if not todos:
        return 1
    return max(t.id for t in todos) + 1

# Creates a new task by asking the user for input and creating a new object of class Task with that input
# Adds the new task to the new_task list and calls the save_data() function to save the tasks into todos.json
def create_task(todos):
    title = input("Title: ").strip()
    if not title:
        print("Cancelled: Title is empty.")
        return
    desc = input("Description (optional): ").strip()
    cat = input("Category (optional): ").strip()
    prio = input("Priority (low, medium, high, critical) [medium]: ").strip().lower()
    
    if prio not in ["low", "medium", "high", "critical", ""]:
        print("Invalid priority. Medium priority entered.")
        prio = "medium"

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
    save_data(todos)
    print(f"Todo added (ID {new_task.id}).")

# Returns a formatted string to be printed out with the show_tasks() function
def format_todo(t: task.Task):
    status = "✔" if t.done else " "
    return f"[{status}] {t.id:3} | {t.title} {t.cat} {t.prio}"

# Prints out filtered tasks. The user can filter with the status or their custom query 
def show_tasks(todos, status="all", query=None):
    clear_terminal()
    filtered = todos

    if status == "open":
        filtered = [t for t in todos if not t.done]
    elif status == "done":
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

# Deletes a task defiend by the user if the task list isn't empty
def delete_task(todos):
    notValid = True
    if todos == []:
        print("The list is empty, there is nothing to delete")
        return 
    clear_terminal()
    show_tasks(todos)
    while notValid:
        try:
            notValid = False
            todo_id = int(input("Enter the ID of the todo to delete or -1 to quit: "))
            if todo_id == -1:
                print("Quitting the deletion process")
                return
        except ValueError:
            notValid = True
            print("Please enter a valid number.")

    for t in todos:
        if t.id == todo_id:
            confirm = input(f"Are you sure you want to delete todo '{t.title}'? (y/n): ").strip().lower()
            if confirm == 'y':
                todos.remove(t)
                save_data(todos)
                print("-" * 60)
                print(f"Todo ID {todo_id} deleted.")
                print("-" * 60)
                return
            else:
                print("-" * 60)
                print("Deletion cancelled.")
                print("-" * 60)
                return

    print("Todo ID not found.")

# Changes the status of a task
def mark_task_done(todos):
    show_tasks(todos)
    try:
        todo_id = int(input("Enter the ID of the todo to change status: "))
    except ValueError:
        print("Please enter a valid number.")
        return

    for t in todos:
        if t.id == todo_id:
            t.done = not t.done
            save_data(todos)
            print("-" * 60)
            print(f"Todo ID {todo_id} marked as {'done' if t.done else 'not done'}.")
            print("-" * 60)
            return

    print("Todo ID not found.")

# Prints out the details of a task chosen by the user
def show_details(todos):
    clear_terminal()
    show_tasks(todos)
    try:
        todo_id = int(input("Enter the ID of the todo to view details: "))
    except ValueError:
        print("Please enter a valid number.")
        return
    for t in todos:
        if t.id == todo_id:
            print("-" * 60)
            print(f"Details for Todo ID {todo_id}:")
            print(f"Title: {t.title}")
            print(f"Description: {t.desc}")
            print(f"Priority: {t.prio}")
            print(f"Category: {t.cat}")
            print(f"Status: {'Done' if t.done else 'Not Done'}")
            print(f"Created: {t.created}")
            print("-" * 60)
            return
    print("Todo ID not found.")

# Lists task with chosen priority
def filter_tasks(todos):
    try:
        todo_prio = str(input("Enter the priority of the todo to filter (low, medium, high, critical): ")).strip().lower()
    except ValueError:
        print("Please enter a valid priority.")
        return
    
    filtered = [t for t in todos if t.prio == todo_prio]
    print("-" * 60)
    if not filtered:
        print("No task with this priority found.")
        print("-" * 60)
        return
    
    for t in filtered:
        print(format_todo(t))
    print("-" * 60)
    return
        
# Menu with filter and change options
def list_filter_and_change_options(todos):
    clear_terminal()
    print("\nFilter Options:")
    print("1. View all todos")
    print("2. Filter by todo-status (open/done)")
    print("3. Search todos by keyword")
    print("4. Filter todos by priority (low, medium, high, critical)")
    print("5. Change todo status (open <-> done)")
    print("6. View todo details")
    print("7. Delete a todo")
    print("B. Back to main menu")
    print("X. Exit")
    choice = input("Choose an option (1-7, B to go back or X to Exit): ").strip().upper()
    
    if choice == '1':
        show_tasks(todos, status="all")
    elif choice == '2':
        status = input("Enter status to filter by (open/done): ").strip().lower()
        if status in ["open", "done"]:
            show_tasks(todos, status=status)
        else:
            print("Invalid status. Please enter 'open' or 'done'.")
    elif choice == '3':
        query = input("Enter keyword to search for: ").strip()
        show_tasks(todos, query=query)
    elif choice == '4':
        filter_tasks(todos)
    elif choice == '5':
        mark_task_done(todos)
    elif choice == '6':
        show_details(todos)
    elif choice == '7':
        delete_task(todos)
    elif choice == 'B':
        return
    elif choice == 'X':
        clear_terminal()
        print("Exiting Todo Manager. Goodbye!")
        exit()
    else:
        print("Invalid option. Please try again.") 
    
# Main function with the main menu
def main():
    print("*" * 40)
    print("Todo Manager Application".center(40))
    print("*" * 40)
    while True:
        todos = load_task()
        print("\nOptions:")
        print("1. View filter and change options")
        print("2. Add Todo")
        print("X. Exit")
        choice = input("Choose an option (1, 2 or X): ").strip().upper()

        if choice == '1':
            list_filter_and_change_options(todos)
        elif choice == '2':
            create_task(todos)
        elif choice == 'X':
            print("Exiting Todo Manager. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

# Clears the terminal 
# cls for windows otherwise use clear
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")

if __name__ == "__main__":
    main()