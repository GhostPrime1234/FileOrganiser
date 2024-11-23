# Error Handling

FileOrganizer uses built-in exceptions to handle errors. Below are the common errors:

## FileNotFounderror
Occurs when the spcified directory does not exist.

```python
try:
    organiser = FileOrganizer(folder_to_watch="nonexistent/folder")
except FileNotFoundError as error:
    print(f"Error: {error}")
```