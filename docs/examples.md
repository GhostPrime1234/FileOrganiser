# Examples

## Example 1: Basic File Organization

Here’s an example to organize files in a directory based on their extensions:

```python
from file_organizer import FileOrganizer

organizer = FileOrganizer(folder_to_watch="path/to/folder", json_file="config.json")
organizer.organize_files()
```

## Example 2: Advanced Configuration

You can also use a more advanced configuration file to manage categories:
```json
{
    "audio": [".mp3", ".wav"],
    "images": [".jpg", ".png"],
    "documents": [".pdf", ".txt"]
}
```