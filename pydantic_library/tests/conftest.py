"""pytest configuration for pydantic_library tests."""
import sys
from pathlib import Path

# Add pydantic_library root to sys.path for imports
tests_dir = Path(__file__).parent
pydantic_lib_root = tests_dir.parent
sys.path.insert(0, str(pydantic_lib_root))
