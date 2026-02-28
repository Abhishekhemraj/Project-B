import os
import csv
import pytest
from phase1_foundation.data_loader import load_jokes

@pytest.fixture
def temp_csv(tmp_path):
    csv_file = tmp_path / "test_jokes.csv"
    with open(csv_file, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(["text"])
        writer.writerow(["Short joke."])
        writer.writerow(["This is a medium length joke that should be classified as medium because it is longer than short."])
    return str(csv_file)

def test_load_jokes(temp_csv):
    jokes = load_jokes(temp_csv)
    assert len(jokes) == 2
    assert jokes[0]["text"] == "Short joke."
    assert "category" in jokes[0]

def test_load_jokes_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_jokes("non_existent_file.csv")
