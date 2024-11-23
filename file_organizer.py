import logging
import json
from os import path, makedirs, listdir, stat
from shutil import move
import time
from typing import Dict, List

logging.basicConfig(filename='file_organizer.log', level=logging.DEBUG)

class FileOrganizer:
    """
    A class that organizes files based on their extensions in the current directory.
    """
    def __init__(self, folder_to_watch: str, json_file: str):
        """
        Initializes the FileOrganizer instance.

        Args:
            folder_to_watch (str): The folder to organize files.
            json_file (str): Path to the JSON containing category information.
        """
        self.folder_to_watch = folder_to_watch
        self.json_file = json_file
        self.default_categories = {
            "Documents & Data": {
                "Documents": [".pdf", ".docx", ".txt", ".odt", ".rtf", ".html", ".epub", ".md", ".tex", ".bib"],
                "Data (CSV, XML, JSON, etc.)": [".csv", ".xml", ".json", ".yaml"]
            },
            "Development": {
                "Project": [".py", ".cpp", ".java", ".js", ".html", ".css", ".rb", ".go", ".php"]
            },
            "Executables": {
                "Installers": [".exe", ".msi"],
                "Scripts": [".bat", ".sh"]
            },
            "Archives": {
                "Compressed Files": [".zip", ".rar", ".tar", ".tar.gz", ".7z", ".gz"],
                "Backups": [".bak", ".backup"]
            },
            "Disk Image": {
                "ISO & Disk Images": [".iso", ".img"]
            },
            "Presentations": {
                "PowerPoint Files": [".pptx", ".key", ".ppt"]
            },
            "Spreadsheets": {
                "Excel and CSV Files": [".xls", ".xlsx", ".csv"]
            },
            "Other": {}  # For any files not recognized
        }
        self.categories = self.load_categories()
        print(f"Organizing folder: {self.folder_to_watch}")

    def load_categories(self) -> Dict[str, List[str]]:
        """
        Load categories from the JSON file or initialize with default categories.

        Example:
            >>> import json
            >>> from os import remove
            >>> # Create a temporary JSON file with categories
            >>> temp_json = 'temp_categories.json'
            >>> with open(temp_json, 'w') as f:
            ...     json.dump({"TestCategory": {"Subcategory": [".tmp"]}}, f)
            >>> organizer = FileOrganizer(".", temp_json)
            Categories loaded from JSON.
            Added missing category: Documents & Data
            Added missing category: Development
            Added missing category: Executables
            Added missing category: Archives
            Added missing category: Disk Image
            Added missing category: Presentations
            Added missing category: Spreadsheets
            Added missing category: Other
            Categories saved to JSON.
            Organizing folder: .
            >>> categories = organizer.load_categories()
            Categories loaded from JSON.
            >>> "TestCategory" in categories
            True
            >>> remove(temp_json)

        Returns:
            dict: The loaded or default categories.
        """
        if path.exists(self.json_file):
            with open(self.json_file, 'r') as file:
                categories = json.load(file)
            print("Categories loaded from JSON.")
            logging.debug(f"Categories loaded: {json.dumps(categories, indent=4)}")

            # Sync categories to ensure no extensions are missing
            categories = self.sync_categories(categories)
        else:
            categories = self.default_categories.copy()
            self.save_categories(categories)
            print("No JSON file found, using default categories.")
            logging.debug("No categories JSON found, using default categories.")  # Adjusted logging here
        return categories
    
    def sync_categories(self, categories: Dict[str, List[str]]) -> Dict[str, List[str]]:
        """
        Ensures all default categories and extensions are present in the loaded categories.
        
        Example:
            >>> organizer = FileOrganizer(".", "non_existent_file.json")
            Categories loaded from JSON.
            Organizing folder: .
            >>> categories = {"TestCategory": {"Subcategory": [".tmp"]}}
            >>> updated_categories = organizer.sync_categories(categories)
            Added missing category: Documents & Data
            Added missing category: Development
            Added missing category: Executables
            Added missing category: Archives
            Added missing category: Disk Image
            Added missing category: Presentations
            Added missing category: Spreadsheets
            Added missing category: Other
            Categories saved to JSON.
            >>> "Documents & Data" in updated_categories
            True
            >>> "TestCategory" in updated_categories
            True

        Args:
            categories (dict): The loaded categories.

        Returns:
            dict: The updated categories with missing entries filled.
    """
        updated = False

        for category, subcategories in self.default_categories.items():
            if category not in categories:
                categories[category] = subcategories
                updated = True
                print(f"Added missing category: {category}")
                logging.debug(f"Added missing category: {category}")
            else:
                # Ensure categories[category] is a dictionary
                if not isinstance(categories[category], dict):
                    print(f"Warning: {category} is not a dictionary, resetting to default.")
                    logging.warning(f"{category} is not a dictionary, resetting to default.")
                    categories[category] = subcategories  # Reset it to the default structure
                    updated = True

                # Now ensure the subcategories are in the correct format (dictionary with list of extensions)
                for subcategory, extensions in subcategories.items():
                    if subcategory not in categories[category]:
                        categories[category][subcategory] = extensions
                        updated = True
                        print(f"Added missing subcategory: {subcategory} to {category}")
                        logging.debug(f"Added missing subcategory: {subcategory} to {category}")

                    # Ensure that each subcategory is a list of extensions
                    if not isinstance(categories[category][subcategory], list):
                        print(f"Warning: {subcategory} under {category} is not a list, resetting to default.")
                        logging.warning(f"{subcategory} under {category} is not a list, resetting to default.")
                        categories[category][subcategory] = extensions  # Reset to default extension list

        # If updates were made, save the categories back to the JSON file
        if updated:
            self.save_categories(categories)

        return categories

    def save_categories(self, categories: Dict[str, List[str]]):
        """
        Save the updated categories to the JSON file.
        
        Args:
            categories (dict): The categories to save.
        """
        with open(self.json_file, 'w') as file:
            json.dump(categories, file, indent=4)
        print("Categories saved to JSON.")
        logging.debug("Categories saved to JSON.")

    def organise_downloads(self, file_path: str):
        """
        Organize downloaded file based on its extension and predefined structure.

        Example:
            >>> import json
            >>> from os import remove, path
            >>> # Create a temporary JSON file with categories
            >>> temp_json = 'temp_categories.json'
            >>> with open(temp_json, 'w') as f:
            ...     json.dump({"TestCategory": {"Subcategory": [".tmp"]}}, f)
            >>> organizer = FileOrganizer(".", temp_json)
            Categories loaded from JSON.
            Added missing category: Documents & Data
            Added missing category: Development
            Added missing category: Executables
            Added missing category: Archives
            Added missing category: Disk Image
            Added missing category: Presentations
            Added missing category: Spreadsheets
            Added missing category: Other
            Categories saved to JSON.
            Organizing folder: .
            >>> categories = organizer.load_categories()
            Categories loaded from JSON.
            >>> "TestCategory" in categories
            True
            >>> remove(temp_json)  # Cleanup step to remove the non-existent file

        Args:
            file_path (str): The path to the file to be organised.
        """
        _, file_extension = path.splitext(file_path)
        file_extension = file_extension.lower()
        logging.debug(f"File extension: {file_extension}")

        # Debugging: Print the file being processed
        print(f"Processing file: {file_path} with extension {file_extension}")
        logging.info(f"Processing file: {file_path} with extension {file_extension}")

        # Check if the file extension exists in any category
        category_found = False
        for category, subcategories in self.categories.items():
            for subcategory, extensions in subcategories.items():
                if file_extension in extensions:
                    category_found = True
                    # Move file to the correct subfolder
                    category_path = path.join(self.folder_to_watch, category, subcategory)
                    if not path.exists(category_path):
                        makedirs(category_path)
                    new_path = path.join(category_path, path.basename(file_path))
                    try:
                        move(file_path, new_path)
                        print(f"Moved {file_path} to {new_path}")
                        logging.info(f"Moved {file_path} to {new_path}")
                    except Exception as e:
                        print(f"Error moving file: {e}")
                        logging.error(f"Error moving file {file_path}: {e}")
                    break
            if category_found:
                break
        
        # If no match is found, move to "Other"
        if not category_found:
            print(f"New file type detected: {file_extension}")
            logging.info(f"New file type detected: {file_extension}")
            new_category = "Other"
            if new_category not in self.categories:
                self.categories[new_category] = {}
            if file_extension not in self.categories["Other"]:
                self.categories[new_category][file_extension] = []
           
            self.save_categories(self.categories)
            # Move to the "Other" category
            other_path = path.join(self.folder_to_watch, "Other")
            if not path.exists(other_path):
                makedirs(other_path)
                logging.debug(f"Created directory: {category_path}")
            new_path = path.join(other_path, path.basename(file_path))
            try:
                logging.debug(f"Moving {file_path} to {new_path}")
                move(file_path, new_path)
                print(f"Moved {file_path} to {new_path}")
                logging.info(f"Moved {file_path} to {new_path}")
            except Exception as e:
                logging.error(f"Error moving file {file_path} to {new_path}: {e}")
                print(f"Error moving file: {e}")

    def organize_files_in_directory(self):
        """
        Organize all files in the directory based on their extensions.

        Example:
            >>> from os import makedirs, remove
            >>> from shutil import rmtree
            >>> # Setup a test environment
            >>> test_folder = "test_folder"
            >>> makedirs(test_folder, exist_ok=True)
            >>> test_file_1 = path.join(test_folder, "test1.pdf")
            >>> test_file_2 = path.join(test_folder, "test2.csv")
            >>> with open(test_file_1, "w") as f1, open(test_file_2, "w") as f2:
            ...     f1.write("Test 1 content.")
            ...     f2.write("Test 2 content.")
            15
            15
            >>> organizer = FileOrganizer(test_folder, "non_existent_file.json")
            Categories loaded from JSON.
            Organizing folder: test_folder
            >>> organizer.organize_files_in_directory()
            Starting to organize files in test_folder
            Processing file: test_folder\\test1.pdf with extension .pdf
            Moved test_folder\\test1.pdf to test_folder\\Documents & Data\\Documents\\test1.pdf
            Processing file: test_folder\\test2.csv with extension .csv
            Moved test_folder\\test2.csv to test_folder\\Documents & Data\\Data (CSV, XML, JSON, etc.)\\test2.csv
            >>> path.exists(path.join(test_folder, "Documents & Data/Documents/test1.pdf"))
            True
            >>> path.exists(path.join(test_folder, "Documents & Data/Data (CSV, XML, JSON, etc.)/test2.csv"))
            True
            >>> rmtree(test_folder)
        """
        print(f"Starting to organize files in {self.folder_to_watch}")
        for file_name in listdir(self.folder_to_watch):
            file_path = path.join(self.folder_to_watch, file_name)
            if path.isfile(file_path):
                self.organise_downloads(file_path)


if __name__ == "__main__":
    folder_to_watch = path.join(path.expanduser("~"), "Downloads")
    json_file = path.join(path.expanduser("~"), "categories.json")
    organizer = FileOrganizer(folder_to_watch, json_file)
    organizer.organize_files_in_directory()
