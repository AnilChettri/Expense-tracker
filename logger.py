# logger.py

import logging

# Set up logging configuration once
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"  # Append mode
)

# Provide a shared logger object
logger = logging.getLogger(__name__)
