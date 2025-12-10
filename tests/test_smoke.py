from pathlib import Path

def test_notebook_exists():
    """Check that the main analysis notebook is present."""
    nb_path = Path("notebooks/UAO_midterm.ipynb")
    assert nb_path.is_file(), f"Notebook not found at {nb_path}"

def test_data_dirs_exist():
    """Check that the expected data directories exist."""
    for p in ["data", "data/raw"]:
        path = Path(p)
        assert path.is_dir(), f"Expected directory {p} to exist"
