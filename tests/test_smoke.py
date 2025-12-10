from pathlib import Path

def test_notebook_exists():
    """Check that the main analysis notebook is present."""
    nb_path = Path("notebooks/UAO_midterm.ipynb")
    assert nb_path.is_file(), f"Notebook not found at {nb_path}"

def test_data_dirs_exist():
    """Check that the expected data directories exist, or are creatable."""
    for p in ["data", "data/raw"]:
        path = Path(p)
        if not path.is_dir():
            # try to create instead of failing
            path.mkdir(parents=True, exist_ok=True)
        assert path.is_dir()

