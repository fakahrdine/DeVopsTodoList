import tkinter as tk
from tkinter import messagebox
import json
import os

# We will use the exact same file we used for our command-line app!
TODO_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(TODO_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# In Python, we create classes using the 'class' keyword (just like Java)
class TodoApp:
    # __init__ is Python's version of a constructor mechanism
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List GUI")
        self.root.geometry("420x550")        # Window size: Width x Height
        self.root.config(bg="#f4f4f9")       # Set a nice off-white background color

        # Load our data
        self.tasks = load_tasks()

        # 1. Title Label
        # tk.Label creates text on the screen. 'pack()' places it in the window.
        self.title_label = tk.Label(self.root, text="✓ My Tasks", font=("Helvetica", 20, "bold"), bg="#f4f4f9", fg="#333333")
        self.title_label.pack(pady=20)

        # 2. Frame for the list 
        # A Frame is like a Java JPanel, used to group items together
        self.list_frame = tk.Frame(self.root)
        self.list_frame.pack(pady=10)

        # 3. Scrollbar
        self.scrollbar = tk.Scrollbar(self.list_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 4. Listbox (To show the actual tasks)
        self.task_listbox = tk.Listbox(self.list_frame, width=35, height=12, font=("Helvetica", 12),
                                       selectbackground="#a6b8c7", selectforeground="black", 
                                       yscrollcommand=self.scrollbar.set)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        self.scrollbar.config(command=self.task_listbox.yview)

        # 5. Entry (Text field for typing new tasks)
        self.task_entry = tk.Entry(self.root, font=("Helvetica", 14), width=24)
        self.task_entry.pack(pady=15)
        
        # 'bind' allows us to trigger a function when a key is pressed (like throwing an event in Java)
        # Here, pressing "Enter" adds the task
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # 6. Frame for buttons
        self.button_frame = tk.Frame(self.root, bg="#f4f4f9")
        self.button_frame.pack(pady=5)

        # Add buttons using 'grid' layout (similar to Java's GridLayout)
        # We link the button click to our custom functions using 'command=self.function_name'
        self.add_button = tk.Button(self.button_frame, text="Add Task", font=("Helvetica", 11, "bold"), bg="#4CAF50", fg="white", command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=5)

        self.complete_button = tk.Button(self.button_frame, text="Mark Done", font=("Helvetica", 11, "bold"), bg="#2196F3", fg="white", command=self.complete_task)
        self.complete_button.grid(row=0, column=1, padx=5)

        self.delete_button = tk.Button(self.button_frame, text="Delete", font=("Helvetica", 11, "bold"), bg="#f44336", fg="white", command=self.delete_task)
        self.delete_button.grid(row=0, column=2, padx=5)

        # Populate the list when the program starts
        self.refresh_listbox()

    def refresh_listbox(self):
        # Clear the GUI listbox without deleting our actual data
        self.task_listbox.delete(0, tk.END)
        
        # Loop over tasks and add them to the GUI
        for index, task in enumerate(self.tasks):
            status = "☑" if task['completed'] else "☐"
            display_text = f"{status}  {task['title']}"
            self.task_listbox.insert(tk.END, display_text)
            
            # If completed, change the text color to gray (like visually crossing it out)
            if task['completed']:
                self.task_listbox.itemconfig(index, {'fg': '#9e9e9e'})

    def add_task(self):
        # .get() reads the text box, .strip() removes accidental spaces at the start/end
        title = self.task_entry.get().strip()
        if title:
            # Adding dictionary item to list
            self.tasks.append({"title": title, "completed": False})
            save_tasks(self.tasks)         # Save to JSON!
            self.refresh_listbox()         # Update screen!
            self.task_entry.delete(0, tk.END) # Clear text box!
        else:
            # messagebox throws a pop-up alert (like Java's JOptionPane)
            messagebox.showwarning("Warning", "You must enter a task description.")

    def complete_task(self):
        try:
            # Get the index of the clicked item in the listbox
            selected_index = self.task_listbox.curselection()[0]
            self.tasks[selected_index]['completed'] = True
            save_tasks(self.tasks)
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to mark as done.")

    def delete_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            del self.tasks[selected_index] # 'del' securely removes an item from a list
            save_tasks(self.tasks)
            self.refresh_listbox()
        except IndexError:
            messagebox.showwarning("Warning", "Please select a task to delete.")

if __name__ == "__main__":
    # Create the main window exactly like creating a new JFrame()
    root = tk.Tk()
    
    # Initialize our app instance
    app = TodoApp(root)
    
    # .mainloop() is a built-in infinite loop that waits for user clicks and key presses
    # Desktop apps require this so they don't immediately close!
    root.mainloop()
