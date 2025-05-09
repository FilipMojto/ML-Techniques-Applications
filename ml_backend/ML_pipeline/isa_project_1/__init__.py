import os, sys
from pathlib import Path

# Get the current notebook's directory
PROJECT_ROOT = Path(os.getcwd()).parent.parent  # Assuming 'notebooks/' is inside the project root

# Add it to sys.path
sys.path.append(str(PROJECT_ROOT))

from ML_pipeline.isa_project_1 import config  # noqa: F401
