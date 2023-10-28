import os

def get_subfolders(path):
    """Get subfolders of a given folder"""
    return [folder for folder in os.listdir(path) if os.path.isdir(os.path.join(path, folder))]

# Start from the directory where the script is located
root_path = os.path.dirname(os.path.abspath(__file__))

# Get immediate folders in the directory
folder_order = get_subfolders(root_path)

# Get subfolders for each folder in folder_order
subfolder_orders = {}
for folder in folder_order:
    subfolder_orders[folder] = get_subfolders(os.path.join(root_path, folder))

# Save to a file
with open("folder_structure.txt", "w") as f:
    f.write("folder_order\n")
    for folder in folder_order:
        f.write(f"{folder}\n")
    f.write("\n")
    
    for folder, subfolders in subfolder_orders.items():
        f.write(f"{folder}_subfolder_order\n")
        for subfolder in subfolders:
            f.write(f"{subfolder}\n")
        f.write("\n")

print("Folder structure saved to folder_structure.txt.")
