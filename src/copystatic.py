import os
import shutil


# Copies all files and directories from the source to the destination.
# If the destination directory already exists, it will be deleted and recreated.
def copy_files(source, destination):
    # Check if the destination directory exists, if so, delete it
    if os.path.exists(destination):
        print("Deleting public directory...")
        shutil.rmtree(destination)  # Deletes the directory and all its contents
    # Create the destination directory
    os.makedirs(destination)
    # Ensure the source path exists before proceeding
    if not os.path.exists(source):
            raise ValueError(f"Source path '{source}' does not exist.")
    # Recursive function to copy files and directories
    def recursive_copy(source, destination):
        # Iterate over each item in the source directory
        for filename in os.listdir(source):
            source_item = os.path.join(source, filename)
            destination_item = os.path.join(destination, filename)
            print(f" * {source_item} -> {destination_item}")
            # If the item is a file, copy it to the destination
            if os.path.isfile(source_item):
                shutil.copy(source_item, destination_item)
            else:
                # If the item is a directory, create it in the destination and recursively copy its contents
                os.makedirs(destination_item, exist_ok=True)
                recursive_copy(source_item, destination_item)
    # Start the recursive copy process from the source to the destination
    recursive_copy(source, destination)