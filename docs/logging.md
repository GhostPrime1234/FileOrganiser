# Logging

FileOrganizer supports logging to track the file organization process. Here's how to configure logging:

```python
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

# Usage in the project
logger.info("File organisation started.")
```

By default, logs are written to the console, but you can configure it to log to a file.