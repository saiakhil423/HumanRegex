# conftest.py — tells pytest to look in src/ for the package
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))
