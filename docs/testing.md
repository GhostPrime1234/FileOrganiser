# Testing

To run tests for FileOrganizer, make sure you have the `pytest` package installed:

```bash
pip install pytest
```

Run thest tests:
pytest

## Example Test
Here’s an example of how to write tests for the FileOrganizer class:

```python
def test_organize_files():
    organizer = FileOrganizer(folder_to_watch="test_folder", json_file="test_config.json")
    organizer.organize_files()
    assert organizer.files_organized == True
```