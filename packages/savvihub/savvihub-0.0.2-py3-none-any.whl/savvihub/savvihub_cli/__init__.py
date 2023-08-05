from pathlib import Path
from .main import app
import os

CUR_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
app()
