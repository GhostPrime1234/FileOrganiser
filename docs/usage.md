# Usage

To use FileOrganiser, create an instance of the `FileOrganizer` class and call its methods. Here's an example:
```python
from file_organizer import FileOrganizer

# Create an instance of FileOrganizer
organizer = FileOrganizer(folder_to_watch="path/to/folder", json_file="config.json")

# Load categories
organizer.load_categories()

# Organize files
organizer.organize_files()
```