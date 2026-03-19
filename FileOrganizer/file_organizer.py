import os
import shutil

# In Python, we define functions using the 'def' keyword instead of 'public void' like in Java.
# There are no curly braces {}; instead, we use a colon : and indentation.
def organize_files(folder_path):
    # 1. List all items in the directory
    # os.listdir() returns a list of strings (file and folder names)
    try:
        items = os.listdir(folder_path)
    except FileNotFoundError:
        print(f"Error: The folder {folder_path} does not exist.")
        return

    print(f"Organizing {len(items)} items in '{folder_path}'...\n")

    # 2. Loop through each item
    # Notice how much cleaner this is than Java's traditional 'for (int i=0; i<items.length; i++)'
    for item in items:
        # Create full paths. Always use os.path.join to handle Windows vs Linux slash differences!
        item_path = os.path.join(folder_path, item)

        # 3. Skip if it's a directory (we only want to organize files)
        if os.path.isdir(item_path):
            continue
            
        # 4. Extract the file extension
        # os.path.splitext() splits "report.txt" into ("report", ".txt")
        # Python allows returning and assigning multiple variables at once!
        filename, extension = os.path.splitext(item)
        
        # Skip files with no extension
        if not extension:
            continue
            
        # Remove the dot and convert to uppercase for the folder name (e.g., ".txt" -> "TXT")
        # extension[1:] means "give me the string starting from character index 1 to the end"
        ext_folder_name = extension[1:].upper()
        ext_folder_path = os.path.join(folder_path, ext_folder_name)

        # 5. Create the destination folder if it doesn't already exist
        if not os.path.exists(ext_folder_path):
            os.makedirs(ext_folder_path)
            print(f"Created new folder: {ext_folder_name}")

        # 6. Move the file using the shutil module
        destination_path = os.path.join(ext_folder_path, item)
        shutil.move(item_path, destination_path)
        print(f"Moved {item} -> {ext_folder_name}/")
    print("\nOrganization complete!")

# This is Python's equivalent to `public static void main(String[] args)`
# It ensures the code below only runs if this script is executed directly, 
# and NOT if it is imported into another script.
if __name__ == "__main__":
    # Define the path to our messy folder
    # We use a raw string (r"...") so we don't have to escape backslashes on Windows
    # In Java, you'd have to write "c:\\Users\\mohamed\\Desktop\\..."
    target_folder = r"c:\Users\mohamed\Desktop\PythonDevOpsProjects\FileOrganizer\messy_folder"
    organize_files(target_folder)
