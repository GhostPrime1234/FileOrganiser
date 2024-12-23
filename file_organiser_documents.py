import os
from os import path
import shutil
import json

class MappingManager:
    """Manages loading and saving the folder mapping."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.mapping = self.load_mapping()

    def load_mapping(self):
        """Load the folder mapping from a JSON file."""
        if path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return {
            "University": ["UOW", "Scanned Documents", "SupportingDocumentation"],
            "Personal": ["invitation", "21st"],
            "Gaming": ["Gaming", "WB Games", "Horizon Forbidden West", "My Games"],
            "Miscellaneous": [],
            "Code": ["Python Scripts", "GitHub", "QtDesignStudio", "Robocode", "Visual Studio 2022"],
            "Software": ["Blackmagic Design", "MAXON", "Custom Office Templates"],
            "Backups": ["Anki Backup"]
        }

    def save_mapping(self):
        """Save the folder mapping to a JSON file."""
        with open(self.file_path, "w") as file:
            json.dump(self.mapping, file, indent=4)

    def add_category(self, category, keyword):
        """Add a new category and keyword to the mapping."""
        if category not in self.mapping:
            self.mapping[category] = []
        self.mapping[category].append(keyword)

class FileMover:
    """Handles the movement of files and folders."""
    def __init__(self, source_folder):
        self.source_folder = source_folder

    def move_item(self, item_path, target_folder):
        """Move an item to the target folder."""
        os.makedirs(target_folder, exist_ok=True)
        destination_path = path.join(target_folder, path.basename(item_path))

        # Check if the source and destination paths are the same
        if path.abspath(item_path) == path.abspath(destination_path):
            print(f"Skipping: Cannot move '{item_path}' into itself.")
            return

        # Ensure we are not trying to move a folder into itself
        if path.isdir(item_path) and path.commonpath([item_path, destination_path]) == path.abspath(item_path):
            print(f"Skipping: Cannot move folder '{item_path}' into itself.")
            return

        shutil.move(item_path, destination_path)


class FolderOrganizer:
    """Organizes files into categorized folders."""
    def __init__(self, source_folder, mapping_manager: MappingManager):
        self.source_folder = source_folder
        self.mapping_manager = mapping_manager
        self.file_mover = FileMover(source_folder)

    def organize(self):
        """Organize files and folders in the source folder."""
        mapping = self.mapping_manager.mapping

        # Ensure target folders exist
        for category in mapping.keys():
            os.makedirs(path.join(self.source_folder, category), exist_ok=True)

        for item in os.listdir(self.source_folder):
            item_path = path.join(self.source_folder, item)

            # Skip category folders and prevent moving into itself
            if path.isdir(item_path) and item in mapping.keys():
                continue

            moved = False

            # Try to match the item to a category
            for category, keywords in mapping.items():
                if any(keyword.lower() in item.lower() for keyword in keywords):
                    target_folder = path.join(self.source_folder, category)
                    self.file_mover.move_item(item_path, target_folder)
                    print(f"Moved '{item}' to '{category}'")
                    moved = True
                    break

            # Handle uncategorized items
            if not moved:
                self.handle_uncategorized_item(item_path, item)

    def handle_uncategorized_item(self, item_path, item):
        """Handle uncategorized items by asking the user for a category."""
        # Skip category folders
        if path.isdir(item_path) and item in self.mapping_manager.mapping.keys():
            print(f"Skipping category folder: '{item}'")
            return

        print(f"Uncategorized item found: '{item}'")
        new_category = input(f"Enter a category for '{item}' (or press Enter for 'Miscellaneous'): ").strip()

        if not new_category:
            new_category = "Miscellaneous"

        # Add the new category and move the item
        self.mapping_manager.add_category(new_category, item)
        target_folder = path.join(self.source_folder, new_category)
        self.file_mover.move_item(item_path, target_folder)
        print(f"Moved '{item}' to '{new_category}'")

        # Save the updated mapping
        self.mapping_manager.save_mapping()


if __name__ == "__main__":
    # Define the folder to organize and the mapping file
    source_folder = path.join(path.expanduser("~"), "Documents")
    mapping_file = path.join(path.expanduser("~"), "folder_mapping.json")

    # Initialize the MappingManager
    mapping_manager = MappingManager(mapping_file)

    # Initialize and run the FolderOrganizer
    organizer = FolderOrganizer(source_folder, mapping_manager)
    organizer.organize()

    os.system(f'notepad {mapping_file}')
