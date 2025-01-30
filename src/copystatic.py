import os
import shutil


def copy_files(source, destination):
    if os.path.exists(destination):
        print("Deleting public directory...")
        shutil.rmtree(destination)  # Deletes the directory and all its contents
    os.makedirs(destination)
    if not os.path.exists(source):
            raise ValueError(f"Source path '{source}' does not exist.")
    def recursive_copy(source, destination):
        for filename in os.listdir(source):
            source_item = os.path.join(source, filename)
            destination_item = os.path.join(destination, filename)
            print(f" * {source_item} -> {destination_item}")
            if os.path.isfile(source_item):
                shutil.copy(source_item, destination_item)
            else:
                os.makedirs(destination_item, exist_ok=True)
                recursive_copy(source_item, destination_item)
    recursive_copy(source, destination)