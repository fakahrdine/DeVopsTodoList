import json
import os

# We will use a JSON file to save our tasks permanently.
# In Python, we define file paths as regular strings. 
# We'll save it in the same directory as the script.
TODO_FILE = "tasks.json"

def load_tasks():
    # If the file doesn't exist yet, return an empty list.
    # In Python, lists are like ArrayLists in Java, defined with square brackets []
    if not os.path.exists(TODO_FILE):
        return []
    
    # We use 'with open(...) as file:' to automatically handle closing the file,
    # even if an error occurs. This is similar to a try-with-resources block in Java!
    try:
        with open(TODO_FILE, 'r') as file:
            # json.load reads the file and converts the JSON string back into Python lists/dictionaries
            return json.load(file)
    except json.JSONDecodeError:
        # If the file is corrupted or empty, we catch the error to prevent a crash
        return []

def save_tasks(tasks):
    # 'w' mode opens the file for writing (overwriting what was there)
    with open(TODO_FILE, 'w') as file:
        # json.dump converts Python objects into a JSON format and writes to the file
        # indent=4 makes the JSON file nicely formatted and easy to read for humans
        json.dump(tasks, file, indent=4)

def show_menu():
    # Python allows multi-line strings easily using triple quotes!
    print("""
==========================
    To-Do List Manager    
==========================
1. View tasks
2. Add a task
3. Complete a task
4. Exit
==========================
    """)

def main():
    # Load existing tasks when the program starts
    tasks = load_tasks()

    # 'while True:' creates an infinite loop, exactly like 'while(true)' in Java.
    # We will use the 'break' keyword to exit the loop when the user chooses to exit.
    while True:
        show_menu()
        
        # 'input()' pauses the program and waits for the user to type something and press Enter
        # It always returns the user's input as a String
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            if not tasks:
                print("\n[!] No tasks found! Your list is empty.")
            else:
                print("\n--- Your Tasks ---")
                # 'enumerate' gives us BOTH the index and the item in the list at the same time
                # This is super useful in Python!
                for index, task in enumerate(tasks):
                    # This is a ternary operator in Python: value_if_true if condition else value_if_false
                    status = "[x]" if task['completed'] else "[ ]"
                    
                    # We add 1 to the index so the display starts at 1, not 0
                    print(f"{index + 1}. {status} {task['title']}")
        
        elif choice == '2':
            title = input("\nEnter the task description: ")
            
            # We use a Dictionary (like a Java HashMap) to store complex objects
            # Dictionaries use curly braces {} and key-value pairs
            new_task = {
                "title": title,
                "completed": False
            }
            # Add the new dictionary to our list
            tasks.append(new_task)
            
            # Save right after modifying
            save_tasks(tasks)
            print(f"[✓] Task '{title}' added successfully!")

        elif choice == '3':
            if not tasks:
                print("\n[!] No tasks to complete!")
                continue

            # We can use try-except to handle invalid inputs (e.g. if they type a letter instead of a number)
            try:
                task_number = int(input("\nEnter task number to complete: "))
                
                # Subtract 1 to convert from 1-based display to 0-based index
                index = task_number - 1
                
                # Check if the list index is valid
                if 0 <= index < len(tasks):
                    tasks[index]['completed'] = True
                    save_tasks(tasks)
                    print("[✓] Task marked as complete!")
                else:
                    print("[!] Invalid task number. Out of range.")
            except ValueError:
                # Caught if int() fails because the user typed text
                print("[!] Please enter a valid number.")

        elif choice == '4':
            print("\nGoodbye! Exiting program...")
            break  # This completely stops the 'while True' loop
        
        else:
            print("\n[!] Invalid choice. Please select from 1 to 4.")

# Standard boilerplate to ensure main() is only called if run directly
if __name__ == "__main__":
    main()
