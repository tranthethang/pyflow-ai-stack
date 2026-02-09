import logging

# Define a library-specific logger
logger = logging.getLogger("pyflow_ai_stack")
logger.addHandler(logging.NullHandler())
